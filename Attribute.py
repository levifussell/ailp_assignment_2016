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


# static factory class for building attributes
class AttributeFactory:

    @staticmethod
    def createAttribute(name, value):
        # get the class of the attribute value
        attrClass = AttributeFactory.__valueToAttributeType(value)

        # create the associated class
        return attrClass(name, value)

    @staticmethod
    def __valueToAttributeType(value):

        try:
            value = float(value)
            return AttributeNumber
        except ValueError:
            if type(value) == str:
                val_lower = value.lower()
                if val_lower == 'true' or val_lower == 'false':
                    return AttributeBool
                else:
                    return AttributeString