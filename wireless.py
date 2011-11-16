"""
Module for scripting the telnet interface of a Cisco 4402 wireless controller.
't' refers to a telnetlib.Telnet object throughout.
"""
import telnetlib, re

def connect(hostname, user, pw):
    """Open up a telnet session to the wireless controller."""
    t = telnetlib.Telnet()
    t.open(hostname)
    t.read_until('User:')
    t.write(user + '\n')
    t.read_until('Password:')
    t.write(pw + '\n')
    t.read_until('>')
    return t

def run_command(t, cmd):
    t.write(cmd + '\n')
    index, match, text = t.expect([re.escape('\n--More-- or (q)uit'),
                                   re.escape('\n(Cisco Controller) >')])
    return text.splitlines()[1:-1] + ([] if index else run_command(t, ''))

def get_clients(t):
    """Returns a list of currently-connected MAC addresses."""
    return [s.split()[0] for s in run_command(t, 'show client summary')[6:-1]]

def get_client_info(t, mac_addr):
    """Returns (ip_address, bytes_received, bytes_sent) for the given MAC address."""
    res = run_command(t, 'show client detail {0}'.format(mac_addr))
    index = res.index('Client Statistics:')
    return res[9].split()[-1], res[index+1].split()[-1], res[index+2].split()[-1]

def get_all_info(hostname, user, pw):
    """Returns [(mac_addr, ip_addr, bytes_rcvd, bytes_sent), ...] for all clients."""
    t, result = connect(hostname, user, pw), []
    for mac_addr in get_clients(t):
        try:
            info = get_client_info(t, mac_addr)
            assert info[0] != 'Unknown'
            result.append((mac_addr,) + info)
        except: pass
    t.close()
    return result
