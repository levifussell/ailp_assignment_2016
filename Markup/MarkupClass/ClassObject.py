class ClassObject:
    """A markup class object used for organsigin markup data into objects"""
    def __init__(self, name):
        self.name = name
        self.attributes = []

    def addAttribute(self, attribute):
        """Add an attribute field to the class"""
        self.attributes.append(attribute)

    def findAttributeByName(self, nameSearch):
        """Find an attribute based on its name"""
        for i in range(0, len(self.attributes)):
            if self.attributes[i].name == nameSearch:
                return self.attributes[i]
        
        raise NameError('attribute name not found')

    def getDefinitionList(self):
        """Return a list of the name and all important attribute names of this object"""
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