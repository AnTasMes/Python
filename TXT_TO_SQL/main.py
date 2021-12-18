import os
from table import Table


def getData(path):
    locs = []
    for roots, dirs, files in os.walk(path):
        for file in files:
            fileLoc = f"{roots}/{file}".replace('\\', '/')
            locs.append(fileLoc)
    return locs


def addTable(line):
    table, arguments = line.replace(')', '').split('(')
    arguments = arguments.split(',')
    return table, arguments


def getFK(line, refSplit='referencira', **kwargs):
    line = line.split(refSplit)
    print(line)
    base, FK = line[0].replace(')', '').split('(')
    target = line[1]
    string = f'{base}:///Foreign key ({FK}) references {target}'
    return string


def hasFKlist(strList):
    tmpList = []
    for string in addStringList:
        tableName, mid, SQL = string.partition(':///')
        tmpList.append(tableName)

    return list(set(tmpList))


def hasNOFKlist(tblNames: list, hasFKlist: list):
    tmpList = []
    for tbl in tblNames:
        if tbl in hasFKlist:
            pass
        else:
            tmpList.append(tbl)

    return tmpList


if __name__ == '__main__':
    path = r"D:\Programming\Python\TXT_TO_SQL\DATA"
    exactPath = r"D:\Programming\Python\TXT_TO_SQL\DATA\Relacioni model - sredjen.txt"
    tempPath = r"D:\Programming\Python\TXT_TO_SQL\DATA\temp_raw.txt"

    listOfTables = []
    addStringList = []

    with open(exactPath) as file:
        for line in file:
            line = line.replace(' ', '').replace('\t', '').strip('\n')
            if ',' in line:
                table, arguments = addTable(line)
                listOfTables.append(Table(table, arguments))
            elif ',' not in line and line:
                addingString = getFK(line)
                addStringList.append(addingString)

    listOfTableNames = []
    for table in listOfTables:
        listOfTableNames.append(table.name)

    listOfHasFK = hasFKlist(addStringList)
    listofHasNoFK = hasNOFKlist(listOfTableNames, listOfHasFK)
    tmpStringSQL = ''
    for table in listOfTables:
        if table.name in listofHasNoFK:
            tmpStringSQL += table.createTable()+'\n'

    for table in listOfTables:
        tmpArgs = []
        if table.name in listOfHasFK:
            for string in addStringList:
                name, mid,  sql = string.partition(':///')
                if name == table.name:
                    tmpArgs.append(sql)

            tmpStringSQL += table.createTable(close=False, args=tmpArgs)+'\n'
    print(tmpStringSQL)
    sqlPATH = r'D:\Programming\Python\TXT_TO_SQL\DATA\sqlDATA.txt'
    with open(sqlPATH, 'w') as sqlFIle:
        sqlFIle.write(tmpStringSQL)
