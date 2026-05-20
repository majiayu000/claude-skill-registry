---
name: azure-init
description: Initialize local dev environment from Azure DevOps by cloning all project repositories. Use when user asks to "initialize Azure project", "clone Azure repos", "setup Azure project locally", or wants to download all repositories from an Azure DevOps project.
compatibility: Requires Azure CLI (with az devops extension) OR Azure DevOps MCP, and Git
allowed-tools: Bash
metadata:
  author: alkj
  version: "2.1.0"
---

# Azure DevOps Project Initialization

Initialize a local development environment from an Azure DevOps project by cloning all repositories.

## Table of Contents

1. [Overview](#overview)
2. [Arguments](#arguments)
3. [Instructions](#instructions) - Steps 0-8
4. [Optional Flags](#optional-flags)
5. [Example Usage](#example-usage)
6. [Example Output](#example-output)
7. [Error Handling](#error-handling)
8. [Prerequisites](#prerequisites)
9. [Reference Materials](#reference-materials)

## Overview

This skill helps users quickly set up a local development environment by:
- Finding an Azure DevOps project by name or ID
- Listing all repositories in that project
- Cloning all repositories to a local directory
- Organizing them in a clean folder structure

## Arguments

When invoked, parse the arguments as follows:
- **First argument** (required): Project name or ID
- **Second argument** (optional): Target directory path (auto-detected from current location if not provided)

## Instructions

Follow these steps when this skill is activated.

**Copy this checklist to track progress:**

```
Azure DevOps Initialization Progress:
- [ ] Step 0: Verify prerequisites (Git, Azure CLI/MCP)
- [ ] Step 1: Parse arguments
- [ ] Step 2: Find the project
- [ ] Step 3: List repositories
- [ ] Step 4: Determine target directory
- [ ] Step 5: Create directory structure
- [ ] Step 6: Clone repositories
- [ ] Step 7: Verify and report
- [ ] Step 8: Handle any failures
```

### 0. Verify Prerequisites

**CRITICAL FIRST STEP**: Before proceeding, verify required tools are available:

**Check Git:**
1. Run `git --version` to verify git is installed
2. If not found, inform user: "Git is not installed. Install it with your package manager (brew install git, apt install git, etc.)"
3. Exit if git is unavailable

**Check Azure DevOps Access (Azure CLI preferred, MCP fallback):**

**Try Azure CLI first:**
1. Check if `az` is available: `az --version 2>/dev/null`
2. If found:
   - Check for azure-devops extension: `az extension show -n azure-devops 2>/dev/null`
   - If extension missing, install it: `az extension add -n azure-devops`
   - Check if default org is configured: `az devops configure --list | grep organization`
   - If no default org found:
     - Ask user: "What is your Azure DevOps organization name?" (use AskUserQuestion)
     - Configure: `az devops configure --defaults organization=https://dev.azure.com/{user-provided-org}`
   - Test: `az devops project list 2>&1`
   - If successful: Use Azure CLI mode for steps 2-3
   - If auth fails: Guide user to run `az login` (READ references/az-cli-installation.md)

**Fall back to MCP if Azure CLI not available:**
1. Try calling `mcp_ado_core_list_projects` (no parameters)
2. If tool exists and succeeds: Use MCP mode for steps 2-3
3. If tool fails or doesn't exist:
   - Inform user neither Azure CLI nor MCP is available
   - READ references/az-cli-installation.md (recommended) OR references/mcp-installation.md
   - Provide quick install options for both
   - Exit gracefully

### 1. Parse Arguments

Extract the project identifier and optional target directory from the args string:
- If only one argument: it's the project name/ID
- If two arguments: first is project name/ID, second is target directory

### 2. Find the Project

**If using Azure CLI mode:**
- Use `az devops project list --output json`
- Parse JSON and search for project by name (case-insensitive partial match)
- Extract: project name, organization from configured default

**If using MCP mode:**
- Use `mcp_ado_core_list_projects`
- Search for project by name (case-insensitive partial match)
- Extract: project ID, project name, organization from project URL

**Common handling:**
- If exact match not found, look for partial matches and ask user to clarify
- If still not found, list available projects matching the search term

### 3. List Repositories

**If using Azure CLI mode:**
- Use `az repos list --project "PROJECT-NAME" --output json`
- Parse JSON to get repository names, IDs, metadata

**If using MCP mode:**
- Use `mcp_ado_repo_list_repos_by_project` with project ID
- Get repository names, IDs, metadata from response

**Common handling:**
- Display repositories found with their names (and sizes if available)
- If no repositories found, inform user and exit

### 4. Determine Target Directory

**If target directory was provided in args:**
- Use it as-is

**If NOT provided, detect base directory:**

1. **Detect current working directory** and check if it matches recognized code directory patterns:
   - `~/code/`, `~/git/`, `~/projects/`, `~/src/`, `~/dev/`, `~/repos/`
   - Run: `pwd` to get current directory
   - If current directory starts with any of these patterns, extract the base directory
   - Example: If `pwd` returns `/Users/you/git/some-project`, use `~/git/` as base

2. **If no recognized pattern found**, ask user where to clone using AskUserQuestion:
   - Question: "Where would you like to clone the repositories?"
   - Options:
     - Current directory: `$(pwd)`
     - Home code directory: `~/code/`
     - Custom path: (user provides custom path)
   - Use the selected path as the base directory

3. **Now determine structure based on repository namespacing:**

**Check if repositories are properly namespaced:**
- A repo is "properly namespaced" if its name contains namespace separator (`.` or `-`) and has 2+ segments
- Examples of properly namespaced:
  - `Acme.Platform.Frontend` (3 segments with `.`)
  - `Contoso.DataHub` (2 segments with `.`)
  - `Fabrikam-Api` (2 segments with `-`)
- Examples of NOT namespaced:
  - `Frontend` (single word)
  - `Api` (single word)
  - `Infrastructure` (single word)

**Decision logic:**
1. Check first 3-5 repositories in the list
2. If ALL are properly namespaced → Place directly in base directory
   - Each repo goes to: `{base-dir}/{sanitized-repo-name}`
3. If ANY are NOT properly namespaced → Use project folder structure
   - Each repo goes to: `{base-dir}/{sanitized-project-name}/{sanitized-repo-name}`

**Sanitization rules** (apply to all directory names):
- Replace spaces with hyphens
- Convert to lowercase (preserve dots and hyphens)
- Remove or replace special characters that aren't filesystem-safe
- Examples:
  - "Platform Services" → "platform-services"
  - "My Project!" → "my-project"
  - "Acme.Platform.Frontend" → "acme.platform.frontend"

### 5. Create Directory Structure

**Based on the namespacing decision from step 4:**

- If placing directly in base directory: No parent directory needed
- If using project folder: Create `{base-dir}/{sanitized-project-name}/`
- Use `mkdir -p` to create parent directories as needed

**Inform the user of the decision:**
```
Repository naming analysis:
✓ Repositories are properly namespaced (e.g., Acme.Platform.Api)
→ Placing directly in {base-dir}/

or

Repository naming analysis:
⚠ Repositories are not namespaced (e.g., Api, Frontend)
→ Organizing in project folder: {base-dir}/platform-services/
```

### 6. Clone Repositories

For each repository:

**Build SSH URL:** `git@ssh.dev.azure.com:v3/{organization}/{project-name}/{repo-name}`
- Use the original project and repo names from Azure DevOps
- URL encode both project name and repo name:
  - Spaces → `%20`
  - Special chars → URL encoded equivalents
  - Example: `git@ssh.dev.azure.com:v3/acmecorp/Platform%20Services/My%20Repo`

**Sanitize directory name:**
- Apply sanitization rules from step 4 to the repository name
- This is ONLY for the local directory name, not the git URL
- Example: "My Repo" → "my-repo" (for directory), but "My%20Repo" in URL

**Determine full clone path:**
- If repos are properly namespaced: `{base-dir}/{sanitized-repo-name}`
- If repos are NOT namespaced: `{base-dir}/{sanitized-project-name}/{sanitized-repo-name}`

**Check if directory already exists:**
- Check if the full clone path exists
- If exists and contains `.git` folder: skip with message "Already cloned"
- If exists but no `.git` folder: warn user and ask whether to remove and re-clone or skip
- If not exists: proceed with clone

**Clone the repository:**
- Run: `git clone {ssh-url} "{full-clone-path}"`
- Show progress for each clone

**Error handling for clone failures:**
- If clone fails with "Permission denied (publickey)":
  - Inform user SSH keys are not configured
  - READ references/az-cli-installation.md for SSH setup instructions
  - Ask: "Continue with remaining repos? (y/n)"
  - If no: exit and suggest cleanup (see Cleanup on Failure section)
- If clone fails with other error:
  - Report the specific error message
  - Ask if user wants to continue with remaining repos
  - If no: exit and document what was cloned successfully

**Rate limiting:**
- Clone repositories sequentially (not in parallel)
- Consider adding 1-2 second delay between clones for large projects (10+ repos)
- This prevents overwhelming Azure DevOps and provides clear progress updates

### 7. Verify and Report

- List the final directory structure using `ls -lh` on the appropriate directory
- Provide a summary including:
  - Number of repositories cloned successfully
  - Number of repositories skipped (already existed)
  - Number of repositories failed (if any)
  - Full path to the location (either project folder or base directory)
  - Next steps suggestion with path to a primary repository

### 8. Cleanup on Failure

If the process exits early (MCP issues, SSH failures, network errors), inform the user of the current state:

**Partial clone scenario (non-namespaced repos):**
```
Clone process incomplete. Current state:
- Successfully cloned: 3 repositories
- Failed/Skipped: 5 repositories
- Location: {base-dir}/platform-services

Options:
1. Fix the issue (SSH keys, network) and run /azure-init again
   - Already cloned repos will be skipped automatically
2. Remove partial setup: rm -rf {base-dir}/platform-services
3. Continue manually: cd {base-dir}/platform-services and clone remaining repos
```

**Partial clone scenario (namespaced repos):**
```
Clone process incomplete. Current state:
- Successfully cloned: 2 repositories
- Failed/Skipped: 3 repositories
- Location: {base-dir} (acme.platform.api, acme.platform.frontend)

Options:
1. Fix the issue (SSH keys, network) and run /azure-init again
   - Already cloned repos will be skipped automatically
2. Remove partial clones: rm -rf {base-dir}/acme.platform.*
3. Continue manually: clone remaining repos to {base-dir}
```

Always provide clear next steps so users know how to proceed or clean up.

## Optional Flags

When parsing arguments, support an optional `--dry-run` flag:

```bash
/azure-init "Platform Services" --dry-run
/azure-init "Platform Services" ~/projects/platform --dry-run
```

**Dry run behavior:**
- Perform all checks (git, MCP, find project)
- List all repositories that would be cloned
- Analyze repository namespacing and show the decision
- Show the target directory structure that would be created
- Calculate total size if available
- Do NOT actually clone any repositories
- Show exact git commands that would be executed

This lets users preview what will happen before committing to large clones.

## Example Usage

```bash
/azure-init "Platform Services"
# Auto-detects base directory from current location (~/code/, ~/git/, ~/projects/, etc.)
# If repos are NOT namespaced (Api, Frontend, etc.):
#   → Clones to {base-dir}/platform-services/api, {base-dir}/platform-services/frontend, etc.
# If repos ARE namespaced (Acme.Platform.Api, Acme.Platform.Frontend, etc.):
#   → Clones to {base-dir}/acme.platform.api, {base-dir}/acme.platform.frontend, etc.

/azure-init "Platform Services" ~/projects/platform
# Clones to ~/projects/platform/ (overrides automatic directory detection)

/azure-init 0d1e562b-95af-4c55-a8ce-8f26508d50ed
# Uses project ID directly, applies same namespacing logic with auto-detected base dir

/azure-init "Platform Services" --dry-run
# Preview what would be cloned without actually cloning
```

## Example Output

See [references/examples.md](references/examples.md) for detailed example outputs showing both namespaced and non-namespaced repository scenarios.

## Error Handling

Handle common errors gracefully. For detailed error messages and setup instructions, see [references/troubleshooting.md](references/troubleshooting.md).

**Common error scenarios:**
- **Azure CLI not installed**: Guide user through Azure CLI installation
- **az devops extension missing**: Auto-install with `az extension add -n azure-devops`
- **Authentication failed**: Guide user to run `az login` or configure PAT
- **SSH not configured**: Provide SSH key generation and setup instructions
- **Project not found**: List available projects or suggest search improvements
- **Clone failures**: Report which repository failed and why
- **Permission issues**: Suggest alternative directory or permission fixes

## Prerequisites

**Required:**
- Git must be installed and available
- **Either** Azure CLI with `azure-devops` extension **OR** Azure DevOps MCP server
- Azure DevOps authentication configured
- SSH authentication for cloning repositories

**Automatic verification** happens in step 0

**Setup guides:**
- Azure CLI installation (recommended): [references/az-cli-installation.md](references/az-cli-installation.md)
- MCP installation (alternative): [references/mcp-installation.md](references/mcp-installation.md)
- Troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

## Reference Materials

When needed during execution, READ these guides:

- **Azure CLI setup**: [references/az-cli-installation.md](references/az-cli-installation.md)
  - Installation steps for macOS, Linux, Windows
  - Azure DevOps extension setup
  - Authentication configuration
  - SSH key setup for cloning

- **MCP setup**: [references/mcp-installation.md](references/mcp-installation.md)
  - Quick installation command
  - When to use MCP vs Azure CLI
  - Authentication flow

- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
  - Azure DevOps access issues
  - SSH configuration problems
  - Common errors and solutions

- **Examples**: [references/examples.md](references/examples.md)
  - Example output for non-namespaced repositories
  - Example output for properly namespaced repositories

## Notes

**Directory detection:**
- The skill auto-detects your preferred code directory by checking if you're in a recognized pattern (~/code/, ~/git/, ~/projects/, ~/src/, ~/dev/, ~/repos/)
- If not in a recognized directory, it asks you where to clone repositories
- You can always override by providing a custom target directory as the second argument

**Namespacing logic:**
- The skill automatically detects if repositories are properly namespaced
- **Properly namespaced** = Contains `.` or `-` separator with 2+ segments (e.g., `Acme.Platform.Api`, `Contoso-DataHub`)
- Namespaced repos go directly to `{base-dir}/{repo-name}` (flat structure)
- Non-namespaced repos go to `{base-dir}/{project-name}/{repo-name}` (nested structure)
- This keeps your code folder organized and consistent with established patterns

**General behavior:**
- Repositories that already exist (with `.git` folder) will be skipped (not re-cloned)
- Re-running the skill after failures will skip already cloned repos automatically
- Large repositories may take time to clone - progress is shown for each repo
- The skill extracts organization name from Azure DevOps project objects automatically
- URL encoding handles both project and repository names with spaces correctly
- Directory names are sanitized (lowercase, spaces→hyphens, preserve dots) for filesystem compatibility
- Rate limiting prevents overwhelming Azure DevOps with parallel clone requests
- All errors are handled gracefully with helpful guidance and recovery options
- Default branch is determined by the repository's Azure DevOps settings
- You can override the automatic directory decision by providing a custom target directory
