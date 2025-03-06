

def unique_ips(ip_list):
    return list(set(ip_list))


if __name__ == "__main__":
    ip_list = [
        "192.168.1.1", "192.168.1.2", "192.168.1.1",
        "192.168.1.3", "192.168.1.2", "192.168.1.4"
    ]
    unique_ip_list = unique_ips(ip_list)
    print("Unique IP addresses:", unique_ip_list)