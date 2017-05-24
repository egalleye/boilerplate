def read_file(filename):
    file_content_str = ""
    with open(filename, "r") as file_descriptor:
        for line in file_descriptor:
            if (line.isspace()):
                continue
            file_content_str += line
    return file_content_str

if __name__ == "__main__":
    filename = "filename.txt"
    file_content_str = read_file(filename)
    print(file_content_str)
