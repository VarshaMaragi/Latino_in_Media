from pyparsing import nestedExpr
from constants import *


def keep_category(category):
	for x in LA_ETHNICITIES:
		if x in category:
			if ((x == "latino" or x == "latina") and ("hispanic" in category)):
				continue
			return True, True, "latino"
	for x in LA_COUNTRIES:
		if x in category:
			return True, False, "latino"
	for x in NOTED_ETHNICITIES:
		if x in category:
			return True, False, "noted"
	for x in NON_LA_ETHNICITIES:
		if x in category:
			return True, False, "non_latino"
	for x in PLACE_WORDS + DESCENT_WORDS + ["latino", "latina", "hispanic"]:
		if x in category:
			return True, False, "other"
	return False, False, ""

def get_birthplace(raw_text):
	index = raw_text.find("birth_place")
	if index > -1:
		raw_bp = raw_text[index + len("birth_place"):].split("\n", 1)[0] 
		raw_bp = raw_bp.strip().strip('=').strip()
		bp = clean_text(raw_bp)
		return bp
	return ""

def clean_text(txt):
	brackets_l = {"{{", "[["}
	brackets_r = {"}}", "]]"}
	
	str_out = "" 
	x_outer = 0
	while x_outer < len(txt):
		if txt[x_outer] == '|':
			str_out = ""
			x_outer += 1
			continue 
		if txt[x_outer:x_outer+2] in brackets_l: 
			x_inner = x_outer + 2
			counter = 1
			bar_idx = -1
			while x_inner < len(txt):
				if counter == 0:
					break
				if txt[x_inner : x_inner + 2] in brackets_l:
					counter += 1
					x_inner = x_inner + 2
					continue
				if txt[x_inner : x_inner + 2] in brackets_r:
					counter -= 1
					x_inner = x_inner + 2
					continue
				x_inner += 1
			if counter != 0:
				print ("Error in parsing: mismatched brackets!")
				return ""
			if bar_idx > 0:
				str_out += clean_text(txt[bar_idx + 1 : x_inner - 2 ])
			else:
				str_out += clean_text(txt[x_outer + 2 :x_inner - 2])
			x_outer = x_inner
			continue
		str_out += txt[x_outer]
		x_outer += 1
	return str_out		

def take_out_angle_brackets(x):
	sentence_tmp = ""
	i = 0
	while i < len(x):
		if x[i] == '<':
			i += 1
			while True:
				if x[i] == '>':
					i += 1
					break
				i += 1
		else:
			sentence_tmp += x[i]
			i += 1
	return sentence_tmp

def keep_sentence(raw_sentence):
	for x in LA_ETHNICITIES:
		idx = raw_sentence.find(x)
		if idx > -1:
			if ((x == "latino" or x == "latina") and ("hispanic" in raw_sentence)):
				continue
			return idx, True, "latino"
	for x in LA_COUNTRIES:
		idx = raw_sentence.find(x)
		if idx > -1:
			return idx, False, "latino"
	for x in NOTED_ETHNICITIES:
		idx = raw_sentence.find(x)
		if idx > -1:
			return idx, False, "noted"
	for x in NON_LA_ETHNICITIES:
		idx = raw_sentence.find(x)
		if idx > -1:
			return idx, False, "non_latino"
	for x in PLACE_WORDS + DESCENT_WORDS + ["latino", "latina", "hispanic"]:
		idx = raw_sentence.find(x)
		if idx > -1:
			return idx, False, "other"
	return -1, False, ""
