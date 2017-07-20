import os
import psycopg2
import binascii
import os
import random
import postgreslib

base_dir = "/home/test/supermicro_benchmarks/"
db_table = "drive_test"
db_name = "hdwr_stats_db"
db_user = "hdwr_stats_db"
db_host = "localhost"
db_password = "supermicro"
db_schema_file = "drive_schema.txt"

def parse_cpu_results():
    cpu_dir = base_dir + "cpu/"
    dir_contents = os.listdir(cpu_dir);
    for csvfile in dir_contents:
        line_num = 0
        print("filename is " + csvfile)
        fullfilename = cpu_dir + csvfile
        with open(fullfilename, "r") as csv_fd:
            for line in csv_fd:
                if (line_num == 0):
                    print("header = " + line)
                else:
                    print("values = " + line)
                line_num += 1

def parse_drive_results():
    cpu_dir = base_dir + "drive/"
    dir_contents = os.listdir(cpu_dir);
    for csvfile in dir_contents:
        line_num = 0
        print("filename is " + csvfile)
        fullfilename = cpu_dir + csvfile
        with open(fullfilename, "r") as csv_fd:
            for line in csv_fd:
                line = line.rstrip('\n')
                if (line_num == 0):
                    print("header = " + line)
                    table_header = line
                else:
                    print("values = " + line)
                    postgres_row = line
                line_num += 1
        postgreslib.pg_insert(db_table, table_header, postgres_row)

def parse_mem_results():
    cpu_dir = base_dir + "mem/"
    dir_contents = os.listdir(cpu_dir);
    for csvfile in dir_contents:
        line_num = 0
        print("filename is " + csvfile)
        fullfilename = cpu_dir + csvfile
        with open(fullfilename, "r") as csv_fd:
            for line in csv_fd:
                if (line_num == 0):
                    print("header = " + line)
                else:
                    print("values = " + line)
                line_num += 1



if __name__ == "__main__":
    postgreslib.pg_connect(db_name, db_user, db_host, db_password)
    (table_names, table_types) = postgreslib.parse_schema(db_schema_file)
    table_header = ", ".join(table_names)
    parse_cpu_results()
    parse_drive_results()
