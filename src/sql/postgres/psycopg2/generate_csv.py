import psycopg2
import binascii
import os
import random
import postgreslib

DUMP_FILE = "sys_stats_timeseries.csv"
db_table = "clustreye"
PATH_TO_CSV = "/var/www/html/sys_stats.csv"

if __name__ == "__main__":
    postgreslib.test_pg_connect()
    (table_names, table_types) = postgreslib.parse_schema()
    table_header = ", ".join(table_names)
    postgreslib.pg_dump_csv(DUMP_FILE, db_table, table_header)


    
