import requests
from bs4 import BeautifulSoup

# target URL
url = 'https://cvpr.thecvf.com/virtual/2024/awards_detail'
target_word = 'language'
response = requests.get(url)
n = 0

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    papers = soup.find_all('div', class_='displaycards touchup-date')
    matching_titles = []

    for paper in papers:
        # 找到论文标题和链接
        title_tag = paper.find('a', class_='small-title text-underline-hover')
        if title_tag:
            title = title_tag.get_text().strip()
            link = title_tag['href']
            full_link = f'https://cvpr2024.thecvf.com{link}'  # 完整链接
            # 找到论文摘要
            abstract_tag = paper.find('div', class_='text-start p-4')
            if abstract_tag:
                abstract = abstract_tag.get_text().strip()
                # 检查摘要中是否包含目标单词
                if target_word in abstract:
                    n += 1
                    matching_titles.append(f'### {n}. {title}')
                    matching_titles.append(f'[CVPR Official Link]({full_link})')
    
    # 导出到Markdown文件
    with open(f'CVPR-Awaded-Papers-{target_word}.md', 'w', encoding='utf-8') as f:
        f.write(f'# CVPR-Awaded-Papers-"{target_word}"\n\n')
        f.write('\n'.join(matching_titles))
        f.write('\n')

    print(f'Found {len(matching_titles)} papers with the word "{target_word}" in the abstract.')

else:
    print('Failed to retrieve the page')
