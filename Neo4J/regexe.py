import re

relate = ''
ln = "ConnectivityNodeRelationsNODE"
x = re.findall("RelationsNODE", ln)

node = {'NODE': 'ACLineSegment', 'mRID': '_7E75B739-9B71-41EF-BD2D-ABF4B134C1EB', 'PerLengthImpedanceRelationNODE': 'PerLengthSequenceImpedance', 'PerLengthImpedanceRelationID': '_9b39adac-e0b9-45cb-ac98-40c1900bb728', 'PerLengthImpedanceVeza': '_9b39adac-e0b9-45cb-ac98-40c1900bb728', 'AssetDatasheetRelationNODE': 'WireInfo', 'AssetDatasheetRelationID': '_c73fb632-16ca-4e1c-9d85-68f84324d8c2', 'AssetDatasheetVeza': '_c73fb632-16ca-4e1c-9d85-68f84324d8c2', 'PSRTypeRelationNODE': 'PSRType', 'PSRTypeRelationID': 'Odsek podzemni NN', 'PSRTypeVeza': 'Odsek podzemni NN', 'EquipmentContainerRelationNODE': 'Circuit', 'EquipmentContainerRelationID': '1006194_I01: HABER', 'EquipmentContainerVeza': '1006194_I01: HABER', 'CircuitRelationNODE': 'Circuit', 'CircuitRelationID': '1006194_I01: HABER', 'CircuitVeza': '1006194_I01: HABER'}


#match (p:Person{name:"Andrej"}),(b:Person) where p.relID = b.id or p.relID2 = b.id merge (p)-[r:VEZA {naziv: b.id}]->(b)

for key in node:
	

for key in node:
	if re.findall("RelationNODE", key):
		relate = ("match (a:"+node['NODE']+"{mRID:"+node['mRID']+"}),(b:"+node[key])		
	if re.findall("RelationID",key):
		relate += "{mRID:"+node[key]+"}) merge (a)-[r:"
	if re.findall("Veza",key):
		relate += key[:-4]+"]->(b)"
		print(relate)
