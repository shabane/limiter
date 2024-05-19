import psutil
import time
import requests

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
        print(snt_rcv)
    return snt_rcv


limit = int(input("Enter a limit: "))
telegram_token = input("Enter Telegram Bot Token: ")
chatid = input("Enter Telegram ChatId: ")
txt = "You Reach your limit"

while True:
    usage = get_network_usage()
    if usage >= limit:
        requests.get(f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chatid}&text={txt}")
    time.sleep(1)

