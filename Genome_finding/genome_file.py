class FASTA_FILE:
    def __init__(self, **kwargs):
        self.prefix = kwargs['prefix']
        self.path = kwargs['path']

    def findGenome(self):
        with open(self.path) as file:
            print(file)
