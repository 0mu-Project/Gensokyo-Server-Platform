from docker import Client
listst = []

def genlist(name):
    cli = Client(base_url='unix://var/run/docker.sock')
    stats_obj = cli.stats(str(name),stream=False)
    global listst 
    listst = stats_obj

def info(name):
    try:
        genlist(name)
    except Exception as e:
        print('dont have this container')
        pass 
    percpu = listst.get('cpu_stats')['cpu_usage']['percpu_usage']
    ptusage = listst.get('precpu_stats')['cpu_usage']['total_usage']
    ctusage = listst.get('cpu_stats')['cpu_usage']['total_usage']
    syspusage = listst.get('precpu_stats')['system_cpu_usage']
    sysctusage = listst.get('cpu_stats')['system_cpu_usage']
    delta = ctusage - ptusage
    sdelta = sysctusage - syspusage
    if sdelta > 0 and delta > 0:
        cpupercent = round(100.0 * float(delta) / sdelta * len(percpu),2)
    else:
        cpupercent = int(0.00)
    memraw = listst.get('memory_stats')['usage'] / 1024 / 1024 / 1024
    memlimraw = listst.get('memory_stats')['limit'] / 1024 / 1024 / 1024
    mempercent = round(100.0 * float(memraw)/float(memlimraw),2)
    rxbyte = listst.get('networks')['eth0']['tx_bytes']
    txbyte = listst.get('networks')['eth0']['rx_bytes']
    return [cpupercent,memraw,memlimraw,mempercent,rxbyte,txbyte]

