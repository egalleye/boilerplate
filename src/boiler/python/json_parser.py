import json
import pprint 

def verify_sys(sys_info):
    system_pn = sys_info['system_pn']
    system_serial = sys_info['system_serial']
    print("sys serial number = " + system_serial)

"""
verify_system() -- break system into hardware categories and call respective tests
[IN]
    system_conf:  json struct of system configuration
[OUT]
    retval: 0 If verification tests passed, -1 if failed
"""
def verify_system(system_conf):
    # pprint.pprint(system_conf)
    # 
    sys_info = system_conf['system']

    mb_pn = system_conf['motherboard']['mb_pn']
    mb_serial = system_conf['motherboard']['mb_serial']

    chassis_pn = system_conf['chassis']['chassis_pn']
    chassis_serial = system_conf['chassis']['chassis_serial']

    cpu_pn = system_conf['cpu']['cpu_pn']

    verify_sys(sys_info)

"""
    for memory_device in system_conf['memory']:
        print("memory device serial" + memory_device['mem_serial'])

    for drive in system_conf['drives']:
        print("drive type " + drive['drive_pn'])

    print("motherboard serial number = " + mb_serial)
    print("chassis serial number = " + chassis_serial)
    print("cpu serial number = " + cpu_pn)
"""

"""
parse_system_config() -- parse file with system details
[IN]:
    system_conf_file: filename of config file
[OUT]:
    system_conf: json struct of config file
"""
def parse_system_config(system_conf_file):
    # open up system file and parse json
    with open(system_conf_file) as system_conf_fp:
        system_conf = json.load(system_conf_fp)
    return system_conf

if __name__ == "__main__":
    system_conf = parse_system_config("system.conf")
    verify_system(system_conf)
    
