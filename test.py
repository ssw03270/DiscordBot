import requests
from bs4 import BeautifulSoup

response = requests.get('https://anonfiles.com/fbt3KaX6ya/main_py')
soup = BeautifulSoup(response.content, 'html.parser')
download = str(soup.select('#download-url'))
start = download.find('href="')
end = download.find('"', start)
start = end + 1
end = download.find('"', start)

print(download[start:end])