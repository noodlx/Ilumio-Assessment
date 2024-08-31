"""
This is a class for parsing flow log files,
reading lookup tables, and generating tag and tuple counts

Author: Natalie Ivers
"""

# Requirement: Only include native python libraries
import os
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
            counts to CSV files. The output is sorted by count, descending.
        process(): Main method to parse inputted flow log and lookup table,
            process the data, and output the results.
    """
    # File Paths for input and output
    protocol_dict_path = "data/protocol-numbers.csv"
    flow_log_path = "data/flow_log.txt"
    lookup_table_path = "data/lookup_table.csv"
    output_path = "output/"

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
                # Strip whitespace from fieldnames
                reader.fieldnames = [
                    field.strip() for field in reader.fieldnames
                ]
                required_fields = {'dstport', 'protocol', 'tag'}
                if not reader.fieldnames or not required_fields.issubset(
                    reader.fieldnames
                ):
                    raise ValueError(
                        "Lookup table file is empty or "
                        "missing required headers."
                    )
                for row in reader:
                    dstport = int(row['dstport'].strip())
                    protocol = row['protocol'].strip().lower()
                    tag = row['tag'].strip().lower()
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
        The output is sorted by count, descending.

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
            for tag, count in sorted(
                tag_counts.items(), key=lambda item: item[1], reverse=True
            ):
                file.write(f'{tag},{count}\n')

        # Output tuple count to CSV
        with open(
            os.path.join(self.output_path, 'port_protocol_counts.csv'),
            'w',
            encoding='utf-8'
        ) as file:
            file.write('Port,Protocol,Count\n')
            for (dest_port, protocol), count in sorted(
                tuple_counts.items(), key=lambda item: item[1], reverse=True
            ):
                file.write(f'{dest_port},{protocol},{count}\n')

    def run(self):
        """
        Method to parse inputted flow log and lookup table,
        process the data, and output the results.
        """
        print("Starting FlowLogProcessor...")

        # Parse Input Data
        print("Reading protocol numbers...")
        protocol_dict = self.read_protocol_numbers()
        print("Protocol numbers read successfully.")

        print("Parsing flow log...")
        parsed_log = self.parse_flow_log(protocol_dict)
        print("Flow log parsed successfully.")

        print("Reading lookup table...")
        lookup_table = self.read_lookup_table()
        print("Lookup table read successfully.")

        # Process Data
        print("Mapping tags to flow log entries...")
        tagged_log = self.map_tags(parsed_log, lookup_table)
        print("Tags mapped successfully.")

        print("Counting tags...")
        tag_counts = self.count_tags(tagged_log)
        print("Tags counted successfully.")

        print("Counting destination port and protocol tuples...")
        dest_protocol_counts = self.count_dest_protocol(tagged_log)
        print("Destination port and protocol tuples counted successfully.")

        # Output Results
        print("Outputting results...")
        self.output_results(tag_counts, dest_protocol_counts)
        print("Results outputted successfully.")

        print("FlowLogProcessor completed successfully.")


if __name__ == "__main__":
    flp = FlowLogProcessor()
    flp.run()
    input("Press Enter to exit...")
