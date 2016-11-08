import re
from abc import ABCMeta, abstractmethod

# class _Attribute_Manager:

#     imporAttr = ['name', 'proposition']

#     @staticmethod
#     def isImportantAttr(attrVal):
#         return attrVal.name in _Attribute_Manager.imporAttr

#     @staticmethod
#     def __getImportantAttributesList():    
#         return imporAttr

# ABSTRACT ATTRIBUTE CLASSES:

class Attribute:
    __metaclass__ = ABCMeta

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @abstractmethod
    def toString(self): 
        raise NotImplementedError( "Attribute method toString not implemented" )

class AttributeList(Attribute):
    __metaclass__ = ABCMeta

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        finalStr = self.name + ': '

        for i in range(0, len(self.value)):
            finalStr += str(self.value[i]) + '|'

        return finalStr + ' (list ' + str(type(self.value)) + ')'

    @abstractmethod
    def __extractList(self): 
        raise NotImplementedError( "AttributeList method __extractList not implemented" )

# ATTRIBUTE IMPLEMENTATIONS:

class AttributeNumber(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, float(value))

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (number)'

class AttributeBool(Attribute):

    def __init__(self, name, value):
        v = True
        if value.lower() == 'false':
            v = False

        Attribute.__init__(self, name, v)

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (bool)'

class AttributeString(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        return self.name + ': ' + self.value + ' (string)'

class AttributeStringList(AttributeList):

    def __init__(self, name, value):
        AttributeList.__init__(self, name, value)

        self.__extractList()

    def __extractList(self):
        items = re.findall('\w.+?[\,|\]]', self.value, re.DOTALL)

        self.value = []
        print('hi')
        for i in range(0, len(items)):
            self.value.append(items[i][0:(len(items[i]) - 1)])

class AttributeTupleList(AttributeList):

    def __init__(self, name, value):
        AttributeList.__init__(self, name, value)

        self.__extractList()

    def __extractList(self):
        tuples = re.findall('\(\w.+?\)', self.value, re.DOTALL)

        self.value = []
        for i in range(0, len(tuples)):
            items = tuples[i][1:(len(tuples[i]) - 1)].split(',')
            self.value.append((items[0], items[1]))

class AttributeDictList(AttributeList):

    def __init__(self, name, value):
        AttributeList.__init__(self, name, value)
        
        self.__extractList()

    def __extractList(self):
        tuples = re.findall('\(\w.+?\)', self.value, re.DOTALL)

        self.value = {}
        for i in range(0, len(tuples)):
            items = tuples[i][1:(len(tuples[i]) - 1)].split(',')
            self.value[items[0]] = float(items[1])

        
