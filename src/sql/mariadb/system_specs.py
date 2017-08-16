import subprocess
import json
import pprint
import pymysql

SYSINFO_ROOTDIR="./sysinfo/"
db_name="rack_hardware_db"
db_user="rackteam"
db_host="localhost"
db_password="supermicro"
conn=None
cursor=None


def bash_cmd(cmd_str):
    if (cmd_str is None or not cmd_str):
        print ("[ERROR] No command specified")
        return None
    try:
       cmd_out=subprocess.check_output(cmd_str, shell=True)
       cmd_out=cmd_out.decode("utf-8")
    except subprocess.CalledProcessError as e:
       print(e.output)
       return None
    return cmd_out

def mariadb_insert(db_table, table_header, insert_vals):
    global conn
    global cursor
    try:
        pg_select_str = "INSERT INTO " + db_table + " (" + table_header + ")  VALUES (" + insert_vals + ");"
        print(pg_select_str)
        # Comment next two lines for testing
        cursor.execute(pg_select_str)
        conn.commit()
    except Exception as e:
        print("mariadb_insert() failed")
        print("Error msg:\n{0}".format(e))

def mariadb_connect(db_name, db_user, db_host, db_password):
    global conn
    global cursor
    try:
        db_connect_str = "dbname='" + db_name \
                         +"' user='" + db_user \
                         + "' host='" + db_host \
                         + "' " + "password='" + db_password + "'"
        # use our connection values to establish a connection
        conn = pymysql.connect(db_host, db_user, db_password, db_name)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        print("pg_connect() failed")
        print("Error msg:\n{0}".format(e))
    return (conn, cursor)

def insert_memory(mem_info):
    db_table = "memory_specs"
    table_header = "mem_serial, mem_partnum, mem_locator, motherboard_serial"
    cpu_pg_row = "'" + mem_info[0] + "', '" + mem_info[1] + "', '" + mem_info[2] + "', '" + mem_info[3] + "'"
    mariadb_insert(db_table, table_header, cpu_pg_row)

def insert_motherboard(mb_info):
    db_table = "motherboard_specs"
    table_header = "mb_serial, mb_partnum"
    cpu_pg_row = "'" + mb_info[0] + "', '" + mb_info[1] + "'"
    mariadb_insert(db_table, table_header, cpu_pg_row)

def insert_cpu(cpu_info):
    db_table = "cpu_specs"
    table_header = "cpu_serial, cpu_partnum, motherboard_serial"
    cpu_pg_row = "'" + cpu_info[0] + "', '" + cpu_info[1] + "', '" + cpu_info[2] + "'"
    mariadb_insert(db_table, table_header, cpu_pg_row)
    

def parse_mem_serials(sys_conf_path):
    memory_serial_num_list = []
    parse_mem_serials_cmd = "cat " + sys_conf_path + "| grep -A 10 'Locator'"
    memory_info = bash_cmd(parse_mem_serials_cmd)
    memory_info = memory_info.split('--')
    for mem_info_blk in memory_info:
        mem_locator = None
        mem_serial_num = None
        mem_partnum = None
        for mem_info_line in mem_info_blk.split('\n'):
            #print (mem_info_line)
            if (("Locator" in mem_info_line) and (not "Bank" in mem_info_line)):
                mem_locator = mem_info_line.split()[1]
            elif ("Serial Number" in mem_info_line):
                mem_serial_num = mem_info_line.split()[2]
                # If we see the string "NO " we'll skip over the block
                if ("NO " in mem_info_line):
                    break;
            elif ("Part Number" in mem_info_line):
                mem_partnum = mem_info_line.split()[2]
                # If we see the string "NO " we'll skip over the block
                if ("NO " in mem_info_line):
                    break;
            # If we've set all values we'll append to list and move on
            if (mem_locator and mem_serial_num and mem_partnum):
                mem_specs_tuple = (mem_locator, mem_serial_num, mem_partnum)
                memory_serial_num_list.append(mem_specs_tuple)
                #print (mem_specs_tuple)
                break
    return memory_serial_num_list
    
def get_memory_info(macaddr_path):
    sys_conf_path = macaddr_path + "/sysinfo/dmidecode.log"
    memory_serial_num_list = parse_mem_serials(sys_conf_path)
    return memory_serial_num_list

def system_info(sys_path):
    #### System info ####
    sys_nic_path = macaddr_path + "/NIC.txt"
    sysinfo_cmd_prefix = "cat " + sys_path
    sysinfo_dict = {}
    sysinfo_parse_cmd_list = [
                       ("sys_serial", "/SN.txt | grep 'System S/N' | awk '{print $3}'"),
                       ("sys_partnum", "/SN.txt | grep 'System P/N' | awk '{print $3}'"),
                       ("sys_macaddr", "/NIC.txt | grep eth0 | sed 's/,/ /g' | awk '{print $2}'"),
                       ("sys_eth0_ip", "/NIC.txt | grep eth0 | sed 's/,/ /g' | awk '{print $3}'"),
                       ("sys_eth1_macaddr", "/NIC.txt | grep eth1 | sed 's/,/ /g' | awk '{print $2}'"),
                       ("sys_ipmi_macaddr", "/NIC.txt | grep ipmi | sed 's/,/ /g' | awk '{print $2}'"),
                       ("sys_ipmi_ip", "/NIC.txt | grep ipmi | sed 's/,/ /g' | awk '{print $3}'"),
                       ("sys_vendor", "/system.conf | grep 'System' | awk '{print $3}'"),
                       ("sys_pn", "/system.conf | grep 'Product PN' | awk '{print $3}'"),
                       ("sys_sn", "/system.conf | grep 'Product SN' | awk '{print $3}'"),
                       ("chassis_serial", "/system.conf | grep 'Chassis SN' | awk '{print $3}'"),
                       ("bios_vendor", "/system.conf | grep 'BIOS Vendor' | awk '{print $3}'"),
                       ("bios_version", "/system.conf | grep 'BIOS Version' | awk '{print $3}'"),
                       ("bios_date", "/system.conf | grep 'BIOS Date' | awk '{print $3}'"),
                       ("motherboard_serial", "/system.conf | grep 'M/B SN' | awk '{print $3}'"),
                       ("motherboard_partnum", "/system.conf | grep 'M/B PN' | awk '{print $3}'"),
                       ("cpu_partnum", "/system.conf | grep 'CPU Model' | awk '{print $3$4$5$6$7}'"),
                       ("cpu_quantity", "/system.conf | grep 'CPU Quantities' | awk '{print $3}'"),
                      ]

    for sysinfo_parse_cmd in sysinfo_parse_cmd_list:
        parsed_info = bash_cmd(sysinfo_cmd_prefix  + sysinfo_parse_cmd[1])
        sysinfo_dict[sysinfo_parse_cmd[0]] = parsed_info.rstrip()

    sys_serial = sysinfo_dict["sys_serial"]
    sys_partnum = sysinfo_dict["sys_partnum"]
    sys_macaddr = sysinfo_dict["sys_macaddr"]
    sys_eth0_ip = sysinfo_dict["sys_eth0_ip"]
    sys_eth1_macaddr = sysinfo_dict["sys_eth1_macaddr"]
    sys_ipmi_macaddr = sysinfo_dict["sys_ipmi_macaddr"]
    sys_ipmi_ip = sysinfo_dict["sys_ipmi_ip"]
    sys_vendor = sysinfo_dict["sys_vendor"]
    chassis_serial = sysinfo_dict["chassis_serial"]
    bios_vendor = sysinfo_dict["bios_vendor"]
    bios_version = sysinfo_dict["bios_version"]
    bios_date = sysinfo_dict["bios_date"]
    motherboard_serial = sysinfo_dict["motherboard_serial"]
    motherboard_partnum = sysinfo_dict["motherboard_partnum"]
    cpu_partnum = sysinfo_dict["cpu_partnum"]
    cpu_quantity = sysinfo_dict["cpu_quantity"]

    print(sys_serial)
    print(sys_partnum)
    print(sys_macaddr)
    print(sys_eth0_ip)
    print(sys_eth1_macaddr)
    print(sys_ipmi_macaddr)
    print(sys_ipmi_ip)
    print(sys_vendor)
    print(bios_vendor)
    print(bios_version)
    print(bios_date)
    print(chassis_serial)
    print(motherboard_serial)
    print(motherboard_partnum)
    print(cpu_partnum)
    print(cpu_quantity)

    #### Memory ####
    memory_serial_num_list = get_memory_info(macaddr_path)

    mb_info = (motherboard_serial, motherboard_partnum)
    insert_motherboard(mb_info)

    cpu_quantity = int(cpu_quantity)
    for cpu in range(0, cpu_quantity):
        cpu_serial = motherboard_serial + '_' + str(cpu)
        cpu_info = (cpu_serial, cpu_partnum, motherboard_serial)
        insert_cpu(cpu_info)

    for mem_card in memory_serial_num_list:
        mem_info = (mem_card[1], mem_card[2], mem_card[0], motherboard_serial)
        insert_memory(mem_info)
    
    #sys_json = json.dumps({"sys_info" : {"sys_serial" : sys_serial, "sys_partnum" : sys_partnum}, "chassis_info" : {"chassis_serial" : chassis_serial}, "motherboard_info" : {"motherboard_serial" : motherboard_serial, "motherboard_partnum" : motherboard_partnum}, "cpu_info" : {"cpu_quantity" : cpu_quantity, "cpu_partnum" : cpu_partnum}, "memory_info" : { "memory_list" : memory_serial_num_list}})
    #pprint.pprint(sys_json)
 
if __name__ == "__main__":
    macaddrs = ["0c-c4-7a-cc-b9-84", "0c-c4-7a-f9-9e-6a", "0c-c4-7a-f9-9e-72", "ac-1f-6b-03-05-ac"]
    mariadb_connect(db_name, db_user, db_host, db_password)
    with open("system_tarballs.conf") as macaddr_config:
         for macaddr_path in macaddr_config:
             macaddr_path = macaddr_path.rstrip()
             if (macaddr_path):
                 system_info(macaddr_path)
    exit(0)
    #macaddr = "0c-c4-7a-f8-9d-f8"
    for macaddr in macaddrs:
        print("\n####################" + macaddr + "################\n")
        system_info(macaddr)
