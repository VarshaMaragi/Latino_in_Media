import urllib
import json
import re
import csv
import codecs
import sys
import time
import requests
from imp import reload
from imdb import IMDb
from imdb import utils as imdb_utils
from socket import error as SocketError
import errno

imdb = IMDb()


URL1="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte="
URL2="&timezone=America/New_York&with_genres=35&include_null_first_air_dates=true&with_original_language=en"

wikipedialistcrew=[[],[]]
wikipedialist=[[],[]]

class Actor(object):	
	def __init__(self, name, role, uncredited):
		self.name = name
		self.start = "0"
		self.end = "0"
		self.epi_num = ""
		if uncredited:
			self.role = role + ' (uncredited)'
		else:
			self.role = role 

class Crew(object):
	
	def __init__(self):
		self.creators = []
		self.directors = []
		self.writers = []
		self.producers = []
		self.exec_producers = []
		self.co_exec_producers = []
		self.misc = []

	def add_crew_member(self, name, role, epi_info):
		if role == "Director":
			self.directors.append([name, role, epi_info])
		if role == "Creator":
			self.creators.append([name, role, epi_info])
			self.writers.append([name+"(creator)", role, epi_info])
		elif role == "Writer":
			self.writers.append([name, role, epi_info])
		elif role == "Executive Producer" or role == "Co-Executive Producer":
			self.exec_producers.append([name, role, epi_info])
		elif "roducer" in role:
			self.producers.append([name, role, epi_info])
		else:
			self.misc.append([name, role, epi_info])

def getTVdetailsby_year(year):
	global wikipedialistcrew, wikipedialist
	print(year)
	start = time.time()
	cast_file=open(str(year) + "TVComedyCast.csv",'a')
	crew_file=open(str(year) + "TVComedyCrew.csv",'a')
	cast_file.write(str(year) + '\n')
	crew_file.write(str(year) + '\n')
	url= URL1 + year + "-01-01&air_date.lte="+ year + "-12-31&page=1" + URL2
	open_url(url,"TVyear2016.json");
	#skip = True
	with open('TVyear2016.json') as data_file:
		data = json.load(data_file)
	total_num = data["total_results"]
	cast_file.write(";Total Comedies: " + str(total_num) + '\n\n')
	crew_file.write(";Total Comedies: " + str(total_num) + '\n\n')
	write_headers(cast_file, crew_file)
	
	for i in range(1, data["total_pages"]+1):
		print("TIME: " + str(time.time() - start))
		#print(wikipedialist)
		#print(wikipedialistcrew)
		#print('\n')
		url_2 = URL1 + year + "-01-01&air_date.lte="+ year + "-12-31&page=" + str(i) + URL2
		time.sleep(1)
		open_url(url_2,"Tvyear2016.json");

		with open('Tvyear2016.json') as data_file2:
			data2 = json.load(data_file2)
		for i in data2["results"]:
			show_name = i.get("original_name").encode('utf-8')
			'''if show_name == "Boomers":
				skip = False
			if skip:
				continue'''
				
			genres = i.get("genre_ids")
			_id = str(i.get("id"))
			if (show_name == "Saturday Night Live"):
				continue
			strs=""
			keep_tv = True
			bad_genres = [10767, 10770, 10763]
			for x in genres:
				if x in bad_genres:
					keep_tv = False
					break
			if not (keep_tv):
				print("Not keeping: " + show_name)
				continue
			print(show_name+ " " + _id)

			season_num, creators = get_season_number(_id,year)
			if season_num == "":
				print ("\tNO SEAS NUM:" + show_name)
				continue

			print("\tSeason: " + str(season_num))
			time.sleep(1)
			url2="https://api.themoviedb.org/3/tv/"+_id+"/season/"+str(season_num)+"?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
			open_url(url2,"./cast2017.json");
			with open('cast2017.json') as data_file2:
				datac = json.load(data_file2)
			cast = {}
			crew =  {}
			for x in creators:
				crew[x + ";Creator"] = [1, int(year), int(year) + 1]
			imdbid = get_imdbid(_id)
			print("\tIMDB: " + imdbid)
			if imdbid == "":
				print("BAD ID")
				continue
			producer_dict = get_producer_dict(_id, season_num)
			cast, crew, distributor = update_with_imdb(imdbid, show_name, season_num, crew, producer_dict)
			if cast == -1 and crew == -1:
				continue
			
			cast_file.write(show_name+'\n')
			crew_file.write(show_name+'\n')
			if distributor != "":
				cast_file.write("Online Show: " + distributor+'\n')
				crew_file.write("Online Show: " + distributor+'\n')
		

			sorted_actors = [cast[k] for k in cast]
			def get_epi_num(x):
				if len(x) < 2:
					return 0
				if x[1] == None or x[1] == "":
					return 0
				return x[1]
			sorted_actors = sorted(sorted_actors, key=get_epi_num, reverse=True) 
			for info in sorted_actors:
				a = info[0]
				a.epi_num = info[1]
				a.start = str(info[2])
				a.end = str(info[3])
				write_actor(cast_file, a)
			sorted_crew = [[k.split(";")[0], k.split(";")[1], crew[k]] for k in crew]
			def get_epi_num_crew(x):
				if x[2][0] == None or x[2][0] == "":
					return 0
				return x[2][0]
			sorted_crew = sorted(sorted_crew, key=get_epi_num_crew, reverse=True) 
			crew_obj = Crew()
			for info in sorted_crew:
				name = info[0]
				role = info[1]
				epi_info = info[2]
				crew_obj.add_crew_member(name, role, epi_info)
			write_crew(crew_file, crew_obj)
			cast_file.write("\n")
			crew_file.write("\n")



		cast_file.close()
		crew_file.close()
		print(str(time.time() - start))
		return (str(year), [wikipedialist[0] + wikipedialistcrew[0], wikipedialist[1] + wikipedialistcrew[1]], False)

def get_imdbid(_id):
	imdbid = ""
	time.sleep(1)
	url = "https://api.themoviedb.org/3/tv/"+_id+"/external_ids?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
	open_url(url,"./show.json");
	with open('show.json') as data_file2:
		datac = json.load(data_file2)
		if "imdb_id" in datac:
			if datac["imdb_id"] != None and len(datac["imdb_id"]) > 2:
				return datac["imdb_id"][2:]
	return imdbid

def get_producer_dict(_id, season_number):
	prod_dict = {}
	url3 = "https://api.themoviedb.org/3/tv/"+_id+"/season/"+str(season_number)+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
	open_url(url3,"./credits2017.json");
	with open('credits2017.json') as data_file2:
		datac = json.load(data_file2)
		if "crew" in datac.keys():
			for j in datac["crew"]:
				job = j.get("job").encode('utf-8')
				name = j.get("name").encode('utf-8')
				if "roducer" in job:
					prod_dict[name] = job
	return prod_dict

def update_with_imdb(_id, _title, season_num, _crew, producer_dict):
	global wikipedialistcrew, wikipedialist
	cast = {}
	crew = _crew
	m = imdb.get_movie(_id)
	title = m['title'].encode('utf-8')
	if str(title) != _title:
		print('\tIncorrect IMDBid ' + str(title)) 
				
	if 'genres' in m.keys():	
		keep_tv = True
		comedy_show = False
		genres_names = m["genres"]
		bad_genres = ["Game-Show", "Animation","Reality-TV"]
		for x in genres_names:
			if x.encode('utf-8') in bad_genres:
				keep_tv = False
			if "Comedy" in x.encode('utf-8'):
				comedy_show = True
		if not (keep_tv) or not comedy_show:
			print("\tNot keeping: " + _id)
			return -1, -1, ""
	
	is_online_show = ""
	online_distros = ['Netflix', 'Hulu', 'Amazon']
	if 'distributors' in m.keys():
		for x in m['distributors']:
			for y in online_distros:
				if y in x['name'].encode('utf-8'):
					is_online_show +=  x['name'].encode('utf-8') + ' '
	
	imdb.update(m, 'episodes')
	if 'episodes' not in m.keys():
		print("\tNONEPI: " + str(m.keys()))
		return -1, -1, is_online_show
	
	if season_num not in m['episodes']:
		print("\tNONSEAS: " + str(season_num))
		return -1, -1, ""
	season = m['episodes'][season_num]
	for episode_num in season:
		e = season[episode_num]
		imdb.update(e)
		imdb.update(e, 'full credits')
		air_date = []
		if 'original air date' in e.keys():
			air_date = e['original air date'].encode('utf-8').split(" ")
		if len(air_date) > 0:
			air_date = int(air_date[-1])
		else:
			air_date = 0
		
		if 'producer' in e.keys():
			for k in e['producer']:
				role = 'Producer'
				name = k['name'].encode('utf-8')
				if name in producer_dict:
					role = producer_dict[name].encode('utf-8')
				p_key = name + ';' + role
				if p_key in crew:
					crew[p_key][0] = crew[p_key][0] + 1
					if air_date > crew[p_key][2]:
						crew[p_key][2] = air_date
				else:
					crew[p_key] = [1, air_date, air_date]
					imdb.update(k)
					imdb_id = k.personID
					bio = ""
					notes = ""
					if 'biography' in k.keys():
						bio = k['biography']
					if 'birth notes' in k.keys():
						notes = k['birth notes']
					wikipedialistcrew[1].append([name,imdb_id,notes,bio])
		
		if 'writer' in e.keys():
			for k in e['writer']:
				role = 'Writer'
				name = k['name'].encode('utf-8')
				p_key = name + ';' + role
				if p_key in crew:
					crew[p_key][0] = crew[p_key][0] + 1
					if air_date > crew[p_key][2]:
						crew[p_key][2] = air_date
				else:
					crew[p_key] = [1, air_date, air_date]
					imdb.update(k)
					imdb_id = k.personID
					bio = ""
					notes = ""
					if 'biography' in k.keys():
						bio = k['biography']
					if 'birth notes' in k.keys():
						notes = k['birth notes']
					wikipedialistcrew[1].append([name,imdb_id,notes,bio])
		
		if 'director' in e.keys():
			for k in e['director']:
				role = 'Director'
				name = k['name'].encode('utf-8')
				p_key = name + ';' + role
				if p_key in crew:
					crew[p_key][0] = crew[p_key][0] + 1
					if air_date > crew[p_key][2]:
						crew[p_key][2] = air_date
				else:
					crew[p_key] = [1, air_date, air_date]
					imdb.update(k)
					imdb_id = k.personID
					bio = ""
					notes = ""
					if 'biography' in k.keys():
						bio = k['biography']
					if 'birth notes' in k.keys():
						notes = k['birth notes']
					wikipedialistcrew[1].append([name,imdb_id,notes,bio])
				

		if 'cast' not in e.keys():
			print("\tNo Cast: " + str(episode_num) + " " + str(season_num))
			continue
		for p in e['cast']:
			name = ""
			if 'name' in p.keys():
				name = p['name'].encode('utf-8')
			else:
				print("\t\t no name: " + str(p))
				print('\t\t' + str(p.keys()))
				continue
			role = ""
			if type(p.currentRole) == imdb_utils.RolesList:
				for x in p.currentRole:
					role += x['name'].encode('utf-8') + '/'
				role = role[:len(role)-1]
			elif 'name'  in p.currentRole.keys():
				role = p.currentRole['name'].encode('utf-8')
			k = str(name + ';' + role)
			if k in cast:
				cast[k][1] = cast[k][1] + 1
				if air_date > cast[k][3]:
					cast[k][3] = air_date
			else:
				uncredited = False
				if 'uncredit' in p.notes.encode('utf-8'):
					uncredited = True
				a = Actor(name, role, uncredited)
				cast[k] = [a, 1, air_date, air_date]
				imdb.update(p)
				imdb_id = p.personID
				bio = ""
				notes = ""
				if 'biography' in p.keys():
					bio = p['biography']
				if 'birth notes' in p.keys():
					notes = p['birth notes']
				wikipedialist[1].append([name,imdb_id,notes,bio])

	return cast, crew, is_online_show

def get_season_number(_id, _year):
	creators = []
	url = "https://api.themoviedb.org/3/tv/"+_id+"?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
	open_url(url,"./show.json");
	with open('show.json') as data_file2:
		datac = json.load(data_file2)
		if "created_by" in datac.keys():
			for x in datac["created_by"]:
				creators.append(x["name"].encode('utf-8'))
		if "seasons" in datac.keys():
			for s in datac["seasons"]:
				if int(s["season_number"]) == 0:
					print('\t Skipping season 0')
					continue
				air_date = s["air_date"]
				if air_date == None:
					continue
				else:
					air_date = s["air_date"].encode('utf-8')
				year = air_date.split('-')[0]
				if str(int(_year)) == year:
					print (str(s["season_number"]) + str(creators))
					return s["season_number"], creators
	return "", creators

def open_url(url, file_name):
	try:
		urllib.urlretrieve(url,file_name);
	except SocketError as e:
    		if e.errno != errno.ECONNRESET:
        		raise # Not error we are looking for
		else:
			print("reset")
    		pass # Handle error here.
	except:
		print("ERROR: " + url)
		return 0
	return 1

def get_imdb_and_bp(_id):
	imdb = ""
	bp = "None"
	time.sleep(1)
	url_1="https://api.themoviedb.org/3/person/"+str(_id)
	url_2 = "?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
	urlimdb= url_1 +"/external_ids" + url_2
	r = open_url(urlimdb,"./actorimdb.json")
	if not r:
		return imdb, bp
	with open('actorimdb.json') as data_fileimdb:
		temp=json.load(data_fileimdb)
		if "imdb_id" in temp.keys():
			imdb=str(temp["imdb_id"])[2:]
	urlimdb= url_1 + url_2
	open_url(urlimdb,"./actorimdb.json")
	with open('actorimdb.json') as data_fileimdb:
		temp=json.load(data_fileimdb)
		if "place_of_birth" in temp.keys():
			bp=(temp["place_of_birth"])
	return imdb, bp					

def write_actor(f, actor):
	s=""
	s=';'+str(actor.name)+";;;;;;"+str(actor.name)+';'+str(actor.role)+';'+str(actor.epi_num)+';'+str(actor.start)+'-'+str(actor.end)+';;;;;;;;;'+str(actor.name)+';'+str(actor.role)+';'
	f.write(s)
	f.write("\n")

def write_crew(f, crew):
	max_len = max(max(len(crew.misc), len(crew.creators)), max(max(len(crew.producers), max(len(crew.writers),len(crew.directors))), max(len(crew.exec_producers), len(crew.co_exec_producers))))
	l = [["","",["","",""]]]*max_len
	crew_lists = [list(l), list(l), list(l), list(l), list(l), list(l)] 
	k = [crew.creators, crew.directors, crew.producers, crew.exec_producers, crew.writers, crew.misc]
	for j in range(len(k)):
		for i in range(len(k[j])):
			crew_lists[j][i] = k[j][i]
	for i in range(max_len):
		'''print(str(i))
		print(crew_lists[0][i][0])
		print(str(crew_lists[0][i][2][0]))
		print(str(crew_lists[0][i][2][1]))
		print(str(crew_lists[0][i][2][2]))
		print('\t 1')
		print(crew_lists[1][i][0])
		print(str(crew_lists[1][i][2][0]))
		print(str(crew_lists[1][i][2][1]))
		print(str(crew_lists[1][i][2][2]))
		print('\t 2')
		print(crew_lists[2][i][0])
		print(str(crew_lists[2][i][1]))
		print(str(crew_lists[2][i][2][0]))
		print(str(crew_lists[2][i][2][1]))
		print(str(crew_lists[2][i][2][2]))
		print('\t 3')
		print(crew_lists[3][i][0])
		print(str(crew_lists[3][i][1]))
		print(str(crew_lists[3][i][2][0]))
		print(str(crew_lists[3][i][2][1]))
		print(str(crew_lists[3][i][2][2]))
		print('\t 4')
		print(crew_lists[4][i][0])
		print(str(crew_lists[4][i][2][0]))
		print(str(crew_lists[4][i][2][1]))
		print(str(crew_lists[4][i][2][2]))
		print('\t 5')
		print(crew_lists[5][i][0])
		print(str(crew_lists[5][i][1]))
		print(str(crew_lists[5][i][2][0]))
		print(str(crew_lists[5][i][2][1]))
		print(str(crew_lists[5][i][2][2]))
		print('\n')'''

		s = ";" + crew_lists[0][i][0] + ";;;;;"+str(crew_lists[0][i][2][0])+";"+str(crew_lists[0][i][2][1])+'-'+str(crew_lists[0][i][2][2])+";;" 
		s += crew_lists[1][i][0] + ";;;;;"+str(crew_lists[1][i][2][0])+";"+str(crew_lists[1][i][2][1])+'-'+str(crew_lists[1][i][2][2])+";;"
		s += crew_lists[2][i][0] + ";" + str(crew_lists[2][i][1]) + ";;;;;"+str(crew_lists[2][i][2][0])+";"+str(crew_lists[2][i][2][1])+'-'+str(crew_lists[2][i][2][2])+";;"
		s += crew_lists[3][i][0] + ";" + str(crew_lists[3][i][1]) + ";;;;;"+str(crew_lists[3][i][2][0])+";"+str(crew_lists[3][i][2][1])+'-'+str(crew_lists[3][i][2][2])+";;"
		s += crew_lists[4][i][0] + ";;;;;"+str(crew_lists[4][i][2][0])+";"+str(crew_lists[4][i][2][1])+'-'+str(crew_lists[4][i][2][2])+";;"  
		s += crew_lists[5][i][0] + ";" + str(crew_lists[5][i][1]) + ";;;;;"+str(crew_lists[5][i][2][0])+";"+str(crew_lists[5][i][2][1])+'-'+str(crew_lists[5][i][2][2])+";;"  
		f.write(s + '\n')
			

def write_headers(cast, crew):
	lic_sect = "Shows;Actor;Latino? Y=1;Latina Female? Y=1; Afro-Latino? Y=1; Latin American Actor/Actress? Y=1;;"
	lr_sect = "Actor; Role; # of Episodes; Year; Notes; Is this Lead Role? Y=1; Latino in Lead Role? Y=1; Is this a Supporting Role? Y=1; Is this an Unnamed Role? Y=1; Is this an Uncredited Role? Y=1; Latino in Uncredited Role? Y=1;;"
	lsr_sect = "Actor; Role; Is This a Stereotypical Role? Y=1; Criminal; Law Enforcement; Comic Relief; Blue Collar; Other Stereotype; Notes;\n"
	cast.write(lic_sect + lr_sect + lsr_sect)

	classifications = "Latino? Y=1;Latina Female? Y=1; Afro-Latino? Y=1; Latin American? Y=1; # of Episodes; Years;;"
	jobs = ["TITLE; Creators;", "Directors;", "Producers;Type of Producer Contains ALL;", "Executive Producers; Type of Exec. Producer;", "Writers(And Creators!);","Others; Role;"]#"Writers (And Creators!)"]
	for j in jobs:
		crew.write(j + classifications)
	crew.write('\n')

def main():
	print(getTVdetailsby_year('2014'))
	#print(get_imdb_and_bp('5374'))

if __name__ == '__main__':
	main()
