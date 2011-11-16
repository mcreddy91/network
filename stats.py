#!/usr/bin/python

import ConfigParser, socket, wired, wireless

def current_stats():
    """Return a dict mapping MAC addresses to client information.
    
    Fields of each client information dictionary:
    'switch' -- either 'wifi' or the tuple (switch_name, port)
    'ip' -- the most recent known IP address.  Not necessarily current.
    'traffic' -- the tuple (bytes received, bytes sent).
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
                result[mac] = {'switch': (host, port), 'traffic': traffic[port]}
                if mac in cisco_table:
                    result[mac]['ip'] = cisco_table[mac]
    for mac, ip, traffic in wireless.get_all_info(c.get('wifi', 'hostname'),
                                                  c.get('wifi', 'user'),
                                                  c.get('wifi', 'pass')):
        result[mac] = {'switch': 'wifi', 'traffic': traffic, 'ip': ip}
    return result

print(current_stats())
