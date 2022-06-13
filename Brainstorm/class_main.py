class global_main: #globalna klasa koja sluzi za pregled citavog fajla
	lvl_pool = [] #stack blokova sa njihovim nivoima i clanovima

	def add_pool(self,obj):
		self.lvl_pool.append(obj)

class obj_pool:
	pool = []

	def pool_avail():
		if obj_pool.pool:
			return 1
		return 0

	def add_pool(var):
		obj_pool.pool.append(var)

class block(global_main):

	def block_size(self):
		return self.end_index - self.start_index + 1

	def __init__(self, level, start_index, end_index, fns = None, vrs = None): #fns = funkcije koje pripadaju tom bloku, vrs = isto samo varijable
		self.level = level
		self.start_index = start_index
		self.end_index = end_index
		self.working_indexes = [i for i in range(start_index,end_index+1)]

		if fns == None:
			self.fns = []
		else:
			self.fns = fns #nizovi objekata funkcija
		if vrs == None:
			self.vrs = None
		else:
			self.vrs = vrs #nizovi objekata varijabli

		super().add_pool(self)

class var:
	instance_num = 0

	def incr(self):
		self.instance_num += 1

	def __init__(self, name, value, level): #varijablama se dodeljuje nivo kojem pripadaju
		self.name = name
		self.value = value
		self.tp = type(value)

		obj_pool.add_pool(self)

		self.incr()

class fn(block):
	instance_num = 0

	def incr(self):
		self.instance_num += 1

	def __init__(self, name, args = None): #funckija odreduje nivo 
		self.name = name
		if args == None:
			self.args = []
		else:
			self.args = args

		obj_pool.add_pool(self)