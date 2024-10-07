import pyodbc
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

rankingURLS = [
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=472",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=473",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=474",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=475",
     "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=42511&category=476"
]

playerSearchURL = "https://bwf.tournamentsoftware.com/find/player"

driver = Chrome()
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

driver.get(playerSearchURL)
driver.find_element(By.ID, "Query").send_keys("Viktor")

try:
     elem = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "ul#searchResultArea > li")) or EC.presence_of_element_located((By.CSS_SELECTOR, "ul#searchResultArea > ul > li"))
     )
except:
     print('ERROR')

page_content = BeautifulSoup(driver.page_source, 'html.parser')
results = page_content.select("ul#searchResultArea > ul > li")
if (len(results) == 0):
     results = page_content.select("ul#searchResultArea > li")

for player in results:
     nameContainer = player.select("a.media__link")[0]
     print(nameContainer.text)

# print(results)

# connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=Juju\\SQLEXPRESS;Database=TutorialDB;Trusted_connection=yes;TrustServerCertificate=yes;')

# cursor = connection.cursor()
# cursor.execute('''Create table People (
#                     name varchar(200)
#                );''')

# connection.commit()

# cursor.execute('''insert into People values ('Justin');''')

# connection.commit()