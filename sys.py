import psutil, os, signal
import platform
from datetime import datetime
import speedtest, json
import paho.mqtt.client as mqtt
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt has been caught. Cleaning up...")
    os._exit(1)
signal.signal(signal.SIGINT, keyboardInterruptHandler)
client = mqtt.Client()
client.connect(" ",1883,60) #add IP address of the MQTT server 
uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
System_Information=json.dumps(
[dict(name='System', description=uname.system),
dict(name='Node Name', description=uname.node),
dict(name='Release', description=uname.release),
dict(name='Version', description=uname.version),
dict(name='Machine', description=uname.machine),
dict(name='Boot_Time', description=f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")])
client.publish("topic/sys",System_Information)
while(1):
    cpufreq = psutil.cpu_freq()
    CPU=json.dumps(
    [dict(name='Total cores', description=psutil.cpu_count(logical=True)),
    dict(name='Max Frequency', description=f"{cpufreq.max:.2f}Mhz"),
    dict(name='Min Frequency', description=f"{cpufreq.min:.2f}Mhz"),
    dict(name='Current Frequency', description=f"{cpufreq.current:.2f}Mhz"),
    dict(name='Total CPU Usage', description=f"{psutil.cpu_percent()}%")])
    client.publish("topic/CPU",CPU)
    svmem = psutil.virtual_memory()
    Memory_Information=json.dumps(
    [dict(name='Total Memory', description=f"{get_size(svmem.total)}"),
    dict(name='Available Memory', description=f"{get_size(svmem.available)}"),
    dict(name='Used Memory', description=f"{get_size(svmem.used)}"),
    dict(name='Memory Percentage', description=f"{svmem.percent}%")])
    client.publish("topic/memory",Memory_Information)
    swap = psutil.swap_memory()
    Swap_Information=json.dumps(
    [dict(name='Total swap', description=f"{get_size(swap.total)}"),
    dict(name='Free Swap', description=f"{get_size(swap.free)}"),
    dict(name='Used Swap', description=f"{get_size(swap.used)}"),
    dict(name='Swap Percentage', description=f"{swap.percent}%")])
    client.publish("topic/swap",Swap_Information)
    disk_lst=[]
    partitions = psutil.disk_partitions()
    for partition in partitions:
        disk_lst.append(dict(name="Device",description=partition.device))
        disk_lst.append(dict(name="Mountpoint",description=partition.mountpoint))
        disk_lst.append(dict(name="File system type",description=partition.fstype ))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disk_lst.append(dict(name="Total Size",description=get_size(partition_usage.total)))
        disk_lst.append(dict(name="Used",description=get_size(partition_usage.used)))
        disk_lst.append(dict(name="Free",description=get_size(partition_usage.free)))
        disk_lst.append(dict(name="Percentage",description=f"{partition_usage.percent}%"))
    disk_io = psutil.disk_io_counters()
    disk_lst.append(dict(name="Total read",description=get_size(disk_io.read_bytes)))
    disk_lst.append(dict(name="Total write",description=get_size(disk_io.write_bytes)))
    client.publish("topic/disk",json.dumps(disk_lst))
    ntw_lst=[]
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            ntw_lst.append(dict(name="Interface",description=interface_name))
            if str(address.family) == 'AddressFamily.AF_INET':
                ntw_lst.append(dict(name="IP Address",description=address.address))
                ntw_lst.append(dict(name="Netmask",description=address.netmask))
                ntw_lst.append(dict(name="Broadcast IP",description=address.broadcast))
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                ntw_lst.append(dict(name="MAC Address",description=address.address))
                ntw_lst.append(dict(name="Netmask",description=address.netmask))
                ntw_lst.append(dict(name="Broadcast MAC",description=address.broadcast))
    client.publish("topic/network",json.dumps(ntw_lst))
    st = speedtest.Speedtest()
    servernames =[]
    st.get_servers(servernames)
    speed=json.dumps(
    [dict(name='download speed', description=f"{get_size(st.download())}ps"),
    dict(name='upload speed', description=f"{get_size(st.upload())}ps"),
    dict(name='ping', description=st.results.ping)])
    client.publish("topic/speed",speed)
