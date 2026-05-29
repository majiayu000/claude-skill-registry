---
name: backend-guidelines
description: Explain backend service strategy and rules to respect all over any realization.
---

When you manipulate data, always respect thoses rules :
- All tasks and services handling data manipulation, including importing, scraping and transforming, must be executed and a separated docker compose service of type backend.
- Backend services could not access directly to databses service, they must access (read and write) through the api services.
- Backend services can schedule task to run periodicaly or staying alive listening to new request.

Keep backend services clear and compliant to thoses rules conversational.