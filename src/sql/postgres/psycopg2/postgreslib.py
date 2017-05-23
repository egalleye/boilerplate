import psycopg2

def color_print(print_str):
    print('\x1b[3;31;40m' + print_str + '\x1b[0m')


def pg_connect():
    try:
        db_connect_str = "dbname='brnintest' user='postgres' host='localhost' " + \
                      "password='!0ngString'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(db_connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        color_print("Uh oh, can't connect. Invalid dbname, user or password?")
        color_print(colors.red("Error msg:\n{0}".format(e)))
    return cursor

def pg_select(cursor):
    try:
        cursor.execute("""SELECT * from burnin_table""")
        rows = cursor.fetchall()
        for row in rows:
            color_print(row)
    except Exception as e:
        color_print("Uh oh, can't connect. Invalid dbname, user or password?")
        color_print("Error msg:\n{0}".format(e))

if __name__ == "__main__":
    cursor = pg_connect()
    pg_select(cursor)
