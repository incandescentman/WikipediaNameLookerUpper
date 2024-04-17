import requests

def get_wikipedia_url(name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={name}&srlimit=1"
    response = requests.get(url)
    data = response.json()

    try:
        if data['query']['search']:
            page_title = data['query']['search'][0]['title']
            page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
            return page_url
    except KeyError:
        pass
    return None

# Read names from the text file
with open('/Users/jay/Downloads/ijf/ijf.txt', 'r') as file:
    names = file.readlines()

# Remove trailing newline characters from each name
names = [name.strip() for name in names]

# Create a new file to store the results
output_file = '/Users/jay/Downloads/ijf/links.txt'

with open(output_file, 'w') as file:
    for name in names:
        url = get_wikipedia_url(name)
        if url:
            file.write(f"{name} has a Wikipedia page: {url}\n")
        else:
            file.write(f"{name} does not have a Wikipedia page.\n")

print(f"Results saved to {output_file}")
