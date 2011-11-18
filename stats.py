#!/usr/bin/python

import ConfigParser, socket, wired, wireless, moira

def update_with_wifi_data(clients):
    """Inject data from the wireless controller into 'clients'. """
    for mac, ip, traffic in wireless.get_all_info():
        if mac in clients:
            clients[mac].update(
                {'wifi': True, 'traffic': traffic, 'ip': ip})

def filter_by_owner(clients, invalid_owners):
    """'clients' is a dict of dicts, and is modified in-place."""
    moira.connect()
    moira.auth('fsilg-netmon')
    for mac in list(clients): # since we modify the dict within the loop
        try:
            query = moira.query('ghst','*',clients[mac]['ip'],'*','*')
            if query[0]['ace_name'] in invalid_owners:
                del clients[mac]
        except: pass # if we can't look someone up, don't sweat it
    moira.disconnect()

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
    result = wired.get_clients()
    update_with_wifi_data(result)
    filter_by_owner(result, c.get('moira', 'invalid').split())
    return result

def subtract_stats(now, before):
    result = {}
    for mac in now:
        if mac in before:
            result[mac] = now[mac].copy()
            result[mac]['traffic'] = [x-y for x,y in zip(now[mac]['traffic'],
                                                         before[mac]['traffic'])]
    return result
