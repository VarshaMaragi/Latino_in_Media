#!/usr/bin/env python

# Import the imdb package.
import imdb
import csv
#import sys(character encoding)
import sys
import csv,codecs,cStringIO






# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb() # by default access the web.
in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()
# Search for a movie (get a list of Movie objects).
#s_result = ia.search_movie('Deadpool')
#p_result = ia.search_person('Cameron Diaz')
#c_result = ia.search_character('Latina')

def moviesbyactor(actor):
	print "actor id"
	print actor.getID()
	#print "Movies by actor"
	person=ia.get_person(actor.getID(),info=["filmography"])
	#print person
	if person:
		#print "inside if"
		if "actor" in person.keys(): 
			listcsv=person["actor"]
		#	print "Movies are"
		#	print listcsv
			if listcsv:
				f=open('Actor.csv', 'a')
				with f as myfile:
					writer = csv.writer(myfile, dialect = 'excel')
					for items in listcsv:
						print "Title of movie"
						print items['title']
						writer.writerow(items['title'].encode('utf-8'))
	print "--------end-------------"

def moviedetails(sresult):
	s_result = ia.search_movie(sresult)
	for item in s_result:
		print "-------------"
		print item['long imdb canonical title'], item.movieID
		print ia.get_movie(item.movieID)
		the_unt = item
		ia.update(the_unt)
		print item.keys()
		if 'cast' in item.keys():
			print "Cast"
			print item['cast']
		ia.update(item,'all')
		ia.update(item,'trivia')
		print item['trivia']



	#print the_unt['runtime']
	#print the_unt['rating']
	#director = the_unt['director']
	#print "director info"
	#print director
	print "---------------"

def persondetails(presult):
	p_result = ia.search_person(presult)
	listcsv=list()
	for item in p_result:
		listkeyvalue=dict()
		print "------------------------------"
		print "Actor"
		print item['long imdb canonical name'],item['name']
		ia.update(item)
		print item.keys()
		if 'mini biography' in item.keys():
			print "mini biography"
			print item['mini biography']
		if 'birth notes' in item.keys():
			listkeyvalue[item['canonical name'].encode('utf-8')]=item['birth notes'].encode('utf-8')
			#print type(item['birth notes'])
			print "birth notes"
			print item['birth notes']
		if listkeyvalue:
			listcsv.append(listkeyvalue)
		moviesbyactor(item)
		print "--------------------------------"

	f=open('xxx.csv', 'a')
	with f as myfile:
		writer = csv.writer(myfile, dialect = 'excel')
		for items in listcsv:
			for k,v in items.items():
				writer.writerow([k,v])
	

def characterdetails(cresult):
	c_result = ia.search_character(cresult)
	for item in c_result:
		print "---------------------------------"
		ia.update(item)
		print item.currentRole
		#print item['Person id']
		for i in item.keys():
			print item[i]
		outp = u'%s\t\t: %s : %s' % (item.characterID, ia.get_imdbID(item),
	                                item['long imdb name'])
		print outp.encode(out_encoding, 'replace')
		actor=ia.get_person(item.characterID)
		print actor['name']
		persondetails(actor['name'])
		print "---------------------------------"

	'''presults=ia.search_person(actor['name'].encode('utf-8'))
	#ia.update(presults)
	for j in presults:
		ia.update(j)
		print j.keys()
		#print j'''
		



# Print the long imdb canonical title and movieID of the results.
'''for item in s_result:
	print "-------------"
	print item['long imdb canonical title'], item.movieID
	print ia.get_movie(item.movieID)
	the_unt = item
	ia.update(the_unt)
	print item.keys()
	if 'cast' in item.keys():
		print "Cast"
		print item['cast']
		ia.update(item,'all')
		ia.update(item,'trivia')
		print item['trivia']



	#print the_unt['runtime']
	#print the_unt['rating']
	#director = the_unt['director']
	#print "director info"
	#print director
	print "---------------"'''

'''listcsv=list()
for item in p_result:
	listkeyvalue=dict()
	print "------------------------------"
	print "Actor"
	print item['long imdb canonical name'],item['name']
	ia.update(item)
	print item.keys()
	if 'mini biography' in item.keys():
		print item['mini biography']
	if 'birth notes' in item.keys():
		#key=listkeyvalue[item['canonical name']
		#fmt=u'{:<15}'*len(key)
		#print(fmt.format(*key.decode('utf-8')))
		listkeyvalue[item['canonical name'].encode('utf-8')]=item['birth notes'].encode('utf-8')
		print type(item['birth notes'])
		print item['birth notes']
	listcsv.append(listkeyvalue)
	
with open('xxx.csv', 'wb') as myfile:
	writer = csv.writer(myfile, dialect = 'excel')
	for items in listcsv:
		for k,v in items.items():
			writer.writerow([k,v])'''

'''with open('xxx.csv','rb') as fin, open('lll.csv','wb') as fout:
    reader = UnicodeReader(fin)
    writer = UnicodeWriter(fout,quoting=csv.QUOTE_ALL)
    for line in reader:
        writer.writerow(line)'''

def main():
	characterdetails('Latina')
	'''for item in c_result:
		print "---------------------------------"
		ia.update(item)
		print item.currentRole
	for i in item.keys():
		print item[i]
	outp = u'%s\t\t: %s : %s' % (item.characterID, ia.get_imdbID(item),
	                                item['long imdb name'])
	print outp.encode(out_encoding, 'replace')
	actor=ia.get_person(item.characterID)
	print actor['name']
	persondetails(actor['name'].encode('utf-8'))'''
	'''presults=ia.search_person(actor['name'].encode('utf-8'))
	#ia.update(presults)
	for j in presults:
		ia.update(j)
		print j.keys()
		#print j'''
	print "---------------------------------"

if __name__ == '__main__':
	try:
		main()
	except Exception,e:
		print(e)


'''search_results=ia.search_movie('Knuckle Draggers')
if search_results:
     movieID = search_results[0].movieID
     ia.update(search_results[0])
     for item in search_results:
     	print item
     print search_results[0]
     #print search_results[0]['celebs']['Born Today']
     movie = ia.get_movie(movieID)
     print "-------------------------"
     #print movie
     print "-------------------------"
     if movie:
         cast = movie.get('cast')
         print "Cast:"
         #dict(cast)
         print type(cast[0])
         topActors = 20
         for actor in cast[:topActors]:
         	#print "actor character"
         	#print actor['character']
         	print actor.keys()
         	print "{0} as {1}".format(actor['name'], actor.currentRole)'''
# Retrieves default information for the first result (a Movie object).
   
# Print some information.
   # get a list of Person objects.

# Get the first item listed as a "goof".
#ia.update(the_unt, 'goofs')
#print the_unt['goofs'][0]

# The first "trivia" for the first director.

#b_depalma = director[0]
#ia.update(b_depalma)
#print b_depalma['trivia'][0]