import requests
import pandas as pd
from bs4 import BeautifulSoup

def extract_paragraphs(urls):
    counts = 0
    for i in urls:
        counts += 1
        all_text = ""
        file_name = "txt_files/output_file" + str(counts) + ".txt"
        response = requests.get(i)
        soup = BeautifulSoup(response.content, 'html.parser')
        target_divs = soup.find_all('div','td-post-content tagdiv-type')

        for j in target_divs:
            for pre in j.find_all('pre'):
                pre.decompose()
            all_text += j.get_text(separator='\n', strip=True) + '\n\n'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(all_text.strip())

df = pd.read_excel('problem_statement/Input.xlsx')

extract_paragraphs(df['URL'])