"""
Module for getting information from wired CNUP equipment
(Netgear switches and Cisco router).
"""
import netsnmp

def format_mac(string):
    return ':'.join(['{0:>02x}'.format(ord(c)) for c in string])

def get_netgear_mac_table(hostname, community):
    """Returns [(port, mac_addr), ...]."""
    macs = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.1',
                            Version = 2,
                            Community = community,
                            DestHost = hostname)
    ports = netsnmp.snmpwalk('.1.3.6.1.2.1.17.4.3.1.2',
                             Version = 2,
                             Community = community,
                             DestHost = hostname)
    return zip(map(int, ports), map(format_mac, macs))

def get_netgear_port_traffic(hostname, community):
    """Returns [(port, octets_rcvd, octets_sent), ...]."""
    rcvd = netsnmp.snmpwalk('.1.3.6.1.2.1.2.2.1.10',
                            Version = 2,
                            Community = community,
                            DestHost = hostname)
    sent = netsnmp.snmpwalk('.1.3.6.1.2.1.2.2.1.16',
                            Version = 2,
                            Community = community,
                            DestHost = hostname)
    return zip(range(1,49), rcvd, sent)

def get_cisco_routing_table(hostname):
    """Returns [(mac_addr, ip_addr), ...]."""
    # Limited to 18.* IP addresses by the OIDs.
    macs = netsnmp.snmpwalk('.1.3.6.1.2.1.3.1.1.2.51.1.18',
                            Version = 1,
                            Community = 'public',
                            DestHost = hostname)
    ips = netsnmp.snmpwalk('.1.3.6.1.2.1.4.22.1.3.51.18',
                           Version = 1,
                           Community = 'public',
                           DestHost = hostname)
    return zip(map(format_mac, macs), ips)
