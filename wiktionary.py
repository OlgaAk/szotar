import requests
from bs4 import BeautifulSoup, NavigableString
import csv


site_base_url = "https://en.wiktionary.org/wiki/"

def get_word_translation(word):
	word_url = site_base_url + word

	response = requests.get(word_url)

	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	
	etymology = soup.find(id="Etymology").parent.findNext("p").text
	
	translations_list = soup.find("strong", "Latn headword").parent.parent.findNext("ol")
	
	translations = []
	
	for translation_element in translations_list.children:
		if not isinstance(translation_element, NavigableString):
			for translation_sub_element in translation_element.children:
				one_translation = []
				if isinstance(translation_sub_element, NavigableString) and not translation_sub_element.strip() == "":
					print("string")
					print(translation_sub_element)
					one_translation.append(translation_sub_element)
				else:
					if translation_sub_element.name == "a":
						one_translation.append(translation_sub_element.text)
				translations.append(one_translation)
		
		
	
	# ~ print(etymology)
	print(translations)
	
	
	

	
	
def save_to_file(words, letter):	
	filename = letter + ".csv"
	with open(filename, 'w') as myfile:
		wr = csv.writer(myfile)
		for word in words:
			wr.writerow([word])
	

def main():
	get_word_translation("akár")
	
	
	
main()
