
def parse_flow_log(file_path):
    flow_logs = []
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split()
            if len(fields) >= 8:
                destination_port = int(fields[6])
                protocol = int(fields[7])
                flow_logs.append((destination_port, protocol))
    return flow_logs

def read_lookup_table(file_path):
    lookup_table = {}
    with open(file_path, 'r') as file:
        next(file)  
        for line in file:
            fields = line.strip().split(',')
            if len(fields) == 3:
                dstport = int(fields[0])
                protocol = fields[1].lower()
                tag = fields[2]
                lookup_table[(dstport, protocol)] = tag
    return lookup_table

def main():        
    flow_logs = parse_flow_log('../data/flow_log.txt')
    lookup_table = read_lookup_table('../data/lookup_table.csv')
    output_file = '../output/output.txt'

    # Write flow_logs to file
    with open(output_file, 'w') as file:
        file.write('Flow Logs:\n')
        for log in flow_logs:
            file.write(f'Destination Port: {log[0]}, Protocol: {log[1]}\n')

    # Write lookup_table to file
    with open(output_file, 'a') as file:
        file.write('\nLookup Table:\n')
        for key, value in lookup_table.items():
            file.write(f'Destination Port: {key[0]}, Protocol: {key[1]}, Tag: {value}\n')