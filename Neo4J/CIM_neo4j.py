from neo4j import GraphDatabase as gd
import xml.etree.ElementTree as ET

import os

path = r'D:/Phy/CIM/DATA/CIM_RDF_23042021_DELTA_24/LV/RP_IVERKA__20KV/DV_BUKOVSKA_VAS__D20_1000186_LV_20210423150910.xml'
dir_path = r'D:/Phy/CIM/DATA/' 

database_connecton = gd.driver(uri = 'neo4j://localhost:7687', auth=('neo4j','123'))
session = database_connecton.session()




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
		node_dict = {}
		for node in tree.iter(child):
			node_dict['NODE'] = node.tag
			node_dict['mRID'] = list(node.attrib.values())[0]
			for column in node:
				if column.attrib:
					column.tag = column.tag.split('}').pop(1)
					column.tag = column.tag.split('.')
					node_dict[column.tag[-1]] = list(column.attrib.values())[0] #<NODE: ConnNode mRID: _75af5797-eaea-45da-ab84-c9b3b69c3df4 ConnectivityNodeContainer: 1006193_I02: KUREJ 
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
	print(f"----- MAKING {node['NODE']} -----")
	create = f"CREATE (n:{node['NODE']} "+"{mRID: '"+node['mRID']+"'}"+")"  #CREATE (n:ConnectivityNode {mRID: '_23fcf0cf-cb8f-4cd5-8d6a-6e15c22bec97'})
	print(create)
	#session.run(create)
	print(f"----- ADDING ATTRIBUTES -----")
	for key in node:
		if key == "mRID" or key == "NODE":
			continue
		add_attribs = "MATCH (n:"+node['NODE']+"{mRID:'"+node['mRID']+"'}) SET n."+key+" = '"+node[key]+"'"	#MATCH (n:ConnectivityNode{mRID:'_23fcf0cf-cb8f-4cd5-8d6a-6e15c22bec97'}) SET n.ConnectivityNodeContainer = '#1006194_I01: HABER'
		print(add_attribs)
		#session.run(add_attribs)

def set_relations(node):
	list_of_statements = []
	#print(node['node'], node['attribs']['relID'],node['relation']['node'],node['relation']['attribs']['relID'])
	#relate = ("match (n:"+node['node']+" {relID: '"+node['attribs']['relID']+"' }),"
			#"(b:"+node['relation']['node']+"{relID: '"+node['relation']['attribs']['relID']+"'}) merge (n)-[r:A]->(b) return n,b")
	print(relate)
	session.run(relate)


files = get_files(dir_path)
nodes = get_nodes_from_xml(path)


""" Ovo koristiti samo kada se zavrsi pun algoritam jer traje dugo i mora da se sredi logika
if __name__ == "__main__":
	for file in files:
		list_of_nodes = get_nodes_from_xml(file)
		for node in nodes:
			make_node(node)
"""
if __name__ == "__main__":
	for node in nodes:
		make_node(node)