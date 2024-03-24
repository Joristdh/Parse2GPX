# This script was mostly written by ChatGPT

import re

# Input file path
input_file = 'input.txt'

# Prefix of the link
link_prefix = 'https://share.iski.cc/shares/share_iski/tracks/'

# Length of the ID
id_length = 20

def extract_ids_from_links(file_path, prefix, id_length):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Define the pattern to match the links
        pattern = rf'{re.escape(prefix)}(\w{{{id_length}}})'
        
        # Find all matches of the pattern in the content
        ids = re.findall(pattern, content)
        
        # Return the IDs separated by space
        return ' '.join(ids)

# Extract IDs from the file
ids = extract_ids_from_links(input_file, link_prefix, id_length)

# Output the extracted IDs
print(ids)
