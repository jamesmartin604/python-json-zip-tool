import zipfile
import json
import csv

# Ask user for the ZIP file path
zip_path = input("Enter the path to your ZIP file: ").strip('"')

with zipfile.ZipFile(zip_path, 'r') as z:
    all_files = z.namelist()

    following_file = next((f for f in all_files if f.endswith("/following.json")), None)
    followers_file = next((f for f in all_files if f.endswith("/followers_1.json")), None)

    # Extract following usernames
    following_usernames = []
    if following_file:
        with z.open(following_file) as f:
            data = json.load(f)
            entries = data.get("relationships_following", [])
            for entry in entries:
                following_usernames.append(entry.get("title"))

    # Extract followers usernames
    followers_usernames = []
    if followers_file:
        with z.open(followers_file) as f:
            data = json.load(f)
            for entry in data:
                for item in entry.get("string_list_data", []):
                    followers_usernames.append(item.get("value"))

# Find users you follow who don't follow back
not_following_back = set(following_usernames) - set(followers_usernames)

# Filter out known celebrities / irrelevant accounts
ignore_list = {
    "instagram", "nasa", "cristiano", "kimkardashian", "therock", "selenagomez", 
    "arianagrande", "nike", "adidas"
    # add more usernames you want to ignore
}

not_following_back_filtered = [u for u in not_following_back if u.lower() not in ignore_list]

# Sort usernames alphabetically
not_following_back_filtered.sort()

# Print result
print("\n--- USERS YOU FOLLOW WHO DO NOT FOLLOW YOU BACK (Filtered) ---\n")
for username in not_following_back_filtered:
    print(username)

# Optional: export to CSV
csv_file = "not_following_back_filtered.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["username"])
    for username in not_following_back_filtered:
        writer.writerow([username])

print(f"\nFiltered list saved to '{csv_file}'")
