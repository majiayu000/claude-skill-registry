---
name: github-assistant
description: Interactive troubleshooting assistant for the top 5 GitHub problems faced by new users. Diagnoses authentication failures, Git vs GitHub confusion, local-remote sync issues, merge conflicts, and accidental sensitive data commits. Provides step-by-step solutions with command execution. Use when users mention GitHub errors, password issues, sync problems, merge conflicts, or accidentally committing secrets.
---

# GitHub Assistant Skill

This skill provides interactive, diagnostic-driven troubleshooting for the most common GitHub problems faced by new users. It identifies which of the 5 major problem scenarios the user is experiencing and provides accurate, step-by-step solutions with command execution support.

## When to Activate This Skill

**Trigger conditions:**
- User mentions GitHub authentication errors: "password doesn't work", "authentication failed", "can't push"
- User is confused about Git vs GitHub: "is Git the same as GitHub?", "which commands are Git?"
- User wants to sync local folder with GitHub: "sync my folder", "automatically update GitHub", "keep in sync"
- User encounters merge conflicts: "merge conflict", "conflicting changes", "pull failed"
- User accidentally committed sensitive data: "committed password", "exposed API key", "sensitive file in GitHub"
- User asks general GitHub help questions for beginners

**Initial offer:**
Greet the user and explain this skill will help diagnose and solve their GitHub issue. Mention that you'll ask a few questions to identify the exact problem and then provide a step-by-step solution.

## Diagnostic Workflow

### Step 1: Problem Identification

Ask the user to describe their issue or choose from common scenarios:

Present these options:
1. **Authentication/Password Issues** - Can't push or clone, password doesn't work
2. **Understanding Git vs GitHub** - Confused about what commands to use where
3. **Syncing Local Folder with GitHub** - Want to keep local files in sync with repository
4. **Merge Conflicts** - Getting conflict errors when pulling or merging
5. **Sensitive Data Exposure** - Accidentally committed passwords, API keys, or secrets
6. **Other/Not Sure** - Describe the issue in your own words

Wait for user response and route to appropriate solution workflow.

**If user chooses "Other/Not Sure":**
Ask them to describe:
- What they were trying to do
- What command they ran (if any)
- The exact error message they received
- Their current situation

Based on their description, identify which of the 5 scenarios best matches and proceed to that workflow.

### Step 2: Route to Appropriate Solution

Based on user selection, proceed to the corresponding solution workflow below.

## Solution Workflow 1: Authentication Failures

**Problem confirmed:** User is experiencing "Support for password authentication was removed" or similar authentication errors.

### Step 1: Explain the Issue

Inform the user:
- GitHub removed password authentication on August 13, 2021
- They now need to use either Personal Access Token (PAT) or SSH keys
- Their GitHub account password will not work for Git operations

### Step 2: Recommend Approach

Ask which authentication method they prefer:
- **Personal Access Token (Recommended for beginners)** - Use a token instead of password
- **SSH Keys (More advanced)** - Set up SSH key authentication

### Step 3a: Personal Access Token Setup (if chosen)

Provide step-by-step instructions:

1. **Generate a PAT on GitHub:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a descriptive name (e.g., "My Laptop Git Access")
   - Set expiration (recommend 90 days for security)
   - Select scopes: Check "repo" for full repository access
   - Click "Generate token" at the bottom
   - **IMPORTANT:** Copy the token immediately - you won't see it again!

2. **Use the token:**
   - When Git prompts for a password, paste the token instead
   - The token should start with `ghp_` or `github_pat_`

3. **Store credentials (optional but recommended):**

Ask if they want help setting up credential caching so they don't have to enter the token every time.

If yes, detect their operating system and provide appropriate command:

**For Windows:**
```bash
git config --global credential.helper wincred
```

**For macOS:**
```bash
git config --global credential.helper osxkeychain
```

**For Linux:**
```bash
git config --global credential.helper cache
# Or for permanent storage:
git config --global credential.helper store
```

Offer to run the appropriate command if they're in a terminal environment.

### Step 3b: SSH Key Setup (if chosen)

Provide step-by-step instructions:

1. **Check for existing SSH keys:**
```bash
ls -al ~/.ssh
```

Offer to run this command for them.

2. **Generate new SSH key (if needed):**
```bash
ssh-keygen -t ed25519 -C "their-email@example.com"
```

Ask for their GitHub email and offer to run this command.

3. **Add SSH key to ssh-agent:**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

4. **Copy public key:**
```bash
cat ~/.ssh/id_ed25519.pub
```

Offer to run this and display the public key for them to copy.

5. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - Paste the public key
   - Give it a title and save

6. **Test connection:**
```bash
ssh -T git@github.com
```

Offer to run this test.

7. **Update remote URL (if needed):**

Check their current remote:
```bash
git remote -v
```

If it shows HTTPS (https://github.com/...), offer to convert to SSH:
```bash
git remote set-url origin git@github.com:username/repo.git
```

### Step 4: Verify Solution

Ask user to try their original operation (push, pull, clone) and confirm it works.

If still having issues, ask for the error message and troubleshoot further.

## Solution Workflow 2: Git vs GitHub Confusion

**Problem confirmed:** User is confused about the difference between Git and GitHub.

### Step 1: Explain the Difference

Provide clear explanation:

**Git** = The version control tool installed on your computer
- Command-line tool you run locally
- Commands: `git init`, `git add`, `git commit`, `git status`, etc.
- Works entirely offline
- Manages your local repository

**GitHub** = The hosting platform (website) for your code
- Remote server accessible at github.com
- Stores your code in the cloud
- Provides web interface for collaboration
- Your code lives here so others can access it

**The Connection:**
- You use Git (locally) to interact with GitHub (remotely)
- Git commands like `git push` send your local changes to GitHub
- Git commands like `git pull` download changes from GitHub

### Step 2: Common Command Breakdown

Show which commands are used for what:

**Local Git Operations (no internet needed):**
- `git init` - Initialize a new repository
- `git add <file>` - Stage files for commit
- `git commit -m "message"` - Save changes locally
- `git status` - Check what's changed
- `git log` - View commit history
- `git branch` - Manage branches

**GitHub Operations (require internet):**
- `git clone <url>` - Download repository from GitHub
- `git push` - Upload your commits to GitHub
- `git pull` - Download changes from GitHub
- `git fetch` - Check for remote changes

**GitHub Web Interface:**
- Creating repositories
- Managing collaborators
- Viewing pull requests
- Adjusting settings

### Step 3: Practical Example

Offer to demonstrate a typical workflow:

1. Create or modify files → **You do this in your editor**
2. `git add .` → **Git command (local)**
3. `git commit -m "description"` → **Git command (local)**
4. `git push` → **Git command that talks to GitHub (remote)**

### Step 4: Address Specific Questions

Ask if they have any specific questions about:
- Which tool to use for their current task
- Where to find certain features
- How to accomplish a specific goal

Provide targeted answers based on their questions.

## Solution Workflow 3: Syncing Local Folder with GitHub

**Problem confirmed:** User wants to keep their local folder synchronized with a GitHub repository.

### Step 1: Set Expectations

Explain that Git is not automatic cloud storage:
- Unlike Dropbox or Google Drive, Git requires manual synchronization
- This is intentional - you control exactly what gets saved and when
- The workflow has three steps: stage → commit → push

### Step 2: Check Current Setup

Ask: "Do you already have a GitHub repository created for this folder?"

**If NO:**

1. **Create repository on GitHub:**
   - Go to: https://github.com/new
   - Give it a name matching your local folder
   - Choose public or private
   - **Do NOT** initialize with README, .gitignore, or license (since you have local files)
   - Click "Create repository"

2. **Initialize local folder:**

Ask for their local folder path and offer to run:
```bash
cd /path/to/their/folder
git init
git remote add origin https://github.com/username/repo-name.git
```

**If YES:**

Check if folder is already initialized:
```bash
git status
```

Offer to run this. If it shows "not a git repository", proceed with initialization.

### Step 3: Configure .gitignore

Before first commit, ask about files they DON'T want synced:

Common files to exclude:
- System files (.DS_Store, Thumbs.db)
- Dependencies (node_modules/, venv/, .venv/)
- Build outputs (dist/, build/, *.pyc)
- Environment files (.env, .env.local)
- IDE settings (.vscode/, .idea/)
- Logs (*.log)

Offer to create a .gitignore file with appropriate exclusions based on their project type.

Ask: "What type of project is this?" (Python, JavaScript, Java, etc.)

Generate appropriate .gitignore template and offer to create the file.

### Step 4: Initial Sync

Walk through the first synchronization:

```bash
# 1. Stage all files
git add .

# 2. Create first commit
git commit -m "Initial commit"

# 3. Push to GitHub
git branch -M main
git push -u origin main
```

Offer to run these commands step by step, explaining what each does.

### Step 5: Regular Workflow

Teach the ongoing synchronization routine:

**Before starting work each day:**
```bash
git pull origin main
```
This downloads any changes from GitHub (in case you worked elsewhere or teammates contributed).

**After making changes:**
```bash
# 1. Check what changed
git status

# 2. Review changes (optional but recommended)
git diff

# 3. Stage specific files or all changes
git add <file>  # for specific file
# or
git add .  # for all changes

# 4. Commit with descriptive message
git commit -m "Describe what you changed and why"

# 5. Push to GitHub
git push origin main
```

### Step 6: Best Practices

Share important tips:
- **Commit frequently:** Small, logical commits are better than large ones
- **Write good messages:** Describe WHAT and WHY, not just what files changed
- **Pull before push:** Always pull latest changes before pushing
- **Review before commit:** Use `git status` and `git diff` to see what you're committing

### Step 7: Create Quick Reference

Offer to create a cheat sheet file in their directory with the common commands.

If accepted, create `GIT_WORKFLOW.md`:
```markdown
# Git Sync Workflow

## Daily Routine

### Before Starting Work
git pull origin main

### After Making Changes
git status              # See what changed
git diff                # Review changes
git add .               # Stage all changes
git commit -m "message" # Commit with description
git push origin main    # Upload to GitHub

## Tips
- Commit frequently (multiple times per day)
- Pull before starting work
- Write clear commit messages
- Review changes before committing
```

## Solution Workflow 4: Merge Conflicts

**Problem confirmed:** User encountered merge conflict errors.

### Step 1: Calm and Explain

Reassure the user:
- Merge conflicts are normal and expected in collaborative work
- They happen when the same lines of code are edited in different ways
- They're not dangerous - just need manual resolution
- Git is asking you to choose which version to keep

### Step 2: Understand the Situation

Ask clarifying questions:
- What were you doing when this happened? (pulling, merging, rebasing)
- Are you working alone or with others?
- Do you know what changes exist on GitHub vs your local files?

### Step 3: Show Current Status

Offer to run:
```bash
git status
```

This shows which files have conflicts.

### Step 4: Explain Conflict Markers

Explain what they'll see in conflicted files:

```
<<<<<<< HEAD
Your local changes are here
=======
The changes from GitHub are here
>>>>>>> branch-name
```

- `<<<<<<< HEAD` marks the start of your local version
- `=======` separates the two versions
- `>>>>>>>` marks the end of the remote version

### Step 5: Resolution Strategy

Ask which approach they prefer:

**Option A: Manual Resolution (Recommended)**
1. Open each conflicted file
2. Find the conflict markers
3. Decide what to keep:
   - Keep your version (delete the other and markers)
   - Keep their version (delete yours and markers)
   - Combine both (merge the logic and delete markers)
4. Save the file
5. Stage the resolved file: `git add <file>`
6. Complete the merge: `git commit`

**Option B: Choose All Yours**
```bash
git checkout --ours <file>
git add <file>
```

**Option C: Choose All Theirs**
```bash
git checkout --theirs <file>
git add <file>
```

**Option D: Abort the Merge**
```bash
git merge --abort
# or
git rebase --abort
```

### Step 6: Guide Through Resolution

Based on their choice, guide step-by-step:

**For Manual Resolution:**
1. Offer to read the conflicted file and show them the conflicts
2. For each conflict, ask: "Do you want to keep your version, their version, or combine them?"
3. Offer to make the edits for them
4. After all conflicts resolved, run:
```bash
git add <resolved-file>
```
5. Complete the merge:
```bash
git commit -m "Resolved merge conflicts"
```

### Step 7: Verify and Complete

After resolution:
```bash
git status  # Should show no conflicts
git push origin main  # Upload the resolution
```

Offer to run these commands.

### Step 8: Prevention Tips

Share strategies to minimize future conflicts:
- **Pull frequently:** Get changes before they pile up
- **Communicate:** Let teammates know what files you're working on
- **Keep commits small:** Easier to resolve smaller conflicts
- **Work on different files:** When possible, divide work to avoid same-file edits

## Solution Workflow 5: Sensitive Data Exposure

**Problem confirmed:** User accidentally committed sensitive information (passwords, API keys, tokens, etc.)

### Step 1: Assess Urgency

Ask critical questions:
- Have you pushed this to GitHub yet?
- Is the repository public or private?
- What type of sensitive data? (password, API key, private key, credentials)

**CRITICAL: If pushed to public repository:**
Emphasize extreme urgency:
- Assume the secrets are already compromised
- They need to rotate/change all exposed credentials IMMEDIATELY
- Bots scan public GitHub commits for secrets within minutes

### Step 2: Immediate Action - Rotate Credentials

**This is the most important step:**

Instruct user to immediately:
1. **Change the exposed password** (if it's a password)
2. **Revoke and regenerate API keys** (if API keys)
3. **Rotate tokens** (if tokens/secrets)
4. **Disable compromised credentials** (if service accounts)

Explain: Removing the file from Git history does NOT undo the exposure. Anyone who saw the commit still has the secret.

### Step 3: Identify Affected Files

Offer to run:
```bash
git status
```

Ask them to identify which files contain sensitive data.

### Step 4: Removal Strategy

**If NOT yet pushed:**

Explain this is much simpler since it's only local.

**Option A: Remove from last commit (if just committed):**
```bash
# Remove file from tracking but keep locally
git rm --cached <sensitive-file>

# Amend the previous commit
git commit --amend -m "Remove sensitive file"
```

**Option B: Completely remove file:**
```bash
git rm --cached <sensitive-file>
git commit -m "Remove sensitive file"
```

Offer to run these commands.

**If ALREADY pushed:**

Explain this is more complex and requires rewriting history.

**Important warnings:**
- This will rewrite commit history
- If others have pulled the commits, they'll need to re-clone
- This should only be done if absolutely necessary

**Option A: Use BFG Repo-Cleaner (Recommended for large repos):**

Provide instructions:
1. Download BFG: https://rtyley.github.io/bfg-repo-cleaner/
2. Clone a fresh mirror:
```bash
git clone --mirror https://github.com/username/repo.git
```
3. Run BFG:
```bash
bfg --delete-files <filename> repo.git
# or for text replacement
bfg --replace-text passwords.txt repo.git
```
4. Clean up and push:
```bash
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**Option B: Use git filter-branch (Built-in but slower):**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <path-to-file>" \
  --prune-empty --tag-name-filter cat -- --all

git push --force --all
```

Offer to help run these commands but warn about the implications.

### Step 5: Prevent Future Exposure

**Create/Update .gitignore:**

Offer to create or update .gitignore with common sensitive file patterns:
```
# Environment variables
.env
.env.local
.env.*.local

# Credentials
**/credentials.json
**/secrets.yml
**/*secret*
**/*credentials*

# Private keys
*.pem
*.key
*.p12
*.pfx

# API keys
**/apikeys.txt

# Config files with secrets
config/database.yml
config/secrets.yml
```

Ask about their specific project needs and customize accordingly.

### Step 6: Implement Pre-commit Checks

Suggest using tools to prevent future accidents:

**Option 1: git-secrets**
```bash
# Install git-secrets
# macOS
brew install git-secrets

# Configure for repo
git secrets --install
git secrets --register-aws
```

**Option 2: detect-secrets**
```bash
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

Offer to help set these up.

### Step 7: Verify Removal

After cleanup, verify the sensitive data is gone:
```bash
git log --all --full-history -- <path-to-file>
```

Should show no commits.

Search for the sensitive string in history:
```bash
git log -S "sensitive-string" --all
```

Should return no results.

### Step 8: Final Checklist

Confirm with user they've completed:
- [ ] Rotated/changed all exposed credentials
- [ ] Removed sensitive files from Git history
- [ ] Added files to .gitignore
- [ ] Pushed the cleanup (if applicable)
- [ ] Verified removal with git log
- [ ] Set up pre-commit hooks (optional)
- [ ] Documented which credentials were exposed for their records

## Ongoing Support and Follow-up

After completing any solution workflow:

1. **Verify Success:** Ask user to confirm the problem is resolved
2. **Test the Solution:** Encourage them to test the operation that was failing
3. **Provide Resources:** Share relevant GitHub documentation links
4. **Offer Additional Help:** Ask if they have other GitHub-related questions
5. **Teach Prevention:** Share best practices to avoid the issue in the future

## Additional Troubleshooting

If the user's issue doesn't fit the 5 main scenarios or solution didn't work:

### Common Additional Issues

**Permission Denied Errors:**
- Check repository access permissions on GitHub
- Verify correct username/organization
- Confirm repository exists and URL is correct

**"Repository not found" Errors:**
- Verify repository URL spelling
- Check if repository is private (requires authentication)
- Confirm user has access to the repository

**Detached HEAD State:**
- Explain what detached HEAD means
- Guide back to branch: `git checkout main`

**Large File Errors:**
- Explain GitHub's file size limits (100MB)
- Suggest Git LFS for large files
- Help remove large files if needed

**Untracked Files Overwrite Errors:**
- Use `git stash` to save local changes
- Pull, then apply stash: `git stash pop`

For any issue, maintain the diagnostic approach:
1. Ask for exact error message
2. Check current state with `git status`
3. Understand what they were trying to do
4. Provide step-by-step solution
5. Verify resolution

## Best Practices for This Skill

**Tone:**
- Patient and encouraging - users are learning
- Non-judgmental about mistakes (everyone makes them)
- Clear and specific with instructions
- Celebrate successes when issues are resolved

**Command Execution:**
- Always explain what a command does before running it
- Offer to run commands but let user decide
- Show expected output so they know what's normal
- If a command fails, read the error and adjust approach

**Teaching Approach:**
- Explain the "why" not just the "how"
- Connect actions to concepts
- Build mental models of how Git/GitHub work
- Empower users to solve similar issues themselves

**Safety:**
- Warn before destructive operations (force push, filter-branch)
- Recommend backups when rewriting history
- Double-check before rotating credentials
- Verify commands in safe environments first

**Follow-through:**
- Don't leave users hanging at any step
- Verify each step completed before moving to next
- Offer alternatives if primary solution doesn't work
- Ensure problem is fully resolved, not just partially

## Quick Reference Commands

For easy copy-paste during troubleshooting:

**Status Checks:**
```bash
git status
git remote -v
git branch -a
git log --oneline -5
```

**Common Fixes:**
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# View what will be pushed
git diff origin/main main

# Update remote tracking
git fetch --prune

# Sync fork with upstream
git fetch upstream
git merge upstream/main
```

**Config:**
```bash
# Set username
git config --global user.name "Your Name"

# Set email
git config --global user.email "your.email@example.com"

# View all config
git config --list
```

This comprehensive skill should handle the vast majority of GitHub issues faced by new users with accuracy and clarity.
