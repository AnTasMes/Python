class var_pool:
	pool = []

	def check_names(var):
		for elem in var_pool.pool:		
			if var.name == elem.name:								
				return 0
		return 1

	def set_pool(var):
		if not var_pool.pool:
			var_pool.pool.append(var)
		else:
			if var_pool.check_names(var):
				var_pool.pool.append(var)

class fn_pool(var_pool):

	def set_args(self):
		print()

	def __init__(self, name, arg = []):
		self.name = name
		self.arg = self.get_args()

class var(var_pool):
	instance_num = 0

	def __delete__(self, instance):
		del self.value

	def in_increment(self):
		self.instance_num += 1

	def __init__(self, name, value):
		self.tp = type(value)
		self.name = name
		self.value = value
		
		var_pool.set_pool(self)
		self.in_increment()


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
	return None

def check_for_obj(line):
	if var_pool.pool:
		for obj in var_pool.pool:
			if line[0] == obj.name:
				obj.in_increment()
				return obj
			else:
				v = var(line[0],line[1]) #line[0] ime, line[1] vrednost
				return v
	else:
		v = var(line[0],line[1])
		return v


operators = ['=','+','-','*','/','<','>','>=','<=','==','!='] #minus i podeljeno cu kasnije

side_ops = ['=','==','!=', '<', '>', '<=', '>=']

with open('testing.txt', 'r') as file:
	for line in file:
		array = find_ops(line)
		if array:	
			v = check_for_obj(line)	

print(var_pool.pool)




#ovo se pokrece po bloku

# with open('testing.txt','r') as file:
# 	for line in file:
# 		for op in operators:
# 			if op in line:
# 				line = trim_by_op(op,line) #finding operators
# 				find_vars(line[0])
# 				v = var(line[0],line[1])
# 				print(line)
# 			if len(line) > 0:
# 				if op in line[1]:
# 					print(op) #ovo neka ostane za sada
# print(v.instance_num)
# #print(var_pool.pool[0].value)




#resavanje imena promenljivih kroz blokove (kasnije)