import os

def organize_by_extension(folder_path):
    if not os.path.exists(folder_path):
        print("❌ Directory does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isdir(file_path):
            continue

        _, ext = os.path.splitext(filename)
        ext = ext[1:].lower() if ext else 'no_extension'

        target_folder = os.path.join(folder_path, ext)
        os.makedirs(target_folder, exist_ok=True)

        new_path = os.path.join(target_folder, filename)
        os.rename(file_path, new_path)
        print(f"Moved: {filename} → {ext}/")

# Example usage
organize_by_extension(os.getcwd())
