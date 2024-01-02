import requests
from bs4 import BeautifulSoup, NavigableString, re
import json


site_base_url = "https://en.wiktionary.org/wiki/"

def get_word_definition(word):
	word_url = site_base_url + word

	response = requests.get(word_url)

	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	
	word_definition = {"etymology": "", "translations": [], "congugation": {}}
	
	content = soup.find("div", "mw-parser-output")
	
	is_hungarian_section = False;
		
	for content_element in content.children:
		
		if content_element.name == "h2":
			
			if is_hungarian_section:
				break

			if content_element.find(id="Hungarian"):
				
				is_hungarian_section = True
				
				continue
		
		if is_hungarian_section:
			 
			if content_element.name == "h3" and content_element.find_all(id=re.compile("^Etymology")):
	
				word_definition["etymology"] = content_element.find_all(id=re.compile("^Etymology"))[0].parent.findNext("p").text
				
			if content_element.name == "ol":
			
				get_translations(content_element, word_definition)
			
	
	return word_definition
	
	
	
	
def get_translations(translations_list, word_definition):
	
	for translation_element in translations_list.children:
		
		if not isinstance(translation_element, NavigableString):
			
			one_translation = {"value": "", "example": "", "synonym": ""}
			
			for translation_sub_element in translation_element.children:
				
				if isinstance(translation_sub_element, NavigableString) and not translation_sub_element.strip() == "":

					if one_translation["value"] == "":
						one_translation["value"] = translation_sub_element.rstrip()
					else:
						one_translation["value"] = one_translation["value"] + " " + translation_sub_element.rstrip()

				else:
					
					if (translation_sub_element.name == "a" or translation_sub_element.name == "span") and not translation_sub_element.text.strip() == "":
						
						if one_translation["value"] == "":
							one_translation["value"] =  translation_sub_element.text.rstrip()
						else:
							one_translation["value"] = one_translation["value"] + " " + translation_sub_element.text.rstrip()
							
					if translation_sub_element.name == "dl":
						
						if translation_sub_element.find("span", "h-usage-example"):
							one_translation["example"] = translation_sub_element.find("span", "h-usage-example").text
							
						if translation_sub_element.find("span", "nyms synonym"):
							text = translation_sub_element.find("span", "nyms synonym").text

							if text[:10] == "Synonyms: ":
								text = text[10:]
								
							if text[:9] == "Synonym: ":
								text = text[9:]
							one_translation["synonym"] = text
						
			if one_translation["value"]:			
				word_definition["translations"].append(one_translation)
	
	
def save_to_file(data, entity):	
	filename = entity + ".json"
	with open(filename, 'a+') as json_file:
	  json.dump(data, json_file, ensure_ascii=False)
	

def main():
	words_list = ["fog", "tesz"]
	for word in words_list:
		definition = get_word_definition(word)
		print(definition)
		save_to_file(definition, "definitions")
	
	
	
	
main()
