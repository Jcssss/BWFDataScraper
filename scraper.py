import pyodbc
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

ranking_urls = [
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=472",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=473",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=474",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=475",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=476"
]

base_url = "https://bwf.tournamentsoftware.com"
player_search_url = "https://bwf.tournamentsoftware.com/find/player"

# Given a player's name, finds the url for that player's profile
def get_player_profile_url_by_name (driver, player_name):

     # Navigate to the page and place the player's name in the search bar
     driver.get(player_search_url)
     driver.find_element(By.ID, "Query").send_keys(player_name)

     # Wait for results to load, there should be exactly one result
     try:
          WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.CSS_SELECTOR, "ul#searchResultArea > li"))
          )
     except:
          print('ERROR')

     # Get the single result corresponding to the player
     page_content = BeautifulSoup(driver.page_source, 'html.parser')
     player_container = page_content.select("ul#searchResultArea > li")[0]

     # Gets the link to the player's profile
     player_link = player_container.select("a.media__link")[0]
     return player_link["href"]

# Given a ranking page, gets all players' names
def get_player_profiles (driver, ranking_url):

     # navigate to the page
     driver.get(ranking_url)

     # select the dropdown for the snapshot week
     driver.find_element(By.CSS_SELECTOR, "a.chosen-single").click()

     # Wait for options to load
     try:
          WebDriverWait(driver, 10).until(
               EC.presence_of_element_located((By.CLASS_NAME, "chosen-results"))
          )
     except:
          print('ERROR')

     # Get the total number of snapshot weeks
     weeks = len(driver.find_elements(By.CSS_SELECTOR, ".chosen-results > li"))

     # Click the menu again to close it
     driver.find_element(By.CSS_SELECTOR, "a.chosen-single").click()

     # For every snapshot week
     for week in range (1, weeks):

          # Select the desired snapshot week
          driver.find_element(By.CSS_SELECTOR, "a.chosen-single").click()
          try:
               WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "chosen-results"))
               )
          except:
               print('ERROR')
          week_option = driver.find_element(By.CSS_SELECTOR, f".chosen-results > li:nth-child({week})")
          week = week_option.text
          date_of_week = datetime.strptime(week.strip(), "%m/%d/%Y")
          print(date_of_week.strftime("%A %B %d, %Y"))
          week_option.click()

          # Iterate through each page of players
          while (True):

               # Get the players on the page
               page_content = BeautifulSoup(driver.page_source, 'html.parser')
               player_containers = page_content.select("table.ruler > tbody > tr")[2:-1]

               # For each player get the relevant data
               for container in player_containers:
                    player_name = container.select("td:has(span.flag) > a")[0].text
                    print(player_name)

                    player_rank = container.select("td.rank")[0].text
                    print(player_rank)

                    player_points = container.select("td.rankingpoints")[0].text
                    print(player_points)

               # Look for the next page button
               try:
                    WebDriverWait(driver, 4).until(
                         EC.presence_of_element_located((By.CSS_SELECTOR, "a.page_next"))
                    )

               # If the button doesn't exist, then we are on the last page, move to next week
               except:
                    print("end")
                    break
               
               # If the button exists, click it and move to the next page
               driver.find_element(By.CSS_SELECTOR, "a.page_next").click()


# Given a player's profile, gets a list of all the tournaments they've played in
def get_player_tournaments (driver, profile_url):

     # Navigate to the players tournament page
     new_url = base_url + profile_url + "/tournaments"
     
     # Navigates through each year's tournaments and extracts the tournament names
     tournament_urls = set()
     for extension in ["2024", "2023", "2022", "2021", "2020", "0"]:
          driver.get(new_url + "/" + extension)

          # Wait for tournaments to load
          try:
               WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "tabcontent"))
               )
          except:
               print('ERROR')

          # Find the list of tournaments
          page_content = BeautifulSoup(driver.page_source, 'html.parser')
          tournament_list = page_content.select("#tabcontent > div")

          # For each tournament fetch the link to the tournament
          for tournament in tournament_list:
               tournament_url_container = tournament.select("a.media__link")[0]
               tournament_urls.add(tournament_url_container["href"])

     return tournament_urls

if __name__ == '__main__':

     # Install an ad blocker chrome extension
     chrome_options = Options()
     chrome_options.add_extension("./adblock.crx")

     # Create an instance of the driver
     driver = Chrome(options=chrome_options)

     # profile_url = get_player_profile_url_by_name(driver, "Viktor Axelsen")
     # get_player_tournaments(driver, profile_url)
     get_player_profiles(driver, ranking_urls[0])


# connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=Juju\\SQLEXPRESS;Database=TutorialDB;Trusted_connection=yes;TrustServerCertificate=yes;')

# cursor = connection.cursor()
# cursor.execute('''Create table People (
#                     name varchar(200)
#                );''')

# connection.commit()

# cursor.execute('''insert into People values ('Justin');''')

# connection.commit()