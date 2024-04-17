import requests
from bs4 import BeautifulSoup
import re

# Send a GET request to the Wikipedia page
url = "https://en.wikipedia.org/wiki/Julia_Angwin"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the text within the <p> tags
text = ' '.join([p.get_text() for p in soup.find_all('p')])

# Use regular expressions to find names that are likely to be people's names
name_regex = r'\b[A-Z][a-zA-Z\'\-]+\s+(?:[A-Z][a-zA-Z\'\-]+\s+)?[A-Z][a-zA-Z\'\-]+\b'
matches = re.findall(name_regex, text)

# Open the files to write the output
with open('links.txt', 'w') as links_file, open('nonlinks.txt', 'w') as nonlinks_file:
    unique_matches = set()  # Set to store unique matches

    for match in matches:
        # Check if the match is already processed (either in original or reversed order)
        if match in unique_matches or ' '.join(match.split()[::-1]) in unique_matches:
            continue

        unique_matches.add(match)  # Add the match to the set of unique matches

        # Check if a Wikipedia page exists for the name
        name_url = f"https://en.wikipedia.org/wiki/{match.replace(' ', '_')}"
        name_response = requests.get(name_url)

        if name_response.status_code == 200:
            links_file.write(f"{match} has a Wikipedia page: {name_url}\n")
        else:
            nonlinks_file.write(f"{match} does not have a Wikipedia page.\n")

print("Output written to links.txt and nonlinks.txt.")
