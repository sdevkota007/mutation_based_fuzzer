# Mutation Based Fuzzer

 - jpg2bmp is a program which converts images files from '.jpg' format to '.bmp' format. This target program consists of 8 hidden bugs which is to be found out using mutation based fuzzing.
 - mutate.py is a mutation based fuzzer which takes a valid input (eg: cross.jpg) for the target program 'jpg2bmp', mutates the input in different ways, and tests the mutated input by feeding it to the target program to find out the hidden bugs. 
 - To run the program simply run
 
 ``$ python mutate.py``
 
 - All of the test files which trigger a bug are archived in the 'archive' directory at the end of the program.
 - mutate.py also produces a report 'report.json' at the end of the program which can be found inside the 'archive' directory at the end of the program. It gives a count for each of the following 
 
        "num_of_test_files": 
        "num_of_bugs_trigerred": 
        "bug1_count": 
        "bug2_count":
        "bug3_count":
        "bug4_count":
        "bug5_count": 
        "bug6_count":
        "bug7_count": 
        "bug8_count": 