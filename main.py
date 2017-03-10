import pprint
import movieinfo as mi
import YearlyComedyCollection as imdb

movie_enumerator = "//Movie title//"

def display_actors(actors):
	for actor in actors:
		print '\t' + actor.name
		print '\t\tBirthplace:\t' + actor.birthplace
		print '\t\tLatino:\t' + str(actor.la_ethnicity)
		if len(actor.tags) != 0:
			print '\t\tWiki Tags:' 
		for x, content in actor.tags.iteritems():
			print '\t\t\t' + x
			for y in content:
				print '\t\t\t\t' + y
		if len(actor.self_info) != 0:
			print '\t\tWiki info:'		
		for x, content in actor.self_info.iteritems():
			print '\t\t\t' + x		
			for y in content:
				print '\t\t\t\t' + y
		print "\n"

def main():
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
				movie_title = True
				movie_list.append([movie_key, actors])
				file_obj = movie.get_file_obj() 
				continue
			m = line.split(',')
			(name, imdb_id, role, birthplace, pic) = parse_line(m)
			actors.append(mi.Actor(name, imdb_id, role, birthplace, pic))
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
