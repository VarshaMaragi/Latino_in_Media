import pprint
import movieinfo as mi
import wikipedia_utils as wiki
from unknown import getmoviesbyyear
import csv
from geopy.geocoders import Nominatim
from geotext import GeoText
from countries_constants import *

def main():
	actors_without_bp  = getmoviesbyyear
	print(str(len(actors_without_bp[1]) + len(actors_without_bp[0])))
	latino_dict, actor_info = get_wiki_info(actors_without_bp[1], actors_without_bp[0], "actor_info.txt")
	update_csv(latino_dict, actor_info)

def get_wiki_info(actors_imdb, actors_without_imdb, filename):
	(missing_a, unsure_a, found_a) = wiki.get_pages(actors_imdb)
	actors_without_imdb = actors_without_imdb + unsure_a
	(missing_b, unsure_b, found_b) = wiki.get_pages_no_imdb(actors_without_imdb)
	missing = missing_a + missing_b
	unsure = unsure_a + unsure_b
	found = found_a + found_b
	actors_wiki = []
	wiki_labels = {}
	wiki_sentences = {}
	for a in found:
		actors_wiki.append([a[0], a[2]])
		wiki_labels[a[2]] = []
		wiki_sentences[a[2]] = []
	wiki_labels = wiki.get_categories(found)
	wiki_sentences = wiki.get_plain_text(found)
	
	actor_info = {}
	latino_dict = {}
	for a in found:
		labels = {}
		sentences = {}
		if a[2] in wiki_labels:
			labels = wiki_labels[a[2]]
		if a[2] in wiki_sentences:
			sentences = wiki_sentences[a[2]]
		actor_info[a[0]] = {
			'labels': labels,
			'sentences': sentences,
		}
		latino_dict[a[0]] = is_latino(labels, sentences, "")
	return (latino_dict, actor_info)
	
def print_actor(actor, labels, sentences, is_latino, filename):
	out_str = actor + '\n'
	if len(labels) != 0:
		out_str += '\t\tWiki Tags:' + '\n'
	for x in labels:
		out_str += '\t\t\t' + str(x) + '\n'
		for y in labels[x]:
			out_str += '\t\t\t\t' + str(y) + '\n'
	if len(sentences) != 0:
		out_str += '\t\tWiki info:' + '\n'		
	for x in sentences: 
		out_str += '\t\t\t' + str(x) + '\n'
		for y in sentences[x]:
			out_str += '\t\t\t\t' + str(y) + '\n'
	out_str += '\t Latino: ' + str(is_latino) + "\n\n"
	with open(filename, 'a') as f:
		f.write(out_str)

def is_latino(labels, sentences, birth_place):
	from_us = -1
	born_in_latino_country = -1
	
	# -1: unknown, 1: born in US, 2: born in la country, 0: born in other country
	def get_born_us(bp):
		l = len(bp)
		if l > 5 and bp[l-4:].lower() == ' us':
			return 1
		if l > 7 and bp[l-6:].lower() == ' u.s.':
			return 1
		if l > 5 and bp[l-4:].lower() == 'usa':
			return 1
		if l > 8 and bp[l-7:].lower() == 'u.s.a.':
			return 1
		if 'united states' in bp.lower():
			return 1
		if la_regex.findall(bp):
			return 2
		if non_la_regex.findall(bp):
			return 0
		
		geolocator = Nominatim()
		location = geolocator.geocode(bp)
		if 'United States of America' in location.display_name:
			return 1
		return -1
			
	def get_from_us(labels):
		for x in labels:
			for y in labels[x]:
				idx = y.find('from')
				if idx == -1:
					continue
				after = y[idx+4:]
				if us_states_regex.findall(after):
					return 1
				new_str = y[:idx+4] + after.title() 
				d = GeoText(new_str).country_mentions
				for i in d:
					if i[0] == 'US':
						return 1
					if i[0] in la_country_codes:
						return 2
					if i[0] in non_la_country_codes:
						return 0
		return -1
			
	
	birth_place = birth_place.strip()
	print (get_born_us(birth_place))
	print (get_from_us(labels))
	# born in US or tag is "from" blank which is place
	# tag of descent, has descent, a parent is of descent
	return False

def update_csv(latino_dict, actor_info_dict):
	str_cast = ""
	with open('Comedy2017Cast.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			if len(row) == 0:
				str_cast += '\n'
				continue
			if len(row) >= 3 and row[0] in latino_dict:
				row.append('Latino')
			for i in range(len(row)-1):
				str_cast += row[i] + ';'
			str_cast += row[len(row)-1] + '\n'
			if row[0] in actor_info_dict:
				filename = '2017_'
				if row[0] not in latino_dict:
					filename += 'not_'
				filename += 'latino.txt'
				print_actor(row[0], actor_info_dict[row[0]]['labels'], actor_info_dict[row[0]]['sentences'], False, filename)
		csvfile.seek(0)
		csvfile.write(str_cast)
		csvfile.truncate()
	str_crew = ""
	with open('Comedy2017Crew.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			if len(row) == 0:
				str_crew += '\n'
				continue
			if len(row) < 3 and row[0] in latino_dict:
				row.append('Latino')
			for i in range(len(row)-1):
				str_crew += row[i] + ';'
			str_crew += row[len(row)-1] + '\n'
		csvfile.seek(0)
		csvfile.write(str_crew)
		csvfile.truncate()


if __name__ == '__main__':
      main()
