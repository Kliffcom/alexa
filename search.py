from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

def search(textToSearch):
    query = quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features='html.parser')
    return ['https://www.youtube.com' + vid['href'] for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}) if 'watch?v=' in vid['href']]