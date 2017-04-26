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

	def add_crew_member(self, name, role):
		if role == "Executive Producer" or role == "Co-Executive Producer":
			self.exec_producers.append([name, role])
		elif "roducer" in role:
			self.producers.append([name, role])
		else:
			self.misc.append([name, role])

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
					cast_file.write(" ;"+str(i.get("original_name"))+'\n')
					crew_file.write(str(i.get("original_name"))+'\n')

					time.sleep(3)
					url2="https://api.themoviedb.org/3/tv/"+str(i.get("id"))+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
					urllib.request.urlretrieve (url2,"./cast2017.json");
					with open('cast2017.json') as data_file2:
						datac = json.load(data_file2)
						if "cast" in datac.keys():
							for j in datac["cast"]:
								a = Actor(str(j.get("name")), str(j.get("character")))
								write_actor(cast_file, a)
						if "crew" in datac.keys():
							crew = Crew()
							for j in datac["crew"]:
								crew.add_crew_member(str(j.get("name")), str(j.get("job")))
							write_crew(crew_file, crew)
					cast_file.write("\n")
					crew_file.write("\n")



		cast_file.close()
		crew_file.close()

def write_actor(f, actor):
	s=""
	s=';;'+actor.name+";"+actor.role
	f.write(s)
	f.write("\n")

def write_crew(f, crew):
	max_len = max(len(crew.misc), max(max(len(crew.producers), len(crew.directors)), max(len(crew.exec_producers), len(crew.co_exec_producers))))
	l = [["",""]]*max_len
	crew_lists = [list(l), list(l), list(l), list(l), list(l)] 
	k = [crew.creators, crew.directors, crew.producers, crew.exec_producers, crew.misc]
	for j in range(len(k)):
		for i in range(len(k[j])):
			crew_lists[j][i] = k[j][i]
	print(crew_lists)
	print()
	print()
	for i in range(max_len):
		s = ";" + crew_lists[0][i][0] + ";;;;;;;;" + crew_lists[1][i][0] + ";;;;;;;;" + crew_lists[2][i][0] + ";" + crew_lists[2][i][1] +  ";;;;;;;;" + crew_lists[3][i][0] + ";" + crew_lists[3][i][1] +  ";;;;;;;;" + crew_lists[4][i][0] + ";" + crew_lists[4][i][1] + ";;;;;;;;"  
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
	getTVdetailsby_year('2015')

if __name__ == '__main__':
	main()
