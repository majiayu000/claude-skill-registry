---
name: sonarcloud-gate
description: Run SonarCloud quality gate analysis
argument-hint: "[--project-key=<key>]"
tags: [quality, sonarcloud, gate, devsecops]
user-invocable: true
---

# SonarCloud Quality Gate

Run SonarCloud analysis and verify quality gate passes.

## What To Do

1. **Configure sonar-project.properties**:
   ```properties
   sonar.projectKey=ERP-CORE-DEV_rh-optimerp-sourcing
   sonar.organization=erp-core-dev
   sonar.sources=src/backend
   sonar.tests=src/backend/Tests
   sonar.cs.opencover.reportsPaths=**/coverage.opencover.xml
   ```

2. **Azure Pipelines**:
   ```yaml
   - task: SonarCloudPrepare@2
     inputs:
       SonarCloud: SonarCloud
       organization: erp-core-dev
       projectKey: $(PROJECT_KEY)
   - script: dotnet build && dotnet test --collect:"XPlat Code Coverage"
   - task: SonarCloudAnalyze@2
   - task: SonarCloudPublish@2
   ```

3. **Quality gate thresholds**: Coverage > 80%, Duplications < 3%, Bugs = 0

## Arguments
- `--project-key=<key>`: SonarCloud project key