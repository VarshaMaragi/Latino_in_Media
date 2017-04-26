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
					crew_file.write(" ;"+str(i.get("original_name"))+'\n')

					time.sleep(3)
					url2="https://api.themoviedb.org/3/tv/"+str(i.get("id"))+"/credits?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
					urllib.request.urlretrieve (url2,"./cast2017.json");
					with open('cast2017.json') as data_file2:
						datac = json.load(data_file2)
						if "cast" in datac.keys():
							for j in datac["cast"]:
								s=""
								s=';;'+str(j.get("name"))+";"+str(j.get("character"))
								cast_file.write(s)
								cast_file.write("\n")
						if "crew" in datac.keys():
							print(str(i.get("original_name")) + str(datac["crew"])+'\n')
							for j in datac["crew"]:
								s=""
								s=';;'+str(j.get("name"))+";"+str(j.get("job"))
								crew_file.write(s)
								crew_file.write("\n")
					cast_file.write("\n")
					crew_file.write("\n")



		cast_file.close()
		crew_file.close()
def main():
	getTVdetailsby_year('2015')

if __name__ == '__main__':
	main()
