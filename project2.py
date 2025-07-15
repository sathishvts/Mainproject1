import os

def search_files(root_path, query):
    matches = []
    for dirpath, _, files in os.walk(root_path):
        for file in files:
            if query.lower() in file.lower():
                matches.append(os.path.join(dirpath, file))
    return matches

# Example usage
query = input("🔍 Enter filename or extension to search (e.g. '.pdf', 'report'): ")
results = search_files(os.getcwd(), query)

print(f"\nFound {len(results)} file(s):")
for r in results:
    print(r)
