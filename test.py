#!/usr/bin/python3
import wiki

import sys

if len(sys.argv) > 2:
    sys.stderr.write("Error: test.py takes exactly one argument.\n")
    exit()

if len(sys.argv) < 2 or sys.argv[1] == 'help' or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("Usage: ./test.py [OPTION]\n")
    print("\tTest CLI for the Wikipedia Bot project.\n")

    print('Options:')
    print("\t* 'help': Show this help message and exit.")
    # Other use cases messages
    print("\t* 'check_link': Test for checking if given string is a valid Wikipedia URL.")
    print("\t* 'api_link': Test for checking generation of Wikipedia API strings given a valid Wikipedia URL.")
    print("\t* 'api_query': Test for retrieving information of Wikipedia page based on valid Wikipedia URL.")
    print("\t* 'format': Test for formatting query response of Wikipedia page based on Wikipedia URL.")


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

# Test query format
elif sys.argv[1] == 'format':
    link = input("Type any Wikipedia link: ")
    domain = link.split('/wiki/')[0]

    type = input("Type output format type: ")

    output = input("Type an output file name: ")

    if output != '' and output != None:
        file = open(output, "w")
        file.write(wiki.format_response(wiki.api_query(link), type=type, domain=domain))
        file.close()
    else:
        print(wiki.format_response(wiki.api_query(link), type=type, domain=domain))

# Default error message
else:
    sys.stderr.write("Error: Invalid test type. Type './test.py help' for a list of valid uses.\n")
    exit()