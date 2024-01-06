import requests
from bs4 import BeautifulSoup, NavigableString, re
import json


site_base_url = "https://en.wiktionary.org/wiki/"

def get_word_definition(word):
	word_url = site_base_url + word

	response = requests.get(word_url)

	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	
	word_definition = {"word": word, "etymology": "", "translations": [], "inflection": {}}
	
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
			
			if content_element.name == "div":
				
				table = content_element.find("table", "inflection-table")
				
				if table:
				
					get_inflections(table, word_definition)
					
			if content_element.name == "table" and "inflection-table" in content_element["class"]:
				
				get_inflections(content_element, word_definition)

					
	
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



def get_inflections(table, word_definition):
	
	table_header = table.find("th").text.lower()
	
	if "inflection" in table_header:
		
		get_noun_forms(table, word_definition)
		
	elif "possessive" in table_header:
		
		get_noun_possessive_forms(table, word_definition)
		
	elif "conjugation" in table_header:
		
		get_verb_forms(table, word_definition)
		
		

def get_noun_forms(table, word_definition):
	
	inflections = {}

	start_row = 2
	
	inflection_positions = {
	"nominative": start_row, 
	"accusative": start_row +1, 
	"dative": start_row +2, 
	"instrumental": start_row +3, 
	"causal-final": start_row +4, 
	"translative": start_row +5, 
	"terminative": start_row +6,   
	"essive-formal": start_row +7,  
	"essive-modal": start_row +8, 
	"inessive": start_row +9,  
	"superessive": start_row +10,
	"adessive": start_row +11,  
	"illative": start_row +12,    
	"sublative": start_row +13,  
	"allative": start_row +14,  
	"elative": start_row +15, 
	"delative": start_row +16, 
	"ablative": start_row +17, 
	}
	
	rows = table.find_all("tr")
	
	for key in inflection_positions.keys():
		
		fill_noun_form(inflections, inflection_positions, rows, key)

	word_definition["inflection"] = inflections
	
	
	
	
def fill_noun_form(inflections, inflection_positions, rows, inflextion_type):
	
	position = inflection_positions[inflextion_type]
	
	columns = rows[position].find_all("td")
	
	print(position)
	
	print(len(columns))
	
	print(columns)
	
	inflections[inflextion_type] = {"singular": columns[0].text.strip(), "plural": columns[1].text.strip()}



def get_noun_possessive_forms(table, word_definition):
	pass
	
	
def get_verb_forms(table, word_definition):
	
	inflections = {
	"present": {"indef": {}, "def": {}}, 
	"past": {"indef": {}, "def": {}}, 
	"conditional": {"indef": {}, "def": {}},  
	"subjunctive": {"indef": {}, "def": {}}, 
	}
	
	inflection_positions = {
	"present": {"indef": 1, "def": 2}, 
	"past": {"indef": 4, "def": 5}, 
	"conditional": {"indef": 7, "def": 8},  
	"subjunctive": {"indef": 10, "def": 11}, 
	}
	
	rows = table.find_all("tr")
	
	for key in inflection_positions.keys():
		
		for form in inflection_positions[key].keys():
		
			fill_verb_form(inflections, inflection_positions, rows, key, form)

	word_definition["inflection"] = inflections
	

def fill_verb_form(inflections, inflection_positions, rows, mood, form):
	
	position = inflection_positions[mood][form]
	
	columns = rows[position].find_all("td")
	
	for i in range(6):	
		inflections[mood][form][i+1] = columns[i].text.strip().replace(u'\xa0or', u', ').replace(u' (or\xa0', u', ').replace(u')', u'')
		
		
			
	
def save_to_file(data, entity):	
	filename = entity + ".json"
	with open(filename, 'a+') as json_file:
	  json.dump(data, json_file, ensure_ascii=False)
	

def main():
	words_list = ["lány"]
	for word in words_list:
		definition = get_word_definition(word)
		print(definition)
		save_to_file(definition, "definitions")
	
	
	
main()
