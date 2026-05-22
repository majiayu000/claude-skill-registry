---
name: testing-guidelines
description: Explain application testing strategy, process and rules to respect all over any realization.
---

Lexique : 
- ***project folder*** : Current folder of user, referece too the root of the project folder. 
- ***documentation files*** : all files containing text explanations, like : spécifications, README, LICENSE, Backlog and all non file writing for human readibility. It could concern media file too, like : image, video, sound, etc...

When you create tests or want to test the application, always respect thoses rules :
- End to end tests and any other tests must be into the folder /tests of the project folder.
- All documentation files related to the tests and tetsing startegy must be into the folder /docs/testing of the project folder.
- Do not create unit test of code. I don't care about code testing and I focus testing on fonctionnal and end to end user experience tests.
- Always create and maintain end to end test of web and mobile applications.
- End to End test should always be up to date the of the product specifications, They must always allow verification of the correct functioning of the behavior expected by the specifications and expeted user experience.
- End to end tests for web interface must be implemented with Typescript and Playwriht
- End to end tests for mobile application must be implemented with Maestro testing framework.
- Global testing strategy should be documented.
- Tests plan must be documented into the test-plan.md file into the folder /docs of the project folder.
- Tests plan file test-plan.md must be maintenained and up to date regarfing to the progression of the iterations.
- Do not specify and produce too many test cases. Focus on few main and strategic test cases.
- Each execution report must be saved, human readable and available for user.
- Do not test accessibility of the user interfaces

Keep testing specifications and automated tests clear and compliant to thoses rules conversational.