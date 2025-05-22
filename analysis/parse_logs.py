import json
import csv
from collections import defaultdict
from datetime import datetime

def parse_log(file_path):
    failed_logins = []
    commands = []
    ip_stats = defaultdict(int)

    with open(file_path, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                event_id = event.get("eventid", "")
                src_ip = event.get("src_ip", "")
                timestamp = event.get("timestamp", "")
                ip_stats[src_ip] += 1

                if event_id == "cowrie.login.failed":
                    failed_logins.append({
                        "timestamp": timestamp,
                        "ip": src_ip,
                        "username": event.get("username", ""),
                        "password": event.get("password", "")
                    })

                elif event_id == "cowrie.session.input":
                    commands.append({
                        "timestamp": timestamp,
                        "ip": src_ip,
                        "command": event.get("input", "")
                    })

            except Exception as e:
                continue

    return failed_logins, commands, ip_stats

def save_to_csv(data, filename, fieldnames):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    file_path = input("Enter path to Cowrie log file (e.g., cowrie.json): ")

    failed_logins, commands, ip_stats = parse_log(file_path)

    print("\n🔐 Failed Login Attempts:")
    for login in failed_logins:
        print(f"[{login['timestamp']}] {login['ip']} tried {login['username']}:{login['password']}")

    print("\n📜 Commands Entered by Attackers:")
    for cmd in commands:
        print(f"[{cmd['timestamp']}] {cmd['ip']} ran: {cmd['command']}")

    print("\n📊 IP Activity Summary:")
    for ip, count in ip_stats.items():
        print(f"{ip}: {count} events")

    # Save reports
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_csv(failed_logins, f"failed_logins_{now}.csv", ["timestamp", "ip", "username", "password"])
    save_to_csv(commands, f"commands_{now}.csv", ["timestamp", "ip", "command"])

    print(f"\n✅ CSV reports saved as failed_logins_{now}.csv and commands_{now}.csv")

if __name__ == "__main__":
    main()