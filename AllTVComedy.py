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

def getTVdetailsby_year(year):
	g=open("AllTVComedy.csv",'a')
	g.write(str(year) + '\n')
	time.sleep(3)
	url="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte="+year+"-01-01&air_date.lte="+year+"-12-31&page=1&timezone=America/New_York&with_genres=35&include_null_first_air_dates=true&with_original_language=en"
	urllib.request.urlretrieve (url,"TVyear2016.json");
	with open('TVyear2016.json') as data_file:
		data = json.load(data_file)
		total_num = data["total_results"]
		g.write(";Total Comedies: " + str(total_num) + '\n\n')
		j = 0
			
		for i in range(1,data["total_pages"]+1):
			url_2 ="https://api.themoviedb.org/3/discover/tv?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&sort_by=popularity.desc&air_date.gte="+year+"-01-01&air_date.lte="+year+"-12-31&page=1&timezone=America/New_York&with_genres=35&include_null_first_air_dates=true&with_original_language=en"
			time.sleep(3)
			urllib.request.urlretrieve (url_2,"Tvyear2016.json");

			with open('Tvyear2016.json') as data_file2:
					
				data2 = json.load(data_file2)

				for i in data2["results"]:
					if (j > 10):
						g.close()
						return 
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
						j += 1 
						continue
					strs=str(" ;"+i.get("original_name"))+";"+str(i.get("first_air_date"))+";"+str(i.get("overview").split('\n')[0])
					#print(i.get("overview").split('\n')[0])
					g.write(strs+"\n")
					j += 1
					'''url2="https://api.themoviedb.org/3/tv/"+str(i.get("id"))+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
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
					h.write("\n")'''



		g.close()
		#h.close()
def main():
	y = 1950
	while (y<2018):
		getTVdetailsby_year(str(y))
		y += 1

if __name__ == '__main__':
	main()
