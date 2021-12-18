import string


class Table:
    """
    Class defining a simple SQL table with PKs and FKs

    Attributes
    ----------
    Name : str 
        Name of the table

    Arguments : list[str]
        Columns of the table

    PKs : list
        List of primary keys of the table

    FKs : list[list[]]
        List of foreign keys and tables referencing
        eg. [[Foreign Key, Target, Target Key]]

    SQLString : str
        String that forms the sql querry after running

    Methods
    -------
    addFK(recTable, key, recKey)
        Adds a Foreign key to the object

    makeSelfSQL(self)
        returns an SQL Create Table querry for the object

    isReady(tblInUse)
        checks whether this table is ready to be written in the querry
        If the table has met all the requirements it can be written in the querry
        and it wont produce any syntaxial problems
    """

    def __init__(self, name, *args) -> None:
        """
        name: str
            Name of the table
        *args : str
            A list of arguments/columns of the table 

        example: Table1 (ID, Name, Age)
        """
        self.Name = name
        self.Arguments = list(args)[0]
        self.PKs = []
        self.FKs = []
        self.SQLString = ''

        for i, elem in enumerate(self.Arguments):
            if '#' in elem:
                elem = elem.replace('#', '')
                self.PKs.append(elem)
                self.Arguments[i] = elem

    def __repr__(self) -> str:
        return f'{self.Name} : {self.Arguments}'

    def addFK(self, recTable, key, recKey):
        self.FKs.append([recTable, key, recKey])

    def makeSelfSQL(self):
        self.SQLString = f'CREATE TABLE {self.Name} ('
        self.SQLString += ' int, '.join([a for a in self.Arguments]) + ' int, '
        self.SQLString += ' PRIMARY KEY ( '
        self.SQLString += ' , '.join([pk for pk in self.PKs]) + ' )'

        if self.FKs:
            self.SQLString += ' , '
            for i, fk in enumerate(self.FKs):
                self.SQLString += f'FOREIGN KEY ({fk[1]}) REFERENCES {fk[0]}({fk[2]})'
                if i < len(self.FKs)-1:
                    self.SQLString += ' , '
        self.SQLString += ');'

    def isReady(self, tblInUse):
        if not self.FKs:
            return True
        for fk in self.FKs:
            if fk[0] in tblInUse or fk[0] == self.Name:
                pass
            else:
                return False  # moze ispod da se doda i ako nije u tabeli, ali ovako mi se svidja
        return True
