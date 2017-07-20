import json
import pprint 
import subprocess


def verify_motherboard_info(motherboard_info):
    linecnt = 0
    motherboard_pn = motherboard_info['mb_pn']
    motherboard_serial = motherboard_info['mb_serial']
    # Call grep to get dmidecode info on motherboard
    try:
        dmidout=subprocess.check_output('cat dmidecode.out | grep -A 4 "Base Board Information"', shell=True)
        dmidout=dmidout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)

    for line in dmidout.split('\n'):
        line = line.rstrip()
        if (linecnt == 2):
            motherboard_prod_num = line.split(':')[1]
            motherboard_prod_num = motherboard_prod_num.lstrip()
        elif(linecnt == 4):
            motherboard_serial_num = line.split(':')[1]
            motherboard_serial_num = motherboard_serial_num.lstrip()
        linecnt += 1

    if (motherboard_pn == motherboard_prod_num):
        print("CHECK: motherboard product number is {0}".format(motherboard_pn))
    else:
        print("FAILED: motherboard product number is {0} expected {1}".format(motherboard_prod_num, motherboard_pn))

    if (motherboard_serial == motherboard_serial_num):
        print("CHECK: motherboard serial number is {0}".format(motherboard_serial))
    else:
        print("FAILED: motherboard serial number is {0} expected {1}".format(motherboard_serial_num, motherboard_serial))


def verify_sys(sys_info):
    linecnt = 0
    system_pn = sys_info['system_pn']
    system_serial = sys_info['system_serial']
    # Call grep to get 4 lines pertaining to system info 
    try:
        dmidout=subprocess.check_output('cat dmidecode.out | grep -A 4 "System Information"', shell=True)
        dmidout=dmidout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)

    for line in dmidout.split('\n'):
        line = line.rstrip()
        if (linecnt == 2):
            system_prod_num = line.split(':')[1]
            system_prod_num = system_prod_num.lstrip()
        elif(linecnt == 4):
            system_serial_num = line.split(':')[1]
            system_serial_num = system_serial_num.lstrip()
        linecnt += 1
    if (system_pn == system_prod_num):
        print("CHECK: system product number is {0}".format(system_pn))
    else:
        print("FAILED: system product number is {0} expected {1}".format(system_prod_num, system_pn))

    if (system_serial == system_serial_num):
        print("CHECK: system serial number is {0}".format(system_serial))
    else:
        print("FAILED: system serial number is {0} expected {1}".format(system_serial_num, system_serial))

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
    motherboard_info = system_conf['motherboard']

    mb_pn = system_conf['motherboard']['mb_pn']
    mb_serial = system_conf['motherboard']['mb_serial']

    chassis_pn = system_conf['chassis']['chassis_pn']
    chassis_serial = system_conf['chassis']['chassis_serial']

    cpu_pn = system_conf['cpu']['cpu_pn']

    verify_sys(sys_info)
    verify_motherboard_info(motherboard_info)

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
    
