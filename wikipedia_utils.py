import requests
import pprint
import json
import page_parser as pp

API_URL = 'http://en.wikipedia.org/w/api.php'
HEADERS = {
    'User-Agent': "Latinos in Comedy Research Project (dmb2238@columbia.edu)"
}

def get_imdb_ids(actors):
	url = 'www.imdb.com/name/nm'
	actor_ids = {}
	actor_str = ""
	for a in actors:
		actor_ids[a[0]] = ["", ""]
		actor_str += a[0] + "|"
	links_dump = get_ext_links(actor_str, url)
	for elem in links_dump:
		for page_id, content in elem['pages'].iteritems():
			if "extlinks" not in content:
				actor_ids[str(content['title'])] = [page_id.encode('utf-8'), ""]
				continue
			for k in content["extlinks"]:
				link = k["*"]
				idx = link.find(url)
				if idx > -1:
					link_tmp = link[idx + len(url):]
					imdb_id = link_tmp.split('/')[0]
					actor_ids[str(content['title'])] = [str(content['pageid']), str(imdb_id.encode('utf-8'))]
				else:
					actor_ids[str(content['title'])] = [page_id.encode('utf-8'), ""]

	return actor_ids

def get_pages(actors):
	actor_ids = get_imdb_ids(actors)

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
			missing_actors.append([a])
		else:
			found_actors.append([a[0], a[1], wiki_id])	
	return missing_actors,unsure_actors, found_actors

def get_plain_text(actors):
	actor_str = ""
	actor_dict = {}
	for a in actors:
		actor_str += a[0] + "|"
		actor_dict[a[1]] = []
	dump = _wiki_query({ 'prop': 'extracts', 'titles': actor_str})
	for elem in dump:
		for page_id, content in elem['pages'].iteritems():
			if str(page_id) not in actor_dict:
				continue
			if 'extract' in content:
				chunks = content['extract'].split("\n")
				for chunk in chunks:
					sentences = chunk.split('.')
					for x in sentences:
						sentence_tmp = ""
						(idx, latino, text_type) = pp.keep_sentence(x.lower())
						if idx > -1:
							actor_dict[page_id].append([text_type, pp.take_out_angle_brackets(x).encode('utf-8')])
	return actor_dict
 	       
 
def get_categories(actors):
	actor_str = ""
	actor_dict = {}
	for a in actors:
		actor_str += a[0] + "|"
		actor_dict[a[1]] = []
	dump = _wiki_query({ 'prop': 'categories', 'titles': actor_str})
	for elem in dump:
		for page_id, content in elem['pages'].iteritems():
			if 'categories' in content:
				for x in content['categories']:
					c = x['title'].split(':')[1].lower()
					(keep, latino, tag_type) = pp.keep_category(c)
					if keep:
						actor_dict[page_id].append([tag_type, c.encode('utf-8')])
	return actor_dict
	

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

def get_birthplace(actors):
	actor_str = ""
	actor_dict = {}
	for a in actors:
		actor_str += a[0] + "|"
		actor_dict[a[1]] = ""
	for elem in get_infobox(actor_str):
		for page_id, content in elem['pages'].iteritems():
			if 'revisions' in content:
				bp = pp.get_birthplace(content['revisions'][0]['*'])
				if bp != "":
					actor_dict[page_id] = pp.take_out_angle_brackets(bp).encode('utf-8')
	return actor_dict

def get_infobox(titles):
	info = _wiki_query({
       		'prop': 'revisions',
       		'rvprop': 'content',
       		'rvsection': 0,
       		'titles': titles
       	})
       	return info
