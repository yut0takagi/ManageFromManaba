
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_html(url,driver):
    """
    指定されたURLからHTMLを取得する関数
    :param url: 取得するURL
    """
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html


def parse_timetable_from_manaba(html: str):

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", class_="stdlist")

    # ヘッダーから曜日のリストを取得
    days = []
    for th in table.find("tr", class_="title").find_all("th")[1:]:
        days.append(th.text.strip())

    timetable_data = []

    # 時限ごとの行を解析
    for tr in table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if not tds:
            continue

        period = tds[0].text.strip()

        for i, td in enumerate(tds[1:]):
            course_div = td.find("div", class_="courselistweekly-c")
            if course_div:
                a_tag = course_div.find("a", href=True)
                if a_tag:
                    title = a_tag.text.strip()
                    href = a_tag['href']
                    has_unsubmitted = any(
                        "未提出の課題があります" in img.get("alt", "") 
                        for img in course_div.find_all("img")
                    )
                    timetable_data.append({
                        "day": days[i],
                        "period": int(period) if period.isdigit() else period,
                        "title": title,
                        "href": href,
                        "has_unsubmitted": has_unsubmitted
                    })

    return timetable_data

def loginManaba(username, password):
    # Chrome ヘッドレス設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome()
    try:
        driver.get("https://room.chuo-u.ac.jp/ct/home")
        driver.find_element(By.ID, "username_input").send_keys("23D7104001I")
        driver.find_element(By.ID, "password_input").send_keys("1025t1025")
        driver.find_element(By.ID, "login_button").click()
        time.sleep(3)
        driver.get("https://room.chuo-u.ac.jp/ct/home")
        html = driver.page_source
        return {"status": "success", "html": html}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}
    

    
    