import class_main



# def find_fn(line): #nalazi funkcije u linijama (ne nove) if has name je bolja ideja ako kreiramo fju, pogledamo samo da li rec postoji u linij
# 	args = []
# 	for br in brs:
# 		if br in line:
# 			line = line.split('(')
# 			if line[1] != ')': #ako nije samo )
# 				args = line[1].split(',')
# 				args[-1] = args[-1].strip(')')
# 	return line

#def get_fn(line):
	

def trim_by_op(op,line):
	line = line.replace('\n','')
	line = line.replace(' ', '')
	line = line.split(op)
	return line

def find_ops(line):
	for ops in operators:
		if ops in line:
			if ops in side_ops:
				line = trim_by_op(ops,line)

				return line
			else:
				print() #ovde sve ako su operatori racunanja
	return line

# def fn_strip(line):
# 	prevline = line
# 	name, args = line.replace('fn ', '').replace('\n','').split('(')
# 	args,line = args.split(')')
# 	print(args)
# 	return line

# def check_in_pool(obj):
# 	for o in obj_pool.pool:
# 		if o == obj:
# 			return 0
# 		else:
# 			obj_pool.pool.append(obj)


def get_vars(line): #proverava da li postoje promenljive u linij
	if class_main.obj_pool.pool: #Not empty
		for obj in class_main.obj_pool.pool:
			if line[0] == obj.name:
				obj.incr()
				return None
			else:
				print(line[0])
				#v = var(line[0],line[1], level = 1)
				#return v
	else: #Empty
		v = class_main.var(line[0],line[1], level = 1)
		return v

# def check_main(file): Main pronadjen u get_blocks
# 	for line in file:
# 		if line.startswith('main'):
# 			line = fn_strip(line)

if __name__ == "__main__":
	brs = ['(', ')']

	operators = ['=','+','-','*','/','<','>','>=','<=','==','!='] #minus i podeljeno cu kasnije

	side_ops = ['=','==','!=', '<', '>', '<=', '>=']

	reserved = ['if', 'else', 'def', 'for', 'while']

	with open('testing.txt', 'r') as file:
		#check_main(file)
		for line in file:
			line = find_ops(line)
			if line:
				v = get_vars(line)
	print(1)

#check_in_pool(1)

#ako linija ima f-ju, proveriti da li ona vec postoji ili se tek instancira