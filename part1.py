from bs4 import BeautifulSoup
import requests

URL = "https://en.wikipedia.org/wiki/Donald_Trump"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib') 
print(soup.prettify())
