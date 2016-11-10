# AILP Assignment 2
**2016**

This assignment asks to implement a system for running a Carneades argumentation Python framework implementation via a raw text file. The syntax of the text file will be referred to as, _Carneades Markup Language_. Understanding this new markup langauge is described below:

**running the test files**

The test files that can be run are `codeTest1.txt`, `codeTest2.txt` and `codeTest3.txt` located in the directory `CodeTests/`. To run these files, run the file `main.py` in the cmd with python3.4 and type either `1`, `2` or `3`. The logger output mode can be set from the `\_Logger\_Thread` class in the `\_LoggerManager.py` file. Currently the Log behaviour is set to _WARNING_, but setting this to _DEBUG_ will give more intuitive output. Setting the Log to only _ERROR_ will make sure it only displays errors and the ouput Carneades, which is useful for analysing the results.

**Carneades Markup Language (CML)**

The _Carneades Markup Language_ is a basic markup language that is used to simplify the compiling of Carneades Python programs. It immitates a simplified version of basic markup:

```xml
<MarkupObject>
  <attributeOfObject>big</attributeOfObject>
  <anotherAttributeOfObject>200</anotherAttributeOfObject>
</MarkupObject>

<!> This is a one line comment <!>
```

**classes**

The simplified markup implementation uses only two layers of markup to describe different Carneades classes. The highest order line, 

```xml
<CMLObject>...</CMLObject>
```

represents the definition of a Carneades class. The only available Carneades classes in CML are:

```xml
<Proposition>...</Proposition>
<Argument>...</Argument>
<CAES>...</CAES>
```

(NOTE: classes not implemented, such as _ProofStandard, Audience, ArgumentSet_, are all created at compile-time; this design decision will be discussed later)

**attributes**

Each Carneades class has a series of CML _attributes_ that are used to define unique details about a specific object. Without these _attributes_ implemented, the generic classes will fail. It is important to note that the order in which _attributes_ are written does not matter, but only some _attributes_ can be excluded (similar to the concept of a constructor). An _attribute_ is defined as a markup object that is one markup layer inside a markup _class_ object (which is always at layer zero) and has a _value item_ one layer inside it:

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
Order (as well as spacing) is irrelevant:

```xml
<CMLObject>

  <CMLAttribute2> value_of_attribute2 </CMLAttribute2>
  
  <CMLAttribute3> <!> comment about this attribute, etc... <!>
    value_of_attribute3 
  </CMLAttribute3>
  
  <CMLAttribute1>value_of_attribute1</CMLAttribute1> </CMLObject>
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
</Argument>

<!>CAES<!>
<CAES>
  <name>...name ID of CAES...</name>
  <assumptions>[list, of, propositions, that, are, audience, assumptions]</assumptions>
</CAES>
```
Some syntactical notes:
* There are 6 types of attributes of which 4 are used when writing CML in a text file:
  1. _String_: any attribute that has written text (make sure to exclude '...', unlike other languages)
  2. _Number_: any attribute that has only a float value (i.e. 0.6)
  3. _Bool_: any attribute that contains the word true/false with any capitalisation. This overrides a string type
  4. _StringList_: any attribute that starts and ends with '[...]' and contains comma-seperated strings
* (IMPORTANT) Defining each proposition before the arguments is not strictly necessary. Arguments will intuitively add propositions that are missing from implementation (this will not happen with the _CAES assumptions attribute_, these propositions must be predefined in an argument/proposition. It is important to note that this implementation can be dangerous; miss-spelt proposition names will be treated as _new_ propositions. Be careful!). There are a few special cases:
  1. If the _proof_ value of a proposition needs to be set to a value other than the default value, 'scintilla', then a proposition must be predefined before the argument(s).
  2. If a _negated_ proposition needs to be implemented, this can be done by adding the exact string 'neg\_' to the start of the proposition's name, like so: 
  ```xml
  ...
  <premises>...[prop1, prop2, neg_prop3]...</premises>
  ...
  ```
  (NOTE: ```neg_prop3``` will make 2 propositions if ```prop3``` has not been defined earlier: ```prop3``` and ```-prop3```)

**compiling**

CML aims to simplify Carneades implimentations by minimising the quantity of code needed to prepare a new _CAES_ object. Therefore a design decision was made to remove the creation of _Audiences_, _ProofStandard_ lists, _ArgumentWeights_ and _ArgumentSets_. Each of these are instead compiled in the background. This results in a few limiting tradeoffs. Compilation of each class is described below:
* _ArgumentSet_: all arguments in the system are added to one argument set in order of creation.
* _ProofStandard_: the _proof attribute_ value is taken from all propositions in the system and compiled into a list of tuples.
* _ArgumentWeights_: the _weight attribute_ value is taken from all arguments in the system and compiled into a dictionary.
* _Audience_: the _assumptions attribute_ value is taken from the _CAES class_ and the previously compiled _ArgumentWeights_ is used
A _CAES_ object is then compiled at the end using the background objects.

# System Design

**this section is irrelevant to knowing how to use CML, but briefly outlines the underlying process of reading and compiling a CML file:**

**reading a CML file**

A CML file is read recursively until the end of the file. Each markup object is read and processed and then seperated into its smaller markup object components and read and processed until the recursion reaches an end. The markup objects are sequentially added to an 'object stack'.

The next step is to read from this 'object stack'. If a 'value' item is popped from the stack, than the next item is popped from the stack (which should be a 'variable' item) and the 'value'/'variable' pair is added to an _attribute queue_ as an attribute. This process continues until a 'variable' item is popped without a 'value' item pairing before it. This varaible should be a markup class and therefore all attributes are taken from the _attribute queue_ and combined with the popped 'variable' item to make a markup class ('variable'/_attribute-queue_). This process repeats until the stack is depleated.

The reading of the CML file ends with outputting a list of generic markup objects, each containing a class name and a set of attributes.

**compiling the CML data**

Compiling the CML data involves taking the generic markup classes created from reading and organising them into Carneades _Skeleton Classes_ (or 'CaesClasses' in the code files). A series of allowable constructors is defined of which a markup object must comply to (at least one). From there the attributes and name of the markup object are analysed to classify it as a specific Caernades class.

Once these _Skeleton Classes_ have been created they are handed to a _CarneadesWriter_ class which manages the transformation of _Skeleton Classes_ to actual Carneades library classes. After this has been performed, the whole conversion process is complete and it will display the end result of the Carneades argumentation system - if no errors were encountered.
