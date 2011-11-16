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
    """Run a command and automatically page through the output."""
    t.write(cmd + '\n')
    index, match, text = t.expect([re.escape('\n--More-- or (q)uit'),
                                   re.escape('\n(Cisco Controller) >')])
    return text.splitlines()[1:-1] + ([] if index else run_command(t, ''))

def get_clients(t):
    """Returns a list of currently-connected MAC addresses."""
    return [s.split()[0] for s in run_command(t, 'show client summary')[6:-1]]

def get_client_info(t, mac_addr):
    """Returns (ip_address, bytes_received, bytes_sent) for the given MAC address."""
    data = run_command(t, 'show client detail {0}'.format(mac_addr))
    client = data[data.index('Client Statistics:')+1:][:2]
    return (data[9].split()[-1], [int(l.split()[-1]) for l in client])

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
