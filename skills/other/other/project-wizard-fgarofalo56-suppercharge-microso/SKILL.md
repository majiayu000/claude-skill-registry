---
name: project-wizard
description: Create new GitHub Copilot-enabled projects from the base template with full security configuration, GitHub integration, and Archon project setup. Use when creating new projects, initializing repositories, or setting up new workspaces. Triggers on new project, create project, setup project, project wizard, project template.
---

# Project Wizard Skill

> Create new GitHub Copilot-enabled projects from the base template with full security configuration, GitHub integration, and Archon project setup.

---

## Triggers

Activate this skill when user mentions:
- "new project", "create project", "setup project"
- "new workspace", "new codebase"
- "project wizard", "project template"
- "initialize repository", "init repo"
- "#new-project", "#project-wizard"

---

## Description

The **Project Wizard** skill guides users through creating new projects from the `github-copilot-base` template. It automates:

1. **Folder Creation** - Creates project directory in specified location
2. **Template Copy** - Copies all base template files
3. **Customization** - Updates README, CODEOWNERS, and configs
4. **Git Setup** - Initializes repo with pre-commit hooks
5. **GitHub Integration** - Creates repo with branch protection and secret scanning
6. **Archon Setup** - Creates project for task management

---

## Workflow Steps

### 1. Gather Information

Collect the following using `ask_user`:

| Question | Purpose | Validation |
|----------|---------|------------|
| Project path | Parent directory location | Must exist |
| Project name | Folder and repo name | Lowercase, hyphens only |
| Project type | Determines README template | Select from list |
| Description | README and GitHub description | Max 200 chars |
| Language | .gitignore additions | Select from list |
| GitHub org | Where to create repo | Must have access |
| Visibility | Public or private | Default: private |

### 2. Execute Setup

```powershell
# Create project directory
$ProjectPath = Join-Path $ParentPath $ProjectName
New-Item -ItemType Directory -Path $ProjectPath -Force

# Copy template files
& "$TemplateRepo\scripts\copy-template.ps1" `
    -SourcePath $TemplateRepo `
    -DestinationPath $ProjectPath

# Initialize git
Set-Location $ProjectPath
git init

# Install pre-commit
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg

# Initial commit
git add .
git commit -m "feat: initial project setup from github-copilot-base template"

# Create GitHub repo
gh repo create "$Org/$ProjectName" --private --source=. --push --description "$Description"

# Enable branch protection
gh api "repos/$Org/$ProjectName/branches/main/protection" -X PUT `
    -f required_status_checks='{"strict":true,"contexts":[]}' `
    -f enforce_admins=false `
    -f required_pull_request_reviews='{"required_approving_review_count":1}'

# Enable secret scanning
gh api "repos/$Org/$ProjectName" -X PATCH `
    -f security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'
```

### 3. Create Archon Project

```javascript
// Create project
const project = await manage_project("create", {
  title: projectName,
  description: description,
  github_repo: `https://github.com/${org}/${projectName}`
});

// Create initial tasks
await manage_task("create", {
  project_id: project.id,
  title: "Complete project setup",
  description: "Review and customize template files",
  status: "todo"
});
```

### 4. Customize Files

Update these files with project-specific information:

- `README.md` - Replace placeholders with project info
- `CODEOWNERS` - Update team references
- `.github/copilot-instructions.md` - Add project context

### 5. Output Summary

Provide completion summary with:
- Project location and URL
- What was configured
- Next steps for the user

---

## Project Types

| Type | Description | README Template |
|------|-------------|-----------------|
| `web-frontend` | React, Vue, Angular, etc. | `templates/readme/web-frontend.md` |
| `backend-api` | Node.js, Python, .NET, etc. | `templates/readme/backend-api.md` |
| `fullstack` | Combined frontend + backend | `templates/readme/fullstack.md` |
| `cli-library` | CLI tools or packages | `templates/readme/cli-library.md` |
| `infrastructure` | Terraform, Docker, K8s | `templates/readme/infrastructure.md` |

---

## Language Support

Additional .gitignore patterns by language:

| Language | Template |
|----------|----------|
| JavaScript/TypeScript | `templates/gitignore/node.gitignore` |
| Python | `templates/gitignore/python.gitignore` |
| C#/.NET | `templates/gitignore/dotnet.gitignore` |
| Go | `templates/gitignore/go.gitignore` |
| Java | `templates/gitignore/java.gitignore` |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Path doesn't exist | Prompt to create or choose different |
| Folder already exists | Prompt to overwrite or rename |
| gh not installed | Show installation guide |
| Not authenticated | Run `gh auth login` |
| No org access | Use personal account |

---

## Prerequisites

- **Git** installed and configured
- **GitHub CLI (`gh`)** installed and authenticated
- **Python** installed (for pre-commit)
- **Archon MCP** server running (optional)

---

## Example

```
User: #new-project

Copilot: 🧙 Project Wizard

Let's create a new project! I'll guide you through the setup.

[Asks questions one by one...]

✅ Creating project folder...
✅ Copying template files...
✅ Initializing git repository...
✅ Installing pre-commit hooks...
✅ Creating GitHub repository...
✅ Enabling branch protection...
✅ Enabling secret scanning...
✅ Creating Archon project...

🎉 Project "my-awesome-api" created successfully!

📍 Location: E:\Repos\MyOrg\my-awesome-api
🔗 Repository: https://github.com/MyOrg/my-awesome-api
📋 Archon Project: proj_abc123

Next steps:
1. Open in VS Code: code E:\Repos\MyOrg\my-awesome-api
2. Review README.md and customize
3. Start building!
```

---

## Related

- [Project Wizard Agent](../agents/project-wizard.agent.md)
- [New Project Prompt](../prompts/new-project.prompt.md)
- [Copy Template Script](../../scripts/copy-template.ps1)
