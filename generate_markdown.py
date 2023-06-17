import os

# specify the directory you want to scan for csv files
directory = '_data/glossary'

# specify the directory you want to place the generated markdown files
output_directory = 'files'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # create a markdown file for this csv
        with open(os.path.join(output_directory, filename.replace('.csv', '.md')), 'w') as f:
            f.write('---\n')
            f.write('layout: raw-csv\n')
            f.write('file: ' + filename.replace('.csv', '') + '\n')
            f.write('---\n')
