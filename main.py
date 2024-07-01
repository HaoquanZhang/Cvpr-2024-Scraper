import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# CVPR 2024 Highlighted Paper List
url = 'https://cvpr.thecvf.com/virtual/2024/awards_detail'
print("The word you want:", end="")
target_word = input()
response = requests.get(url)
n = 0

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    papers = soup.find_all('div', class_='displaycards touchup-date')
    matching_titles = []

    for paper in tqdm(papers):
        # 找到论文标题和链接
        title_tag = paper.find('a', class_='small-title text-underline-hover')
        if title_tag:
            title = title_tag.get_text().strip()
            link = title_tag['href']
            full_link = f'https://cvpr.thecvf.com{link}'

            # find abstract and authors
            abstract = paper.find('div', class_='text-start p-4').get_text().strip()
            authors = paper.find('div', class_='author-str').get_text().strip()
            if abstract:
                # check if target word exist
                if target_word in abstract:
                    n += 1
                    matching_titles.append(f'### {n}. {title}')
                    matching_titles.append(f'{authors}\n')
                    matching_titles.append(f'[[CVPR Official Link]]({full_link})')
    
    # export to md
    with open(f'CVPR-Awaded-Papers-{target_word}.md', 'w', encoding='utf-8') as f:
        f.write(f'# CVPR-Awaded-Papers-"{target_word}"\n\n')
        f.write('\n'.join(matching_titles))
        f.write('\n')

    print(f'Found {len(matching_titles)/3} papers with the word "{target_word}" in the abstract.')

else:
    print('Failed to retrieve the page')
