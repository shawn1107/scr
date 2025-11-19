# Python 爬蟲學習專案（從零開始）

這份文件將會是你專屬的爬蟲學習計畫與筆記空間。
我會把每天的學習內容、示範程式碼、練習題都放在這裡。

---

## **Day 1：最基礎爬蟲 — 抓取網頁內容（requests）**

### 📘 程式碼逐行解析（詳細版）

以下是你在 Day 1 寫出的程式碼，每一行的作用都幫你整理好了：

```python
import requests

url = "https://www.ptt.cc/bbs/HatePolitics/index.html"
response = requests.get(url)

print("狀態碼：", response.status_code)
print(response.text[:500])
```

#### 1. `import requests`

載入 `requests` 套件，用來發送 HTTP GET/POST 請求。

#### 2. `url = "https://www.ptt.cc/..."`

把要爬的網址存成變數，方便管理、修改。

#### 3. `response = requests.get(url)`

向指定的 URL 發送 GET 請求，並把伺服器回傳的結果存入 `response`。

#### 4. `response.status_code`

顯示伺服器的回應狀態，例如 200（成功）、404（找不到）。

#### 5. `response.text[:500]`

`response.text` 是整段 HTML 字串，而 `[:500]` 表示只印出前 500 個字避免太長。

---

### 📘 title 標籤解析

你也執行了以下程式：

```python
html = response.text

start = html.find("<title>")
end = html.find("</title>")

print("完整標題：", html[start+7:end])
```

#### 1. `html = response.text`

把整份 HTML 存成變數 `html`。

#### 2. `start = html.find("<title>")`

找到 `<title>` 在 HTML 中的位置。

#### 3. `end = html.find("</title>")`

找到 `</title>` 的位置。

#### 4. `html[start+7:end]`

`<title>` 有 7 個字，`start+7` 可以跳過 `<title>` 本身，取得中間真正的文字。

顯示結果：

```
完整標題：看板 HatePolitics 文章列表 - 批踢踢實業坊
```

---

（以下為原本 Day 1 課程內容）

### 🌐 1. 什麼是 HTTP？

* **HTTP Request**：你的程式送出請求（我要看這個網頁）。
* **HTTP Response**：伺服器回傳內容（把網頁 HTML 給你）。

### 📌 2. 安裝必要套件

```bash
pip install requests
```

### 📄 3. 使用 `requests` 抓取網頁 HTML

```python
import requests

url = "https://www.google.com"
response = requests.get(url)

print("狀態碼：", response.status_code)
print("前300字HTML：")
print(response.text[:300])
```

### ✔️ 4. 基本錯誤處理

```python
import requests

url = "https://www.google.com"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # 如果不是 200 會噴錯
    print("成功取得資料！")
except requests.exceptions.RequestException as e:
    print("發生錯誤：", e)
```

### 📝 Day 1 練習題

1. 改成抓取：`https://www.ptt.cc/bbs/HatePolitics/index.html`
2. 印出：

   * 狀態碼
   * HTML 前 500 字
3. 試著把錯誤處理成功跑起來（故意打錯網址測試）

---

## **Day 2：解析網頁資料 — BeautifulSoup 入門**

### 🧠 1. 為什麼需要 BeautifulSoup？

`requests` 只能抓 HTML，難以解析內容；`BeautifulSoup` 可以讓你直接用標籤 (tag) 找出你要的資訊。

---

### 📦 2. 安裝 BeautifulSoup

```bash
pip install beautifulsoup4
```

---

### 🔍 3. BeautifulSoup 基本使用

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/HatePolitics/index.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

print("網頁標題：", soup.title.text)
```

---

### 📄 4. 抓取 PTT 文章列表（標題）

```python
articles = soup.find_all("div", class_="title")

for a in articles:
    if a.a:  # 有些文章被刪除沒有 a 標籤
        print(a.a.text.strip())
```

---

### 🔥 strip() 為什麼要用？（重要概念）

在 PTT 的 HTML 裡，`<a>` 標籤內容通常長這樣：

```html
<a href="xxx">
    [爆卦] 某某某
</a>
```

包含：

* 前後換行 `
  `
* 前後空格、縮排 `    `

若直接寫：

```python
a.a.text
```

你會得到：

```
"
    [爆卦] 某某某
"
```

資料會變成「醜醜的」，存到檔案也會有空白問題。

使用：

```python
a.a.text.strip()
```

會自動清除：

* 前後空白
* 換行 `
  `
* tab `	`

讓你得到乾淨標題：

```
"[爆卦] 某某某"
```

這是爬蟲非常重要的習慣。

---

### ⭐ 正確的多頁爬蟲方法（使用上一頁按鈕）

PTT 的頁碼不是 index2、index3，而是類似 index4287.html，需要從「上一頁」按鈕取得。

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/HatePolitics/index.html"

for i in range(5):  # 爬五頁
    print(f"
===== 第 {i+1} 頁：{url} =====")

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 抓取標題
    articles = soup.find_all("div", class_="title")
    for a in articles:
        if a.a:
            print(a.a.text.strip())

    # 取得上一頁按鈕（最穩定寫法）
    paging = soup.find("div", class_="btn-group btn-group-paging")
    prev_btn = paging.find_all("a")[1]  # 第二個按鈕 = 上一頁

    url = "https://www.ptt.cc" + prev_btn["href"]
```

---

### 📝 Day 2 練習題

1. 印出 PTT HatePolitics 所有文章的標題（乾淨版）。
2. 印出標題 + 完整網址。
3. 自動爬五頁資料。
4. 思考：strip() 不加會有什麼差異？

---

（以下為 Day 3）：解析網頁資料 — BeautifulSoup 入門**

### 🧠 1. 為什麼需要 BeautifulSoup？

`requests` 可以拿到整份 HTML，但 HTML 是一大段字串，不好找資料。

`BeautifulSoup` 讓我們能：

* 用標籤（tag）直接找到資料
* 自動解析 HTML 結構
* 輕鬆取得文字、連結、屬性

---

### 📦 2. 安裝 BeautifulSoup

```bash
pip install beautifulsoup4
```

---

### 🔍 3. 基本使用方法

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/HatePolitics/index.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# 抓取網頁標題
print(soup.title.text)
```

#### 📌 `BeautifulSoup(res.text, "html.parser")`：

把 HTML 變成可搜尋的樹狀結構。

#### 📌 `soup.title.text`：

自動找到 `<title>` 並取出文字。

---

### 📄 4. 抓取 PTT 文章列表（標題）

```python
articles = soup.find_all("div", class_="title")

for a in articles:
    if a.a:  # 有些文章可能被刪除，沒有 a 標籤
        print(a.a.text)
```

#### 解析：

* `find_all("div", class_="title")` → 找所有標題區塊
* `a.a.text` → `<a>` 裡的文章標題文字

---

### 📝 Day 2 練習題

1. 印出 PTT HatePolitics 所有文章的 **標題**。
2. 同時印出 **標題 + 網址**（提示：用 `a.get("href")`）。
3. 試著抓其他板，如 Gossiping（注意 18 禁問題）。

---

（以下為 Day 3）：解析網頁資料 — BeautifulSoup 入門**

* HTML 結構講解
* 使用 `BeautifulSoup` 抓取標題、段落、連結
* 練習：抓取 PTT / 一般網頁標題

---

## **Day 3：爬取表格數據 — pandas + BeautifulSoup 結合**

* 抓取政府公開資料的 HTML 表格
* 使用 pandas 轉成 DataFrame
* 輸出成 Excel

---

## **Day 4：處理較複雜網站 — headers、User-Agent、避免封鎖**

* 什麼是防爬蟲？
* 加上 request headers 模擬瀏覽器
* 加上 delay 避免被封鎖（Too Many Requests）

---

## **Day 5：進階爬蟲 — 抓圖片、JSON、API 返回資料**

* 抓取網站圖片
* 解析 JSON（如公開資料 API）
* 合併爬蟲與 pandas 自動化

---

你可以開始 Day 1，我會隨時根據你的進度補充內容與練習題。
