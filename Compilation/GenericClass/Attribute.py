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