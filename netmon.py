#!/usr/bin/python

import sys, time, stats
sleeptime = float(sys.argv[1])

t = time.time()
now = stats.current_stats()

while True:
    time.sleep(t + sleeptime - time.time())
    t = time.time()
    then, now = now, stats.current_stats()
    result = stats.subtract_stats(now, then)
    for mac in result:
        print(mac)
        print(result[mac])
