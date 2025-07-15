import os
import shutil

def organize_directory(path):
    if not os.path.exists(path):
        print(" The specified path does not exist.")
        return

    # List all files in the directory
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, ext = os.path.splitext(file)
        ext = ext.lower().strip('.')

        if ext == '':
            ext = 'no_extension'

        # Create folder for the extension if it doesn't exist
        folder_path = os.path.join(path, ext)
        os.makedirs(folder_path, exist_ok=True)

        # Move the file
        new_file_path = os.path.join(folder_path, file)
        shutil.move(file_path, new_file_path)
        print(f" Moved: {file} → {ext}/")

# Example usage
organize_directory("C:/Users/YourUsername/Downloads")
