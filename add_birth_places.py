import pprint
import movieinfo as mi
import YearlyComedyCollection as imdb
import wikipedia_utils as wiki
#from YearlyComedyCollection import getmoviesbyyear
from unknown import getmoviesbyyear
import csv

def main():
	actors_without_bp  = getmoviesbyyear
	print(str(len(actors_without_bp[1]) + len(actors_without_bp[0])))
	add_birth_places(actors_without_bp[1], actors_without_bp[0], "")

def add_birth_places(actors_imdb, actors_without_imdb, filename):
	(missing_a, unsure_a, found_a) = wiki.get_pages(actors_imdb)
	actors_without_imdb = actors_without_imdb + unsure_a
	(missing_b, unsure_b, found_b) = wiki.get_pages(actors_without_imdb)
	missing = missing_a + missing_b
	unsure = unsure_a + unsure_b
	found = found_a + found_b
	actors_wiki = []
	for a in found:
		actors_wiki.append([a[0], a[2]])
	ids_bp = wiki.get_birthplace(actors_wiki)
	print (len(ids_bp))
	name_bp = {}
        for a in found:
		if a[2] in ids_bp:
			name_bp[a[0]] = ids_bp[a[2]]
	update_csv(name_bp)
	
def update_csv(name_bp):
	str_cast = ""
	with open('Comedy2017Cast.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			if len(row) >= 3 and row[0] in name_bp:
				row[2] = name_bp[row[0]]
			for i in range(len(row)-1):
				str_cast += row[i] + ';'
			str_cast += row[len(row)-1] + '\n'
    		csvfile.seek(0)
    		csvfile.write(str_cast)
    		csvfile.truncate()
	str_crew = ""
	with open('Comedy2017Crew.csv', 'r+') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in spamreader:
			if len(row) < 3:
				continue
			if row[0] in name_bp:
				row[2] = name_bp[row[0]]
			for i in range(len(row)-1):
				str_crew += row[i] + ';'
			str_crew += row[len(row)-1] + '\n'
    		csvfile.seek(0)
    		csvfile.write(str_crew)
    		csvfile.truncate()
			
        

if __name__ == '__main__':
      main()
