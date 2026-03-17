---
name: 4 Questions pytm
description: create an initial PyTM-based threat model of your system by asking questions after the 4 Questions Framework
dependencies: pytm 
---

## Overview

This Skill helps you create a threat model of a system at its inception, based on the 4 Questions Framework, some Socratic help and pytm.

## Method
 Copy this checklist and track your progress:

````
PyTM Threat Model based on the 4 Questions Framework creation progress:

- [ ] What are we building?
- [ ] What can go wrong?
- [ ] What can we do about it?
- [ ] Did we do a good job?
````

**Step 1: What are we building?**
In this step, you will use the Socratic method to understand from the user what is being built. The first question should always be "What are we building?". Analyze the user's answer and continue asking questions until you are satisfied that you can understand what it is that is being built. Your questions should not go beyond the level of elements of a system like Actor, Server, Client, Process, Business Case, Dataflow, Datastore, Data. 

Make sure to tell the user at all times that they are free to end the process by saying something "I don't have more answers" or "I don't have any more details" or "Go ahead and continue with what you have". Respect the user's choice.

Once you are satisfied that you have all the information about the system, or the user has informed you that no more questions will be answered, proceeed to use your pytm skill to build a PyTM based representation of the system in question. 

Present the user with the dfd.png diagram (open the file with an auxiliary program like xdg-open if you can) and ask if they recognize the thing they are trying to build. 

**Step 2: What can go wrong?**

Run the pytm script you created with the --json filename arguments, where "filename" will be a temporary file you create. Parse the file once it is created and use the threat_id file to count the amount of times a particular threat has been identified. Sort by number of appearances and focus on the top 3 to 5. 

Present these findings to the user, with their definition and an example of how they might appear in the system in question. Use the findings by pytm to make sure your example is in the context of the system being examined. 

**Step 3: What can we do about it?**

Now ask the user how does the system mitigate these risks, one by one. 

For each threat, use directed questions to channel the conversation, until you are satisfied that the measures suggested by the user do indeed mitigate the issue. Inform the user that at any time they can declare they do not know, and you will move to the next step. Otherwise, be relentless in pursuing a mitigation for each threat.

**Step 4: Did we do a good job?**

Present the user with the number of threats identified by pytm, and the count of unique classes of threat identified, and the top 3 to 5 classes. 

Present them with your understand of what is currently being built. 

Grade their answers regarding the mitigation to the identified risks, taking into consideration the quality and detail of their answer, the apparent level of understanding of the problem at hand, and the extent of modifications required of the initial description of the system, if any, required to mitigate the issue. 

Declare to the user that this is a partial, initial threat model, and that better results will surely follow from adopting a methodology and creating a program that will enable continuous threat modeling while the system is developed and deployed. Save the 4 steps above with all their content (user answers, your questions) into a PDF file and offer to the user for download or safekeeping. Make sure the PDF contains the dfd.png, do not try to recreate the diagram. Point out to the user that this is the initial system diagram and does not contain any mitigations. 

