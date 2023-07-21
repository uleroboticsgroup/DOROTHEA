#!/usr/bin/env python3

import nmap3
import socket
import json
import netifaces

def calculate_network_address(ip_address, net_mask):
    ip_parts = ip_address.split('.')
    net_mask_parts = net_mask.split('.')
    
    # Convert IP address and net mask parts to integers
    ip_int = [int(part) for part in ip_parts]
    net_mask_int = [int(part) for part in net_mask_parts]
    
    # Calculate network address using bitwise AND
    network_address = [str(ip_int[i] & net_mask_int[i]) for i in range(4)]
    
    return '.'.join(network_address)

def get_ip_of_interface(interface_name):
    try:
        addresses = netifaces.ifaddresses(interface_name)
        ipv4_addresses = addresses[netifaces.AF_INET]
        if ipv4_addresses:
            return ipv4_addresses[0]
    except (ValueError, KeyError):
        pass
    return None

if __name__ == '__main__':
    interface_name = 'eth0'  # Replace with the name of the desired interface

    # Host details
    host_ip = get_ip_of_interface(interface_name)['addr']
    host_netmask = get_ip_of_interface(interface_name)['netmask']

    network_address = calculate_network_address(host_ip, host_netmask) + '/24'

    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(network_address)

    for block in ['runtime', 'stats', 'task_results']:
        result_blok = json.dumps(results[block], indent=4)
        print(f'"{block}": ', end='')
        print(result_blok)
    



    if network_address:
        print(f"Network Address of {interface_name}: {network_address}")
    else:
        print(f"No IP address found for {interface_name}")
