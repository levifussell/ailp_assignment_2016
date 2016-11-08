import re
from abc import ABCMeta, abstractmethod

# ABSTRACT ATTRIBUTE CLASSES:

class Attribute:
    """Abstract attribute class defining a single property of a markup class"""
    __metaclass__ = ABCMeta

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @abstractmethod
    def toString(self): 
        raise NotImplementedError( "Attribute method toString not implemented" )

class AttributeList(Attribute):
    """Abstract attribute list class defining a single property that utilises a list"""
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
    """A markup attribute that uses a float value"""
    def __init__(self, name, value):
        Attribute.__init__(self, name, float(value))

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (number)'

class AttributeBool(Attribute):
    """A markup attribute that uses a boolean value"""
    def __init__(self, name, value):
        v = True
        if value.lower() == 'false':
            v = False

        Attribute.__init__(self, name, v)

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (bool)'

class AttributeString(Attribute):
    """A markup attribute that uses a string value"""
    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        return self.name + ': ' + self.value + ' (string)'

class AttributeStringList(AttributeList):
    """A markup attribute that uses a list of string values"""
    def __init__(self, name, value):
        AttributeList.__init__(self, name, value)

        self.__extractList()

    def __extractList(self):
        items = re.findall('\w.+?[\,|\]]', self.value, re.DOTALL)

        self.value = []
        for i in range(0, len(items)):
            self.value.append(items[i][0:(len(items[i]) - 1)])

class AttributeTupleList(AttributeList):
    """A markup attribute that uses a list of tuple values"""
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
    """A markup attribute that uses a dictionary value"""
    def __init__(self, name, value):
        AttributeList.__init__(self, name, value)
        
        self.__extractList()

    def __extractList(self):
        tuples = re.findall('\(\w.+?\)', self.value, re.DOTALL)

        self.value = {}
        for i in range(0, len(tuples)):
            items = tuples[i][1:(len(tuples[i]) - 1)].split(',')
            self.value[items[0]] = float(items[1])
        
