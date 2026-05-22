# Azure DevOps CLI Skill

---

name: azure-devops-cli
description: Expert guidance for Azure DevOps CLI (az devops) - automation, pipelines, repos, boards, and artifacts management. Use when working with Azure DevOps, managing pipelines, creating work items, or when user mentions ADO, builds, releases, or Azure repos.
keywords:

- azure devops
- az devops
- ado cli
- pipelines
- azure pipelines
- boards
- azure boards
- repos
- azure repos
- artifacts
- azure artifacts
- yaml pipeline
- build pipeline
- release pipeline
- work items
- pull requests
- git repos
- artifacts feed

<!-- prettier-ignore-start -->
auto_activate: true
version: 1.0.0
token_budget: 1800
<!-- prettier-ignore-end -->

---

## Quick Start

### Installation & Authentication

```bash
# Install Azure DevOps CLI extension
az extension add --name azure-devops

# Authenticate (choose one method)
az login                                    # Interactive browser login
az devops login --organization https://dev.azure.com/YOUR_ORG  # PAT token login

# Configure defaults (recommended)
az devops configure --defaults organization=https://dev.azure.com/YOUR_ORG project=YOUR_PROJECT

# Verify setup
az devops project list
```

### Configuration Patterns

```bash
# Set defaults to avoid repeating --organization and --project
az devops configure --defaults organization=https://dev.azure.com/myorg project=myproject

# List current configuration
az devops configure --list

# Use Git aliases for common commands
az devops configure --defaults use-git-aliases=true

# Common output formats
--output table    # Human-readable tables (default)
--output json     # JSON for scripting
--output tsv      # Tab-separated values
```

## Essential Commands by Group

### 1. DevOps (Organization & Projects)

```bash
# List projects
az devops project list --organization https://dev.azure.com/myorg

# Create project
az devops project create --name "MyProject" --visibility private

# Show project details
az devops project show --project MyProject

# Delete project
az devops project delete --id PROJECT_ID --yes

# Manage users/teams
az devops user list
az devops team list --project MyProject
```

### 2. Pipelines (Build & Release)

```bash
# List pipelines
az pipelines list --project MyProject

# Run a pipeline
az pipelines run --name "MyPipeline" --branch main

# Show pipeline runs
az pipelines runs list --pipeline-ids 123

# Show run details
az pipelines runs show --id RUN_ID

# Create pipeline from YAML
az pipelines create --name "NewPipeline" --repository myrepo --branch main --yml-path azure-pipelines.yml
```

### 3. Boards (Work Items & Sprints)

```bash
# List work items
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'Active'"

# Create work item
az boards work-item create --type "User Story" --title "New Feature" --assigned-to me@example.com

# Update work item
az boards work-item update --id 123 --state "In Progress"

# Show work item
az boards work-item show --id 123

# List iterations/sprints
az boards iteration project list
```

### 4. Repos (Git Repositories)

```bash
# List repositories
az repos list --project MyProject

# Create repository
az repos create --name "myrepo" --project MyProject

# List pull requests
az repos pr list --repository myrepo --status active

# Create pull request
az repos pr create --repository myrepo --source-branch feature/new --target-branch main --title "New Feature"

# Show PR details
az repos pr show --id PR_ID
```

### 5. Artifacts (Package Management)

```bash
# List feeds
az artifacts feed list

# Create feed
az artifacts feed create --name "myfeed" --project MyProject

# List packages
az artifacts universal list --feed myfeed --project MyProject

# Publish package
az artifacts universal publish --feed myfeed --name mypackage --version 1.0.0 --path ./dist

# Download package
az artifacts universal download --feed myfeed --name mypackage --version 1.0.0 --path ./download
```

## Common Workflows

### Workflow 1: CI/CD Pipeline Automation

```bash
# Create pipeline, run it, and monitor
az pipelines create --name "API-Build" --repository myrepo --yml-path ci/azure-pipelines.yml
az pipelines run --name "API-Build" --branch main
az pipelines runs show --id RUN_ID --open  # Opens in browser
```

### Workflow 2: Pull Request Review Automation

```bash
# List active PRs, show details, add comment
az repos pr list --repository myrepo --status active --output table
az repos pr show --id 456 --open
az repos pr update --id 456 --status approved
```

### Workflow 3: Work Item Batch Creation

```bash
# Create multiple work items from template
for title in "Feature A" "Feature B" "Feature C"; do
  az boards work-item create --type "User Story" --title "$title" --assigned-to team@example.com
done
```

### Workflow 4: Pipeline Status Dashboard

```bash
# Get recent pipeline runs with status
az pipelines runs list --top 10 --query "[].{Name:pipeline.name, Status:status, Result:result, Started:startTime}" --output table
```

### Workflow 5: Repository Clone Automation

```bash
# List all repos and clone them
az repos list --query "[].{Name:name, URL:remoteUrl}" --output tsv | while IFS=$'\t' read -r name url; do
  git clone "$url" "./$name"
done
```

### Workflow 6: Sprint Planning Helper

```bash
# List current sprint work items
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.IterationPath] = @CurrentIteration" --output table
```

### Workflow 7: Release Gate Checking

```bash
# Check if all PRs are approved before release
PENDING=$(az repos pr list --status active --query "length([?status!='approved'])")
if [ "$PENDING" -eq 0 ]; then
  az pipelines run --name "Release-Pipeline"
fi
```

### Workflow 8: Artifact Versioning

```bash
# Publish versioned artifact with timestamp
VERSION="1.0.$(date +%Y%m%d%H%M%S)"
az artifacts universal publish --feed myfeed --name myapp --version "$VERSION" --path ./build
```

### Workflow 9: Team Dashboard Data

```bash
# Export team metrics to JSON
az devops project show --project MyProject > project.json
az pipelines runs list --top 50 > recent-runs.json
az repos pr list --status all > all-prs.json
```

### Workflow 10: Environment Sync

```bash
# Copy pipeline variables across environments
az pipelines variable list --pipeline-name "MyPipeline" --output json > vars.json
# Edit vars.json as needed
az pipelines variable-group create --name "Production" --variables @vars.json
```

## Troubleshooting

### Common Issues

**Authentication Failures:**

```bash
# Clear cached credentials
az account clear
az login

# Use PAT token directly
export AZURE_DEVOPS_EXT_PAT=your_personal_access_token
az devops login
```

**Default Configuration:**

```bash
# Reset defaults if commands fail
az devops configure --defaults organization="" project=""
# Then set explicitly in each command
az pipelines list --organization https://dev.azure.com/myorg --project MyProject
```

**Extension Issues:**

```bash
# Update Azure DevOps extension
az extension update --name azure-devops

# Check extension version
az extension show --name azure-devops
```

**Query Syntax:**

```bash
# WIQL queries require proper escaping
az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active' AND [System.AssignedTo] = 'me@example.com'"
```

## Advanced Patterns

### REST API Access

```bash
# Direct REST API calls for unsupported operations
az devops invoke --area build --resource builds --route-parameters project=MyProject --api-version 6.0 --http-method GET

# POST with JSON body
az devops invoke --area git --resource repositories --route-parameters project=MyProject --http-method POST --in-file payload.json
```

### Scripting with JMESPath

```bash
# Complex queries using JMESPath
az pipelines runs list --query "[?result=='failed'].{Pipeline:pipeline.name, Branch:sourceBranch, Time:finishedDate}" --output table

# Filter and transform data
az repos pr list --query "[?targetRefName=='refs/heads/main' && status=='active'].{ID:pullRequestId, Title:title, Author:createdBy.displayName}"
```

### Aliases and Functions

```bash
# Create shell aliases for common commands
alias azdo-pipelines="az pipelines list --output table"
alias azdo-prs="az repos pr list --status active --output table"
alias azdo-builds="az pipelines runs list --top 20 --output table"

# Function for quick PR creation
azdo-pr() {
  az repos pr create --source-branch "$(git branch --show-current)" --target-branch main --title "$1" --open
}
```

## Extended Content

For comprehensive command references and advanced workflows, see:

- **Complete Command References**: `examples/pipelines-reference.md`, `examples/boards-reference.md`, `examples/repos-reference.md`, `examples/artifacts-reference.md`
- **Advanced Workflows**: `examples/workflows/ci-cd-automation.md`, `examples/workflows/release-management.md`, `examples/workflows/team-collaboration.md`
- **Testing Scenarios**: `tests/test-scenarios.md`

## References

- Azure DevOps CLI Documentation: https://learn.microsoft.com/en-us/cli/azure/devops
- WIQL Syntax: https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax
- REST API: https://learn.microsoft.com/en-us/rest/api/azure/devops
