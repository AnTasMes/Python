class Table():
    listOfPK = []
    lsitOfFK = []
    string = ''

    def __init__(self, name: str, arguments: list) -> None:
        self.name = name
        self.arguments = arguments

    def createTable(self, close=True, args=[], **kwargs):
        self.listOfPK = []
        self.lsitOfFK = []
        self.string = ''
        self.string = f'CREATE TABLE {self.name} ( '
        # print(self.name, self.arguments)

        for arg in self.arguments:
            if arg.startswith('#'):
                arg = arg[1:]
                self.listOfPK.append(arg)
            self.string += f'{arg} int, '
        self.string += 'PRIMARY KEY ( '

        for PK in self.listOfPK:
            self.string += f'{PK}, '
        self.string = self.string[:-2]
        self.string += ' )'
        if not close:
            self.string += ','
            for a in args:
                self.string += f'{a},'
            self.string = self.string[:-2]
            self.string += '));'
        else:
            self.string += ');'

        return self.string
        # print(self.string)
