---
name: pytm threat model
description: create an initial PyTM-based threat model of your system when asked to perform a threat model
dependencies: pytm 
---

## Overview

This Skill analyzes the code in your directory and uses the PyTM python library to build a representation (model) and a list of possible threats affecting it.

## Method
 Copy this checklist and track your progress:

````
PyTM Threat Model creation progress:

- [ ] Analysis
- [ ] Mapping to pytm elements
- [ ] Adding attributes
- [ ] Create pytm script
- [ ] Execute the script
- [ ] Validate the script
- [ ] Try a use case analysis of the project
````

**Step 1: Analysis**

Analyze the codebase (either the current directory or project, or some path or project reference given by the user as an argument in the prompt) looking for the basic architectural components of the system: Actors (which are possibly humans interacting with the system), Clients, Servers, Serverless Processes, Datastores, Trust Boundaries (where the identity of the user or process is different on both sides of a dataflow), and, most importantly, Dataflows that carry data from one element of the system to another. Pay special attention to where in the codebase each one of the elements discovered is created or referred for the first time. 

**Step 2: Mapping to pytm elements**
Once you have those elements mapped, use the Python pytm library and create a relationship between what you identified and the pytm building blocks: Asset, Lambda, Server, ExternalEntity, Datastore, Actor, Process, SetOfProcesses, Boundary and Dataflow. You are also free to create pytm assumptions in the form of the assumption attribute of the TM, and any security controls you identify should appear as an addition to the controls attribute of the TM. Particular items of data should be represented using the Data class. 

**Step 3: Adding attributes**
For attributes of data instances you can identify from the code and documentation of the project, fill the instances attributes. For anything that you are not sure about, or that you cannot find a value but think is important to have, add a comment like "# TODO - find the real value for this attribute". Make sure that the origin of the element that you remember from Step 1 is the value of the appropriate attribute. 

**Step 4: Create pytm script**
Create a pytm script that uses your findings to describe the system. Use the content of ./REFERENCE.md as an example of a pytm script if you need it. Create a directory named tm in the root of the project, if it doesn't exist yet. Save your pytm script in the tm directory, naming it with the name of the project followed by _pytm.py 

**Step 5: Validate the script**
Using a python linter, verify that the newly created script is syntactically correct.
Only proceed when the script is syntactically correct.
Finalize by telling the user where to find the script in the filesystem.

**Step 6: Execute the script**
Run the newly created script with the argument "--json findings.json". If there are any Python level errors, correct them considering the syntaxt of pytm objects, their attributes and relationships. Repeat this step as many times as necessary until the script runs with no error messages. Once there are no error messages, run the script with the argument "--dfd dfd.png" and then again with the argument "--seq | plantuml -p -tpng > seq.png". You should end up with three new files in the tm directory: findings.json, seq.png and dfd.png. If you don't have them, stop here and alert the user there is a problem.

**Step 7: Try a use case analysis of the project
Using your understanding of the code base and any documentation locally available, create a file in the tm directory called business_tm.md in Markdown with the following structure. Relate to the strings written in camel case as placeholders that you will fill as necessary.
As a primary step, extract the findings from the JSON structure in the file findings.json you created previously. 
# Project: nameOfTheProject
## Structure
proseExpressingWhatYouUnderstandOfTheProjectStructure

## Apparent business case
proseExpressingWhatYouBelieveTheSystemUsesAre

## Findings
anyFindingsFromTheJSONOutput

Do not add any other content apart from the structure above. If you feel you are missing details, feel free to ask the user to provide them until you are satisfied.

