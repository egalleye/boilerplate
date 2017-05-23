"""
This is intended to be a lib for weird print format stuff
I run into all the time. 

Import it as a lib by specifying:
import /full/path/to/printlib.py

"""


"""
This function is useful to hook into if you have a 
print_err() type function
"""
def color_print(print_str):
    print('\x1b[3;31;40m' + print_str + '\x1b[0m')

if __name__ == "__main__":
    color_print("whattup world!?")
  
