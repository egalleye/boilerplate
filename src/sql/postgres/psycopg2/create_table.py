import psycopg2
"""
This function is in a different file since it seems to be needed
less often and has potential to be abused.
"""

def pg_create_table(table_name, schema_str, db_name, db_user, db_host, db_password):
    pg_createtable_str = "CREATE TABLE " + table_name + " (\n" + schema_str + ");"
    print(pg_createtable_str)
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



def read_file(db_schema):
    file_content_str = ""
    with open(db_schema, "r") as schema_fd:
        for line in schema_fd:
            if (line.isspace()):
                continue
            file_content_str += line
    return file_content_str

if __name__ == "__main__":
    db_name = "burnintest"
    db_user = "postgres"
    db_host = "localhost"
    db_password = "!0ngString"
    db_table = "burnin_table_auto"

    # NOTE: DB schema should be the full schema between CREATE TABLE ( <==> );
    db_schema = "database_schema.txt"
    schema_str = read_file(db_schema)
    pg_create_table(db_table, schema_str, db_name, db_user, db_host, db_password)
