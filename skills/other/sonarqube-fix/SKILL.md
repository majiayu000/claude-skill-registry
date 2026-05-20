---
name: sonarqube-fix
description: This skill should be used when fixing SonarQube quality gate failures. It runs the sonarqube:check skill to identify failures, fixes the identified issues, and then commits the changes using the git:commit skill.
---

1. Run /sonarqube-check
2. Fix the SonarQube quality gate failures identified in step 1
3. Run /git-commit
