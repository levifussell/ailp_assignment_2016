# AILP Assignment 2
**2016**

This assignment introdcues implementing a system for running a Carneades argumentation Python framework implementation via a raw text file. The syntax of the _Carneades Markup Language_ used in writing the text files is described in detail below:

**Carneades Markup Language (CML)**
The _Carneades Markup Language_ is a basic markup language that is used to simplify the compiling of Carneades Python programs. It immitates a simplified version of basic markup:

```xml
<MarkupObject>
  <attributeOfObject>big</attributeOfObject>
  <anotherAttributeOfObject>200</anotherAttributeOfObject>
</MarkupObject>

<!> This is a one line comment </!>
```

The simplified implementation uses only two layers of markup to describe different Carneades classes. The highest order line, 

```xml
<MarkupObject>...</MarkupObject>
```

represents the definition of a Carneades class. The possible Carneades classes to create are:

```xml
<Proposition>...</Proposition>
<Argument>...</Argument>
<CAES>...</CAES>
```
