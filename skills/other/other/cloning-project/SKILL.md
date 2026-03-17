---
name: cloning-project
description: Exports project instructions and knowledge files from the current Claude project. Use when users want to clone, copy, backup, or export a project's configuration and files.
metadata:
  version: 1.0.0
---

# Cloning Project

When users request to clone, copy, export, or backup their current project:

## Step 1: Verify Project Context

Check if the user is in a project by looking for project-specific indicators:
- Project instructions in the context window
- Knowledge files mentioned in `<available_skills>` or similar sections
- User explicitly stating they're in a project

If not in a project, inform the user that this skill requires being inside a Claude project.

## Step 2: Gather Project Instructions

Project instructions are typically found in the context window as XML or markdown content describing the project's purpose and configuration. Extract and save these instructions to a file.

Create the instructions file:
```bash
cat > /home/claude/project-instructions.md << 'INSTRUCTIONS'
[Extracted project instructions content]
INSTRUCTIONS
```

## Step 3: Locate Knowledge Files

Knowledge files are user-uploaded documents stored in `/mnt/user-data/uploads/`. List all files:

```bash
ls -lh /mnt/user-data/uploads/
```

If knowledge files exist, copy them to the working directory for bundling:
```bash
cp /mnt/user-data/uploads/* /home/claude/project-export/
```

## Step 4: Create Export Bundle

**If only project instructions exist (no knowledge files):**
- Copy instructions directly to outputs:
  ```bash
  cp /home/claude/project-instructions.md /mnt/user-data/outputs/
  ```

**If project has both instructions and knowledge files:**
- Create an organized export directory:
  ```bash
  mkdir -p /home/claude/project-export
  cp /home/claude/project-instructions.md /home/claude/project-export/
  cp /mnt/user-data/uploads/* /home/claude/project-export/ 2>/dev/null || true
  ```
- Create zip bundle:
  ```bash
  cd /home/claude
  zip -r /mnt/user-data/outputs/project-export.zip project-export/
  ```
- Show bundle contents:
  ```bash
  unzip -l /mnt/user-data/outputs/project-export.zip
  ```

## Step 5: Provide Files and Instructions to User

Link the exported files:

**For single instructions file:**
```markdown
[Download project-instructions.md](computer:///mnt/user-data/outputs/project-instructions.md)
```

**For bundled export:**
```markdown
[Download project-export.zip](computer:///mnt/user-data/outputs/project-export.zip)
```

Then provide clear setup instructions:

```markdown
## How to Import Into a New Project

1. **Create a new Claude project** (or open an existing one where you want to clone this configuration)

2. **Add project instructions:**
   - Open the new project's settings
   - Navigate to the "Instructions" section
   - Copy and paste the content from `project-instructions.md`
   - Save the instructions

3. **Upload knowledge files** (if applicable):
   - In the new project, go to the "Knowledge" section
   - Upload all files from the export (except project-instructions.md)
   - Files will become available as project knowledge

Your project is now cloned with the same configuration and knowledge base.
```

## Edge Cases

**Empty project (no custom instructions or knowledge):**
- Inform the user that the project has no custom configuration to export
- Explain that projects by default only have access to Claude's base capabilities

**Large knowledge bases:**
- If the zip file exceeds reasonable size (~50MB), warn the user and suggest selective export
- Provide individual file links as fallback

**Corrupted or inaccessible files:**
- Skip files that cannot be read
- Report which files were successfully exported vs. skipped
- Provide export anyway with available content

## Usage Examples

**Trigger phrases:**
- "Clone this project"
- "Export my project configuration"
- "How do I copy this project setup?"
- "Backup my project"
- "Save this project's settings"
