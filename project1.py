import os

def get_folder_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.stat(fp).st_size
            except FileNotFoundError:
                pass  # skip broken links or deleted files
    return total

def print_folder_sizes(root_path):
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            size = get_folder_size(item_path)
            print(f"{item} — {round(size / (1024 * 1024), 2)} MB")

# Example usage
print_folder_sizes(os.getcwd())
