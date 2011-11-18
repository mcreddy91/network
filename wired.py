"""
Module for getting information from wired CNUP equipment
(Netgear switches and Cisco router).
"""
import netsnmp, socket, ConfigParser

c = ConfigParser.ConfigParser()
c.readfp(open('network.cfg'))
netgear_hostnames = c.get('netgear', 'hostnames').split()
netgear_community = c.get('netgear', 'community')
cisco_ip = socket.gethostbyname(c.get('cisco', 'hostname'))

def format_mac(string):
    return ':'.join(['{0:>02x}'.format(ord(c)) for c in string])

def get_netgear_mac_table(hostname):
    """Returns [(port, mac_addr), ...]."""
    macs = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.1',
                            Version = 2,
                            Community = netgear_community,
                            DestHost = hostname)
    ports = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.2',
                             Version = 2,
                             Community = netgear_community,
                             DestHost = hostname)
    return zip(map(int, ports), map(format_mac, macs))

def get_netgear_port_traffic(hostname):
    """Returns [(port, octets_rcvd, octets_sent), ...]."""
    rcvd = netsnmp.snmpwalk('.1.3.6.1.2.1.2.2.1.10',
                            Version = 2,
                            Community = netgear_community,
                            DestHost = hostname)
    sent = netsnmp.snmpwalk('.1.3.6.1.2.1.2.2.1.16',
                            Version = 2,
                            Community = netgear_community,
                            DestHost = hostname)
    return zip(range(1,49), [map(int, k) for k in zip(rcvd, sent)])

def get_cisco_routing_table():
    """Returns [(mac_addr, ip_addr), ...]."""
    macs = netsnmp.snmpwalk('.1.3.6.1.2.1.3.1.1.2.51.1',
                            Version = 1,
                            Community = 'public',
                            DestHost = cisco_ip)
    ips = netsnmp.snmpwalk('.1.3.6.1.2.1.4.22.1.3.51',
                           Version = 1,
                           Community = 'public',
                           DestHost = cisco_ip)
    return zip(map(format_mac, macs), ips)

def get_cisco_inet_traffic():
    """Returns (rcvd, sent).  Note that rcvd == inbound."""
    rcvd = netsnmp.snmpget('.1.3.6.1.2.1.2.2.1.10.49',
                           Version = 1,
                           Community = 'public',
                           DestHost = cisco_hostname)[0]
    sent = netsnmp.snmpget('.1.3.6.1.2.1.2.2.1.16.49',
                           Version = 1,
                           Community = 'public',
                           DestHost = cisco_hostname)[0]
    return int(rcvd), int(sent)

def get_clients():
    result = {}
    ip_table = dict(get_cisco_routing_table())
    for hostname in netgear_hostnames:
        table = get_netgear_mac_table(hostname)
        traffic = dict(get_netgear_port_traffic(hostname))
        for port, mac in table:
            if ip_table.get(mac) == cisco_ip: uplink_port = port
        for port, mac in table:
            if port != uplink_port:
                result[mac] = {'switch': hostname, 'port': port,
                               'traffic': traffic[port], 'wifi': False}
                if mac in ip_table: result[mac]['ip'] = ip_table[mac]
    return result
