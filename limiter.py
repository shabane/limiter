#!/usr/bin/env python3
import psutil
import time
import requests
import argparse


parser = argparse.ArgumentParser(description='Get notify when your server rich a network data transfer limit.')
parser.add_argument('--limit', type=int, help='Threshold Number Of Limit[MB]')
parser.add_argument('--chatid', type=str, help='Telegram User ChatId Or Channel @Username/ID')
parser.add_argument('--message', type=str, help='The Message As Notify[Optional]', default='You Reach Your Limit')
parser.add_argument('--token', type=str, help='Telegram Bot Token')
parser.add_argument('--repeat-msg', type=int, help='Repeat Message Time[Miniut]', default=1)
parser.add_argument('--send-startup-message', type=bool, action='store_true', help='Send A Message That Indicate The Script Is Running', default=False)
args = parser.parse_args()


def get_network_usage():
    snt_rcv = 0
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface_name, interface_addresses in addrs.items():
        if interface_name in stats:
            print(f"Interface: {interface_name}")
            st = stats[interface_name]
            print(f"  Status: {'active' if st.isup else 'down'}")
            print(f"  Speed: {st.speed}Mbps")
            
            # Get IO statistics since boot
            io_counters = psutil.net_io_counters(pernic=True)
            io = io_counters[interface_name]
            print(f"  Bytes Sent: {io.bytes_sent / (1024 * 1024):.2f} MB")
            print(f"  Bytes Received: {io.bytes_recv / (1024 * 1024):.2f} MB")
            print(f"Total: {(io.bytes_sent / (1024 * 1024))+(io.bytes_recv / (1024 * 1024))}")
            snt_rcv += (io.bytes_sent / (1024 * 1024))+(io.bytes_recv / (1024 * 1024))
        print(f'Sum On All Interfaces: {snt_rcv}')
    return snt_rcv


if args.send_startup_message:
    requests.get(f"https://api.telegram.org/bot{args.token}/sendMessage?chat_id={args.chatid}&text=Limiter Started...")

while True:
    usage = get_network_usage()
    if usage >= args.limit:
        requests.get(f"https://api.telegram.org/bot{args.token}/sendMessage?chat_id={args.chatid}&text={args.message}")
        time.sleep(args.repeat_msg)
    time.sleep(1)
