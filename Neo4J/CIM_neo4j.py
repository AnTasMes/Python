from neo4j import GraphDatabase as gd
import xml.etree.ElementTree as ET

import os
import re
from Reader_Node import getRelations

def get_nodes_from_xml(path_to_xml):
	tree = ET.parse(path_to_xml)
	root = tree.getroot()
	list_of_children = []
	list_of_nodes = []
	for child in root:
		child.tag = child.tag.split('}').pop(1)
		list_of_children.append(child.tag)

	list_of_children = list(dict.fromkeys(list_of_children))
	
	for child in list_of_children:		
		for node in tree.iter(child):
			node_dict = {}
			node_dict['NODE'] = node.tag
			node_dict['mRID'] = list(node.attrib.values())[0]
			for column in node:
				column.tag = column.tag.split('}').pop(1)
				column.tag = column.tag.split('.')
				if column.attrib:					
					if list(column.attrib.values())[0][0] == "#":
						column.attrib[list(column.attrib.keys())[0]] = column.attrib[list(column.attrib.keys())[0]][1:]
					node_dict[column.tag[-1]] = list(column.attrib.values())[0] #<NODE: ConnNode mRID: _75af5797-eaea-45da-ab84-c9b3b69c3df4 ConnectivityNodeContainer: 1006193_I02: KUREJ> 
				if column.text:
					node_dict[column.tag[-1]] = column.text
			list_of_nodes.append(node_dict)
	return list_of_nodes 
					
def get_files(path):
	list_of_locs = []
	for roots, dirs, files in os.walk(path):
		for file in files:
			if file.endswith('.xml'):
				loc = f'{roots}/{file}'.replace('\\','/')
				list_of_locs.append(loc)
	return list_of_locs

def make_node(node):
	create = f"CREATE (n:{node['NODE']} "+"{mRID: '"+node['mRID']+"'"  #CREATE (n:ConnectivityNode {mRID: '_23fcf0cf-cb8f-4cd5-8d6a-6e15c22bec97'})
	for key in node:
		if key == 'mRID' or key == 'NODE':
			continue
		create += ","+key+":'"+node[key]+"'"
	create += "})"
	print(create)
	session.run(create)

def set_relations(node):
	#print(f"SETTING UP: {node['NODE'], node['mRID']}")
	relate = ''
	for key in node:
		try:
			if re.findall("RelationNODE", key):
				relate = ("match (a:"+node['NODE']+"{mRID:'"+node['mRID']+"'}),(b:"+node[key])
				has_node = 1		
			if re.findall("RelationID",key):
				relate += "{mRID:'"+node[key]+"'}) merge (a)-[r:"
				has_node += 1
			if re.findall("Veza",key):
				relate += key[:-4]+"]->(b)"			
				if has_node == 2:
					session.run(relate)
					print(relate) 	#(b:ACLineSegment{mRID:"_D59AD9BF-08EF-4969-AFB1-560534E00C55"}) merge (a)-[r:ConCont]->(b)
		except:
			break
			
#------ MAKING CONNECTION ------

database_connecton = gd.driver(uri = 'neo4j://localhost:7687', auth=('neo4j','123'))
session = database_connecton.session()

#------ GETTING IMPORTANT DATA ------

#path = r'D:/Phy/CIM/DATA/CIM_RDF_23042021_DELTA_24/LV/RP_IVERKA__20KV/DV_BUKOVSKA_VAS__D20_1000186_LV_20210423150910.xml'
#dir_path = r'D:/Phy/CIM/DATA/CIM_RDF_23042021_DELTA_24/LV/RP_IVERKA__20KV/' 
main_dir_path = r'D:/Phy/CIM/DATA/'

files = get_files(main_dir_path)
relations = getRelations(main_dir_path)

if __name__ == "__main__":
	print("SETTING UP NODES.....")	
	for file in files:
		nodes = get_nodes_from_xml(file)
		#print(f"\nFILE: {file} working....\n")
		for node in nodes:
			#print(node['NODE'],node['mRID'])
			make_node(node)

	print("SETTING UP RELATIONS.....")	
	for related in relations:
		set_relations(related)

	
		



#def make_node_old(node):
#	create = f"CREATE (n:{node['NODE']} "+"{mRID: '"+node['mRID']+"'}"+")"  #CREATE (n:ConnectivityNode {mRID: '_23fcf0cf-cb8f-4cd5-8d6a-6e15c22bec97'})
#	session.run(create)
#	for key in node:
#		if key == "mRID" or key == "NODE":
#			continue
#		add_attribs = "MATCH (n:"+node['NODE']+"{mRID:'"+node['mRID']+"'}) SET n."+key+" = '"+node[key]+"'"	#MATCH (n:ConnectivityNode{mRID:'_23fcf0cf-cb8f-4cd5-8d6a-6e15c22bec97'}) SET n.ConnectivityNodeContainer = '#1006194_I01: HABER'
#		session.run(add_attribs)

""" Ovo koristiti samo kada se zavrsi pun algoritam jer traje dugo
if __name__ == "__main__":
	for file in files:
		list_of_nodes = get_nodes_from_xml(file)
		for node in nodes:
			make_node(node)
"""