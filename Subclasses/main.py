class MainClass:
    _registry = {}

    def __init_subclass__(cls, prefix, **kwargs) -> None:
        super.__init_subclass__(**kwargs)
        cls._registry[prefix] = cls

    def __new__(cls, path: str, key=None):
        prefix, sufix, string = path.partition(':///')

        subclass = cls._registry[prefix]
        obj = object.__new__(subclass)
        obj.string = string
        obj.prefixString = prefix
        return obj


class SubClass(MainClass, prefix='Sub'):
    def printClass(self):
        print("SUB CLASS: ", self.prefixString, self.string)


class AnotherSubClass(MainClass, prefix='An'):
    def printClass(self):
        print("AN CLASS: ", self.prefixString, self.string)


if __name__ == "__main__":
    MainClass('An:///anotherThing').printClass()
