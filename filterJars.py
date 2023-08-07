import sys
import re
import argparse

def filter_matching_jars(output_file, matching_string):
    matching_jars = set()
    jar_pattern = re.compile(r'^[\w.]+\s+->\s+(.+)$')

    with open(output_file, 'r') as f:
        for line in f:
            match = jar_pattern.match(line.strip())
            if match:
                jar_paths = match.group(1).split(', ')
                for jar in jar_paths:
                    if matching_string.lower() in jar.lower():
                        matching_jars.add(jar)

    return matching_jars

def main():
    parser = argparse.ArgumentParser(description='Filter JAR paths by a matching string.')
    parser.add_argument('output_file', help='Path to the output file from the previous script')
    parser.add_argument('matching_string', help='The string to match in the JAR paths')

    args = parser.parse_args()
    output_file = args.output_file
    matching_string = args.matching_string

    matching_jars = filter_matching_jars(output_file, matching_string)

    if not matching_jars:
        print(f"No JARs matching '{matching_string}' found in the output.")
    else:
        for jar in matching_jars:
            print(jar)

if __name__ == '__main__':
    main()
