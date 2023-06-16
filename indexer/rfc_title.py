import os
import re
import sys


def parse_header(header_line):
    pattern = re.compile(r'^\x0c?(RFC \d+[a-z]?)(?: -\s+)?\s{2,}(.*)\s{2,}(.*)$')
    match = pattern.match(header_line)

    if match:
        return match.group(1), match.group(2).rstrip(), match.group(3)

    return None

def parse_rfc_files(directory_path):
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a valid directory.")
        return

    problematic_files = []
    pattern_never_issued = re.compile(r'^rfc .* never issued', re.IGNORECASE)

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            try:
                if not extract_header(directory_path, pattern_never_issued, filename):
                    problematic_files.append(filename)
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")
                problematic_files.append(filename)
    
    print("\nProblematic files: ", len(problematic_files))
    for filename in problematic_files:
        print(filename)

def extract_header(directory_path, pattern_never_issued, filename):
    with open(os.path.join(directory_path, filename), 'r') as file:
        header_found = False
        left_margin = 0
        right_margin = 0
        for line in file:
            if line.startswith('\x0c'):  # End of page, break the loop
                break
                        # Find the widest common leading whitespace (left margin)
            left_margin = min(left_margin, len(line) - len(line.lstrip()))
                        # Find the widest common trailing whitespace (right margin)
            right_margin = min(right_margin, len(line) - len(line.rstrip()))
                    
                    # Reset the file pointer
        file.seek(0)
        is_first_line = True
        for line in file:
            # Trim margins only if they contain only whitespace
            line = line[left_margin:] if line[:left_margin].isspace() else line
            line = line[:-right_margin] if right_margin > 0 and line[-right_margin:].isspace() else line


            # If the line matches "RFC .... never issued ..."
            if is_first_line:
                is_first_line = False
                if pattern_never_issued.match(line):
                    print(f"{filename} contains a never issued RFC: {line.strip()}")
                    header_found = True
                    break
                        
            header = parse_header(line)
            if header:
                # If the title is missing, use the next line as the title
                if not header[1]:
                    header = (header[0], next(file, '').strip(), header[2])
                print(f"File: {filename}, Header: {header}")
                header_found = True
                break

        return header_found
            

def main():
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    parse_rfc_files(directory_path)

if __name__ == "__main__":
    main()
