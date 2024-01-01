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
			print(translation_element.name)
			one_translation = {"value": "", "example": ""}
			for translation_sub_element in translation_element.children:
				if isinstance(translation_sub_element, NavigableString) and not translation_sub_element.strip() == "":
					print("string")
					print(translation_sub_element)
					if one_translation["value"] == "":
						one_translation["value"] = translation_sub_element.rstrip()
					else:
						one_translation["value"] = one_translation["value"] + " " + translation_sub_element.rstrip()

				else:
					if translation_sub_element.name == "a" and not translation_sub_element.text.strip() == "":
						if one_translation["value"] == "":
							one_translation["value"] =  translation_sub_element.text.rstrip()
						else:
							one_translation["value"] = one_translation["value"] + " " + translation_sub_element.text.rstrip()
					if translation_sub_element.name == "dl":
						one_translation["example"] = translation_sub_element.find("span", "h-usage-example").text
			translations.append(one_translation)
				
		
		
	
	print(etymology)
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
