from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json


def get_html(url):
    """
    指定されたURLからHTMLを取得する関数
    :param url: 取得するURL
    """
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    # Get the page source
    html = driver.page_source
    driver.quit()
    return html

def parse_timetable_from_manaba(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", class_="stdlist")

    # ヘッダーから曜日のリストを取得
    days = []
    for th in table.find("tr", class_="title").find_all("th")[1:]:  # 最初の1列目は時限列なので除く
        days.append(th.text.strip())

    timetable_data = []

    # 時限ごとの行を解析
    for tr in table.find_all("tr")[1:]:  # 最初の行はヘッダーなので除く
        tds = tr.find_all("td")
        if not tds:
            continue

        period = tds[0].text.strip()  # 時限番号

        # 各曜日の列を処理
        for i, td in enumerate(tds[1:]):  # 最初の列は時限列なので除く
            a_tag = td.find("a")
            if a_tag:
                title = a_tag.text.strip()
                href = a_tag.get("href")
                timetable_data.append({
                    "day": days[i],
                    "period": int(period) if period.isdigit() else period,
                    "title": title,
                    "href": href
                })

    return timetable_data