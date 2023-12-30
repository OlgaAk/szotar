import requests
from bs4 import BeautifulSoup


def get_letter_links():
	letters_url = "https://www.arcanum.com/hu/online-kiadvanyok/Lexikonok-a-magyar-nyelv-ertelmezo-szotara-1BE8B/"

	letter_selector = "list-group-item list-group-item-action"

	letter_link_list = {}

	response = requests.get(letters_url)

	html = response.text

	soup = BeautifulSoup(html, 'html.parser')

	letters = soup.find_all("a", letter_selector)

	for letter in letters:
		if len(letter.text) < 6:
			letter_link_list[letter.text] = letter.get("href")

	return letter_link_list
	
	
	
print(get_letter_links())
