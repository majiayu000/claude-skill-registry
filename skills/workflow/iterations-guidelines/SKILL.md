---
name: iterations-guidelines
description: Explain iterations strategy, process and rules to respect all over any realization. Iteration is the main conception workflow of any conception and modification of the project.
---

Lexique : 
- ***project folder*** : Current folder of user, referece too the root of the project folder. 
- ***documentation files*** : all files containing text explanations, like : spécifications, README, LICENSE, Backlog and all non file writing for human readibility. It could concern media file too, like : image, video, sound, etc...
- ***iteration folder*** : subfolder of an iteration.

When you read or create or modify application, always respect thoses rules :
- Any user request of creation or modification of application must be splited into smaller iterations and must be realized iteration by iteration.
- Each iteration must have its own subfolder into the folder /docs/iterations/ of project folder to store all documentation files related to the iteration.
- Any iteration must be documented and its extpected must be clearly specified into the file EXPECTED.md file into its iteration subfolder, ex : /docs/iterations/1.
- Any iteration delivery must be documented and and clearly explaned into the file DELIVERY.md file into its iteration subfolder.
- Iterations' subfolders must only contain those two file EXPECTED.md and DELIVERY.md. Any ither form of documentation or specification file must be written in the folder /docs/specs of the project folder.
- All iterations must be listed and quick describe into the file /docs/ITERATIONS_BACKLOGS.md of project folder. The file ITERATIONS_BACKLOGS.md is the iterations backlog and must always be up to date of the user requests and progressions of iterations.  
- Iterations backlog must always be written and maintain by the product owner agent. 

Each iteration must follow this worfkow of steps :
- ***Product specification*** : create or modify product specificatison files to integrate the iteration product specifications changes.
- ***Design specification*** : create of modify design specifications files to integrate the iteration design specifications changes.
- ***Technical architecture specification*** : create of modify technical architecture specifications files to integrate the iteration architectural specifications changes.
- ***Coding*** : adapt code base and project files to implement all code changes.
- ***Debug*** : build and launch all the services of the applications to correct building and configuration errors until the application is successfully up and running. From this point onwards, always leave the application running and all its services running for the following steps of the iteration.
- ***Testing*** : create or modify automated tests files to integrate new specificatison changes and then run tests and correct application until every tests successfully pass. A non regression test report of the iteration must always been documented and written in the iteration folder.

The aim of this workflow is to guarantee to the user that the deliverable of the iteration is fully functional and usable.

Keep iteration specifications and expected clear and compliant to those rules conversational.