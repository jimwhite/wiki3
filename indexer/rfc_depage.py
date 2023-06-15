import re
import sys

# Initialize variables
sw = 1
b_count = 0
b_sw = False
last_indent = 0

for line in sys.stdin:
    stripped_line = line.strip()

    # Count blank lines but don't write them
    if stripped_line == '':
        if sw > 0: 
            sw = 0
        if sw == -1:
            sw = -2  # The line following the footer has a FF char which in Python3 is a line break.
        else:
            b_count += 1
    else: # Handle a non-blank line
        if sw == 0: 
            sw = 1
        if sw < 0: 
            sw -= 1 # If we're between pages, count footer/dashes/header
        if sw <= -4: # If we're at the header, resume printing
            this_indent = len(line) - len(line.lstrip())
            if b_sw or this_indent < last_indent: 
                print('') # Print a blank line, if needed
            sw = 1
            b_count = 0
            b_sw = False

        if re.search(r'\[Page [0-9]+\] *$', stripped_line): # Found the footer:
            sw = -1 # Stop output
            b_sw = b_count > 3 # true = print blank line when resuming output
        elif sw > 0:
            # Print a blank line if the previous line(s) was/were blank
            if b_count: 
                print('')
            b_count = 0
            print(line, end='')
            last_indent = len(line) - len(line.lstrip())

# # Print final line break for consistency with the awk script
# print()
