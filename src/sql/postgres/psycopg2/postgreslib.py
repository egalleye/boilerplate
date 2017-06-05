import psycopg2
import binascii 
import os
import random

# global declare
conn = None
cursor = None
db_name = "pg_db"
db_user = "postgres"
db_host = "localhost"
db_password = "xxxxxxxxxxxx"
db_table = "clustreye"
csv_file = "clustreye.csv"
db_schema_file = "database_schema.txt"


def pg_create_table(table_name, schema_str, db_name, db_user, db_host, db_password):
    global conn
    global cursor
    pg_createtable_str = "CREATE TABLE " + table_name + " (\n" + schema_str + ");"
    try:
        db_connect_str = "dbname='" + db_name \
                         +"' user='" + db_user \
                         + "' host='" + db_host \
                         + "' " + "password='" + db_password + "'"
        print(pg_createtable_str)
        # use our connection values to establish a connection
        conn = psycopg2.connect(db_connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        cursor.execute(pg_createtable_str)
        conn.commit()
        cursor.close()
        conn.close()
        """
        """
    except Exception as e:
        color_print("pg_create_table() failed")
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
        # Comment next two lines for testing
        cursor.execute(pg_select_str)
        conn.commit()
        print(pg_select_str);
    except Exception as e:
        color_print("pg_insert() failed")
        print("Error msg:\n{0}".format(e))

def pg_dump_csv(dumpfile, ds_table, csv_header):
    global cursor
    # remove old csv file 
    try:
        os.remove(dumpfile)
    except OSError:
        pass
    with open(dumpfile, 'a') as csvfile:
        csvfile.write(csv_header + "\n")
        try:
            cursor = conn.cursor()
            pg_select_str = "SELECT * FROM " + db_table
            cursor.execute(pg_select_str)
            rows = cursor.fetchall()
            for row in rows:
                row_str_format = ""
                for item in row:
                    row_str_format += str(item) + ", "
                # Hack to get rid of trailing comma
                row_str_format = row_str_format.strip().rstrip(',')
                row_str_format += '\n'
                print(row_str_format)
                csvfile.write(row_str_format)
                
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
    global db_schema_file
    
    # NOTE: DB schema should be the full schema between CREATE TABLE ( <==> );
    schema_str = read_file(db_schema_file)
    pg_create_table(db_table, schema_str, db_name, db_user, db_host, db_password)

def test_pg_connect():
    global db_name
    global db_user
    global db_host
    global db_password
    retval = pg_connect(db_name, db_user, db_host, db_password)

"""
parse_schema()
Helper function to parse the database_schema
Inputs: None
Outputs: tups of (table names, table types) that should be 1:1
"""
def parse_schema():
    global db_schema_file
    table_names = []
    table_types = []
    with open(db_schema_file, 'r') as schema_fd:
        for line in schema_fd:
            # allow for empty lines without barfing...
            if (len(line.strip()) == 0):
                continue
            line = line.replace(',', '')
            line = line.lstrip()
            line = line.rstrip()
            splitline = line.split(' ')
            varname = splitline[0]
            vartype = splitline[1]
            vartype = vartype.strip()
            table_names.append(varname)
            table_types.append(vartype)
    if (len(table_names) != len(table_types)): 
        color_print("Mismatch between types and variable names in db schema")
        return None
    return (table_names, table_types)

def create_row(table_types):
    values_row = ""
    fake_text = "testtxt"
    fake_serial = "1234567890abcd"
    fake_memsize = "24730272"
    fake_ip = "192.168.0.111"
    fake_date = "now()"
    fake_int = 24
    fake_real = 72.24

    for dbtype in table_types:
        if (dbtype == "text"):
            values_row += "'" + fake_text + "', "
        elif (dbtype == "integer"):
            values_row += str(fake_int) + ", "
        elif (dbtype == "date"):
            values_row += "now()" + ", " 
        elif (dbtype == "timestamp"):
            values_row += "now()" + ", " 
        elif (dbtype == "macaddr"):
            values_row +=  "'" + rand_mac() + "'" + ", " 
        elif (dbtype == "inet"):
            values_row +=  "'" + fake_ip + "'" + ", " 
        elif (dbtype == "real"):
            values_row +=  str(fake_real)  + ", " 
        else:
            color_print("ERROR: Unknown row type!" + dbtype)
    # Hack to remove trailing ', ' that is added by for loop
    values_row = values_row.strip().rstrip(',')
    return values_row
                

def test_pg_insert():
    global db_table
    row_range_start = 0
    row_range_end = 31
    (table_names, table_types) = parse_schema()
    insert_str = ""
    table_header = ", ".join(table_names)
    table_header.strip().rstrip(',')
    for itor in range(row_range_start, row_range_end):
        insertvals = create_row(table_types)
        #insert_str = "INSERT INTO burnin_table_a (" + table_header + ") VALUES (" + row + ");"
        pg_insert(db_table, table_header, insertvals)

        print(insert_str)

def test_pg_dump_csv():
    global db_table
    global csv_file
    (table_names, table_types) = parse_schema()
    csv_header = ", ".join(table_names)
    pg_dump_csv(csv_file, db_table, csv_header)


if __name__ == "__main__":
    # Uncomment to test pg_create_table()
    #test_pg_create_table()

    # Uncomment to test pg_connect()
    test_pg_connect()

    # Uncomment to test pg_insert()
    test_pg_insert()
    
    # Uncomment to test pg_dump_csv()
    #test_pg_dump_csv()



