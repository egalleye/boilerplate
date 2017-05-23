import psycopg2

def color_print(print_str):
    print('\x1b[3;31;40m' + "ERROR: " + print_str + '\x1b[0m')

"""
pg_connect()
Connect to database
[IN]

[OUT]
    None
"""
def pg_connect(db_name, db_user, db_host, db_password):
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
    return cursor

def pg_select_all(cursor):
    try:
        cursor.execute("""SELECT * from burnin_table""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        color_print("pg_select() failed")
        print("Error msg:\n{0}".format(e))

def pg_insert(db_name, cursor):
    print("dbname " + db_name)
    try:
        cursor.execute("""INSERT INTO " + db_name+ " """)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        color_print("pg_select() failed")
        print("Error msg:\n{0}".format(e))


if __name__ == "__main__":
    db_name = "burnintest"
    db_user = "postgres"
    db_host = "localhost"
    db_password = "!0ngString"
    cursor = pg_connect(db_name, db_user, db_host, db_password)
    pg_select_all(cursor)
    print("Inserting shit!")
    #pg_insert(db_name, cursor)
