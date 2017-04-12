import re
from geopy.geocoders import Nominatim
from geotext import GeoText
from countries_constants import *
 
def get_born_us(bp):
	'''This function determines if person was born in the US. It returns -1,0,1, or 2.
	-1: unknown, 1: born in US, 2: born in latin country, 0: born in other country'''
	l = len(bp)
	#us_regex = 
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
	if location != None and 'United States of America' in location.address:
		return 1
	return -1
		
def get_from_us(labels):
	out = [-1, -1, -1]
	for x in labels:
		for y in labels[x]:
			idx = y.find('from')
			if idx != -1:
				after = y[idx+4:]
				if us_states_regex.findall(after):
					print ('contains state: ' + after)
					out[0] = 1
				new_str = y[:idx+4] + after.title() 
				d = GeoText(new_str).country_mentions
				for i in d:
					if i[0] == 'US':
						out[0] = 1
					if i[0] in la_country_codes:
						out[1] = 1
					if i[0] in non_la_country_codes:
						out[2] = 1
			if la_regex.findall(y) or la_ethnicities_regex.findall(y):
				out[1] = 1
			if non_la_regex.findall(y) or ethnicities_regex.findall(y):
				out[2] = 1
	return out
		
def get_sentence_data(sentences):
	return [-1,-1,-1]
