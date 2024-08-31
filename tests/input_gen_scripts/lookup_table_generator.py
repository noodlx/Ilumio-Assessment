""" Generate a lookup table with random mappings. """

import csv
import random
import string


def generate_random_tag(length=4):
    """Generate a random tag of specified length."""
    return ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=length))


def generate_lookup_table(filename, num_entries):
    """Generate a lookup table with the specified number of entries."""
    protocols = ['tcp', 'udp', 'icmp']
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['dstport', 'protocol', 'tag'])
        for _ in range(num_entries):
            dstport = random.randint(1, 65535)
            protocol = random.choice(protocols)
            tag = generate_random_tag()
            writer.writerow([dstport, protocol, tag])


if __name__ == "__main__":
    FILENAME = "sample_lookup_table.csv"
    NUM_ENTRIES = 10000  # Number of mappings
    generate_lookup_table(FILENAME, NUM_ENTRIES)
    print(f"Generated {NUM_ENTRIES} mappings in {FILENAME}\n")
