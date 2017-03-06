import pprint
import movieinfo

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
	movie = movieinfo.MovieInfo("tmp movie title")
	display_actors(movie.actors)

if __name__ == '__main__':
      main()
