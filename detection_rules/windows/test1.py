import os
import re

def process_sql_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regex to capture fields inside INSERT INTO (...)
    insert_pattern = re.compile(r'(INSERT INTO \{\{[^}]+\}\}.\{\{[^}]+\}\} \([^\)]*)(fieldD)([^\)]*\))', re.DOTALL)
    content = insert_pattern.sub(r'\1\3', content)
    
    # Regex to capture fields inside SELECT ... (keeping FROM on a new line)
    select_pattern = re.compile(r'(SELECT\s+.*?)(fieldD)(\s+FROM)', re.DOTALL)
    content = select_pattern.sub(r'\1\3', content)
    
    return content

def rename_and_process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".sql"):  # Ensure we process only SQL files
            old_path = os.path.join(directory, filename)
            new_filename = f"DEVELOPMENT_{filename.split('.')[0]}_meta.sql"
            new_path = os.path.join(directory, new_filename)
            
            updated_content = process_sql_file(old_path)
            
            with open(new_path, 'w') as new_file:
                new_file.write(updated_content)
            
            print(f"Processed: {filename} -> {new_filename}")

# Ask user for directory path
directory_path = input("Please enter the directory path where your SQL files are stored: ")

# Check if the directory exists before proceeding
if os.path.isdir(directory_path):
    rename_and_process_files(directory_path)
else:
    print("The specified directory does not exist. Please check the path and try again.")
