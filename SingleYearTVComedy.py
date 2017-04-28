import urllib
import json
import re
import csv
import codecs
import sys
import time
import requests
from imp import reload
import urllib.request

URL1="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte="
URL2="&timezone=America/New_York&with_genres=35&include_null_first_air_dates=true&with_original_language=en"

class Actor(object):	
	def __init__(self, name, role):
		#self.latino = False
		self.role = role
		self.name = name
		self.start = "0"
		self.end = "0"
		self.epi_num = ""
		#num_epi = ""
		#years = ""
		

class Crew(object):
	
	def __init__(self):
		self.creators = []
		self.directors = []
		self.producers = []
		self.exec_producers = []
		self.co_exec_producers = []
		self.misc = []

	def add_crew_member(self, name, role, epi_info):
		if role == "Director":
			self.directors.append([name, role, epi_info])
		elif role == "Writer":
			self.creators.append([name, role, epi_info])
		elif role == "Executive Producer" or role == "Co-Executive Producer":
			self.exec_producers.append([name, role, epi_info])
		elif "roducer" in role:
			self.producers.append([name, role, epi_info])
		else:
			self.misc.append([name, role, epi_info])

def getTVdetailsby_year(year):
	cast_file=open(str(year) + "TVComedyCast.csv",'a')
	crew_file=open(str(year) + "TVComedyCrew.csv",'a')
	cast_file.write(str(year) + '\n')
	crew_file.write(str(year) + '\n')
	url= URL1 + year + "-01-01&air_date.lte="+ year + "-12-31&page=1" + URL2
	urllib.request.urlretrieve (url,"TVyear2016.json");
	with open('TVyear2016.json') as data_file:
		data = json.load(data_file)
		total_num = data["total_results"]
		cast_file.write(";Total Comedies: " + str(total_num) + '\n\n')
		crew_file.write(";Total Comedies: " + str(total_num) + '\n\n')
		write_headers(cast_file, crew_file)
		
		end = 3 if (data["total_pages"]+1 > 3) else data["total_pages"]+1
		for i in range(1, end):
			url_2 = URL1 + year + "-01-01&air_date.lte="+ year + "-12-31&page=" + str(i) + URL2
			time.sleep(3)
			urllib.request.urlretrieve (url_2,"Tvyear2016.json");

			with open('Tvyear2016.json') as data_file2:
					
				data2 = json.load(data_file2)

				for i in data2["results"]:
					strs=""
					genres = i.get("genre_ids")
					keep_tv = True
					for x in genres:
						if (x  == 10767):
							print("Late Night: " + i.get("original_name"))
							keep_tv = False
							break
						if (x  == 10770):
							print("TV Movie: " + i.get("original_name"))
							keep_tv = False
							break
					if not (keep_tv):
						continue
					cast_file.write(str(i.get("original_name"))+'\n')
					crew_file.write(str(i.get("original_name"))+'\n')

					time.sleep(3)
					url2="https://api.themoviedb.org/3/tv/"+str(i.get("id"))+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
					urllib.request.urlretrieve (url2,"./cast2017.json");
					with open('cast2017.json') as data_file2:
						datac = json.load(data_file2)
						actors = {}
						crew =  {}
						if "cast" in datac.keys():
							for j in datac["cast"]:
								a = Actor(str(j.get("name")), str(j.get("character")))
								actors[str(j.get("character"))] = [a, 0, 6000, -1]
						if "crew" in datac.keys():
							for j in datac["crew"]:
								crew[str(j.get("name")) + ";" + str(j.get("job"))] = [0, 6000, -1]
						actors, crew = get_episode_counts(i.get("id"), actors, crew)
						sorted_actors = [actors[k] for k in actors]
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
							a.start = info[2]
							a.end = info[3]
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

def get_episode_counts(_id, cast, crew):
	episode_list = get_episodes_dict(_id)
	for x in episode_list:
		seas_num = x[0]
		epi_num_list = x[1]
		air_date = x[2]
		for epi_num in range(1, epi_num_list):
			time.sleep(3)
			url = "https://api.themoviedb.org/3/tv/" + str(_id) + "/season/" + str(seas_num) + "/episode/" + str(epi_num) + "/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c"
			print(url)
			urllib.request.urlretrieve (url,"./episode.json");
			with open('episode.json') as data_file2:
				datac = json.load(data_file2)
				if "cast" in datac.keys():
					for j in datac["cast"]:
						if str(j.get("character")) in cast:
							cast[str(j.get("character"))][1] = cast[str(j.get("character"))][1] + 1
							if air_date < cast[str(j.get("character"))][2]:
								cast[str(j.get("character"))][2] = air_date
							if air_date > cast[str(j.get("character"))][3]:
								cast[str(j.get("character"))][3] = air_date
						else:
							a = Actor(str(j.get("name")), str(j.get("character")))
							cast[str(j.get("character"))] = [a, 1, air_date, air_date]
				if "guest_stars" in datac.keys():
					for j in datac["guest_stars"]:
						if str(j.get("character")) in cast:
							cast[str(j.get("character"))][1] = cast[str(j.get("character"))][1] + 1
							if air_date < cast[str(j.get("character"))][2]:
								cast[str(j.get("character"))][2] = air_date
							if air_date > cast[str(j.get("character"))][3]:
								cast[str(j.get("character"))][3] = air_date
						else:
							a = Actor(str(j.get("name")), str(j.get("character")))
							cast[str(j.get("character"))] = [a, 1, air_date, air_date]
				if "crew" in datac.keys():
					for j in datac["crew"]:
						if str(str(j.get("name")) + ";" + str(j.get("job"))) in crew:
							crew[str(j.get("name")) + ";" + str(j.get("job"))][0] =  crew[str(j.get("name")) + ";" + str(j.get("job"))][0] + 1
							if air_date < crew[str(j.get("name")) + ";" + str(j.get("job"))][1]:
								crew[str(j.get("name")) + ";" + str(j.get("job"))][1] = air_date
							if air_date > crew[str(j.get("name")) + ";" + str(j.get("job"))][2]:
								crew[str(j.get("name")) + ";" + str(j.get("job"))][2] = air_date
						else:
							crew[str(j.get("name")) + ";" + str(j.get("job"))] = [1, air_date, air_date]
	return cast, crew					

def get_episodes_dict(_id):
	seasons = []
	time.sleep(3)
	url = "https://api.themoviedb.org/3/tv/" + str(_id) + "?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
	urllib.request.urlretrieve (url,"./episode.json");
	with open('episode.json') as data_file2:
		datac = json.load(data_file2)
		if "seasons" in datac.keys():
			print(datac["seasons"])
			for j in datac["seasons"]:
				air_date = -1
				if j.get("air_date") != None:
					air_date = int(j.get("air_date")[:4])
				seasons.append([int(j.get("season_number")), int(j.get("episode_count")), air_date])
	return seasons
	

def write_actor(f, actor):
	s=""
	s=';'+str(actor.name)+";;;;;;"+str(actor.name)+';'+str(actor.role)+';'+str(actor.epi_num)+';'+str(actor.start)+'-'+str(actor.end)+';;;;;;;;;'+str(actor.name)+';'+str(actor.role)+';'
	f.write(s)
	f.write("\n")

def write_crew(f, crew):
	max_len = max(max(len(crew.misc), len(crew.creators)), max(max(len(crew.producers), len(crew.directors)), max(len(crew.exec_producers), len(crew.co_exec_producers))))
	l = [["","",["","",""]]]*max_len
	crew_lists = [list(l), list(l), list(l), list(l), list(l)] 
	k = [crew.creators, crew.directors, crew.producers, crew.exec_producers, crew.misc]
	for j in range(len(k)):
		for i in range(len(k[j])):
			crew_lists[j][i] = k[j][i]
	for i in range(max_len):
		s = ";" + crew_lists[0][i][0] + ";;;;;"+str(crew_lists[0][i][2][0])+";"+str(crew_lists[0][i][2][1])+'-'+str(crew_lists[0][i][2][2])+";;" 
		s += crew_lists[1][i][0] + ";;;;;"+str(crew_lists[1][i][2][0])+";"+str(crew_lists[1][i][2][1])+'-'+str(crew_lists[1][i][2][2])+";;"
		s += crew_lists[2][i][0] + ";" + str(crew_lists[2][i][1]) + ";;;;;"+str(crew_lists[2][i][2][0])+";"+str(crew_lists[2][i][2][1])+'-'+str(crew_lists[2][i][2][2])+";;"
		s += crew_lists[3][i][0] + ";" + str(crew_lists[3][i][1]) + ";;;;;"+str(crew_lists[3][i][2][0])+";"+str(crew_lists[3][i][2][1])+'-'+str(crew_lists[3][i][2][2])+";;"
		s += crew_lists[4][i][0] + ";" + str(crew_lists[4][i][1]) + ";;;;;"+str(crew_lists[4][i][2][0])+";"+str(crew_lists[4][i][2][1])+'-'+str(crew_lists[4][i][2][2])+";;"  
		f.write(s + '\n')
			

def write_headers(cast, crew):
	lic_sect = "Shows;Actor;Latino? Y=1;Latina Female? Y=1; Afro-Latino? Y=1; Latin American Actor/Actress? Y=1;;"
	lr_sect = "Actor; Role; # of Episodes; Year; Notes; Is this Lead Role? Y=1; Latino in Lead Role? Y=1; Is this a Supporting Role? Y=1; Is this an Unnamed Role? Y=1; Is this an Uncredited Role? Y=1; Latino in Uncredited Role? Y=1;;"
	lsr_sect = "Actor; Role; Is This a Stereotypical Role? Y=1; Criminal; Law Enforcement; Comic Relief; Blue Collar; Other Stereotype; Notes;\n"
	cast.write(lic_sect + lr_sect + lsr_sect)

	classifications = "Latino? Y=1;Latina Female? Y=1; Afro-Latino? Y=1; Latin American? Y=1; # of Episodes; Years;;"
	jobs = ["TITLE; Creators;", "Directors;", "Producers;Type of Producer Contains ALL;", "Executive Producers; Type of Exec. Producer;", "Others; Role;"]#"Writers (And Creators!)"]
	for j in jobs:
		crew.write(j + classifications)

def main():
	getTVdetailsby_year('2016')

if __name__ == '__main__':
	main()
