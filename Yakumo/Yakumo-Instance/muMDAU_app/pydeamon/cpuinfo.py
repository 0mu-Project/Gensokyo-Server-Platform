import psutil, sys
if sys.argv[1] == "percent":
    a = psutil.cpu_percent(interval=0.3)
    print(a)
elif sys.argv[1] == "core":
    a = psutil.cpu_count(logical=False)
    print(a)
