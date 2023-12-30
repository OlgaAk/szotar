import requests
from bs4 import BeautifulSoup

letters_url = "https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/"

letter_selector = "#page-main-content > div.row > div.col-lg-9 > div.list-group.mb-3 > a"

letter_link_list = []

response = requests.get(letters_url)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

print(soup.title)
