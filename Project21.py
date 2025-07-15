from urllib.parse import urljoin


base_url = "https://example.com/"

def build_url():
    print("\n--- URL Builder ---")
    path = input("Enter path (e.g., /products/view): ").strip().lstrip('/')

    # Collect query parameters
    query_params = {}
    while True:
        add_param = input("Add query param? (y/n): ").lower()
        if add_param == 'n':
            break
        key = input("  Param name: ").strip()
        value = input("  Param value: ").strip()
        query_params[key] = value

    # Build full URL
    full_url = urljoin(base_url, path)
    if query_params:
        full_url += "?" + url_encode(query_params)

    print("\n🔗 Generated URL:")
    print(full_url + "\n")

def menu():
    while True:
        print("=== URL Builder ===")
        print("1. Build new URL")
        print("2. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            build_url()
        elif choice == "2":
            break
        else:
            print("❌ Invalid choice.")

menu()
