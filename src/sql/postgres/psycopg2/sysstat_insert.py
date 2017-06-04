import psycopg2
import binascii
import os
import random
import postgreslib

db_table = "clustreye"
PATH_TO_CSV = "/var/www/html/sys_stats.csv"

if __name__ == "__main__":
    postgreslib.test_pg_connect()
    (table_names, table_types) = postgreslib.parse_schema()
    table_header = ", ".join(table_names)
    with open(PATH_TO_CSV) as csv_fd:
        linecount = 0
        for line in csv_fd:
            linecount += 1
            if (linecount == 2):
                (cpu_usage, disc_usage, mem_usage) = line.split(',')
        
    csv_fd.close()
    postgres_row = "now()" + ', ' + cpu_usage + ',' + disc_usage + ',' + mem_usage 
    postgreslib.pg_insert(db_table, table_header, postgres_row)


    
