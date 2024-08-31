"""
This is a class for parsing flow log files,
reading lookup tables, and generating tag and tuple counts
based on the data.

Author: Natalie Ivers
"""

import os
from pathlib import Path
import csv


class FlowLogProcessor:
    """
    A class that processes flow log data.
    Attributes:
        protocol_dict_path (str): Path to the protocol numbers file.
        flow_log_path (str): Path to the flow log file.
        lookup_table_path (str): Path to the lookup table file.
        output_path (str): Path to the output directory

    Methods:
        read_protocol_numbers(): Reads a protocol numbers file and returns
            a dictionary of protocol number to keyword.
        parse_flow_log(protocol_dict): Parses a flow log file and returns a
            list of tuples containing destination port and protocol keyword.
        read_lookup_table(): Reads a lookup table file and returns a dictionary
            of (destination port, protocol) to tag.
        count_tags(dest_protocol_tuples, lookup_table): Counts the number of
            times each tag appears in the flow log.
        count_port_protocol(dest_protocol_tuples): Counts the number of times
            each (destination port, protocol) tuple appears in the flow log.
        output_results(tag_counts, tuple_counts): Outputs the tag and tuple
            counts to CSV files.
        process(): Main method to parse inputted flow log and lookup table,
            process the data, and output the results.
    """

    # Filepaths for input and output files
    protocol_dict_path = Path("data/protocol-numbers.csv")
    flow_log_path = Path("data/flow_log.txt")
    lookup_table_path = Path("data/lookup_table.csv")
    output_path = Path("output/")

    def read_protocol_numbers(self):
        """
        Reads a protocol numbers file and returns a dictionary of
        protocol number to keyword.

        From:
            https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

        Returns:
            dict: dictionary of protocol number to keyword
        """
        protocol_dict = {}
        try:
            with open(self.protocol_dict_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    protocol_number = int(row['Decimal'])
                    protocol_keyword = row['Keyword'].lower()
                    protocol_dict[protocol_number] = protocol_keyword
        except FileNotFoundError as e:
            print(f"Error reading protocol numbers file: {e}")
        except IOError as e:
            print(f"Error reading protocol numbers file: {e}")
        return protocol_dict

    def parse_flow_log(self, protocol_dict):
        """
        Parses a flow log file and returns a list of tuples
        containing destination port and protocol keyword.

        Args:
            protocol_dict (dict): dictionary of protocol number to keyword

        Returns:
            list: list of tuples containing destination port and protocol
                keyword
        """
        dest_protocol_tuples = []
        try:
            with open(self.flow_log_path, 'r', encoding='utf-8') as file:
                for line in file:
                    fields = line.strip().split()
                    if len(fields) >= 8:
                        destination_port = int(fields[6])
                        protocol_number = int(fields[7])
                        protocol_keyword = protocol_dict.get(
                            protocol_number, 'unknown'
                        )
                        dest_protocol_tuples.append(
                            (destination_port, protocol_keyword)
                        )
        except FileNotFoundError as e:
            print(f"Error reading flow log file: {e}")
        except IOError as e:
            print(f"Error reading flow log file: {e}")
        return dest_protocol_tuples

    def read_lookup_table(self):
        """
        Reads a lookup table file and returns a dictionary of
        (destination port, protocol) to tag.

        Returns:
            dict: dictionary of (destination port, protocol) to tag
        """
        lookup_table = {}
        try:
            with open(self.lookup_table_path, 'r', encoding='utf-8') as file:
                next(file)  # skip header
                for line in file:
                    fields = line.strip().split(',')
                    if len(fields) == 3:
                        dstport = int(fields[0])
                        protocol = fields[1].lower()
                        tag = fields[2]
                        lookup_table[(dstport, protocol)] = tag
        except FileNotFoundError as e:
            print(f"Error reading lookup table file: {e}")
        except IOError as e:
            print(f"Error reading lookup table file: {e}")
        return lookup_table

    def count_tags(self, dest_protocol_tuples, lookup_table):
        """
        Counts the number of times each tag appears in the flow log.

        Args:
            dest_protocol_tuples (list): list of tuples containing
                destination port and protocol
            lookup_table (dict): dictionary of (destination port, protocol)
                to tag

        Returns:
            dict: dictionary of tag to count
        """
        tag_counts = {}
        for dest_port, protocol in dest_protocol_tuples:
            if (dest_port, protocol) in lookup_table:
                tag = lookup_table[(dest_port, protocol)]
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts

    def count_port_protocol(self, dest_protocol_tuples):
        """
        Counts the number of times each (destination port, protocol) tuple
        appears in the flow log.

        Args:
            dest_protocol_tuples (list): list of tuples containing
                destination port and protocol

        Returns:
            dict: dictionary of (destination port, protocol) tuple to count
        """
        tuple_counts = {}
        for dest_port, protocol in dest_protocol_tuples:
            tuple_counts[(dest_port, protocol)] = tuple_counts.get(
                (dest_port, protocol), 0
            ) + 1
        return tuple_counts

    def output_results(self, tag_counts, tuple_counts):
        """
        Outputs the tag and tuple counts to CSV files.

        Args:
            tag_counts (dict): dictionary of tag to count
            tuple_counts (dict): dictionary of (destination port, protocol) to
                count

        Returns:
            None
        """
        # Output tag count to CSV
        os.makedirs(self.output_path, exist_ok=True)
        with open(
            os.path.join(self.output_path, 'tag_count.csv'),
            'w',
            encoding='utf-8'
        ) as file:
            file.write('Tag,Count\n')
            for tag, count in tag_counts.items():
                file.write(f'{tag},{count}\n')

        # Output tuple count to CSV
        with open(
            os.path.join(self.output_path, 'port_protocol_counts.csv'),
            'w',
            encoding='utf-8'
        ) as file:
            file.write('Port,Protocol,Count\n')
            for (dest_port, protocol), count in tuple_counts.items():
                file.write(f'{dest_port},{protocol},{count}\n')

    def run(self):
        """
        method to parse inputted flow log and lookup table,
        process the data, and output the results.
        """
        # Parse Input Data
        protocol_dict = self.read_protocol_numbers()
        dest_protocol_tuples = self.parse_flow_log(protocol_dict)
        lookup_table = self.read_lookup_table()

        # Process Data
        tag_counts = self.count_tags(dest_protocol_tuples, lookup_table)
        dest_protocol_counts = self.count_port_protocol(dest_protocol_tuples)

        # Output Results
        self.output_results(tag_counts, dest_protocol_counts)


if __name__ == "__main__":
    flp = FlowLogProcessor()
    flp.run()
