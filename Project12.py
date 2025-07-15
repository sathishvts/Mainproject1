import re

def extract_ips(file_path):
    try:
        with open(file_path, 'r') as f:
            log_data = f.read()
        ips = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", log_data)
        print(f"\n Found {len(ips)} IP address(es):")
        for ip in set(ips):
            print(f" - {ip}")
    except FileNotFoundError:
        print(" Log file not found.")

# Example usage
extract_ips("server.log")
