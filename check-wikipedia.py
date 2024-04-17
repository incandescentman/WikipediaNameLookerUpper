import requests
import re

def check_name(firstname, lastname, url):
    fullname_regex = fr"{firstname}.*{lastname}|{lastname}.*{firstname}"
    match = re.search(fullname_regex, url, re.IGNORECASE)
    if match:
        return True
    else:
        return False

def get_wikipedia_url(name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={name}&srlimit=1"
    response = requests.get(url)
    data = response.json()

    try:
        if data['query']['search']:
            page_title = data['query']['search'][0]['title']
            page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"

            # Check if the name contains a space
            if ' ' in name:
                first_name, last_name = name.split(' ', 1)
                if check_name(first_name, last_name, page_url):
                    return page_url
            else:
                if name.lower() in page_title.lower():
                    return page_url
    except KeyError:
        pass
    return None

# Read names from the text file
with open('/Users/jay/Downloads/ijf/names.txt', 'r') as file:
    names = file.readlines()

# Remove trailing newline characters from each name
names = [name.strip() for name in names]

# Create a new file to store the results
output_file = '/Users/jay/Downloads/ijf/links.txt'
known_names_file = '/Users/jay/Downloads/ijf/known-names.txt'

with open(output_file, 'w') as file, open(known_names_file, 'w') as known_file:
    for name in names:
        url = get_wikipedia_url(name)
        if url:
            file.write(f"{name} has a Wikipedia page: {url}\n")
            known_file.write(f"{name}: {url}\n")
        else:
            file.write(f"{name} does not have a Wikipedia page.\n")

# Read the known-names.txt file
with open(known_names_file, 'r') as file:
    lines = file.readlines()

# Create a dictionary to store URLs and their corresponding lines
url_dict = {}
for line in lines:
    url = line.strip().split(': ')[1]
    if url in url_dict:
        url_dict[url].append(line)
    else:
        url_dict[url] = [line]

# Write the updated lines back to known-names.txt
with open(known_names_file, 'w') as file:
    for url, lines in url_dict.items():
        file.write(lines[0])

print(f"Results saved to {output_file}")
print(f"Names with Wikipedia pages saved to {known_names_file}")
