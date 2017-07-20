import psycopg2
import binascii
import os
import random
import postgreslib

DUMP_FILE = "drive_test.csv"
db_table = "drive_test"
db_name = "hdwr_stats_db"
db_user = "hdwr_stats_db"
db_host = "localhost"
db_password = "supermicro"
db_schema_file = "drive_schema.txt"

PATH_TO_CSV = "/usr/share/nginx/html/drive_test.csv"

if __name__ == "__main__":
    postgreslib.pg_connect(db_name, db_user, db_host, db_password)
    (table_names, table_types) = postgreslib.parse_schema(db_schema_file)
    table_header = ", ".join(table_names)
    postgreslib.pg_dump_csv(DUMP_FILE, db_table, table_header)


    
