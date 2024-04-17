import wikipedia

def has_wikipedia_page(name):
    try:
        page = wikipedia.page(name)
        return page.title.lower() == name.lower()
    except wikipedia.exceptions.DisambiguationError:
        return False
    except wikipedia.exceptions.PageError:
        return False

# Read names from the text file
with open('/Users/jay/Downloads/ijf/ijf.txt', 'r') as file:
    names = file.readlines()

# Remove trailing newline characters from each name
names = [name.strip() for name in names]

# Check if each person has a Wikipedia page
for name in names:
    if has_wikipedia_page(name):
        print(f"{name} has a Wikipedia page.")
    else:
        print(f"{name} does not have a Wikipedia page.")
