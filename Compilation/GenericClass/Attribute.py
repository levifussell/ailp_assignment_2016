import re

class Attribute:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def toString(self):
        return self.name + ': ' + self.value + ' (generic)'

class AttributeNumber(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (number)'

class AttributeBool(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        return self.name + ': ' + str(self.value) + ' (bool)'

class AttributeString(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

    def toString(self):
        return self.name + ': ' + self.value + ' (string)'

class AttributeList(Attribute):

    def __init__(self, name, value):
        Attribute.__init__(self, name, value)

        self.__extractList()

    def __extractList(self):
        items = re.findall('\w.+?[\,|\]]', self.value, re.DOTALL)

        self.value = []
        for i in range(0, len(items)):
            self.value.append(items[i][0:(len(items[i]) - 1)])

    def toString(self):
        finalStr = self.name + ': '

        for i in range(0, len(self.value)):
            finalStr += str(self.value[i]) + '|'

        return finalStr + ' (list)'