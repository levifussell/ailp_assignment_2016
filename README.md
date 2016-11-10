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
<CMLObject>...</CMLObject>
```

represents the definition of a Carneades class. The only available Carneades classes in CML:

```xml
<Proposition>...</Proposition>
<Argument>...</Argument>
<CAES>...</CAES>
```

(NOTE: classes not implemented such as _ProofStandard, Audience, ArgumentSet_ are all created at compile-time; this design decision will be discussed later)

Each Carneades class has a series of CML _attributes_ that are used to define unique details about the specific objects. Without these _attributes_ implemented, the generic classes will fail. It is important to note that the order in which _attributes_ are written does not matter, but only some _attributes_ can be excluded (similar to the concept of a constructor). An _attribute_ is defined as a markup object that is one layer inside a markup _class_ object (which is always at layer one) and has a _value item_ one layer inside it:

```xml
<CMLObject>
  <CMLAttribute>value_of_attribute</CMLAttribute>
</CMLObject>
```

The inclusion of the _value item_ (```value_of_attribute_```) is required for the object to be an _attribute_. The name of the value, class objects and attribute objects follow the general naming scheme of python variables. _Attributes_ are written in series:

```xml
<CMLObject>
  <CMLAttribute1>value_of_attribute1</CMLAttribute1>
  <CMLAttribute2>value_of_attribute2</CMLAttribute2>
</CMLObject>
```
And order (as well as spacing) is irrelevant:

```xml
<CMLObject>

  <CMLAttribute2> value_of_attribute2 </CMLAttribute2>
  
  <CMLAttribute1>value_of_attribute1</CMLAttribute1>
</CMLObject>
```
