import requests
from bs4 import BeautifulSoup


site_base_url = "https://www.arcanum.com"

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
	



def get_list_of_words_for_letter(letter, letter_url):
	response = requests.get(site_base_url + letter_url)

	html = response.text
	soup = BeautifulSoup(html, 'html.parser')
	
	word_selector = "list-group-item list-group-item-action"
	
	word_html_elements = soup.find_all("a", word_selector)
	
	words = []
	
	for element in word_html_elements:
		if not "[" in element.text:
			words.append(element.text)
	
	return words
	

def main():
	links = get_letter_links()
	key = list(links.keys())[0]
	url = links[key]
	print(key)
	print(get_list_of_words_for_letter(key, url))
	
	
	
main()
