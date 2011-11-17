#!/usr/bin/python

import sys, time, stats
sleeptime = float(sys.argv[1])

t = time.time()
now = stats.current_stats()

while True:
    try:
        time.sleep(t + sleeptime - time.time())
        t = time.time()
        then, now = now, stats.current_stats()
        result = stats.subtract_stats(now, then)
        macs = sorted(result.keys(), key = lambda mac: -sum(result[mac]['traffic']))
        for mac in macs[:5]:
            rcvd, sent = [octets/(sleeptime * 2**17) for octets in result[mac]['traffic']]
            print('{0}\t{1}\t{2:.3} mb/s\t{3:.3} mb/s'.format(mac, result[mac]['ip'], rcvd, sent))
    except KeyboardInterrupt:
        break
        
