import psycopg2

def read_file(db_schema):
    file_content_str = ""
    with open(db_schema, "r") as schema_fd:
        for line in schema_fd:
            if (line.isspace()):
                continue
            file_content_str += line
        
    print(file_content_str)

if __name__ == "__main__":
    # NOTE: DB schema should be the full schema between CREATE TABLE ( <==> );
    db_schema = "database_schema.txt"
    input_str = read_file(db_schema)
    #create_db(input_str)
