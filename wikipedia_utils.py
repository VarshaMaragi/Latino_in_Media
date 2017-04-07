import requests
import pprint
import json
import page_parser as pp
from nltk.tokenize import sent_tokenize

API_URL = 'http://en.wikipedia.org/w/api.php'
HEADERS = {
    'User-Agent': "Latinos in Comedy Research Project (dmb2238@columbia.edu)"
}

def get_imdb_ids(actors):
	url = 'www.imdb.com/name/nm'

	def _get_ids(actor_str, actor_ids):
		links_dump = get_ext_links(actor_str, url)
		for elem in links_dump:
			for page_id, content in elem['pages'].items():
				if int(str(page_id)) <= 0:
					actor_ids[str(content['title'])] = ["", ""]
					continue
				if "extlinks" not in content:
					if "missing" in content:
						actor_ids[str(content['title'])] = [str(page_id), ""]
					continue
				for k in content["extlinks"]:
					link = k["*"]
					idx = link.find(url)
					if idx > -1:
						link_tmp = link[idx + len(url):]
						imdb_id = link_tmp.split('/')[0]
						actor_ids[content['title']] = [str(page_id), str(imdb_id)]
					else:
						actor_ids[str(content['title'])] = [str(page_id), ""]
		return actor_ids
	actor_ids = {}
	actor_out = {}
	actor_str = ""
	i = 0
	for a in actors:
		if i >= 49:
			actor_out = dict(actor_out, **_get_ids(actor_str, actor_ids))
			actor_str = ""
			actor_ids = {}
			i = 0
		actor_ids[a[0]] = ["", ""]
		actor_str += a[0] + "|"
		i+= 1
	actor_out = dict(actor_out, **_get_ids(actor_str, actor_ids))
	return actor_out

def get_wiki_ids(actors):

	def _get_ids(actor_str, actor_ids):
		extract_dump = get_extracts(actor_str)
		for elem in extract_dump:
			for page_id, content in elem['pages'].items():
				if int(str(page_id)) <= 0:
					actor_ids[str(content['title'])] = ["", ""]
					continue
				if "extract" not in content:
					if "missing" in content:
						actor_ids[str(content['title'])] = [str(page_id), ""]
					continue
				actor_ids[str(content['title'])] = [str(content['pageid']), str(content["extract"])]
		return actor_ids

	actor_ids = {}
	actor_out = {}
	actor_str = ""
	i = 0
	for a in actors:
		if i >= 49:
			actor_out = dict(actor_out, **_get_ids(actor_str, actor_ids))
			actor_str = ""
			actor_ids = {}
			i = 0
		actor_ids[a[0]] = ["", ""]
		actor_str += a[0] + "|"
		i+= 1
	actor_out = dict(actor_out, **_get_ids(actor_str, actor_ids))
	return actor_out

def get_pages(actors):
	print (actors)
	actor_ids = get_imdb_ids(actors)
	print (actor_ids)
	missing_actors = []
	unsure_actors = []
	found_actors = []
	for a in actors:
		wiki_id, imdb_id = actor_ids[a[0]]
		if wiki_id == "":
			missing_actors.append(a)
		elif imdb_id == "":
			unsure_actors.append([a[0], a[1], wiki_id])
		elif imdb_id != a[1]:
			missing_actors.append(a)
		else:
			found_actors.append([a[0], a[1], wiki_id])	
	return missing_actors,unsure_actors, found_actors

def get_pages_no_imdb(actors):

	def keep_description(descript):
		l = ['director', 'actor', 'actress', 'performer', 'comedian', 'film', 'television', 'movie']
		for x in l:
			if x in descript:
				return True
		return False

	actor_ids = get_wiki_ids(actors)
	missing_actors = []
	unsure_actors = []
	found_actors = []
	for a in actors:
		wiki_id, description = actor_ids[a[0]]
		if wiki_id == "":
			missing_actors.append(a)
		elif keep_description(description):
			found_actors.append([a[0], None, wiki_id])
		else:
			unsure_actors.append([a[0], None, wiki_id])	
	return missing_actors,unsure_actors, found_actors

def get_plain_text(actors):

	def _get_plain_text(actor_str, actor_dict):
		dump = _wiki_query({ 'prop': 'extracts', 'titles': actor_str})
		for elem in dump:
			for page_id, content in elem['pages'].items():
				if str(page_id) not in actor_dict:
					continue
				if 'extract' in content:
					chunks = content['extract'].split("\n")
					for chunk in chunks:
						sentences = sent_tokenize(chunk)
						for x in sentences:
							(idx, latino, text_type) = pp.keep_sentence(x.lower())
							if idx > -1:
								if text_type in actor_dict[page_id]:
									actor_dict[page_id][text_type].append(str(pp.take_out_angle_brackets(x)))
								else:
									actor_dict[page_id][text_type] = [str(pp.take_out_angle_brackets(x))]
		return actor_dict

	actor_dict = {}
	actor_out = {}
	actor_str = ""
	i = 0
	for a in actors:
		if i >= 49:
			actor_out = dict(actor_out, **_get_plain_text(actor_str, actor_dict))
			actor_str = ""
			actor_dict = {}
			i = 0
		actor_dict[a[2]] = {}
		actor_str += a[0] + "|"
		i+= 1
	actor_out = dict(actor_out, **_get_plain_text(actor_str, actor_dict))
	return actor_out
 	       
 
def get_categories(actors):
	
	def _get_cate(actor_str, actor_dict):
		dump = _wiki_query({ 'prop': 'categories', 'titles': actor_str})
		for elem in dump:
			for page_id, content in elem['pages'].items():
				if 'categories' in content:
					for x in content['categories']:
						c = x['title'].split(':')[1].lower()
						(keep, latino, tag_type) = pp.keep_category(c)
						if keep:
							if tag_type not in actor_dict[str(page_id)]:
								actor_dict[str(page_id)][tag_type] = [str(c)]
							if tag_type in actor_dict[str(page_id)]:
								actor_dict[str(page_id)][tag_type].append(str(c))
		return actor_dict
	
	actor_dict = {}
	actor_out = {}
	actor_str = ""
	i = 0
	for a in actors:
		if i >= 49:
			actor_out = dict(actor_out, **_get_cate(actor_str, actor_dict))
			actor_str = ""
			actor_dict = {}
			i = 0
		actor_dict[a[2]] = {}
		actor_str += a[0] + "|"
		i+= 1
	actor_out = dict(actor_out, **_get_cate(actor_str, actor_dict))
	return actor_out
	

def get_ext_links(actor_str, url):
	return _wiki_query({ 
		'prop': 'extlinks', 
		'elquery': url,
		'elprotocol': 'http',
		'titles': actor_str
	})
		

def get_full_page():
	actor_str = ""
	for a in actors:
		actor_str += a[0] + "|"
	text = _wiki_query({ 
		'prop': 'revisions', 
		'rvprop':'content', 
		'titles': actor_str
	})
	return True
	
def search_titles():
	text, cont = _wiki_query_no_continue({ 
		'list': 'search', 
		'srsearch':'jackie cruz', 
		#'srwhat': 'title'
		'srlimit': 10,
		'srprop': ''#'titlesnippet'
	})
	return True
	
def get_birthplace(actors):
	def _get_bp(actor_titles, actor_dict):
		print ("a: " + actor_titles)
		for elem in get_infobox(actor_titles):
			for page_id, content in elem['pages'].iteritems():
				if 'revisions' in content:
					bp = pp.get_birthplace(content['revisions'][0]['*'])
					if bp != "":
						actor_dict[page_id] = str(pp.take_out_angle_brackets(bp))
		return actor_dict

	actor_str = ""
	actor_dict = {}
	actor_out = {}
	i = 0
	for a in actors:
		if i >= 49:
			actor_out.update(_get_bp(actor_str, actor_dict))
			i = 0
			actor_str = ""
			actor_dict = {}
		actor_str += a[0] + "|"
		actor_dict[a[1]] = ""
		i += 1
	actor_out.update(_get_bp(actor_str, actor_dict))
	return actor_out

def get_infobox(titles):
	info = _wiki_query({
       		'prop': 'revisions',
       		'rvprop': 'content',
       		'rvsection': 0,
       		'titles': titles
       	})
	return info

def get_extracts(titles):
	info = _wiki_query({
       		'prop': 'extracts',
       		'exchars': '200',
       		'titles': titles
       	})
	return info

def _wiki_query_no_continue(params, offset=0):
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
	
def _wiki_query(params):
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
