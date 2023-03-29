class mainSeq:
    count = {'TTG': 0, 'TAT': 0, 'AGG': 0, 'AGT': 0, 'END': 0}
    steps = 0

    def increaseCount(self, key):
        self.count[key] += 1
        return self.count[key]

    def resetCount(self):
        for c in self.count:
            self.count[c] = 0

    def increaseSteps(self):
        self.steps += 1

    def resetSteps(self):
        self.steps = 0


class Sequence(mainSeq):
    _registry = {}

    def __init_subclass__(cls, seq: str, **kwargs) -> None:
        super.__init_subclass__(**kwargs)
        cls._registry[seq] = cls

    def __new__(cls, seq: str, **kwargs):
        subclass = cls._registry[seq]
        obj = object.__new__(subclass)
        obj.sequence = seq
        if 'cord' in kwargs:
            obj.cord = kwargs['cord']
        else:
            obj.cord = [0, 0]
        obj.id = cls.increaseCount(cls, seq[:3])

        return obj

    # Checks for difference in two sequences
    def findPrev(self, currObj: object, prevObj: object, **kwargs):
        if currObj.space == [0, 0]:
            return 1
        diff = currObj.cord[0] - prevObj.cord[1]
        if diff >= currObj.space[0] and diff <= currObj.space[1]:
            return 1
        return 0


class TTG(Sequence, seq='TTGACA'):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.space = [0, 0]
        self.failSpace = len(self.sequence) - 1

    def __repr__(self) -> str:
        return repr(f"ID: {self.id} ==> SEQUENCE: '{self.sequence}' ; COORDS: {self.cord}")

    def findPrev(self, prevObj: object):
        return super().findPrev(self, prevObj)


class TAT(Sequence, seq='TATAAT'):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.space = [15, 19]
        self.failSpace = len(self.sequence) - 1

    def __repr__(self) -> str:
        return repr(f"ID: {self.id} ==> SEQUENCE: '{self.sequence}' ; COORDS: {self.cord}")

    def findPrev(self, prevObj: object):
        return super().findPrev(self, prevObj)


class AGG(Sequence, seq='AGGAGGT'):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.space = [0, 0]
        self.failSpace = len(self.sequence) - 1

    def __repr__(self) -> str:
        return repr(f"ID: {self.id} ==> SEQUENCE: '{self.sequence}' ; COORDS: {self.cord}")

    def findPrev(self, prevObj: object):
        return super().findPrev(self, prevObj)


class AGT(Sequence, seq='AGT'):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.space = [5, 9]
        self.failSpace = 3

    def __repr__(self) -> str:
        return repr(f"ID: {self.id} ==> SEQUENCE: '{self.sequence}' ; COORDS: {self.cord}")

    def findPrev(self, prevObj: object):
        return super().findPrev(self, prevObj)


class TAA(Sequence, seq='END'):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.space = [900, 100]
        self.sequences = ['TAA', 'TAG', 'TGA']
        self.failSpace = 3

    def __repr__(self) -> str:
        return repr(f"ID: {self.id} ==> SEQUENCE: '{self.sequence}' ; COORDS: {self.cord}")

    def findPrev(self, prevObj: object):
        return super().findPrev(self, prevObj)


if __name__ == "__main__":
    sequenceArray = []
    sequenceArray.append(Sequence('TTGACA'))
    sequenceArray.append(Sequence('TATAAT'))
    sequenceArray.append(Sequence('AGGAGGT'))

    mainSeq.resetCount(mainSeq)
    sequenceArray[0].cord = [20, 23]
    sequenceArray[1].cord = [39, 42]
    one = sequenceArray[2].findPrev(sequenceArray[1])
    print(one)
