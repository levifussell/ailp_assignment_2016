class ClassObject:

    def __init__(self, name):
        self.name = name
        self.attributes = []

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

    def findAttributeByName(self, nameSearch):
        for i in range(0, len(self.attributes)):
            if self.attributes[i].name == nameSearch:
                return self.attributes[i]
        
        raise NameError('attribute name not found')

    # return a list of the name and all attribute names of this object
    def getDefinitionList(self):
        defList = [self.name]
        
        for i in range(0, len(self.attributes)):
            defList.append(self.attributes[i].name)

        return defList

    def toString(self):
        classObjStr = self.name + ' {\n'

        for i in range(0, len(self.attributes)):
            classObjStr += ' ' + self.attributes[i].toString() + '\n'

        classObjStr += '}\n'

        return classObjStr