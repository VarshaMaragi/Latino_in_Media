import wikipedia_utils as wiki
import files_utils as files

class Actor(object):
	
	def __init__(self, name, imdb_id):
		self.name = name
		self.imdb_id = imdb_id
		self.wiki_id = -1
		self.birthplace = ""
		self.self_info = {"latino": [], "noted": [], "non_latino": [], "other":[]}
		self.descent = {"latino": [], "noted": [], "non_latino": []}
		self.tags = {"latino": [], "noted": [], "non_latino": [], "other": []}
		self.la_ethnicity = False
		self.ethnicities = []
		self.on_file = -1

	def add_sentence(self, sent_type, txt):
		self.self_info[sent_type].append(txt)

	def add_tag(self, tag_type, tag):
		self.tags[tag_type].append(tag)
		
	def add_wiki_id(self, wiki_id):
		self.wiki_id = wiki_id
		

class MovieInfo(object):
	
	def __init__(self, movie_title):
		self.title = movie_title
		self.actors = self.tmp_make_actors()
		self.add_file_info()
		self.add_imdb_info()
		#self.add_wiki_info()
		self.add_last_name_info()

	def tmp_make_actors(self):
		#This will be replaced by a funtion that gets this info from imdb
		actor_dict = {"Jackie Cruz": '3117320', "Laura Gomez": '0327041', "Stephanie Beatriz": '3715867',  "Dascha Polanco": '4745601', "Elizabeth Rodriguez": '0735300'}
		actor_list = []
		for name, imdb_id  in actor_dict.iteritems():
			actor_list.append(Actor(name, imdb_id))
		return actor_list

	def add_wiki_info(self):
		wiki_obj = wiki.WikiPages(self.actors)
		wiki_obj.determine_latino()

	def add_last_name_info(self):
		#TODO
		return True

	def add_imdb_info(self):
		#TODO
		return True

	def add_file_info(self):
		file_obj = files.XMLfile(self.actors, self.title)
		file_obj.find_actors()
		file_obj.write_new_movie()
