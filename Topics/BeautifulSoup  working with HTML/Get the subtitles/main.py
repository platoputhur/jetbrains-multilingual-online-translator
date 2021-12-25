import requests

from bs4 import BeautifulSoup

index = input()
link = input()
response = requests.get(link)
soup = BeautifulSoup(response.content, "html.parser")
headers = soup.find_all('h2')
print(headers[int(index)].text)
