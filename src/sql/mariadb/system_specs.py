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
    """
    memory_serial_nums = memory_serial_nums.split('\n')
    
    for serial_num in memory_serial_nums:
        if not (serial_num.startswith("NO")):
            if (serial_num):
                memory_serial_num_list.append(serial_num)
    """
    return memory_serial_num_list
    
def get_memory_info(macaddr_path):
    sys_conf_path = macaddr_path + "/sysinfo/dmidecode.log"
    memory_serial_num_list = parse_mem_serials(sys_conf_path)
    return memory_serial_num_list

def parse_cpu_quantity(sys_conf_path):
    parse_cpu_quantity_cmd = "cat " + sys_conf_path + "| grep 'CPU Quantities' | awk '{print $3}'"
    cpu_quantity = bash_cmd(parse_cpu_quantity_cmd)
    return cpu_quantity.rstrip()

def parse_cpu_partnum(sys_conf_path):
    parse_cpu_partnum_cmd = "cat " + sys_conf_path + "| grep 'CPU Model' | awk '{print $3$4$5$6$7}'"
    cpu_partnum = bash_cmd(parse_cpu_partnum_cmd)
    return cpu_partnum.rstrip()

def get_cpu_info(macaddr_path):
    sys_conf_path = macaddr_path + "/system.conf"
    cpu_quantity = parse_cpu_quantity(sys_conf_path)
    cpu_partnum = parse_cpu_partnum(sys_conf_path)
    return cpu_quantity, cpu_partnum

def parse_motherboard_serial(sys_conf_path):
    parse_motherboard_serial_cmd = "cat " + sys_conf_path + "| grep 'M/B SN' | awk '{print $3}'"
    motherboard_serial = bash_cmd(parse_motherboard_serial_cmd)
    return motherboard_serial.rstrip()

def parse_motherboard_partnum(sys_conf_path):
    parse_motherboard_partnum_cmd = "cat " + sys_conf_path + "| grep 'M/B PN' | awk '{print $3}'"
    motherboard_partnum = bash_cmd(parse_motherboard_partnum_cmd)
    return motherboard_partnum.rstrip()
   

def get_motherboard_info(macaddr_path):
    sys_conf_path = macaddr_path + "/system.conf"
    motherboard_serial = parse_motherboard_serial(sys_conf_path)
    motherboard_partnum = parse_motherboard_partnum(sys_conf_path)
    return motherboard_serial, motherboard_partnum


def chassis_info(macaddr_path):
    sys_conf_path = macaddr_path + "/system.conf"
    parse_chassis_serial_cmd = "cat " + sys_conf_path + "| grep 'Chassis SN' | awk '{print $3}'"
    chassis_serial = bash_cmd(parse_chassis_serial_cmd)
    return chassis_serial

def parse_sys_partnum(sys_conf_path):
    parse_sys_partnum_cmd = "cat " + sys_conf_path + "| grep 'System P/N' | awk '{print $3}'"
    sys_partnum = bash_cmd(parse_sys_partnum_cmd)
    return sys_partnum.rstrip()

def parse_sys_serial(sys_conf_path):
    parse_sys_serial_cmd = "cat " + sys_conf_path + "| grep 'System S/N' | awk '{print $3}'"
    sys_serial = bash_cmd(parse_sys_serial_cmd)
    return sys_serial.rstrip()

def system_info(macaddr_path):
    sys_conf_path = macaddr_path + "/SN.txt"
    #### System info ####
    sys_serial = parse_sys_serial(sys_conf_path)
    sys_partnum = parse_sys_partnum(sys_conf_path)

    #### Chassis info ####
    chassis_serial = chassis_info(macaddr_path)

    #### Motherboard info ####
    motherboard_serial, motherboard_partnum = get_motherboard_info(macaddr_path)

    #### CPU ####
    cpu_quantity, cpu_partnum = get_cpu_info(macaddr_path)
 
    #### Memory ####
    memory_serial_num_list = get_memory_info(macaddr_path)
    
    sys_json = json.dumps({"sys_info" : {"sys_serial" : sys_serial, "sys_partnum" : sys_partnum}, "chassis_info" : {"chassis_serial" : chassis_serial}, "motherboard_info" : {"motherboard_serial" : motherboard_serial, "motherboard_partnum" : motherboard_partnum}, "cpu_info" : {"cpu_quantity" : cpu_quantity, "cpu_partnum" : cpu_partnum}, "memory_info" : { "memory_list" : memory_serial_num_list}})

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
