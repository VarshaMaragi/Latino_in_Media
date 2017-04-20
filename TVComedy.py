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

def getTVdetailsby_year():

	g=open("TVComedy.csv",'w')
	h=open("TVComedyCast.csv",'w')
	url="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte=2016&first_air_date.gte=2016&page=1&timezone=America/New_York&with_genres=35&without_genres=28,12,16,18,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,37,10752&include_null_first_air_dates=false&with_original_language=en"
	urllib.request.urlretrieve (url,"TVyear2016.json");
	with open('TVyear2016.json') as data_file:
		data = json.load(data_file)
		print("Total Pages",data["total_pages"])
			
		for i in range(1,data["total_pages"]+1):
			print ("Page",i)
			print ("-------------------------------------------")
			time.sleep(3)
			url="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte=2016&first_air_date.gte=2016&page=1&timezone=America/New_York&with_genres=35&without_genres=28,12,16,18,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,37,10752&include_null_first_air_dates=false&with_original_language=en"
			urllib.request.urlretrieve (url,"Tvyear2016.json");
			

			with open('Tvyear2016.json') as data_file2:
					
				data2 = json.load(data_file2)
				print ("data2")
				print (data2)

				for i in data2["results"]:
					strs=""
					print("Original Name\t",i.get("original_name"))
					print("First air date\t",i.get("first_air_date"))
					print("Overview\t",i.get("overview"))
					strs=str(i.get("original_name"))+";"+str(i.get("first_air_date"))+";"+str(i.get("overview"))
					g.write(strs+"\n")
					time.sleep(2)
					url2="https://api.themoviedb.org/3/tv/"+str(i.get("id"))+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
					urllib.request.urlretrieve (url2,"./cast2017.json");
					h.write(str(i.get("original_name")))
					h.write("\n")
					with open('cast2017.json') as data_file2:
						datac = json.load(data_file2)
						if "cast" in datac.keys():

							for j in datac["cast"]:
								s=""
								print("Name",j.get("name"))
								print("Character",j.get("character"))
								s=str(j.get("name"))+";"+str(j.get("character"))
								h.write(s)
								h.write("\n")
					h.write("\n")



		g.close()
		h.close()
def main():
	getTVdetailsby_year()

if __name__ == '__main__':
	main()