import enum
from table2 import Table
import string


def makeTable(line):
    name, arguments = line.replace(')', '').split('(')
    arguments = arguments.split(',')
    return Table(name, arguments)


def findObjectIndex(list: list, name: str):
    for index, obj in enumerate(list):
        if obj.Name == name:
            return index
    return None


def getData(path: str, refSplit: str = 'refna'):
    """
    Function for getting the data from the PMOV file

    Parameters
    ----------
    path : str
        Destination of the file
    refSplit : str, optional
        String splitting two tables where one references another
        eg. Table1(RmKey) references Table2(sKey)

    Returns
    ----------
    listOfTables : list[Table]
        A list of objects : Table
    """
    listOfTables = []
    with open(path, 'r') as file:

        for line in file:
            line = line.replace(' ', '').replace('\t', '').strip()
            if line:
                if refSplit in line:
                    mainTbl, recieverTbl = line.split(refSplit)
                    mainTbl, key = mainTbl.replace(')', '').split('(')
                    recieverTbl, nKey = recieverTbl.replace(')', '').split('(')

                    listOfTables[findObjectIndex(listOfTables, mainTbl)].addFK(  # Finds the object where Foreign Keys have to be added
                        recieverTbl, key, nKey)
                else:
                    listOfTables.append(makeTable(line))

    for tbl in listOfTables:
        tbl.makeSelfSQL()

    return listOfTables


def main():
    path = r'D:\Programming\Python\TXT_TO_SQL\DATA\raw_data.txt'
    rm = r'D:\Programming\Python\TXT_TO_SQL\DATA\Relacioni model - sredjen.txt'
    ExportPath = r'D:\Programming\Python\TXT_TO_SQL\DATA\expoSQL.txt'
    Tables = getData(rm, refSplit='referencira')
    tablesInUse = []
    with open(ExportPath, 'w+') as file:
        while len(tablesInUse) < len(Tables):
            for tbl in Tables:
                if tbl.isReady(tablesInUse) and not tbl.Name in tablesInUse:
                    file.write(f'{tbl.SQLString}\n')
                    tablesInUse.append(tbl.Name)


if __name__ == '__main__':
    main()
