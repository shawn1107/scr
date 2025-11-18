import requests
from bs4 import BeautifulSoup

url = f"https://www.ptt.cc/bbs/nba/index.html"
headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
response = requests.get(url,headers = headers)

soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all("div", class_="r-ent")
print(articles)


# if response.status_code == 200:
#     with open('output.html', 'w' , encoding='utf-8') as f:
#         f.write(response.text)
#         print("寫入成功")
# else :
#     print("網址輸入錯誤")