import class_main


def trim_to_fn(line):
	function = []
	line = line.replace(' ','').replace('def','').replace('{\n','')
	name, args = line.split('(')
	args, temp = args.split(')')
	if args == '':
		args = None
	else:
		args = args.split(',')
	function.append(name)
	function.append(args)
	return function

def get_names():
	names = []
	for nm in class_main.obj_pool.pool:
		names.append(nm.name)
	return names

def get_lvls():
	lvls = []
	for lvl in class_main.global_main.lvl_pool:
		lvls.append(lvl.level)
	if lvls:
		return max(lvls)+1
	return 1

def check_obj_pool(name):
	names = get_names()
	if class_main.obj_pool.pool_avail():
		if name in names:
			return 0
		else:
			return 1
	else:
		return 1

def add_to_fn(function, start_index, end_index):
	if check_obj_pool(function[0]):
		fun = class_main.fn(function[0], args = function[1])
		b = class_main.block(get_lvls(), start_index, end_index, fun) #dodaje nivoe funckijama i blokovima
		#print(b.level, b.fns.name, b.fns.args) #testing print za blokove i funkcije
			
if __name__ == "__main__": #dobijamo definisanje funkcija
	with open('testing.txt', 'r') as file: 
		for main_line in enumerate(file):
			line = main_line[1]				#0 je index, 1 je vrednost linije
			index = main_line[0]
			if line.startswith('def'): #ako pocinje sa def, onda je funkcija
				start_index = index
				function = trim_to_fn(line)
			if line.startswith('}'):
				end_index = index
				add_to_fn(function, start_index, end_index) #indexi sluze kako bi odredili od kog do kog dela ide funkcija (kom nivou pripadaju ti indexi)
				
	for i,obj in enumerate(class_main.global_main.lvl_pool):
		print("---------------------------------------------------------------------")
		print("level: ",class_main.global_main.lvl_pool[i].level)
		print("fns.name: ",class_main.global_main.lvl_pool[i].fns.name)
		print("args: ",class_main.global_main.lvl_pool[i].fns.args)
		print("start_index: ",class_main.global_main.lvl_pool[i].start_index)
		print("end_index: ",class_main.global_main.lvl_pool[i].end_index)
		print("block_size: ",class_main.global_main.lvl_pool[i].block_size())
		print("working_indexes: ",class_main.global_main.lvl_pool[i].working_indexes)

print("---------------------------------------------------------------------")

	

