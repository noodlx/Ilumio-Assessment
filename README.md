# Flow Log Processor
Author: Natalie Ivers


## Installation

1. Download and extract this program and all it's items to your chosen directory.
2. Verify that flog_log.txt, lookup_table.csv, and protocol-numbers.csv are present in the /data/ directory
    - Alternatively, you may change the default input file locations
      at the beginning of class definition in src/main.py
3. Open a command line in, or navigate a command line to the directory (ilumio-assessment)
4. Enter 'python src/main.py' in the command line and press enter
5. When the program is complete, the resulting output csv files will be located in the /output/ directory
   and the program will prompt the user to exit the program


## Testing

In the /tests/ directory, there are a few items:
1. /input_gen_scripts/:
    - scripts that can be used to create sample flow_logs.txt and lookup_table.csv files
    - these files resulting from these scripts will be written in the same /tests/input_gen_scripts/ directory
    - the parameters of these files (number of entries/variations of entry fields) can be set by editing the
      constants in flow_log_generator.py and lookup_table_generator.py
2. /test_input/:
    - these are sample input files that can be (and were) used to test the edge cases of the program
      (very full input files/empty input files)
3. /test_output/:
    - these are the resulting output files of the test involving a 10 MB flow_log.txt and a 10,000 entry lookup_table
    - the empty entry test does not result in output files, as the program catches an empty file, alerts the user,
      and exits.
4. testing.md: 
    - this is a list of all tests I performed on the program.

Though it would be satisfying so see "test_<function>()" dopplegangers of all my code, It seemed unnecessary for the
scope of the assessment, the items in the /testing/ file are my claim that I debugged and tested my code thoroughly.


## Assumptions

1. All input is well-formatted to the specifications provided to me
2. Python is installed on the user system
3. Flow logs are in default format and version 2 exclusively
4. Case is irrelevant for all inputs/outputs
5. The output/ directory is writable, and user has permission to write on the file system.
6. The Final line 'Press Enter to exit...' assumes that the user is running this script in a console and can provide
   input.
7. Flow log files are in a plain text format, instead of a more complex format like JSON.


## Limitations and Design Decisions


1. The paths to the protocol numbers file, flow log file, lookup table file, and output directory are hardcoded.
    - This relates to a choice of how the program recieves input, I had three ideas for how I might go about this: 
      Hardcoded filepaths:
        -Pros:
            Simplicity: No need for additional logic to handle inputs, and the paths are directly available within
            the code, reducing the likelihood of input errors. In addition, its easy to set up and particularly
            effective for a one-off project. Likewise, that simplicity leads to fewer dependencies for external
            configuration file or command-line argument parsing, which reduces complexity and potential points of
            failure.
        -Cons:
            Lack of Flexibility: In the event of modification, the code must be changed directly, which is not ideal
            for reusable or production code.
      Pass the inputs as arguments in the command line:
        -Pros:
            Flexibility: Allows the user to specify different file paths without having to move files around or modify
            the code directly, especially useful if this program were to be automated into a larger project or used
            for batch processing
        -Cons: 
            Additional Complexity: Requires adding argument parsing logic and handling invalid cases where the arguments are erroneous. The correct syntax would have to be documented and communicated with the user, unpractical for code that will not be reused.
      Set the filepaths in an external configuration file:
        -Pros: 
            Scalability: the configuration could be used to manage all sorts of options within the entire program, including configurations pertaining to testing. As far as input freedom, this option allows a degree of freedom between a command line argument and a hardcoded implementation.
        -Cons:
            Setup Overhead: I think the documentation and implementation within the main.py of a configuration file
            would be overkill for the scope and simplicity of this program, which is essentially single use. 
    
    Decision: In a controlled assessment environment, hardcoding file paths simplifies the submission process and ensures that the code runs as expected without additional setup. This allows the evaluator to focus on the core logic and functionality rather than configuration.
2. Error Handling
    - The program assumes well-formatted data, If the files are incorrectly formatted, the program might not handle these cases gracefully and could result in uncaught errors or incorrect parsing. The errors handled by the program are some of the simplest user errors to catch and correct, as i determined those were the most important
    for this assessment.

    Decision: While the error handling in the code is basic (e.g., printing errors and exiting), it is my belief that
    this is sufficient for the scope of a take-home assessment. It ensures that the program doesn't proceed with incorrect or missing data, which could lead to misleading results. In a real-world scenario, more sophisticated error handling would be necessary, but for the assessment, the current level of error handling is appropriate and keeps the code simple and readable.
3. Logging
    - The program prints error messages, which were useful during my development of the code. However, from a maintenance standpoint, it would be better to develop that outwards into a logging system to help debug future
    errors. I began programming the logs for this program when I decided that I'd already spent more than the two hours on the program, and I found it unlikely you expected me to develop that far into the scope of this assessment. 

    Decision: Simple print statements suffice to demonstrate that the program is processing data as expected. In a production environment, logging would be critical, but for the assessment, this level of detail is unnecessary.
4. Data Validation
    - The program assumes that all input data is correctly formatted. For production code that would have more time
    spent developing, testing, and coument, this would surely be implemented. 

    Decision: This allows me to focus on the main task of processing the data and generating the required outputs. In a real-world scenario, more robust validation would be necessary, but for the assessment, the current level is sufficient to demonstrate my skill.


## Conclusion

This project was developed with simplicity and functionality in mind, focusing on delivering accurate results within the constraints of the assessment. While there are opportunities for further refinement and expansion, the current implementation effectively demonstrates my programming skills, including file handling, data processing, and basic error management. The provided testing scripts and the clear documentation ensure that the code is both reliable and easy to understand to the best of my ability.

Thank you for your time.