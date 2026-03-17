---
name: ctm
description: examine a given development story and decide if it has security value that warrants inclusion in a threat model
dependencies: pytm 
---

## Overview

Given a business case, a user-story, a development request or similar, examine it in the context of the project and the existing baseline threat model and decide if it is a "security notable event" according to Continuous Threat Modeling.

## Method
 Copy this checklist and track your progress:

````
Security notable event checklist

- [ ] Find a baseline threat model
- [ ] Enrich the request
- [ ] Use the CTM Developer Checklist
````

**Step 1: Find a baseline threat model

Examine the project's directory for documentation that resembles a threat model. If one is found, use that as the baseline threat model. 
If one is not found, ask the user if they would like to use the pytm skill to create one, or if they can provide a baseline threat model. Give the user the option to not have a baseline threat model but point out the quality of the analysis will be diminished.

**Step 2: Enrich the request

If a baseline threat model is available, use it to enrich the corpus of the request. 
Feel free to ask the user as many elucidative questions about the request as you consider necessary. Use the answers to enrich the request.

**Step 3: Use the CTM Developer Checklist

Using the content of ./Secure_Developer_Checklist.md try to identify in the user request instances that match the "If you did THIS ..." side of the reference table. If matches are found, use the "... then do THAT" respective field to suggest mitigations to the issue identified.

There can be many matches in any given request. Return all those matches.

If there are notable events, suggest to the user that a ticket be created reflecting this change so the threat model can be updated.


