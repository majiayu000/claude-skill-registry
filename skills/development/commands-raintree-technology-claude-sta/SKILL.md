---
name: commands-raintree-technology-claude-sta
description: Install a Claude Code skill from a GitHub repository URL with guided
  setup and validation.
---

# Install Skill

Install a Claude Code skill from a GitHub repository URL with guided setup and validation.

**Usage:** `/install-skill <github-url> [--personal|--project]`

**Options:**
- `--personal` - Install to `~/.claude/skills/` (available in all projects)
- `--project` - Install to `.claude/skills/` (project-specific, default)

**Examples:**
- `/install-skill https://github.com/user/repo/blob/main/skill.md`
- `/install-skill https://raw.githubusercontent.com/user/repo/main/skill.md --personal`
- `/install-skill https://github.com/user/skills/tree/main/api/stripe.md --project`

## Overview

This command helps you safely install Claude Code skills from GitHub repositories with:

✅ URL validation and conversion to raw format
✅ Skill content preview and security review
✅ Installation location selection
✅ Automatic file naming from skill title
✅ Installation verification
✅ Documentation update suggestions

## Workflow

### 1. Parse and Validate URL

**Accept these GitHub URL formats:**
- `https://github.com/user/repo/blob/branch/path/skill.md`
- `https://raw.githubusercontent.com/user/repo/branch/path/skill.md`
- `https://github.com/user/repo/tree/branch/path/skill.md`

**Convert to raw URL:**
```
github.com/user/repo/blob/main/skill.md
↓
raw.githubusercontent.com/user/repo/main/skill.md
```

**Validate:**
- ✅ Valid GitHub domain
- ✅ Repository exists
- ✅ File is `.md` format
- ✅ URL is accessible

If validation fails, show error and suggest corrections.

### 2. Fetch Skill Content

Download the skill file from the raw GitHub URL.

**Use WebFetch or curl to retrieve:**
```bash
curl -sL <raw-github-url>
```

**Check for errors:**
- 404: File not found
- 403: Access denied or rate limited
- Invalid format: Not a markdown file

### 3. Preview and Security Review

**Display skill preview:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: {extracted title}
Source: {github-url}
Size: {file-size}

Description:
{first 500 chars of skill content}

Keywords/Triggers:
{extracted keywords if visible}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Security Notice:**
```
⚠️  SECURITY REVIEW REQUIRED

Please review this skill's content before installing:

1. Check the code doesn't contain malicious commands
2. Verify it matches your use case
3. Confirm the source repository is trustworthy
4. Review any bash commands or file operations

Would you like to:
  [A] View full skill content
  [B] Continue with installation
  [C] Cancel installation
```

Wait for user confirmation before proceeding.

### 4. Determine Installation Location

**If user specified flag:**
- `--personal` → Install to `~/.claude/skills/`
- `--project` → Install to `.claude/skills/`

**If no flag specified:**
- Default to `.claude/skills/` (project-specific)
- Show installation location
- Ask user to confirm or change

**Validate location:**
```bash
# Check if directory exists
ls ~/.claude/skills/ 2>/dev/null
ls .claude/skills/ 2>/dev/null

# Create if needed
mkdir -p ~/.claude/skills/
mkdir -p .claude/skills/
```

### 5. Determine Filename

**Extract skill title from content:**
- Read first `# Heading` in markdown
- Convert to kebab-case filename
- Ensure `.md` extension

**Examples:**
- `# Stripe API` → `stripe-api.md`
- `# Docker Compose Helper` → `docker-compose-helper.md`
- `# SQL Query Optimizer` → `sql-query-optimizer.md`

**Handle conflicts:**
If file already exists:
```
⚠️  File already exists: {filename}

Options:
  [O] Overwrite existing skill
  [R] Rename to {filename}-2.md
  [C] Cancel installation
```

### 6. Install the Skill

**Download and save:**
```bash
# Using curl
curl -o {install-path}/{filename} {raw-github-url}

# Verify file was created
ls -lh {install-path}/{filename}
```

**Show progress:**
```
Installing skill...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: {github-url}
Target: {install-path}/{filename}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Downloading... ✓
Saving... ✓
```

### 7. Verify Installation

**Check installation:**
```bash
# Confirm file exists and has content
ls -lh {install-path}/{filename}
wc -l {install-path}/{filename}
```

**Show success message:**
```
✅ Skill installed successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill: {title}
Location: {install-path}/{filename}
Size: {file-size}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The skill will auto-activate when you:
{list activation scenarios from skill description}
```

### 8. Suggest Next Steps

**Post-installation guidance:**

```
Next Steps:

1. Test the skill:
   Try asking Claude about {skill-domain}
   The skill should auto-activate

2. Update documentation:
   Add this skill to your project's .claude/DIRECTORY.md

3. Find more skills:
   Use /discover-skills to browse SkillsMP

4. Manage skills:
   View: ls {install-path}/
   Remove: rm {install-path}/{filename}
   Update: /install-skill {url} (overwrites)
```

## Examples

### Example 1: Install from GitHub URL

**Command:**
```
/install-skill https://github.com/anthropics/skills/blob/main/api/stripe.md
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: Stripe API
Source: anthropics/skills
Size: 15.2 KB

Description:
Expert knowledge of Stripe API v2024. Provides
guidance on payments, subscriptions, customers,
webhooks, and best practices...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Review skill content? [View/Continue/Cancel]: c

✅ Skill installed successfully!

Location: .claude/skills/stripe-api.md
Size: 15.2 KB

The skill will auto-activate when you:
  • Mention Stripe API integration
  • Work with payment processing
  • Configure webhooks or subscriptions
```

### Example 2: Install to Personal Directory

**Command:**
```
/install-skill https://raw.githubusercontent.com/user/repo/main/docker.md --personal
```

**Output:**
```
Installing to personal directory...
This skill will be available in ALL your projects.

✅ Skill installed successfully!

Location: ~/.claude/skills/docker.md
Size: 8.4 KB

Next steps:
  • Test: Ask Claude about Docker containers
  • View all personal skills: ls ~/.claude/skills/
```

### Example 3: Handle Existing File

**Command:**
```
/install-skill https://github.com/user/repo/blob/main/sql.md
```

**Output:**
```
⚠️  File already exists: .claude/skills/sql.md

Current file: 12.1 KB (installed 3 days ago)
New file: 14.3 KB (updated 1 day ago)

Options:
  [O] Overwrite with newer version
  [R] Rename to sql-2.md
  [C] Cancel

Choice: o

✅ Skill updated successfully!

Location: .claude/skills/sql.md
Size: 14.3 KB (updated from 12.1 KB)
```

## Error Handling

### Invalid URL
```
❌ Error: Invalid GitHub URL

Expected format:
  https://github.com/user/repo/blob/branch/path/skill.md

Received:
  {user-provided-url}

Tip: Get the URL from SkillsMP or directly from GitHub
```

### File Not Found (404)
```
❌ Error: Skill file not found

URL: {github-url}
Status: 404 Not Found

Possible causes:
  • File moved or deleted
  • Wrong branch name
  • Private repository
  • Incorrect path

Try:
  • Check repository on GitHub
  • Verify file still exists
  • Use /discover-skills to find alternatives
```

### Not a Markdown File
```
❌ Error: Invalid file format

Expected: .md (Markdown)
Received: {extension}

Claude Code skills must be markdown files (.md)
```

### Permission Denied
```
❌ Error: Cannot write to {install-path}

Possible causes:
  • Directory doesn't exist
  • Insufficient permissions

Try:
  • Create directory: mkdir -p {install-path}
  • Check permissions: ls -ld {install-path}
```

## Advanced Usage

### Batch Installation

Install multiple skills from a list:

```bash
# Create skills-list.txt with URLs
cat > skills-list.txt <<EOF
https://github.com/user/repo/blob/main/skill1.md
https://github.com/user/repo/blob/main/skill2.md
https://github.com/user/repo/blob/main/skill3.md
EOF

# Install each (requires manual approval for security)
while read url; do
  /install-skill "$url"
done < skills-list.txt
```

### Update Existing Skills

To update a skill to the latest version:
```
/install-skill <original-url>
# Choose [O] Overwrite when prompted
```

### Remove Skills

```bash
# Remove project skill
rm .claude/skills/skill-name.md

# Remove personal skill
rm ~/.claude/skills/skill-name.md

# List and remove interactively
ls .claude/skills/
rm .claude/skills/<tab-complete>
```

## Security Best Practices

**Before installing any skill:**

1. ✅ **Review the source:**
   - Check repository reputation
   - Verify maintainer identity
   - Look for community stars/activity

2. ✅ **Inspect the content:**
   - View full skill markdown
   - Check for suspicious bash commands
   - Verify file operations are safe

3. ✅ **Test in isolation:**
   - Install to project directory first
   - Test functionality
   - Verify expected behavior

4. ✅ **Keep updated:**
   - Check for skill updates periodically
   - Re-install from source to update
   - Review changelog if available

## Related Commands

- `/discover-skills` - Browse SkillsMP marketplace
- See `.claude/DIRECTORY.md` - View all installed skills
- See `.claude/skills/ai/skill-builder.md` - Create your own skills

## Resources

- **SkillsMP:** https://skillsmp.com
- **Claude Code Docs:** https://code.claude.com/docs/skills
- **Security Guide:** Always review code before installation
