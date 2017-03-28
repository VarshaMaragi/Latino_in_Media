import pprint
import movieinfo as mi
import YearlyComedyCollection as imdb
import wikipedia_utils as wiki

movie_enumerator = "//Movie title//"

def display_actors(actors):
	for actor in actors:
		print '\t' + actor.name
		print '\t\tBirthplace:\t' + actor.birthplace
		if len(actor.wiki_info.tags) != 0:
			print '\t\tWiki Tags:' 
		for x, content in actor.wiki_info.tags.iteritems():
			print '\t\t\t' + x
			for y in content:
				print '\t\t\t\t' + y
		if len(actor.wiki_info.self_info) != 0:
			print '\t\tWiki info:'		
		for x, content in actor.wiki_info.self_info.iteritems():
			print '\t\t\t' + x		
			for y in content:
				print '\t\t\t\t' + y
		print "\n"

def main():
	actors_imdb  = [["Vincent Van Gogh", ""], ["Ashton Kutcher", "0005110"], ["Mila Kunis", "0005109"], ["Justin Timberlake", "0005493"]]
	missing, unsure, found = wiki.get_pages(actors_imdb)
	# name, imdb_id, wiki_id
	actors = unsure + found
	actors_wiki = []
	for a in actors:
		actors_wiki.append([a[0], a[2]])
	print wiki.get_birthplace(actors_wiki)
	print '\n'
	print wiki.get_categories(actors_wiki)
	print '\n'
	print wiki.get_plain_text(actors_wiki)



def make_xml():
	#imdb.getmoviesbyyear()
	movie_list = []
	movie_title = True
	movie_key = ""
	with open("Comedy2017Cast.csv") as f:
		file_obj = 0
		for line in f.read().splitlines():
			line = line.strip(',')
			if line == "" or line == "Crew" or line == "Cast":
				continue
			if movie_title:
				movie_key = line.split(',')[0]
				actors = []
				movie_title = False
				continue
			if line == movie_enumerator:
				movie = mi.MovieInfo(movie_key, actors)
				movie_list.append([movie_key, actors])
				file_obj = movie.get_file_obj() 
				movie_title = True
				continue
			m = line.split(',')
			(name, imdb_id, role, birthplace, pic) = parse_line(m)
			actors.append(mi.Actor(name, imdb_id, role, 0, 0, 0, birthplace, pic))
		mi.write_to_file(file_obj, movie_list)

def parse_line(word_list):
	l = []
	i = 0
	while i < 4 and i < len(word_list):
		l.append(word_list[i])
		i += 1
	while i < 4:
		l.append("")
		i += 1	
	return l[0], 0, l[1], l[2], l[3]	

if __name__ == '__main__':
      main()
