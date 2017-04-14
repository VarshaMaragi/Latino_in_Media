import wikipedia_utils as wiki
from unknown import getmoviesbyyear
#from YearlyComedyCollection import getmoviesbyyear
import csv
from countries_constants import *
from past_actors import *
import ethnicity_utils as ethni

def main():
	actors_without_bp  = getmoviesbyyear#()
	print(str(len(actors_without_bp[1]) + len(actors_without_bp[0])))
	latino_dict, actor_info = get_wiki_info(actors_without_bp[1], actors_without_bp[0])
	update_csv(latino_dict, actor_info)

def get_bp_dict(actors_wiki, found):
	return wiki.get_birthplace(actors_wiki)

def get_wiki_info(actors_imdb, actors_without_imdb):
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


	#VERY TEMPORARY
	bp_dict.update(get_bp_dict(actors_wiki_without_bp, found))
	print (bp_dict)
	print (len(bp_dict))

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

def update_csv(latino_dict, actor_info_dict):
	str_cast = ""
	with open('Comedy2017Cast.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			print (row)
			latino = "Unknown"
			if len(row) == 1 and (row[0] == '0' or row[0] == '00'):
				continue
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
				filename = '2017_'
				if latino == 'Not Latino':
					filename += 'not_'
				if latino == 'Unknown':
					filename += 'unknown_'
				filename += 'latino.txt'
				print_actor(row[0], actor_info_dict[row[0]], latino, filename)
		csvfile.seek(0)
		print (str_cast)
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
				row.append(latino_dict[row[0]])
			for i in range(len(row)-1):
				str_crew += row[i] + ';'
			str_crew += row[len(row)-1] + '\n'
		csvfile.seek(0)
		csvfile.write(str_crew)
		csvfile.truncate()


if __name__ == '__main__':
      main()
