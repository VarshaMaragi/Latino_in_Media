import requests
import pprint
import json
import page_parser as pp

API_URL = 'http://en.wikipedia.org/w/api.php'
HEADERS = {
    'User-Agent': "Latinos in Comedy Research Project (dmb2238@columbia.edu)"
}

class WikiPages(object):

	def __init__(self, actors):
		self.actors = {}
		tmp_title_string = ""
		for a in actors:
			tmp_title_string = tmp_title_string + a.name + "|"
		self.titles = tmp_title_string
	
		id_dict = self.get_imdb_ids()
		no_wiki_id = []
		new_title_string = ""
		for a in actors:
			if a.name in id_dict:
				if str(a.imdb_id) == id_dict[a.name][1]:
					new_title_string = new_title_string + a.name + "|"
					a.add_wiki_id(id_dict[a.name][0])
					self.actors[id_dict[a.name][0]] = a
					continue
			no_wiki_id.append(a)
		self.titles = new_title_string
	
	def get_imdb_ids(self):
		url = 'www.imdb.com/name/nm'
		actor_ids = {}
		for a in self.actors:
			actor_ids[a.name] = 0
#		links_dump = self.get_ext_links(url)
#		for elem in links_dump:
#			for page_id, content in elem['pages'].iteritems():
#				if "extlinks" not in content:
#					continue
#				for k in content["extlinks"]:
#					link = k["*"]
#					idx = link.find(url)
#					if idx > -1:
#						link_tmp = link[idx + len(url):]
#						imdb_id = link_tmp.split('/')[0]
#						actor_ids[str(content['title'])] = [str(content['pageid']), str(imdb_id.encode('utf-8'))]
		return actor_ids

	def get_updated_title_string(self, disqualifier_field, disqualifier_val):
		out = ""
		for a in self.actors:
			if self.actors[a].birthplace == disqualifier_val:
				out += self.actors[a].name + "|"
		return out	
	
	def determine_latino(self):
		#self.search_titles()
		y = self.get_birthplace() #will come from IMDB
		y = self.get_categories()
		self.get_plain_text()
		return y
			
	def get_birthplace(self):
		for elem in self.get_infobox(self.get_updated_title_string("birthpace", "")):
			for page_id, content in elem['pages'].iteritems():
				if 'revisions' in content:
					bp = pp.get_birthplace(content['revisions'][0]['*'])
					if bp != "":
						self.actors[str(page_id)].birthplace = pp.take_out_angle_brackets(bp)
		return self.actors

	def get_plain_text(self):
		dump = self._wiki_query({ 'prop': 'extracts', 'titles': self.titles})
		for elem in dump:
			for page_id, content in elem['pages'].iteritems():
				if str(page_id) not in self.actors:
					continue
				curr_actor = self.actors[str(page_id)]
				if 'extract' in content:
					chunks = content['extract'].split("\n")
					for chunk in chunks:
						sentences = chunk.split('.')
						for x in sentences:
							sentence_tmp = ""
							(idx, latino, text_type) = pp.keep_sentence(x.lower())
							if idx > -1:
								if latino:
									curr_actor.la_ethnicity = True
								curr_actor.add_sentence(text_type, pp.take_out_angle_brackets(x))
		return True
 	       
	def get_infobox(self, titles):
		info = self._wiki_query({
 	       		'prop': 'revisions',
 	       		'rvprop': 'content',
 	       		'rvsection': 0,
 	       		'titles': titles
 	       	})
 	       	return info
 
	def get_categories(self):
		dump = self._wiki_query({ 'prop': 'categories', 'titles': self.titles})
		for elem in dump:
			for page_id, content in elem['pages'].iteritems():
				if 'categories' in content:
					curr_actor = self.actors[str(page_id)]
					for x in content['categories']:
						c = x['title'].split(':')[1].lower()
						(keep, latino, tag_type) = pp.keep_category(c)
						if keep:
							if latino:
								curr_actor.la_ethnicity = True
							curr_actor.add_tag(tag_type, c)
		return self.actors
	

	def get_ext_links(self, url):
		return self._wiki_query({ 
			'prop': 'extlinks', 
			'elquery': url,
			'elprotocol': 'http',
			'titles': self.titles
		})
		

	def get_full_page(self):
		text = self._wiki_query({ 
			'prop': 'revisions', 
			'rvprop':'content', 
			'titles': self.titles
		})
		return True
	
	def search_titles(self):
		text, cont = self._wiki_query_no_continue({ 
			'list': 'search', 
			'srsearch':'jackie cruz', 
			#'srwhat': 'title'
			'srlimit': 10,
			'srprop': ''#'titlesnippet'
		})
		return True
	
	def _wiki_query_no_continue(self, params, offset=0):
		params['format'] = 'json'
		params['action'] = 'query'
		params['offset'] = offset
 	       
 	       	out = []
 	       	result = requests.get(API_URL, params=params, headers = HEADERS).json()
 	       	if 'error' in result:
 	           		raise Error(result['error'])
        	if 'warnings' in result:
            		print(result['warnings'])
        	if 'query' in result:
            		out.append(result['query'])
        	if 'continue' not in result:
			return out, False
		return out, True
	
	def _wiki_query(self, params):
		params['format'] = 'json'
		params['action'] = 'query'
 	       
 	       	last_continue = {'continue': ''}
 	       	p = params.copy()
 	       	out = []
 	       	while True:
			p.update(last_continue)
 	       		result = requests.get(API_URL, params=p, headers = HEADERS).json()
 	       		if 'error' in result:
 	        	   		raise Error(result['error'])
        		if 'warnings' in result:
            			print(result['warnings'])
        		if 'query' in result:
            			out.append(result['query'])
        		if 'continue' not in result:
            			break
       			last_continue = result['continue']
		return out
