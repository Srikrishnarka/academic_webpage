import requests
import yaml
import os

# ORCID ID and Base URL
ORCID_ID = "0000-0001-5187-6879"  # Replace with your ORCID ID
BASE_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

# Headers for API request
HEADERS = {
    "Accept": "application/json"
}

# Directory for publications
PUBLICATIONS_DIR = "_publications"
os.makedirs(PUBLICATIONS_DIR, exist_ok=True)

def fetch_orcid_data():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching ORCID data: {response.status_code}")
        return None

def create_publication_file(publication):
    # Extract relevant fields
    title = publication.get("title", {}).get("title", {}).get("value", "Untitled")
    year = publication.get("publication-date", {}).get("year", {}).get("value", "Unknown")
    authors = ", ".join([author["credit-name"]["value"] for author in publication.get("contributors", {}).get("contributor", []) if "credit-name" in author])
    journal = publication.get("journal-title", {}).get("value", "")
    url = publication.get("url", {}).get("value", "")

    # YAML front matter
    front_matter = {
        "title": title,
        "year": year,
        "authors": authors,
        "journal": journal,
        "url": url,
        "layout": "publication"
    }

    # File content
    content = f"---\n{yaml.dump(front_matter, default_flow_style=False)}---\n"

    # Write to markdown file
    filename = f"{PUBLICATIONS_DIR}/{year}-{title.replace(' ', '-').replace('/', '-')}.md"
    with open(filename, "w") as file:
        file.write(content)
    print(f"Created: {filename}")

def main():
    data = fetch_orcid_data()
    if data:
        works = data.get("group", [])
        for work in works:
            publication = work.get("work-summary", [{}])[0]
            create_publication_file(publication)

if __name__ == "__main__":
    main()
