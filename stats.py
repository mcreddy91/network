#!/usr/bin/python

import ConfigParser, wired, wireless

c = ConfigParser.ConfigParser()
c.readfp(open('network.cfg'))

cisco = dict(c.items('cisco'))
print(wired.get_cisco_routing_table(cisco['hostname']))

netgear = dict(c.items('netgear'))
for host in netgear['hostnames'].split():
    print(wired.get_netgear_mac_table(host, netgear['community']))
    print(wired.get_netgear_port_traffic(host, netgear['community']))

wifi = dict(c.items('wifi'))
print(wireless.get_all_info(wifi['hostname'], wifi['user'], wifi['pass']))
