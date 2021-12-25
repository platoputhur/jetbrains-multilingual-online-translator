import requests

from bs4 import BeautifulSoup

letter = 'S'
url = input()
# topic_prefix = "http://web.archive.org/web/20201201053628/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
links = soup.find_all('a')
topics = []
for link in links:
    href = link.get('href')
    if href:
        if "topics" in href or "entity" in href:
            if len(link.text) > 1 and link.text[0] == letter:
                topics.append(link.text)
print(topics)

