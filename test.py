#!/usr/bin/python3
import sys

from wiki import Wiki

if len(sys.argv) > 2:
    sys.stderr.write("Error: test.py takes exactly one argument.\n")
    exit()

if len(sys.argv) < 2 or sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("Usage: ./test.py [OPTION]\n")
    print("\tTest CLI for the Wikipedia Bot project.\n")

    print('Options:')
    print("\t* 'help': Show this help message and exit.")
    # Other use cases messages

# Actual switch for use cases
elif sys.argv[1] == 'foo':
    pass

# Default error message
else:
    sys.stderr.write("Error: Invalid test type. Type './test.py help' for a list of valid uses.\n")
    exit()