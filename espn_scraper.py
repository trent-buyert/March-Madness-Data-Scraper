import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests as rq

ncaa_team_stats_url = "https://www.espn.com/mens-college-basketball/stats/team"

driver = webdriver.Chrome()
driver.get(ncaa_team_stats_url)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[3]/div/div/section/div/div[5]/a")

for _ in range(7):
    wait = WebDriverWait(driver, 5)
    locator = By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[3]/div/div/section/div/div[5]/a"
    try:
        # Wait for the element to be present and clickable
        element = wait.until(EC.element_to_be_clickable(locator))
        # Click the element
        element.click()
    except Exception as e:
        print(f"An error occurred: {e}")
        break
time.sleep(2)
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("tbody")
rows = table.find_all("tr")
for row in rows[:-1]:
    team_ranking = row.find('td', class_='Table__TD').text.strip()
    team_name = row.find_all('a', class_='AnchorLink')[1].text.strip()
    print(f"{team_ranking}: {team_name}")

driver.close()