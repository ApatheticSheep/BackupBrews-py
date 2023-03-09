#!/usr/bin/python3
import os
import re
import requests
from bs4 import BeautifulSoup

backup_dir = './brewBackups'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def cleanUpBrew(brew):
    prefix = "<code><pre style=\"white-space: pre-wrap;\">"
    suffix = "</pre></code>"
    brew = brew.replace(prefix, "").replace(suffix, "")
    brew = brew.replace("&gt;", ">").replace("&lt;", "<")
    return brew

with open("brews.txt", "r") as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')
for brewItem in soup.find_all('div', attrs={'class': 'brewItem'}):
    shareLink = brewItem.find('a', attrs={'class': 'shareLink'})['href']
    shareLink = shareLink.replace('/share/', '')

    # Fetch markdown source from shareLink
    response = requests.get('https://homebrewery.naturalcrit.com/source/' + shareLink)
    markdown_source = response.text

    # Clean up markdown source
    cleaned_up_markdown = cleanUpBrew(markdown_source)

    # Replace characters that shouldn't be part of a file name with more friendly characters
    friendly_text = re.sub(r'[^\w\s-]', '', brewItem.find('h2').text.strip())
    friendly_text = re.sub(r'[-\s]+', '-', friendly_text)

    # Write cleaned-up markdown to file
    filename = os.path.join(backup_dir, friendly_text + '.md')
    with open(filename, 'w') as f:
        f.write(cleaned_up_markdown)

    print('Backup saved to', filename)

