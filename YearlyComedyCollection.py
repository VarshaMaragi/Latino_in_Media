import urllib
import json
import re
import csv
import codecs
import sys
import time
import requests


#LA_COUNTRIES = ["Cuba", "Dominican Republic","Puerto Rico", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Argentina", "Bolivia", "Chile", "Colombia", "Ecuador",  "Guyana", "Paraguay", "Peru", "Uruguay", "Venezuela"]
reload(sys)
sys.setdefaultencoding('utf8')
def getmoviesbyyear():
	dcode=dict()
	totalactors=0
	latinoactors=0
	latinolead=0
	genlead=0
	gensupport=0
	latinosupport=0
	dcode["comedy"]=35
	dcode["action"]=28
	dcode["animation"]=16
	dcode["adventure"]=12
	dcode["crime"]=80
	dcode["documentary"]=99
	dcode["drama"]=18
	LA_COUNTRIES=re.compile(".*Cuba.*|.*Dominican Republic.*|.*Puerto Rico.*|.*Costa Rica.*|.*El Salvador.*|.*Guatemala.*|.*Mexico.*|.*Nicaragua.*|.*Panama.*|.*Argentina.*|.*Nicaragua.*|.*Bolivia.*|.*Chile.*|.*Colombia.*|.*Ecuador.*|.*Guyana.*|.*Paraguay.*|.*Peru.*|.*Uruguay.*|.*Venezuela.*")
	LA_NAMES=re.compile(".*ez$|.*do$|.*ro$")
	year=raw_input("Enter year: ")
	g=raw_input("Entre the genre: ")
	genre=dcode.get(g)
	url="https://api.themoviedb.org/3/discover/movie?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year="+str(year)+"&with_genres=35&year="+str(year)+"&without_genres=28,12,16,18,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,37,10752&with_original_language=en"
	urllib.urlretrieve (url,"year2017.json");
	with open('year2017.json') as data_file:
		data = json.load(data_file)
		print data["total_pages"]
		for i in range(1,data["total_pages"]+1):
			print "Page",i
			print "-------------------------------------------"
			time.sleep(3)
			url="https://api.themoviedb.org/3/discover/movie?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&page="+str(i)+"&primary_release_year="+str(year)+"&with_genres=35&year="+str(year)+"&without_genres=28,12,16,18,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,37,10752&with_original_language=en"
			urllib.urlretrieve (url,"year2017.json");
			
			with open('year2017.json') as data_file2:
				data2 = json.load(data_file2)
				print "data2"
				print data2
				if "results" in data2.keys():
					print "in results"
					for i in data2["results"]:
						if i.get("original_language")=="en":

							print i.get("original_title")
							f=open('Comedy'+str(year)+'Cast.csv', 'a')
							g=open('Comedy'+str(year)+'Crew.csv','a')
							s=(i.get("original_title").encode('utf-8','ignore').decode('utf-8'))
							#s=unicode(s.strip(codecs.BOM_UTF8), 'utf-8')
							f.write(s)
							g.write(s)
							rescast=i.get("id")
							print str(rescast)
							overviewmovie=i.get("overview")
							if LA_COUNTRIES.findall(overviewmovie) or LA_NAMES.findall(overviewmovie):
								f.write("\n")
								f.write("possible Latino movie")
								f.write("\n")
								g.write("\n")
								g.write("possible Latino movie")
								g.write("\n")
							#time.sleep(2)
							url2="https://api.themoviedb.org/3/movie/"+str(rescast)+"/casts?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c"
							urllib.urlretrieve (url2,"./cast2017.json");
							with open('cast2017.json') as data_file2:
								datac = json.load(data_file2)
								strtemp="" 
								strtemp2=""
								pob=""

								if "cast" in datac.keys():
									for j in datac["cast"]:
										flag=0
										attachleadornot=""
										attachnamebased=""
										print j.get("name")
										if j.get("order")<=2:
											genlead=genlead+1
										else:
											gensupport=gensupport+1
										if LA_NAMES.findall(j.get("name")):
											attachnamebased="Latinx"
											print "order",j.get("order")
											latinoactors=latinoactors+1
											flag=1
											if j.get("order")>2:
													attachleadornot="Not lead"
													latinosupport=latinosupport+1
											else:
												latinolead=latinolead+1
								
										time.sleep(1)
										url3="https://api.themoviedb.org/3/person/"+str(j.get("id"))+"?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
										urllib.urlretrieve(url3,"./placeofbirth.json")
										pob=""
										pp=""
										attach=""
										gen=""
										with open('placeofbirth.json') as data_file3:
											dataperson = json.load(data_file3)
											if "gender" in dataperson.keys():
												gen=dataperson["gender"]
											if "place_of_birth" in dataperson.keys():
												pob=dataperson["place_of_birth"]
												if pob!=None:
													if LA_COUNTRIES.findall(pob):
														
														attach="Latinx"
														if flag==0:
															latinoactors=latinoactors+1
															if j.get("order")>2:
																latinosupport=latinosupport+1
															else:
																latinolead=latinolead+1

											print "pob",pob

											if "profile_path" in dataperson.keys():
												if dataperson["profile_path"]!=None:
													pp="http://image.tmdb.org/t/p/w185//"+dataperson["profile_path"]
											#if not pob:
										strtemp=strtemp+j.get("name").encode('utf-8','ignore').decode('utf-8')+";"+j.get("character").encode('utf-8','ignore').decode('utf-8')+";"+str(pob)+";"+str(pp)+";"+str(gen)+";"+str(attachnamebased)+";"+str(attach)+";"+str(attachleadornot)+"\n"
										totalactors=totalactors+1
										#strtemp=strtemp+j.get("name").encode('utf-8')+"\t\t"+j.get("character").encode('utf-8')+"\n"

									for j in datac["crew"]:
										attachnamebased=""

										print j.get("name")
										if LA_NAMES.findall(j.get("name")):
											attachnamebased="Latinx"
										#strtemp2=strtemp2+j.get("name").encode('utf-8')+"\t\t"+j.get("job").encode('utf-8')+"\n"
										#time.sleep(1)
										url3="https://api.themoviedb.org/3/person/"+str(j.get("id"))+"?api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c&language=en-US"
										urllib.urlretrieve(url3,"./placeofbirth.json")
										pob=""
										pp=""
										attach=""
										gen=""
										with open('placeofbirth.json') as data_file3:
											dataperson = json.load(data_file3)
											if "gender" in dataperson.keys():
												gen=dataperson["gender"]
											if "place_of_birth" in dataperson.keys():
												pob=dataperson["place_of_birth"]
												if pob!=None:
													if LA_COUNTRIES.findall(pob):
														
														attach="Latinx"
											print "pob",pob
											#if not pob:

											if "profile_path" in dataperson.keys():
												if dataperson["profile_path"]!=None:
													pp="http://image.tmdb.org/t/p/w185//"+dataperson["profile_path"]
										strtemp2=strtemp2+j.get("name").encode('utf-8','ignore').decode('utf-8')+";"+j.get("job").encode('utf-8','ignore').decode('utf-8')+";"+str(pob)+";"+str(pp)+";"+str(gen)+";"+str(attachnamebased)+";"+	str(attach)+"\n"
										#strtemp2=strtemp2+j.get("name").encode('utf-8')+"\t\t"+j.get("character").encode('utf-8')+"\n"

							f.write("\n")
							g.write("\n")			
							f.write("Cast")
							g.write("Crew")
							f.write("\n")
							g.write("\n")
							f.write(strtemp)
							g.write(strtemp2)
							f.write("\n")
		
							g.write("\n")
		#print(totalactors)
		#print(latinoactors)
		f.write(str(totalactors))
		f.write("\n")
		f.write(str(latinoactors))
		f.write("\n")
		f.write(str(latinolead))
		f.write("\n")
		f.write(str(genlead))
		f.write("\n")
		f.write(str(gensupport))
		f.write("\n")
		f.write(str(latinosupport))


	
def getmoviesdirect():
	url = 'http://api.themoviedb.org'
	params = '/3/discover/movie?with_genres=35&primary_release_year=2017&page=1&include_video=false&include_adult=false&sort_by=vote_count.desc&language=en    -US&api_key=17ce03ebb1e89f2dcf4eec0e9c2b8e6c'
	result = requests.get(str(url + params), headers = {}).json()
	print result
	print (type(data))
	print(data.decode("utf-8"))
	print ("----------------------------------------")


def main():
	getmoviesbyyear()

if __name__ == '__main__':
	try:
		main()
	except Exception,e:
		print(e)
