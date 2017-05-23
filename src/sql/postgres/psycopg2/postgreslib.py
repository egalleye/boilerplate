import psycopg2

def pg_connect():
    try:
        connect_str = "dbname='burnintest' user='postgres' host='localhost' " + \
                      "password='!0ngString'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        #cursor.execute("""CREATE TABLE tutorials (name char(40));""")
        # run a SELECT statement - no data in there, but we can try it
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    return cursor

def pg_select(cursor):
    try:
        cursor.execute("""SELECT * from burnin_table""")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

if __name__ == "__main__":
    print("whattup world!")
    cursor = pg_connect()
    pg_select(cursor)
