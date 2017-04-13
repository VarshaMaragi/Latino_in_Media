import re
from geopy.geocoders import Nominatim
from geotext import GeoText
from countries_constants import *
 
def get_born_us(bp):
	'''This function determines if person was born in the US. It returns -1,0,1, or 2.
	-1: unknown, 1: born in US, 2: born in latin country, 0: born in other country'''
	us_regex = re.compile(" us$|u\.s\.a\.|u\.s\.$|usa$|united states")
	if us_regex.findall(bp.lower()):
		return 1
	if la_regex.findall(bp.lower()):
		return 2
	if non_la_regex.findall(bp.lower()):
		return 0

	geo_out = get_country_GeoText(bp)
	if geo_out[0]:
		return 1
	if geo_out[1]:
		return 2
	if geo_out[2]:
		return 0
	
	geolocator = Nominatim()
	location = geolocator.geocode(bp)
	if location != None:
		if 'United States of America' in location.address:
			return 1
		geo_out = get_country_GeoText(location.address)
		if geo_out[0]:
			return 1
		if geo_out[1]:
			return 2
		if geo_out[2]:
			return 0
	return -1

def get_country_GeoText(text):
	d = GeoText(text).country_mentions
	out = [0,0,0]
	for i in d:
		if i == 'US':
			out[0] = 1
		if i in la_country_codes:
			out[1] = 1
		if i in non_la_country_codes:
			out[2] = 1
	return out

def get_is_american(text):
	if 'is an American' in text:
		return 1
	return 0
		
def get_from_us(labels):
	'''This function determines if person this person should be characterized as American. It returns a list of three numbers. Eavh place in the list represents a fact: from America; form a latin country; from neither. 1 means true, -1 means unknown.''' 
	out = [-1, -1, -1]
	for x in labels:
		for y in labels[x]:
			if us_states_regex.findall(y.lower()):
				out[0] = 1
			geo_out = get_country_GeoText(y)
			if geo_out[0]:
				out[0] = 1
			if geo_out[1]:
				out[1] = 1
			if geo_out[2]:
				out[2] = 1
			if la_regex.findall(y.lower()) or la_ethnicities_regex.findall(y):
				out[1] = 1
			if non_la_regex.findall(y.lower()) or ethnicities_regex.findall(y):
				out[2] = 1
			if 'American' in y:
				out[0] = 1
	return out
		
def get_sentence_data(sentences):
	'''This function determines where a person is colloquially "from". It returns a list of three numbers. Each place in the list represents a fact: from America; form a latin country; from neither. 1 means true, -1 means unknown.''' 
	#TODO: UNSURE BUT SHOULD BE LOOKED AT
	out = [-1, -1, -1]
	for x in sentences:
		if x == 'first_sent':
			if get_is_american(sentences[x][0]):
				out[0] = 1
		for y in sentences[x]:
			if ('Latina' in y or 'Latino' in y or la_ethnicities_regex.findall(y)):
				if (descent_regex.findall(y) or parents_regex.findall(y)):
					out[1] = 1
			if ethnicities_regex.findall(y):
				if (descent_regex.findall(y) or parents_regex.findall(y)):
					out[2] = 1
			if 'raised in' in y:
				if us_states_regex.findall(y.lower()):
					out[0] = 1
				geo_out = get_country_GeoText(y)
				if geo_out[0]:
					out[0] = 1
				if geo_out[1]:
					out[1] = 1
				if geo_out[2]:
					out[2] = 1
	return out
