#!/usr/bin/python

import netsnmp, ConfigParser

c = ConfigParser.ConfigParser()
c.readfp(open('network.cfg'))
pdu_hostname = c.get('pdu', 'hostname')
pdu_community = c.get('pdu', 'community')

def set_plug(index, status):
    message = netsnmp.Varbind('.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.{0}'.format(index),
                              val = 1 if status else 2, type = 'int')
    netsnmp.snmpset(message, Version = 1,
                    Community = pdu_community,
                    DestHost = pdu_hostname)
