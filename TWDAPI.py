from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

# 設定 Selenium 無頭模式
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')

# 啟動 WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://www.cbc.gov.tw/tw/lp-645-1.html")

# 等待匯率表格出現（最多 10 秒）
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "rwd-table"))
)

# 取得畫面 HTML
html = driver.page_source
driver.quit()

# 用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html, "lxml")
tbody = soup.find("table", class_="rwd-table").find("tbody")
rows = tbody.find_all("tr")

# 取出最新一列（第 1 列是最新匯率資料）
latest_row = rows[1]
tds = latest_row.find_all("td")
latest_date = tds[0].find("span").text.strip()
latest_rate = tds[1].find("span").text.strip()

# 封裝成 JSON 格式
data = {
    "date": latest_date,
    "rate": latest_rate
}

# 儲存為 JSON 檔案
with open("TWD_USD_rate.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
