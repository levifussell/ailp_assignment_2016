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

**classes**

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

**attributes**

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
The _class/attribute_ combinations (constructors) for each class are displayed below. Optional _attributes_ are indicated by a comment: 

```xml
<!>PROPOSITIONS<!>
<Proposition>
  <name>...name ID of proposition...</name>
  <truth>...truth value of the proposition. Default value is 'True'...</truth> <!>optional<!>
  <proof>...standard of proof for the proposition. Default value is 'scintilla'...</proof> <!>optional<!>
</Proposition>

<Proposition>
  <name>...name ID of proposition...</name>
  <negate>...name-tag of the proposition to copy and negate...</negate>
  <proof>...standard of proof for the proposition. Default value is 'scintilla'...</proof> <!>optional<!>
</Proposition>

<!>ARGUMENTS<!>
<Argument>
  <name>...name ID of argument...</name>
  <conclusion>...conclusional proposition of the argument...</conclusion>
  <premises>...[list, of, premises, of, the, argument]...</premises>
  <exceptions>...[list, of, exceptions, of, the, argument]...</exceptions> <!>optional<!>
  <weight>...float value of the weight of this argument...</weight>
  <weight></weight>
</Argument>

<!>CAES<!>
<CAES>
  <name>...name ID of argument...</name>
  <assumptions>[list, of, propositions, that, are, audience, assumptions]</assumptions>
</CAES>
```
Some syntactical notes:
* There are 6 types of attributes of which 4 are used when writing CML:
  1. _String_: any attribute that has written text (without '...') is a string
  2. _Number_: any attribute that has only a float value is a number (i.e. 0.6)
  3. _Bool_: any attribute that contains the word true/false with any capitalisation is a bool. This overrides a string type
  4. _StringList_: any attribute that starts and ends with '[...]' and contains comma-seperated strings is a string list
* Creating each proposition for the arguments is not strictly necessary. Arguments will intuitively add propositions that are missing from implementation. There are a few special cases:
  1. If the _proof_ value of a proposition needs to be set to a value other than the default, 'scintilla', then a proposition must be predefined before the argument(s).
  2. If a _negated_ proposition needs to be implemented, this can be done by adding the exact string '\_neg' to the start of the proposition's name, like so: 
  ```xml
  ...
  <premises>...[prop1, prop2, neg_prop3]...</premises>
  ...
  ```
  (NOTE: ```neg_prop3``` will make 2 propositions if ```prop3``` has not been defined earlier: ```prop3``` and ```-prop3```)
