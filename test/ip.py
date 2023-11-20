import ipaddress

try:
    hostname = ipaddress.ip_interface('192.168.82.1/22')
    hostname = str(hostname.ip)
except ValueError as e:
    # print(f'address is invalid: %s' % e)
    hostname = None

print(hostname)
