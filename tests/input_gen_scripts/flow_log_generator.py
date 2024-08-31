""" Generate a sample flow log file for testing purposes. """

import random
import time


def generate_flow_log_entry():
    """Generate a random flow log entry"""
    version = 2
    account_id = "123456789012"
    eni_id = f"eni-{''.join(random.choices('abcdef0123456789', k=8))}"
    srcaddr = (
        f"{random.randint(1, 255)}."
        f"{random.randint(0, 255)}."
        f"{random.randint(0, 255)}."
        f"{random.randint(0, 255)}"
    )
    dstaddr = (
        f"{random.randint(1, 255)}."
        f"{random.randint(0, 255)}."
        f"{random.randint(0, 255)}."
        f"{random.randint(0, 255)}"
    )
    dstport = random.choice([443, 23, 25, 110, 993, 143, 1024, 80])
    srcport = random.randint(49152, 65535)

    # Randomly choose the protocol
    protocol = random.choice([6, 17, 1])  # 6: TCP, 17: UDP, 1: ICMP

    packets = random.randint(5, 25)
    bytes_transferred = random.randint(2000, 20000)
    start_time = int(time.time())
    end_time = start_time + random.randint(10, 60)
    action = random.choice(["ACCEPT", "REJECT"])
    log_status = "OK"

    return (
        f"{version} {account_id} {eni_id} {srcaddr} {dstaddr} {dstport} "
        f"{srcport} {protocol} {packets} {bytes_transferred} {start_time}"
        f"{end_time} {action} {log_status}"
    )


def generate_flow_log_file(filename, num_entries):
    """Generate a flow log file with the specified number of entries."""
    with open(filename, 'w') as file:
        for _ in range(num_entries):
            entry = generate_flow_log_entry()
            file.write(entry + '\n')


if __name__ == "__main__":
    FILENAME = "sample_flow_log.txt"
    NUM_ENTRIES = 100000  # Adjust the number of entries as needed
    generate_flow_log_file(FILENAME, NUM_ENTRIES)
    print(f"Generated {NUM_ENTRIES} flow log entries in {FILENAME}")