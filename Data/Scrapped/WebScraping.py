import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib.font_manager import json_dump

import Refactors.Splitter as customSplitter

pd.set_option('display.max_colwidth', None)
url = 'https://www.kikkararlari.com/haftanin-kik-karari/haftanin-kik-karari.html'
response = requests.get(url)
content = response.content

data = []

soup = BeautifulSoup(content, 'html.parser')

answer = soup.find_all('table', {'class': 'contentpaneopen'})[1].text
question = soup.find('td', {'class': 'contentheading'}).text


#judgmentResult = soup.find('table', {'style': 'margin-top:12px; text-align:justify; color: #cc0000; width: 100%; font-weight: bold; background: #F2F2F2; border: 1px #6699CC solid; border-collapse: collapse; border-spacing: 0px; '})

#if(judgmentResult.find('td') is not None):
#    judgmentResult = judgmentResult.find('td').text




list = customSplitter.splitAnswer(answer)
list.append(['SORU', question])
#list.append(['KARAR SONUCU', judgmentResult])

for i in list:
    i[1] = customSplitter.clean_text(i[1])


output = pd.DataFrame(list)
output.to_json('/Users/eyupkahraman/Desktop/deneme/output.json', orient='records', lines=True)
print(output)

