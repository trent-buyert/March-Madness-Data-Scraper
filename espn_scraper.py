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
columns = []
thead = soup.find_all("thead")[1]
tr = thead.find("tr")
ths = tr.find_all("th")
first_title = ths[0].find("div").text.strip()
columns.append(first_title)
for th in ths[1:]:
    title = th.find("a").text.strip()
    columns.append(title)
stats_table = soup.find_all("tbody")[1]
rows_stats = stats_table.find_all('tr', class_='Table__TR')
stats_grid = []
for row in rows_stats[:-1]:
    stat_cells = row.find_all('td', class_='Table__TD')
    stats_row = [float(cell.get_text(strip=True)) for cell in stat_cells]
    stats_grid.append(stats_row)

table = soup.find("tbody")
rows = table.find_all("tr")
ppg_ranking = []
for row in rows[:-1]:
    team_ranking = row.find('td', class_='Table__TD').text.strip()
    team_name = row.find_all('a', class_='AnchorLink')[1].text.strip()
    team_ranking = int(team_ranking)
    ppg_ranking.append((team_name, team_ranking))


def create_team_stats_dataframe(team_rankings, column_names, rows_of_stats):
    df_stats = pd.DataFrame(rows_of_stats, columns=column_names)

    # Create a dictionary for team rankings
    team_dict = {team: rank for team, rank in team_rankings}

    # Add team names to the DataFrame
    df_stats.insert(0, 'Team', [team for team, _ in team_rankings])

    # Set the team names as the index
    df_stats.set_index('Team', inplace=True)

    # Add the rankings as a new column
    df_stats['Ranking'] = [team_dict[team] for team in df_stats.index]

    # Move the 'Ranking' column to the first position
    df_stats = df_stats[['Ranking'] + column_names]

    return df_stats


df = create_team_stats_dataframe(ppg_ranking, columns, stats_grid)
df.to_csv("2024_regular_season_offensive_stats.csv")

driver.close()