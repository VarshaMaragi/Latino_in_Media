import wikipedia_utils as wiki
import files_utils as files

class Actor(object):
	
	def __init__(self, name, imdb_id, role, role_info, stereotype_info, latino_info, bp, pic):
		self.name = name
		self.imdb_id = imdb_id
		self.wiki_id = -1
		self.birthplace = bp
		self.wiki_info = {
			'self_info' : {"latino": [], "noted": [], "non_latino": [], "other":[]},
			'descent' : {"latino": [], "noted": [], "non_latino": []},
			'tags' : {"latino": [], "noted": [], "non_latino": [], "other": []}
		}
		self.ethinicity_info = {
			'la_ethnicity' : False,
			'ethnicities' : [],
			'latino_info' : latino_info
		}
		self.on_file = -1
		self.role = {
			'role': role,
			'role_info': role_info,
			'stereotype_info': stereotype_info
		}
		self.picture = pic
		self.latino = -1

	def add_sentence(self, sent_type, txt):
		self.wiki_info.self_info[sent_type].append(txt)

	def add_tag(self, tag_type, tag):
		self.wiki_info.tags[tag_type].append(tag)
		
	def add_wiki_id(self, wiki_id):
		self.wiki_id = wiki_id

	def decide_latino(self):
		if self.on_file != -1:
			self.latino = self.on_file
			return
		if self.ethinicity_info.la_ethnicity:
			if self.birthplace.contains("USA") or self.birthplace.contains("U.S."):
				self.latino = 1
		#add info gotten from wiki
		
class MovieInfo(object):
	
	def __init__(self, movie_title, actors):
		self.title = movie_title
		self.actors = actors
		self.file_obj = self.add_file_info()
		#self.add_imdb_info()
		#self.add_wiki_info()
		self.add_last_name_info()

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
		return file_obj

	def get_file_obj(self):
		return self.file_obj

def write_to_file(file_obj, movies):
	files.write_new_movie(file_obj, movies)
	
