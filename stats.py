#!/usr/bin/python

import ConfigParser, socket, wired, wireless

c = ConfigParser.ConfigParser()
c.readfp(open('network.cfg'))

result = {}

cisco_ip = socket.gethostbyname(c.get('cisco', 'hostname'))
cisco_table = dict(wired.get_cisco_routing_table(cisco_ip))

netgear_comm = c.get('netgear', 'community')
for host in c.get('netgear', 'hostnames').split():
    table = wired.get_netgear_mac_table(host, netgear_comm)
    for port, mac in table:
        if cisco_table.get(mac) == cisco_ip:
            uplink_port = port
    for port, mac in table:
        if port != uplink_port:
            result[mac] = "Connected to switch {0} on port {1}\n".format(host, port)

wifi = dict(c.items('wifi'))
wifi_data = wireless.get_all_info(wifi['hostname'], wifi['user'], wifi['pass'])


for mac, ip, rcvd, sent in wifi_data:
    result[mac] = result.get(mac, '') + 'Connected to wifi with IP address {0}\n'.format(ip)
for mac in result:
    if mac in cisco_table:
        result[mac] += 'Cisco says it has IP address {0}\n'.format(cisco_table[mac])

for mac in result:
    print(mac)
    print(result[mac])
