from .Attribute import AttributeNumber, AttributeBool, AttributeString, AttributeStringList, AttributeTupleList, AttributeDictList

class AttributeFactory:
    """Factory for creating attribute objects given a value from the markup"""

    @staticmethod
    def createAttribute(name, value):
        # get the class of the attribute value
        attrClass = AttributeFactory.__valueToAttributeType(value)

        # create the associated class
        return attrClass(name, value)

    @staticmethod
    def __valueToAttributeType(value):
        """Analyses the value type to determine the attribute class to build"""

        try:
            # attempt to parse value to number
            value = float(value)
            return AttributeNumber
        # if fails, try other attributes
        except ValueError:
            # first check that the value is a string
            if type(value) == str:
                # convert value to a generic value
                val_lower = value.lower()
                
                # test if value is boolean
                if val_lower == 'true' or val_lower == 'false':
                    return AttributeBool
                # check if value contains a list structure
                elif val_lower[0] == '[':
                    try:
                        # check for tuple structure
                        if val_lower[1] == '(':
                            return AttributeTupleList
                        else:
                            return AttributeStringList
                    except:
                        return AttributeStringList
                # check if value contains a dictionary structure
                elif val_lower[0] == '{':
                    return AttributeDictList
                else:
                    return AttributeString