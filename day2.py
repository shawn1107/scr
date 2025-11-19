import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/HatePolitics/index.html"

for i in range(5):
    print(f"\n===== 第 {i+1} 頁：{url} =====")

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 取得所有文章標題
    articles = soup.find_all("div", class_="title")
    for a in articles:
        if a.a:
            print(a.a.text)

    # 用 class 找「上一頁」按鈕（最穩定的方法）
    paging = soup.find("div", class_="btn-group btn-group-paging")
    prev_btn = paging.find_all("a")[1]   # 0=最舊, 1=上一頁, 2=最新

    # 取得真正的上一頁網址
    url = "https://www.ptt.cc" + prev_btn["href"]
