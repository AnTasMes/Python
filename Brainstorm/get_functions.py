class obj_pool:
	pool = []

	def add_pool(var):
		obj_pool.pool.append(var)

class fn(obj_pool):
	instance_num = 0

	block_lines = []

	def incr(self):
		self.instance_num += 1

	def __init__(self, name, block_id, args = []):
		self.name = name
		self.args = args
		self.block_id = block_id

def fn_strip(line):
	prevline = line
	name, args = line.replace('fn ', '').replace('\n','').split('(')
	args,line = args.split(')')
	print(args)
	return line

prevline = ""

reserved = ['if', 'else', 'def', 'for', 'while']
with open('function.txt','r') as file:
	for line in file:
		for res in reserved:
			if line.startswith('def'):
				line = fn_strip(line)
				#print(line)

#print(f.args)
"""		
prevline = prevline.split('(')
				prevline[-1] = prevline[-1].strip('){\n')
				args = prevline[1].split(',')
"""


#napraviti posebnu funkciju koja pregleda generalni pool i pravi objekat za odgovarajucu klasu


# for line in file:

	# 	if '{' in line and '(' in line and ')' in line:	
	# 		ln = fn_strip(line)
	# 		f = fn(name = ln[0], args = ln[1], block_id = 1)

	# 	elif '{' in line:
	# 		if '(' in prevline and ')' in prevline:				
	# 			ln = fn_strip(prevline)
	# 			f = fn(name = ln[0], args = ln[1], block_id = 1)

	# 	if '}' in line:
	# 		break
	# 	prevline = line