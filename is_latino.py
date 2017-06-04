import wikipedia_utils as wiki
#from unknown import getmoviesbyyear
from YearlyComedyCollection import getmoviesbyyear
from SingleYearTVComedy import getTVdetailsby_year
from out2014 import l
#from output2015 import l_actor_info
#from output2015 import l_latino_dict
import csv
from countries_constants import *
from past_actors import *
import ethnicity_utils as ethni

YEAR = ""

def main():
	global YEAR
	'''	
	out  = getTVdetailsby_year('2015')
	print(out)
	'''
	YEAR = l[0]
	print (YEAR)
	actors_without_bp  = l[1] 
	is_movie = l[2]
	#actors_without_bp  = getmoviesbyyear
	latino_dict, actor_info = get_wiki_info(actors_without_bp[1], actors_without_bp[0])
	print(latino_dict)
	print(actor_info)
	#print(actor_info)
	#latino_dict = l_latino_dict
	#actor_info = l_actor_info
	if is_movie:
		update_csv_movie(latino_dict, actor_info)
	else:
		update_csv_tv(latino_dict, actor_info)

def get_bp_dict(actors_wiki, found):
	return wiki.get_birthplace(actors_wiki)

def get_wiki_info(actors_imdb, actors_without_imdb):
	imdb_bios = {}
	for a in actors_imdb:
		imdb_bios[a[1]] = a[3]#.encode('utf-8')
		a[2] = str(a[2])#.encode('utf-8')
	(missing_a, unsure_a, found_a) = wiki.get_pages(actors_imdb)
	actors_without_imdb = actors_without_imdb + unsure_a
	(missing_b, unsure_b, found_b) = wiki.get_pages_no_imdb(actors_without_imdb)
	missing = missing_a + missing_b
	unsure = unsure_a + unsure_b
	found = found_a + found_b
	actors_wiki = []
	actors_wiki_without_bp = []
	wiki_labels = {}
	wiki_sentences = {}
	bp_dict = {}
	for a in found:
		actors_wiki.append([a[0], a[2]])
		wiki_labels[a[2]] = []
		wiki_sentences[a[2]] = []
		if a[3] != None and a[3] != "" and a[3] != "None":
			bp_dict[a[2]] = a[3]
		else:
			actors_wiki_without_bp.append([a[0], a[2]])

	bp_dict.update(get_bp_dict(actors_wiki_without_bp, found))

	wiki_labels = wiki.get_categories(found)
	wiki_sentences = wiki.get_plain_text(found)
	
	actor_info = {}
	latino_dict = {}
	for a in found:
		labels = {}
		sentences = {}
		from_old_files = False
		bp = 'birthplace not found'
		if a[2] in wiki_labels:
			labels = wiki_labels[a[2]]
		if a[2] in wiki_sentences:
			sentences = wiki_sentences[a[2]]
		if a[1] in imdb_bios:
			sentences['IMDb Bio'] = [imdb_bios[a[1]]]
		if a[2] in bp_dict:
			bp = bp_dict[a[2]]
		if a[2] in past_actors_latino:
			from_old_files = True
			latino_dict[a[0]] = 'Latino'
		elif a[2] in past_actors_not_latino:
			from_old_files = True
			latino_dict[a[0]] = 'Not Latino'
		else:
			latino_dict[a[0]] = is_latino(labels, sentences, bp)	
		actor_info[a[0]] = {
			'labels': labels,
			'sentences': sentences,
			'birthplace': bp,
			'from_old_files': from_old_files
		}
	return (latino_dict, actor_info)
	
def print_actor(actor, info, is_latino, filename):
	labels = info['labels']
	sentences = info['sentences']
	bp = info['birthplace']
	from_old = info['from_old_files']
	out_str = actor + '\n'
	if from_old:
		out_str += '\t \t Catalogued in old file \n\n'
	else:
		if bp != 'birthplace not found':
			out_str += '\t\tBirthplace:' + bp + '\n'
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
		out_str += '\t Latino: ' + is_latino + "\n\n"
	with open(filename, 'a') as f:
		f.write(out_str)

def is_latino(labels, sentences, birth_place):
	from_us = -1
	born_in_latino_country = -1
	
	birth_place = birth_place.strip()
	born = ethni.get_born_us(birth_place)
	_from = ethni.get_from_us(labels)
	sentences = ethni.get_sentence_data(sentences)
	us = 0
	if born == 1 or _from[0] == 1 or sentences[0] == 1:
		us = 1
	la = 0
	if born == 2 or _from[1] == 1 or sentences[1] == 1:
		la = 1
	not_la = 0
	if born == 0 or _from[2] == 1 or sentences[2] == 1:
		not_la = 1

	if la*us > 0:
		return "Latino"
	if not_la:
		return "Not Latino"
	
	return 'Unknown'
	# tag of descent, has descent, a parent is of descent

def update_csv_movie(latino_dict, actor_info_dict):
	str_cast = ""
	with open('Comedy'+YEAR+'Cast.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			latino = "Unknown"
			if len(row) == 0:
				str_cast += '\n'
				continue
			if len(row) >= 3 and row[0] in latino_dict:
				row[5] = latino_dict[row[0]]
				row[2] = actor_info_dict[row[0]]['birthplace']
				latino = latino_dict[row[0]]
			for i in range(len(row)-1):
				str_cast += row[i] + ';'
			str_cast += row[len(row)-1] + '\n'
			if row[0] in actor_info_dict:
				filename = YEAR + '_cast_'
				if latino == 'Not Latino':
					filename += 'not_'
				if latino == 'Unknown':
					filename += 'unknown_'
				filename += 'latino.txt'
				print_actor(row[0], actor_info_dict[row[0]], latino, filename)
		csvfile.seek(0)
		csvfile.write(str_cast)
		csvfile.truncate()
	str_crew = ""
	with open('Comedy'+YEAR+'Crew.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			print (row)
			latino = "Unknown"
			if len(row) == 0:
				str_crew += '\n'
				continue
			if len(row) >= 3 and row[0] in latino_dict:
				row[5] = latino_dict[row[0]]
				row[2] = actor_info_dict[row[0]]['birthplace']
				latino = latino_dict[row[0]]
			for i in range(len(row)-1):
				str_crew += row[i] + ';'
			str_crew += row[len(row)-1] + '\n'
			if row[0] in actor_info_dict:
				print ('YES')
				filename = YEAR + '_crew_'
				if latino == 'Not Latino':
					filename += 'not_'
				if latino == 'Unknown':
					filename += 'unknown_'
				filename += 'latino.txt'
				print_actor(row[0], actor_info_dict[row[0]], latino, filename)
		csvfile.seek(0)
		csvfile.write(str_crew)
		csvfile.truncate()

def update_csv_tv(latino_dict, actor_info_dict):
	str_cast = ""
	with open(YEAR+'TVComedyCast.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			latino = "Unknown"
			if len(row) < 3:
				for i in range(len(row)):
					str_cast += row[i] + ';'
				str_cast += '\n'
				continue
			if len(row) >= 3 and row[1] in latino_dict:
				print("YEA")
				latino = latino_dict[row[1]]
				if latino == "Not Latino":
					row[2] = '0'
				elif latino == "Latino":
					row[2] = '1'	
				elif latino == "Unknown":
					row[2] = '-'
				else:
					print("ERROR: " + row[1] + latino)
			for i in range(len(row)-1):
				str_cast += row[i] + ';'
			str_cast += row[len(row)-1] + '\n'
			if row[1] in actor_info_dict:
				filename = YEAR + '_cast_'
				if latino == 'Not Latino':
					filename += 'not_'
				if latino == 'Unknown':
					filename += 'unknown_'
				filename += 'latino.txt'
				print_actor(row[1], actor_info_dict[row[1]], latino, filename)
		csvfile.seek(0)
		csvfile.write(str_cast)
		csvfile.truncate()
	str_crew = ""
	with open(YEAR+'TVComedyCrew.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			latino = "Unknown"
			if len(row) == 0:
				str_crew += '\n'
				continue
			if len(row) >= 43:
				row_line = row[0]+ ';'
				crew_line = [list(row[1:9]), list(row[9:17]), list(row[17:26]), list(row[26:35]), list(row[35:43])]
				for member in crew_line:
					print (member)
					if member[0] in latino_dict:
						latino = latino_dict[member[0]]
						if latino == "Not Latino":
							member[len(member) - 7] = '0'
						elif latino == "Latino":
							member[len(member) - 7] = '1'	
						elif latino == "Unknown":
							member[len(member) - 7] = '-'
						else:
							print("ERROR: " + member[1] + latino)
					if member[0] in actor_info_dict:
						print ('YES')
						filename = YEAR + '_crew_'
						if latino == 'Not Latino':
							filename += 'not_'
						if latino == 'Unknown':
							filename += 'unknown_'
						filename += 'latino.txt'
						print_actor(member[0], actor_info_dict[member[0]], latino, filename)
					for i in range(len(member)):
						row_line += member[i] + ';'
				str_crew += row_line[:len(row_line) - 1] + '\n'
			else:
				for i in range(len(row)-1):
					str_crew += row[i] + ';'
				str_crew += row[len(row)-1] + '\n'
		csvfile.seek(0)
		csvfile.write(str_crew)
		csvfile.truncate()

if __name__ == '__main__':
      main()
