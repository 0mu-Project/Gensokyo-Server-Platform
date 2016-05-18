import psutil, sys
net = psutil.net_io_counters() 
if sys.argv[1] == "recv":
    print('{0:.2f} Mb'.format(net.bytes_recv / 1024 /1024)  )
elif sys.argv[1] == "sent":
    print('{0:.2f} Mb'.format(net.bytes_sent / 1024 /1024)  )
