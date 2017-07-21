import json
import pprint 
import subprocess

def verify_drive(drive):
    linecnt = 0
    devdir = "/dev/" + drive['locator']
    drive_pn = drive['drive_pn']
    drive_serial = drive['drive_serial']
    smartctl_cmd = "sudo smartctl -i " + devdir
    
    try:
        smartctl_out=subprocess.check_output(smartctl_cmd, shell=True)
        smartctl_out=smartctl_out.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)
        return -1

    for line in smartctl_out.split('\n'):
        if (linecnt == 5):
            drive_prod_num = line.split(':')[1].rstrip().lstrip()
        elif (linecnt == 6):
            drive_serial_num = line.split(':')[1].rstrip().lstrip()
        linecnt += 1

    if (drive_prod_num == drive_pn):
        print("CHECK: drive product number is {0}".format(drive_pn))
    else:
        print("FAILED: drive product number is {0} expected {1}".format(drive_prod_num, drive_pn))
        return -1

    if (drive_serial_num == drive_serial):
        print("CHECK: drive serial number is {0}".format(drive_serial))
    else:
        print("FAILED: drive serial number is {0} expected {1}".format(drive_serial_num, drive_serial))
        return -1

    return 0
       
    

def verify_drives(drive_info):
    linecnt = 0
    try:
        inxi_out=subprocess.check_output("inxi -Dplxx -c 0", shell=True)
        inxi_out=inxi_out.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)
        return -1

    for line in inxi_out.split('\n'):
        if (linecnt == 0):
            linecnt += 1
            continue
        if not line:
            continue
        columns = list(filter(None, line.split(' ')))
        print(columns[4])
        print(columns[8])
        linecnt += 1

def verify_cpu(cpu_info):
    linecnt = 0
    cpu_pn = cpu_info['cpu_pn']
    # Call lshw to get info on cpu
    try:
        cpu_prod_num=subprocess.check_output("sudo lshw -c cpu | grep version | awk '{print $5}'", shell=True)
        cpu_prod_num=cpu_prod_num.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)
        return -1

    cpu_prod_num = cpu_prod_num.rstrip()
    cpu_prod_num = cpu_prod_num.lstrip()
    if (cpu_prod_num == cpu_pn):
        print("CHECK: cpu product number is {0}".format(cpu_pn))
    else:
        print("FAILED: cpu product number is {0} expected {1}".format(cpu_prod_num, cpu_pn))
        return -1
    return 0

def verify_chassis(chassis_info):
    linecnt = 0
    chassis_pn = chassis_info['chassis_pn']
    chassis_serial = chassis_info['chassis_serial']

    # Call grep to get dmidecode info on chassis
    try:
        dmidout=subprocess.check_output('cat dmidecode.out | grep -A 5 "Chassis Information"', shell=True)
        dmidout=dmidout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)

    for line in dmidout.split('\n'):
        line = line.rstrip()
        if (linecnt == 4):
            chassis_prod_num = line.split(':')[1]
            chassis_prod_num = chassis_prod_num.lstrip()
        elif(linecnt == 5):
            chassis_serial_num = line.split(':')[1]
            chassis_serial_num = chassis_serial_num.lstrip()
        linecnt += 1

    if (chassis_pn == chassis_prod_num):
        print("CHECK: chassis product number is {0}".format(chassis_pn))
    else:
        print("FAILED: chassis product number is {0} expected {1}".format(chassis_prod_num, chassis_pn))
        return -1

    if (chassis_serial == chassis_serial_num):
        print("CHECK: chassis serial number is {0}".format(chassis_serial))
    else:
        print("FAILED: chassis serial number is {0} expected {1}".format(chassis_serial_num, chassis_serial))
        return -1
    return 0
 


def verify_motherboard(motherboard_info):
    linecnt = 0
    motherboard_pn = motherboard_info['mb_pn']
    motherboard_serial = motherboard_info['mb_serial']
    # Call grep to get dmidecode info on motherboard
    try:
        dmidout=subprocess.check_output('cat dmidecode.out | grep -A 4 "Base Board Information"', shell=True)
        dmidout=dmidout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)
        return -1

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
        return -1

    if (motherboard_serial == motherboard_serial_num):
        print("CHECK: motherboard serial number is {0}".format(motherboard_serial))
    else:
        print("FAILED: motherboard serial number is {0} expected {1}".format(motherboard_serial_num, motherboard_serial))
        return -1


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
        return -1

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
    chassis_info = system_conf['chassis']

    chassis_pn = system_conf['chassis']['chassis_pn']
    chassis_serial = system_conf['chassis']['chassis_serial']

    cpu_info = system_conf['cpu']

    drive_info = system_conf['drives']

    for memory_device in system_conf['memory']:
        print("memory device serial" + memory_device['mem_serial'])



    verify_sys(sys_info)
    verify_motherboard(motherboard_info)
    verify_chassis(chassis_info)
    #verify_cpu(cpu_info)
    verify_drives(drive_info)

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
    
