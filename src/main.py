"""
This is a class for parsing flow log files,
reading lookup tables, and generating tag and tuple counts

Author: Natalie Ivers
"""

# Requirement: Only include native python libraries
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
        map_tags(parsed_log, lookup_table): Maps tags to each flow log entry.
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
    flow_log_path = Path("data/big_test_flow_log.txt")
    lookup_table_path = Path("data/big_test_lookup_table.csv")
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
                if not reader.fieldnames:
                    raise ValueError(
                        "Protocol numbers file is empty or missing headers."
                    )
                for row in reader:
                    protocol_number = int(row['Decimal'])
                    protocol_keyword = row['Keyword'].lower()
                    protocol_dict[protocol_number] = protocol_keyword
        except FileNotFoundError as e:
            print(f"Error reading protocol numbers file: {e}")
            exit(1)
        except IOError as e:
            print(f"Error reading protocol numbers file: {e}")
            exit(1)
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
        parsed_log = []
        try:
            with open(self.flow_log_path, 'r', encoding='utf-8') as file:
                for line in file:
                    fields = line.strip().split()
                    protocol_number = int(fields[7])
                    protocol_keyword = protocol_dict.get(
                        protocol_number, 'unknown'
                    )
                    # Replace protocol number
                    # with string and append
                    fields[7] = protocol_keyword.lower()
                    parsed_log.append(fields)
        except FileNotFoundError as e:
            print(f"Error reading flow log file: {e}")
            exit(1)
        except IOError as e:
            print(f"Error reading flow log file: {e}")
            exit(1)
        return parsed_log

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
                reader = csv.DictReader(file)
                if not reader.fieldnames:
                    raise ValueError(
                        "Lookup table file is empty or missing headers."
                    )
                for row in reader:
                    dstport = int(row['dstport'])
                    protocol = row['protocol'].lower()
                    tag = row['tag'].lower()
                    lookup_table[(dstport, protocol)] = tag
        except FileNotFoundError as e:
            print(f"Error reading lookup table file: {e}")
            exit(1)
        except IOError as e:
            print(f"Error reading lookup table file: {e}")
            exit(1)
        return lookup_table

    def map_tags(self, parsed_log, lookup_table):
        """
        Maps tags to each flow log entry.

        Args:
            parsed_log (list): list of flow log entries
            lookup_table (dict): dictionary of (destination port, protocol)
                to tag

        Returns:
            list: list of flow log entries with tags
        """
        tagged_log = []
        for entry in parsed_log:
            dest_port = int(entry[6])
            protocol = entry[7]
            tag = lookup_table.get((dest_port, protocol), 'untagged')
            entry.append(tag)
            tagged_log.append(entry)
        return tagged_log

    def count_tags(self, tagged_log):
        """
        Counts the number of times each tag appears in the flow log.

        Args:
            tagged_log (list): list of flow log entries with tags

        Returns:
            dict: dictionary of tag to count
        """
        tag_counts = {}
        for entry in tagged_log:
            tag = entry[-1]  # The tag is the last element in the entry
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts

    def count_dest_protocol(self, tagged_log):
        """
        Counts the number of times each (destination port, protocol) tuple
        appears in the flow log.

        Args:
            tagged_log (list): list of flow log entries with tags

        Returns:
            dict: dictionary of (destination port, protocol) tuple to count
        """
        tuple_counts = {}
        for entry in tagged_log:
            dest_port = int(entry[6])
            protocol = entry[7].lower()
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
        parsed_log = self.parse_flow_log(protocol_dict)
        lookup_table = self.read_lookup_table()

        # Process Data
        tagged_log = self.map_tags(parsed_log, lookup_table)
        tag_counts = self.count_tags(tagged_log)
        dest_protocol_counts = self.count_dest_protocol(tagged_log)

        # Output Results
        self.output_results(tag_counts, dest_protocol_counts)


if __name__ == "__main__":
    flp = FlowLogProcessor()
    flp.run()
