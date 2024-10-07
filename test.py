import pyodbc
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ranking_urls = [
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=472",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=473",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=474",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=475",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=476"
]

player_search_url = "https://bwf.tournamentsoftware.com/find/player"

# Given a players name, finds the url for that players profile
def get_player_profile_url (driver, player_name):

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

if __name__ == '__main__':
     driver = Chrome()
     get_player_profile_url(driver, "Viktor Axelsen")

# print(results)

# connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=Juju\\SQLEXPRESS;Database=TutorialDB;Trusted_connection=yes;TrustServerCertificate=yes;')

# cursor = connection.cursor()
# cursor.execute('''Create table People (
#                     name varchar(200)
#                );''')

# connection.commit()

# cursor.execute('''insert into People values ('Justin');''')

# connection.commit()