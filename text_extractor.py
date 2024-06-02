import pandas as pd
import requests
from bs4 import BeautifulSoup

def parse_url(id, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pre_tag = soup.find_all('pre')
    for p in pre_tag:
        p.decompose()
    title = soup.title.text
    content_box = soup.find('div', attrs={'class': "td-post-content tagdiv-type"})
    if content_box is None:
        content_box = soup.find('div', attrs={'class': "td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type"})
    content = content_box.text if content_box else "Content not found"

    filename = f"{id}.txt"
    with open("txt_files/"+filename, 'w', encoding='utf-8') as textfile:
        textfile.write(f'{title}\n{content}')
    print(filename + " written successfully")

data = pd.read_excel("problem_statement/Input.xlsx")

for index, row in data.iterrows():
    parse_url(row['URL_ID'], row['URL'])