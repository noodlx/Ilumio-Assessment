import os

def parse_flow_log(file_path):
    flow_logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split()
                if len(fields) >= 8:
                    destination_port = int(fields[6])
                    protocol = int(fields[7])
                    flow_logs.append((destination_port, protocol))
    except Exception as e:
        print(f"Error reading flow log file: {e}")
    print(f"Parsed flow logs: {flow_logs}")
    return flow_logs

def read_lookup_table(file_path):
    lookup_table = {}
    try:
        with open(file_path, 'r') as file:
            next(file)  
            for line in file:
                fields = line.strip().split(',')
                if len(fields) == 3:
                    dstport = int(fields[0])
                    protocol = fields[1].lower()
                    tag = fields[2]
                    lookup_table[(dstport, protocol)] = tag
    except Exception as e:
        print(f"Error reading lookup table file: {e}")
    print(f"Parsed lookup table: {lookup_table}")
    return lookup_table

def main():        
    flow_logs = parse_flow_log('data/flow_log.txt')
    lookup_table = read_lookup_table('data/lookup_table.csv')
    


if __name__ == "__main__":
    main()