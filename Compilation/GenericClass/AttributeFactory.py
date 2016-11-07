from .Attribute import AttributeNumber, AttributeBool, AttributeString, AttributeList

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
                elif val_lower[0] == '[':
                    return AttributeList
                else:
                    return AttributeString