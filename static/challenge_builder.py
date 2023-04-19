# this is meant to be run via pyscript as part of the challenge builder web app

import toml

# import js
import uuid
from pyscript import Element
from js import document

num_flags = 1
num_hints = 1

flag_html_template = """
<div class="card card-body" id="flag_set_XXX">
	Flag: XXX
	<p>
		Flag Title:<input type="text" class="form-control flag" name="flag_XXX_title" id="flag_XXX_title" placeholder="Flag description for display; this may be visible to players">
		Flag Value:<input type="text" class="form-control flag" name="flag_XXX_value" id="flag_XXX_value" placeholder="How many points is THIS flag worth?">
		Actual Flag:<input type="text" class="form-control flag" name="flag_XXX_flag" id="flag_XXX_flag" placeholder="This is the actual flag as a player would submit it e.g. FLAG{good_job_solving}">
	</p>
</div>
"""

hint_html_template = """
<div class="card card-body" id="hint_set_XXX">
	Hint: XXX
	<p>
		Hint Cost:<input type="text" class="form-control hint" name="hint_XXX_cost" id="hint_XXX_cost" placeholder="How much will a player have to pay to view this hint?">
		Hint text:<textarea class="form-control hint" name="hint_XXX_text" id="hint_XXX_text" rows="2" width="100%" placeholder="This is the actual hint you are providing..."></textarea>
	</p>
</div>
"""

class hashabledict(dict):
  def __key(self):
    return tuple((k,self[k]) for k in sorted(self))
  def __hash__(self):
    return hash(self.__key())
  def __eq__(self, other):
    return self.__key() == other.__key()

def collect_flags():
	flags = list()
	#print('here')
	for i in range(1,num_flags):
		#print(i)
		title = Element(f'flag_{i}_title')
		value = Element(f'flag_{i}_value')
		flag = Element(f'flag_{i}_flag')
		#print('flag values', title.value, value.value, flag.value)
		if title.value == None or value.value == None or flag.value == None: 
			break
		try:
			flag_points = int(value.value.strip())
		except ValueError as e:
			flag_points = 0

		tmp = hashabledict({
			'flag_title': title.value.strip(),
			'flag_value': flag_points,
			'flag_flag' : flag.value.strip()
		})
		flags.append(tmp)
		#print(flags)

	return list(set(flags))

def collect_hints():
	hints = list()
	for i in range(1,num_hints):
		#print(i)
		cost = Element(f'hint_{i}_cost')
		text = Element(f'hint_{i}_text')
		#print('hint values', cost.value, text.value)
		if cost.value == None or text.value == None :
			break
		
		try:
			cost = int(cost.value.strip())
		except ValueError as e:
			cost = 0
		
		tmp = hashabledict({
			'hint_cost': cost ,
			'hint_text': text.value.strip()
		})
		hints.append(tmp)
		#print(hints)

	return list(set(hints))	



def add_flag():
	global num_flags
	# print(f'adding a flag, {num_flags} total' )
	
	this_flag_html = flag_html_template.replace("XXX", str(num_flags))
	this_flag_div = document.createElement("div")
	this_flag_div.innerHTML = this_flag_html
	flag_div = document.getElementById('flag_div')
	flag_div.appendChild(this_flag_div)
	num_flags += 1
	
	

def add_hint():
	global num_hints
	# print(f'adding a hint, {num_hints} total' )
	
	this_hint_html = hint_html_template.replace("XXX", str(num_hints))
	this_hint_div = document.createElement("div")
	this_hint_div.innerHTML = this_hint_html
	flag_div = document.getElementById('hint_div')
	flag_div.appendChild(this_hint_div)
	num_hints += 1

def build_challenge():
	tags = list(set([x for x in Element('tags').value.replace(' ','').lower().split(',') if x != '']))
	depends_on = list(set([x for x in Element('depends_on').value.replace(' ','').lower().split(',') if x != '']))

	challenge_object = {
		'author': Element("author").value.strip(),
		'challenge_title': Element("challenge_title").value.strip(),
		'uuid': str(uuid.uuid4()),
		'challenge_description': Element("challenge_description").value.strip(),
		'tags': tags,
		'depends_on': depends_on,
		'flags': collect_flags(),
		'hints': collect_hints()
	}

	ret = toml.dumps(challenge_object)

	output = Element('outputDiv')
	output.write(ret)

	return challenge_object