P = pass

Unit Tests:
--read_protocol_numers
P - Valid protocol numbers entry
P - Correctly terminates and reports empty/missing entry
P - Correctly terminates and reports invalid entry file format
P - Correctly runs with nonessential fields empty

--parse_flow_log
P - Valid flow log entry 
P - Logs containing variety of protocols
P - Correctly terminates and reports empty flow log
P - Case sensitivity test

--read_lookup_table
P - Valid lookup table entry
P - Correctly terminates and reports empty/missing lookup table
P - Multiple tuples mapping to single tag
P - Case sensitivity test

--map_tags
P - Multiple tuples mapping to single tag
P - Correctly terminates and reports empty inputs before reaching this point

--count_tags
P - Correctly accumulates tags with valid data
P - Correctly terminates and reports empty data before reaching this point

--count_dest_protocol
P - Correctly accumulates tags with valid data
P - Correctly terminates and reports empty data before reaching this point

Integration Tests:
P - End to end functional
P - Results match expected outcome

Edge Cases:
P  - Flow log is large (10mb)
P  - Lookup table is large (10000 mappings)
P  - No matching tags