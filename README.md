# Flow Log Processor
Author: Natalie Ivers


## Installation and Usage

1. Download and extract all files or clone the repository to your desired directory.
2. Verify that flow_log.txt, lookup_table.csv, and protocol-numbers.csv are present in the /data/ directory
    - Note: You can modify the default input file locations in the src/main.py file, at the beginning of the class definition.
3. Open a command line terminal and navigate to the program directory (Ilumio-Assessment-main).
4. Enter 'python src/main.py' in the command line and press enter
5. When the program is complete, the resulting output csv files will be located in the /output/ directory
   and the program will prompt the user to exit the program

To use your own flow log file and lookup table, rename your files to flow_log.txt and lookup_table.csv respectively
and replace the default files in /data/

!! Do not remove or replace protocol-numbers.csv !!


## Testing

In the /tests/ directory, there are a few items:
1. /input_gen_scripts/:
    - These scripts that can be used to create sample flow_logs.txt and lookup_table.csv files
    - The files resulting from these scripts will be written in the same /tests/input_gen_scripts/ directory
    - The parameters of these files (number of entries/variations of entry fields) can be set by editing the
      constants in flow_log_generator.py and lookup_table_generator.py
2. /test_input/:
    - These are sample input files that can be (and were) used to test the edge cases of the program
      (very full input files/empty input files)
3. /test_output/:
    - These are the resulting output files of the test involving a 10 MB flow_log.txt and a 10,000 entry lookup_table
    - The empty entry test does not result in output files, as the program catches an empty file, alerts the user,
      and exits.
4. testing.md: 
    - This is a list of all tests I performed on the program.

While it would have been ideal to create test_xyz() counterparts for all my code, it seemed beyond the necessary scope of this assessment. Instead, I focused on manual testing, as outlined in the /testing/ directory, to demonstrate that I've thoroughly debugged and tested my code.


## Assumptions

1. All input is well-formatted to the specifications provided in the assessment description
2. Python is installed on the user system
3. Flow logs are in default format and version 2 exclusively
4. Case is irrelevant for all inputs/outputs
5. The /output/ directory is writable, and user has permission to write on the file system.
6. The Final line 'Press Enter to exit...' assumes that the user is running this script in a console and can provide
   input.
7. Flow log files are in a plain text format, instead of a more complex format like JSON.
8. The user knows how to download/clone the repository from github


## Limitations and Design Decisions


1. The paths to the protocol numbers file, flow log file, lookup table file, and output directory are hardcoded.
    
    - I had three ideas for how I might handle input in regards to this program: 
      
      1. Hardcoded filepaths

        - Pros:        
            Simplicity - No need for additional logic to handle inputs, and the paths are directly available
            within the code, reducing the likelihood of input errors. In addition, its easy to set up and particularly effective for a one-off project. Likewise, that simplicity leads to fewer dependencies for external configuration file or command-line argument parsing, which reduces complexity and potential points of failure.
        - Cons:
            Lack of Flexibility - In the event of modification, the code must be changed directly, which is not ideal for reusable or production code.
      
      2. Pass the inputs as arguments in the command line

        - Pros:
            Flexibility - Allows the user to specify different file paths without having to move files around or modify the code directly, especially useful if this program were to be automated into a larger project or used for batch processing
        - Cons: 
            Additional Complexity - Requires adding argument parsing logic and handling invalid cases where the arguments are erroneous. The correct syntax would have to be documented and communicated with the user, unpractical for code that will not be reused.
      
      3. Set the filepaths in an external configuration file

        - Pros: 
            Scalability - the configuration could be used to manage all sorts of options within the entire program, including configurations pertaining to testing. As far as input freedom, this option allows a degree of freedom between a command line argument and a hardcoded implementation.
        - Cons:
            Setup Overhead - I think the documentation and implementation within the main.py of a configuration file
            would be overkill for the scope and simplicity of this program, which is essentially single use. 

    Decision: In a controlled assessment environment, hardcoding file paths simplifies the submission process and ensures that the code runs as expected without additional setup. This allows the evaluator to focus on the core logic and functionality rather than configuration.
2. Error Handling
    
    - The program assumes well-formatted data, If the files are incorrectly formatted, the program might not handle these cases gracefully and could result in uncaught errors or incorrect parsing. The errors handled by the program are some of the simplest user errors to catch and correct, and I determined those were the most important for this assessment.

    Decision: While the error handling in the code is basic (e.g., printing errors and exiting), it is my belief that this is sufficient for the scope of a take-home assessment. It ensures that the program doesn't proceed with incorrect or missing data, which could lead to misleading results. In a real-world scenario, more sophisticated error handling would be necessary, but for the assessment, the current level of error handling is appropriate and keeps the code simple and readable.
3. Logging
    - The program prints error messages, which were useful during my development of the code. However, from a maintenance standpoint, it would be better to develop that outwards into a logging system to help debug future
    errors. I began programming the logs for this program when I decided that I'd already spent more than the two hours on the program, and I found it unlikely you expected me to develop that far into the scope of this assessment. 

    Decision: Simple print statements suffice to demonstrate that the program is processing data as expected. In a production environment, logging would be critical, but for the assessment, this level of detail is unnecessary.
4. Data Validation
    - The program assumes that all input data is correctly formatted. For production code that would have more time
    spent developing, testing, and embedded within a larger system, this would surely be implemented. 

    Decision: This allows me to focus on the main task of processing the data and generating the required outputs. In a real-world scenario, more robust validation would be necessary, but for the assessment, the current level is sufficient to demonstrate my skill.


## Conclusion

This project was developed with simplicity and functionality in mind, focusing on delivering accurate results within the constraints of the assessment. While there are opportunities for further refinement and expansion, the current implementation effectively demonstrates my programming skills, including file handling, data processing, and basic error management. The provided testing details and the clear documentation ensure that the code is both reliable and easy to understand to the best of my ability.

Thank you for your time.