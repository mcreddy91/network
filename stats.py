#!/usr/bin/python

import ConfigParser, socket, wired, wireless

def current_stats():
    """Return a dict mapping MAC addresses to client information.
    
    Fields of each client information dictionary:
    'switch' -- hostname of the switch the client is connected to
    'port' -- number of the Ethernet port the client is plugged in to
    'ip' -- the most recent known IP address (not necessarily current)
    'traffic' -- the tuple (bytes received, bytes sent)
    'wifi' -- True iff this client is on the wireless network
    """
    c = ConfigParser.ConfigParser()
    c.readfp(open('network.cfg'))
    cisco_ip = socket.gethostbyname(c.get('cisco', 'hostname'))
    community = c.get('netgear', 'community')
    result = {}
    cisco_table = dict(wired.get_cisco_routing_table(cisco_ip))
    for host in c.get('netgear', 'hostnames').split():
        table = wired.get_netgear_mac_table(host, community)
        traffic = dict(wired.get_netgear_port_traffic(host, community))
        for port, mac in table:
            if cisco_table.get(mac) == cisco_ip:
                uplink_port = port
        for port, mac in table:
            if port != uplink_port:
                result[mac] = {'switch': host, 'port': port,
                               'traffic': traffic[port], 'wifi': False}
                if mac in cisco_table:
                    result[mac]['ip'] = cisco_table[mac]
    for mac, ip, traffic in wireless.get_all_info(c.get('wifi', 'hostname'),
                                                  c.get('wifi', 'user'),
                                                  c.get('wifi', 'pass')):
        if mac in result:
            result[mac].update({'wifi': True, 'traffic': traffic, 'ip': ip})
    return result

def subtract_stats(now, before):
    result = {}
    for mac in now:
        if mac in before:
            result[mac] = now[mac]
            result[mac]['traffic'] = [x-y for x,y in zip(now[mac]['traffic'],
                                                         before[mac]['traffic'])]
    return result

s1 = current_stats()
import time
time.sleep(5)
s2 = current_stats()

result = subtract_stats(s2, s1)
for mac in result:
    print(mac)
    print(result[mac])
    print('\n')
