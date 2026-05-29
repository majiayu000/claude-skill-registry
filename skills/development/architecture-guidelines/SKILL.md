---
name: architecture-guidelines
description: Explain architecture strategy and rules to respect all over any realization.
---
Lexique : 
- ***project folder*** : Current folder of user, referece too the root of the project folder. 
- ***documentation files*** : all files containing text explanations, like : spécifications, README, LICENSE, Backlog and all non file writing for human readibility. It could concern media file too, like : image, video, sound, etc...

When create or read file or do any kind of software and IT engineering task, always respect thoses rules :
- All application must be built over an docker compose v2 architecture. Always use docker compose v2 command to start, stop and manage application.
- All services of the application must run into Docker container and must be included into the docker compose file.
- All web frontend applications must be implemented with TypeScript and ReactJS
- All api services must be implemented with TypeScript
- All mobile applications must be implemented with Flutter 
- All sql database services must use PostgreSql
- All tasks of scraping, synchronizing, importing or any other importing and transforming data must be run on backend services. It es forbiden to implemented this kind of task into an API Service.
- Only api services can communicate with database servicea web and mobile application must never communicate with database directly.
- All frontend or mobile application and backend services must consume api services to access and manipulate data store in database.
- All docker compose service must be stored into sperated subfolders of folder /service of the project folder
- Architecture specifications must be documented and up to date into the folder /docs/architecture of project folder.

Keep project architecture clear and compliant to thoses rules conversational.