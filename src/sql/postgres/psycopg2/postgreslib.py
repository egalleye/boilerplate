import psycopg2
import binascii 
import json
import os
import random

# global declare
conn = None
cursor = None
db_name = "burnintest"
db_user = "postgres"
db_host = "localhost"
db_password = "xxxxxxxxxxxx"
db_table = "burnin_table_a"
json_file = "burnintest.json"


def pg_create_table(table_name, schema_str, db_name, db_user, db_host, db_password):
    global conn
    global cursor
    pg_createtable_str = "CREATE TABLE " + table_name + " (\n" + schema_str + ");"
    try:
        db_connect_str = "dbname='" + db_name \
                         +"' user='" + db_user \
                         + "' host='" + db_host \
                         + "' " + "password='" + db_password + "'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(db_connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute(pg_createtable_str)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        color_print("pg_connect() failed")
        print("Error msg:\n{0}".format(e))
    return 0



"""
pg_connect()
Connect to database
[IN]
    db_name - Name of database
    db_user - Alias of database user
    db_host - Hostname of database
    db_password - Password for database
[OUT]
    conn - object that holds psycog2 connection
"""
def pg_connect(db_name, db_user, db_host, db_password):
    global conn
    global cursor
    try:
        db_connect_str = "dbname='" + db_name \
                         +"' user='" + db_user \
                         + "' host='" + db_host \
                         + "' " + "password='" + db_password + "'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(db_connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        color_print("pg_connect() failed")
        print("Error msg:\n{0}".format(e))
    return 0

def pg_select_all(db_table):
    global cursor
    try:
        cursor = conn.cursor()
        pg_select_str = "SELECT * FROM " + db_table
        cursor.execute(pg_select_str)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        color_print("pg_select_all() failed")
        print("Error msg:\n{0}".format(e))

def pg_insert(db_table, table_header, insert_vals):
    global conn
    global cursor
    try:
        pg_select_str = "INSERT INTO " + db_table + " (" + table_header + ")  VALUES (" + insert_vals + ");"
        print(pg_select_str)
        # Comment next two lines for testing
        cursor.execute(pg_select_str)
        conn.commit()
    except Exception as e:
        color_print("pg_insert() failed")
        print("Error msg:\n{0}".format(e))

def pg_dump_json(dumpfile, ds_table, json_header):
    global cursor
    # remove old json file 
    try:
        os.remove(dumpfile)
    except OSError:
        pass
    with open(dumpfile, 'a') as jsonfile:
        jsonfile.write(json_header + "\n")
        try:
            cursor = conn.cursor()
            pg_select_str = "SELECT * FROM " + db_table
            cursor.execute(pg_select_str)
            rows = cursor.fetchall()
            #hrdwr_mac = ""
            #proj_name = ""
            #sys_serial = ""
            #memsize = 0
            #position = 0
            #date_tested = ""
            #prejson_tup = ("", 0)
            for row in rows:
                #print(row)
                row_str_format = ""
                for item in row:
                    row_str_format += str(item) + '\t'
                row_str_format += '\n'
                print(row_str_format)
                jsonfile.write(row_str_format)
                #hrdwr_mac = row[0]
                #proj_name = row[1]
                #sys_serial = row[2]
                #memsize = row[3]
                #position = row[4]
                #date_tested = row[5]
                # print("hrdwr_mac = {0} proj_name = {1} sys_serial = {2} memsize = {3} position = {4} date_tested = {5}".format(hrdwr_mac, proj_name, sys_serial, memsize, position, date_tested))
                #print("hrdwr_mac = {0} position = {1}".format(hrdwr_mac, position))
                #prejson_tup = (hrdwr_mac, position)
                #json_entry = json.dumps(prejson_tup)
                # jsonfile.write(hrdwr_mac + "\t" + date_tested.strftime('%x') + "\t" + str(position) + "\n")

                
        except Exception as e:
            color_print("pg_select_all() failed")
            print("Error msg:\n{0}".format(e))



def color_print(print_str):
    print('\x1b[3;31;40m' + "ERROR: " + print_str + '\x1b[0m')

def read_file(db_schema):
    file_content_str = ""
    with open(db_schema, "r") as schema_fd:
        for line in schema_fd:
            if (line.isspace()):
                continue
            file_content_str += line
    return file_content_str

# This function from minhazul-haque 
# URL: https://gist.github.com/pklaus/9638536
def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def test_pg_create_table():
    global db_table
    global db_name
    global db_user
    global db_host
    global db_password
    
    # NOTE: DB schema should be the full schema between CREATE TABLE ( <==> );
    db_schema = "database_schema.txt"
    schema_str = read_file(db_schema)
    pg_create_table(db_table, schema_str, db_name, db_user, db_host, db_password)

def test_pg_connect():
    global db_name
    global db_user
    global db_host
    global db_password
    retval = pg_connect(db_name, db_user, db_host, db_password)

def test_pg_insert():
    global db_table
    global db_name
    global db_user
    global db_host
    global db_password
    global json_file
    row_range_start = 0
    row_range_end = 31

    table_header = "lan1_mac, lan1_ip, rack_location, all_nics_mac, all_nics_chipset, all_nics_bandwidth, bmc_mac, bmc_ip, bmc_fru_tag, cpu_model, cpu_quality, cpu_current_speed, cpu_temp ,memeory_model, memory_quantity, memory_size, memory_current_speed, hdd_models, hdd_quantity, hdd_bandwidth, hdd_iops, gpu_model, gpu_quantity, mb_model, mb_serial, pcie_slot, pcie_device, power_supply_model, power_supply_quantity, power_supply_status, fan_model, fan_quantity, fan_speed, system_model, system_sn, system_temperature, system_uid_status, system_power_consumption, system_location, chassis_model, chassis_sn, ipmi_event, mce_log, bios_version, bios_date, ipmi_firmware_version, ipmi_firmware_date, testing_apps_list, current_running_app, app_starting_time, app_ending_time, app_status, app_result, app_logfile_location, final_result"
    #insert_vals = "'0025904C91cc', 'test7', '1234567890abcdk', 24730272, 7, now()"
    seqchar0 = 'a'
    # Setup to auto insert with random vals
    test_text = "testtxt"
    test_serial = "1234567890abcd"
    test_memsize = "24730272"
    test_ip = "192.168.0.111"
    test_date = "now()"
    for iter in range(row_range_start, row_range_end):
        position = str(iter)
        mac_ext = binascii.b2a_hex(os.urandom(3)).decode("utf-8")
        seqchar0 = chr(iter + 100)
        insertvals = "'" + rand_mac() + "', "  \
                     + "'" + test_ip + "', " \
                     + "'" + test_text + "', " \
                     + "'" + rand_mac() + "', "  \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + rand_mac() + "', "  \
                     + "'" + test_ip + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + position + ", " \
                     + position + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + position + ", " \
                     + position + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + position + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + position + ", " \
                     + "'" + test_text + "', " \
                     + position + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + test_date + ", " \
                     + "'" + test_text + "', " \
                     + test_date + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + test_date + ", " \
                     + test_date + ", " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "', " \
                     + "'" + test_text + "'"

        pg_insert(db_table, table_header, insertvals)
        print(insertvals)



def test_pg_dump_json():
    global db_table
    global json_file
    json_header = "lan1_mac	lan1_ip	rack_location	all_nics_mac	all_nics_chipset	all_nics_bandwidth	bmc_mac	bmc_ip	bmc_fru_tag	cpu_model	cpu_quality	cpu_current_speed	cpu_temp ,memeory_model	memory_quantity	memory_size	memory_current_speed	hdd_models	hdd_quantity	hdd_bandwidth	hdd_iops	gpu_model	gpu_quantity	mb_model	mb_serial	pcie_slot	pcie_device	power_supply_model	power_supply_quantity	power_supply_status	fan_model	fan_quantity	fan_speed	system_model	system_sn	system_temperature	system_uid_status	system_power_consumption	system_location	chassis_model	chassis_sn	ipmi_event	mce_log	bios_version	bios_date	ipmi_firmware_version	ipmi_firmware_date	testing_apps_list	current_running_app	app_starting_time	app_ending_time	app_status	app_result	app_logfile_location	final_result"
    pg_dump_json(json_file, db_table, json_header)


if __name__ == "__main__":
    # Uncomment to test pg_create_table()
    #test_pg_create_table()

    # Uncomment to test pg_connect()
    test_pg_connect()

    # Uncomment to test pg_insert()
    #test_pg_insert()
    
    # Uncomment to test pg_dump_json()
    test_pg_dump_json()
    """
    table_header = "hrdwr_mac, proj_name, sys_serial, memsize, position, date_tested"
    insert_vals = "'0025904C91cc', 'test7', '1234567890abcdk', 24730272, 7, now()"
    retval = 0
    seqchar0 = 'a'
    
    retval = pg_connect(db_name, db_user, db_host, db_password)
    pg_dump_json(json_file, db_table)
    # Print out entire table
    pg_select_all(db_table)

    # Setup to auto insert with random vals
    hrdwr_mac = "002590"
    proj_name = "test"
    sys_serial = "1234567890abcd"
    memsize = "24730272"
    date_tested = "now()"
    for iter in range(13, 25):
        position = str(iter)
        mac_ext = binascii.b2a_hex(os.urandom(3)).decode("utf-8")
        seqchar0 = chr(iter + 100)
        insertvals = "'" + hrdwr_mac + mac_ext + "', '" + proj_name + position + "', '" + sys_serial + seqchar0 + "', " + memsize + ", " + position + ", " + date_tested
        pg_insert(db_table, table_header, insertvals)
        #print(insertvals)
    """



