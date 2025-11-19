from typing import dataclass_transform

import requests
from bs4 import BeautifulSoup
import json
url = f"https://www.ptt.cc/bbs/nba/index.html"
headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
response = requests.get(url,headers = headers)

soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all("div", class_="r-ent")
data_list = []

for a in articles:
    data = {}
    title = a.find("div", class_="title")
    if title and title.a.text:
        title = title.a.text
        # print(title.a.text)
    else:
        title = "沒有標題"
    data["標題"] = title
    # print(title)
    popular = a.find("div",class_="nrec")
    if popular and popular.span:
        popular = popular.span.text
    else:
        popular = "N/A"
    data["人氣"] = popular

    date = a.find("div",class_="date")
    if date :
        date = date.text
    else:
        date = "N/A"
    data["日期"] = date
    data_list.append(data)
with open("ppt_nba_data.json", "w",encoding = "utf-8") as file:
    json.dump(data_list, file,ensure_ascii=False, indent = 4)
print("成功儲存")
# print(data_list)
    # print(f"標題:{title} 人氣:{popular} 日期:{date}")