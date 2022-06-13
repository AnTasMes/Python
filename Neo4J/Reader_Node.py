import xml.etree.ElementTree as ET
import os

elements = {}

class Element:
	mrid = ""
	name = ""
	atributi = {}

	def __init__(self):
		self.mrid = ""
		self.ime = ""
		self.name = ""
		self.atributi = {}

def get_children(root):
	list_of_children = []
	for child in root:
		child.tag = child.tag.split('}').pop(1)
		list_of_children.append(child.tag)
	list_of_children = list(dict.fromkeys(list_of_children))
	return list_of_children

def get_and_export_data(list_of_children, tree, file_name):
	list_of_dataframes = []
	list_of_elments = {}
	for elem in list_of_children: #Element je glavni TAG (ConnectivityNode, ACLineSegment, Terminal,.....) REDOVI		
		list_of_dataframes = []
		for node in tree.iter(elem): #Ovde se vrsi Iteracija PO SVAKOM GLAVNOM TAGU (Prolazi se kroz CN, ACLineS......)
			list_of_attribs = []
			dict_of_atribs = {} #Kreiranje i praznjenje listi po iteraciji petlje
			list_of_tags = []
			e = Element()
			e.name = elem
			mrid = ""
			for child in node:	#Ovo je u stvari svaka kolona koji se nalaze u tagovima (Sve u CN, ACLineS........)		
				child.tag = child.tag.split('}').pop(1)
				list_of_tags.append(child.tag) #Pravi se lista tagova (child)
				if child.text is not None:			
					dict_of_atribs[child.tag] = child.text
				else:
					dict_of_atribs[child.tag] = child.attrib.values()
				
				if child.tag == "IdentifiedObject.mRID":
					e.mrid = child.text
					mrid = child.text
				elif child.tag == "IdentifiedObject.name":
					if e.name == "":
						e.name = child.text
				else:	
					if not child.text is not None:			
						e.atributi[child.tag.rpartition('.')[2]] = list(child.attrib.values())[0]
						#e.atributi[child.tag.rpartition('.')[2]] = child.text
					#else:
						#e.atributi[child.tag.rpartition('.')[2]] = list(child.attrib.values())[0]
			elements[mrid] = e

def get_locs(path):
	list_of_locs = []
	for roots, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.xml'):
				loc = f'{roots}/{file}'.replace('\\','/')
				list_of_locs.append(loc)
	return list_of_locs

def get_file_name(path):
	file_name = path.split('/')[-1].replace('.xml','')
	return file_name

locs = []
path = r'D:/Phy/CIM/DATA/CIM_RDF_23042021_DELTA_24/LV/RP_IVERKA__20KV/DV_BUKOVSKA_VAS__D20_1000186_LV_20210423150910.xml'
children = []

def getRelations(path):
	locs = get_locs(path)
	for file in locs:
		tree = ET.parse(file)
		root = tree.getroot()
		children = get_children(root)
		f_name = get_file_name(file)
		get_and_export_data(children, tree, f_name)


	refined_elements = []	
	for key in elements:
		e = elements[key]
		row = {}
		row["NODE"] = e.name
		row["mRID"] = key
		for k in e.atributi:
			e2 = e.atributi[k]
			if e2[1:] in elements.keys():
				row[k+"RelationNODE"] = elements[e2[1:]].name
				row[k+"RelationID"] = elements[e2[1:]].mrid
			row[k+"Veza"] = e2[1:]
			refined_elements.append(row)
	
	return refined_elements	