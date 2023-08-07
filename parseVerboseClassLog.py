import re
import argparse

JAVA_STANDARD_PACKAGES = [
    'java.', 'javax.', 'sun.', 'com.sun.', 'jdk.', 'org.w3c.', 'org.xml.'
]

def is_third_party_library(jar_path):
    return not (jar_path.startswith('jrt:/java.base') or jar_path.startswith('file:/path/to/jre/lib/rt.jar'))

def parse_verbose_class_logs(logs):
    class_pattern = re.compile(r'^\[\d+\.\d+s\]\[info\]\[class,load\s*\]\s+([^\s]+)\s+source:\s+(.*)$')
    classes_loaded = {}
    classes_seen = set()

    for line in logs.splitlines():
        match = class_pattern.match(line)
        if match:
            class_name, jar_path = match.groups()
            for package_prefix in JAVA_STANDARD_PACKAGES:
                if class_name.startswith(package_prefix):
                    break
            else:
                if is_third_party_library(jar_path):
                    if class_name not in classes_seen:
                        classes_loaded[class_name] = [jar_path]
                        classes_seen.add(class_name)
                    else:
                        classes_loaded[class_name].append(jar_path)

    return classes_loaded

def main():
    parser = argparse.ArgumentParser(description='Parse Java verbose:class logs and list loaded classes with their sources.')
    parser.add_argument('log_file', help='Path to the Java verbose:class log file')

    args = parser.parse_args()
    log_file = args.log_file

    try:
        with open(log_file, 'r') as f:
            verbose_class_logs = f.read()
    except FileNotFoundError:
        print("Error: Log file not found.")
        return

    parsed_classes = parse_verbose_class_logs(verbose_class_logs)

    if not parsed_classes:
        print("No relevant 3rd party class loading logs found in the provided log file.")
    else:
        for class_name, jar_paths in parsed_classes.items():
            unique_jar_paths = list(set(jar_paths))
            print(f"{class_name} -> {', '.join(unique_jar_paths)}")

if __name__ == '__main__':
    main()
