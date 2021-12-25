#!/usr/bin/python3
import wiki

import sys
import requests

if len(sys.argv) > 2:
    sys.stderr.write("Error: test.py takes exactly one argument.\n")
    exit()

if len(sys.argv) < 2 or sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("Usage: ./test.py [OPTION]\n")
    print("\tTest CLI for the Wikipedia Bot project.\n")

    print('Options:')
    print("\t* 'help': Show this help message and exit.")
    # Other use cases messages

# ---------------------------
# Actual switch for use cases
# ---------------------------

# Test if string is a Wiki article 
elif sys.argv[1] == 'check_link':
    link = input("Type any Wikipedia link: ")
    in_between = '*'
    if not wiki.is_wiki_article(link):
        in_between = ' not*'
    print(f"The link *is{in_between} a Wiki article")

# Test API link generation
elif sys.argv[1] == 'api_link':
    link = input("Type any Wikipedia link: ")
    print(f"API request link: {wiki.api_link(link)}")

# Test API query
elif sys.argv[1] == 'api_query':
    link = input("Type any Wikipedia link: ")
    response = wiki.api_query(link)
    if response.status_code == 200:
        print(response.json())

# Test query sanitization
elif sys.argv[1] == 'sanitize':
    # link = input("Type any Wikipedia link: ")
    # response = wiki.api_query(link)
    # if response.status_code == 200:
    print(wiki.sanitize_response(wiki.api_query('https://en.wikipedia.org/wiki/En_passant'), format=None))

# Default error message
else:
    sys.stderr.write("Error: Invalid test type. Type './test.py help' for a list of valid uses.\n")
    exit()