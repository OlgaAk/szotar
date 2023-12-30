import requests
from bs4 import BeautifulSoup
import csv


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
	last_page_number = get_page_count_for_letter(letter, letter_url)
		
	all_words = []
	
	for i in range(0, int(last_page_number) + 1):
		words = get_list_of_words_for_letter_on_one_page(letter, letter_url, i, all_words)
	
	return all_words
	
	
	
def get_list_of_words_for_letter_on_one_page(letter, letter_url, page_number, all_words):
	
	page_url = letter_url if page_number == 0 else letter_url + "?page=" + str(page_number)
	
	response = requests.get(site_base_url + page_url)

	html = response.text
	soup = BeautifulSoup(html, 'html.parser')
	
	word_selector = "list-group-item list-group-item-action"
	
	word_html_elements = soup.find_all("a", word_selector)
	
	for element in word_html_elements:
		if not "[" in element.text:
			all_words.append(element.text)
	
	
def get_page_count_for_letter(letter, letter_url):
	response = requests.get(site_base_url + letter_url)

	html = response.text
	soup = BeautifulSoup(html, 'html.parser')
	
	pagination = soup.find("ul", "pagination")	
	last_pagination_element = pagination.find_all("a", "page-link")[-1]
	
	return last_pagination_element.text
	
	
def save_to_file(words, letter):	
	filename = letter + ".csv"
	with open(filename, 'w') as myfile:
		wr = csv.writer(myfile)
		for word in words:
			wr.writerow([word])
	

def main():
	links = get_letter_links()
	key = list(links.keys())[0]
	url = links[key]
	words = get_list_of_words_for_letter(key, url)
	print(len(words))
	
	save_to_file(words, key)
	
	
	
main()
