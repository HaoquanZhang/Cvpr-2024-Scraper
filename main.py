import requests
from bs4 import BeautifulSoup

# target URL
url = 'https://cvpr.thecvf.com/virtual/2024/awards_detail'
response = requests.get(url)

if response.status_code == 200:
    # parse
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1').get_text()
    
    print('Page Title:', title)

    paragraphs = soup.find_all('p')
    
    for idx, p in enumerate(paragraphs):
        print(f'Paragraph {idx+1}:', p.get_text())
else:
    print('Failed to retrieve the page')
