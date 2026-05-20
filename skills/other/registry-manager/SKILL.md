---
name: registry-manager
description: Maintain the skills registry by scanning installed skills and updating skills.json. Use when adding, removing, or auditing skills.
---

# Registry Manager v1.1.0

## Core Principle

**Single source of truth. Scan → Parse → Update → Validate.**

The registry is auto-generated from scanning `SKILL.md` files. Never edit it manually—always regenerate.

---

## When to Use

- After installing new skills
- After removing skills
- To audit what skills are available
- When registry files are missing or outdated
- During project setup

---

## Output Files

The rebuild script generates **two files**:

| File | Size | Purpose |
|------|------|---------|
| `skills.json` | ~20KB | Full registry for tools, validation, CI |
| `skills-index.json` | ~5KB | Compact index optimized for LLMs |

### skills-index.json (LLM-optimized)

```json
{
  "v": "1.1.0",
  "n": 30,
  "skills": {
    "core": [
      {"id": "bd", "desc": "Backlog management...", "path": ".claude/core/bd"},
      {"id": "git", "desc": "Git hygiene...", "path": ".claude/core/git"}
    ],
    "devops": [...]
  }
}
```

**Benefits:**
- 71% smaller than full registry
- Grouped by category for fast scanning
- Truncated descriptions (120 chars max)
- Short keys (`v`, `n`, `desc`) save tokens

---

## Skills Locations

Skills can exist in **multiple locations**:

```
project/
├── .claude/
│   ├── skills.json           ← Full registry
│   ├── skills-index.json     ← LLM-optimized index
│   ├── rebuild-registry.js   ← Rebuild script
│   └── skills/               ← Primary location
│       ├── core/
│       ├── engineering/
│       └── [any-category]/   ← Categories auto-detected
│
└── .github/
    └── skills/               ← Alternative location
        └── [any-category]/
```

**Rules:**
- Categories are **auto-detected** from folder names
- Skills are deduplicated by `id` (first found wins)
- Both outputs always go to `.claude/`

---

## Quick Rebuild (Recommended)

```bash
cd .claude && node rebuild-registry.js
```

**Output:**
```
╔════════════════════════════════════╗
║   Skills Registry Rebuild v1.1.0   ║
╚════════════════════════════════════╝

Scanning locations:
  📁 .claude/skills/
  📁 .github/skills/

  ✓ bd (.claude)
  ✓ git (.claude)
  ...

────────────────────────────────────
✅ Registry updated: 30 skills

📄 Generated files:
   skills.json       19.7KB (full)
   skills-index.json 5.7KB (LLM-optimized)

📊 By category:
   core: 15
   engineering: 4
   ...
────────────────────────────────────
```

---

## Full Rebuild Process (Manual)

Execute these steps **in order**, one skill at a time.

### Step 0: Initialize Registry

```bash
# Create empty registry if missing
cat > .claude/skills.json << 'EOF'
{
  "version": "1.0.0",
  "updated_at": "",
  "skills": []
}
EOF
```

### Step 1: Discover All Skills

```bash
# Find all SKILL.md files
find .claude/skills -name "SKILL.md" -type f | sort
```

**Record the list.** Process each file one by one in the following steps.

### Step 2: Parse One Skill

For each `SKILL.md` file found, extract metadata:

```bash
# Example: parsing a single skill
SKILL_FILE=".claude/skills/core/git/SKILL.md"

# Extract frontmatter (lines between --- markers)
sed -n '/^---$/,/^---$/p' "$SKILL_FILE" | head -20
```

**Extract these fields from frontmatter:**

| Field | Source | Required |
|-------|--------|----------|
| `id` | `name` field in frontmatter | ✅ Yes |
| `name` | Convert id to Title Case | ✅ Yes |
| `description` | `description` field | ✅ Yes |
| `category` | Parent folder name | ✅ Yes |
| `path` | Relative path from `.claude/` | ✅ Yes |
| `tags` | Extract from description keywords | Optional |
| `triggers` | From "When to Use" section | Optional |
| `dependencies` | Look for skill references | Optional |

### Step 3: Build Skill Entry

Transform parsed data into a registry entry:

```json
{
  "id": "git",
  "name": "Git",
  "description": "Git hygiene for multi-agent work. Use when committing, pushing, or syncing with remote.",
  "category": "core",
  "tags": ["git", "version-control", "sync"],
  "triggers": ["git pull", "git push", "commit", "sync remote"],
  "path": "skills/core/git/SKILL.md",
  "dependencies": []
}
```

### Step 4: Validate Entry

Before adding, verify:

```
□ id matches folder name
□ id is lowercase with hyphens only
□ description is under 300 chars
□ path points to existing file
□ category matches parent folder
□ no duplicate id in registry
```

**If validation fails:** Log the error, skip this skill, continue to next.

### Step 5: Add to Registry

Append the validated entry to the skills array.

### Step 6: Repeat for All Skills

Go back to Step 2 for the next `SKILL.md` file until all are processed.

### Step 7: Finalize Registry

```bash
# Update timestamp
# The final skills.json should look like:
{
  "version": "1.0.0",
  "updated_at": "2026-01-25T12:00:00Z",
  "skills": [
    { /* skill 1 */ },
    { /* skill 2 */ },
    ...
  ]
}
```

---

## Quick Rebuild Script

Use this Node.js script for automated rebuilding:

```javascript
#!/usr/bin/env node
// rebuild-registry.js

const fs = require('fs');
const path = require('path');

const SKILLS_DIR = '.claude/skills';
const REGISTRY_PATH = '.claude/skills.json';
const CATEGORIES = ['core', 'engineering', 'devops', 'documentation', 'research'];

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  
  const frontmatter = {};
  match[1].split('\n').forEach(line => {
    const [key, ...rest] = line.split(':');
    if (key && rest.length) {
      frontmatter[key.trim()] = rest.join(':').trim();
    }
  });
  return frontmatter;
}

function extractTriggers(content) {
  const whenToUse = content.match(/## When to Use[\s\S]*?(?=\n## |$)/);
  if (!whenToUse) return [];
  
  const triggers = [];
  const lines = whenToUse[0].split('\n');
  lines.forEach(line => {
    const match = line.match(/^[-*]\s+(.+)/);
    if (match) {
      // Extract key phrases
      const phrase = match[1].toLowerCase()
        .replace(/when |use |for |to /g, '')
        .trim()
        .slice(0, 50);
      if (phrase.length > 3) triggers.push(phrase);
    }
  });
  return triggers.slice(0, 5);
}

function extractTags(description, id) {
  const words = description.toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .split(/\s+/)
    .filter(w => w.length > 3 && !['when', 'with', 'this', 'that', 'from', 'using'].includes(w));
  
  const tags = [...new Set([id, ...words.slice(0, 4)])];
  return tags.slice(0, 6);
}

function scanSkills() {
  const skills = [];
  const errors = [];
  
  CATEGORIES.forEach(category => {
    const categoryPath = path.join(SKILLS_DIR, category);
    if (!fs.existsSync(categoryPath)) return;
    
    const folders = fs.readdirSync(categoryPath, { withFileTypes: true })
      .filter(d => d.isDirectory());
    
    folders.forEach(folder => {
      const skillPath = path.join(categoryPath, folder.name, 'SKILL.md');
      
      if (!fs.existsSync(skillPath)) {
        errors.push(`Missing SKILL.md: ${skillPath}`);
        return;
      }
      
      try {
        const content = fs.readFileSync(skillPath, 'utf-8');
        const frontmatter = parseFrontmatter(content);
        
        if (!frontmatter || !frontmatter.name || !frontmatter.description) {
          errors.push(`Invalid frontmatter: ${skillPath}`);
          return;
        }
        
        // Validate id matches folder
        if (frontmatter.name !== folder.name) {
          errors.push(`Name mismatch: ${frontmatter.name} vs folder ${folder.name}`);
        }
        
        const skill = {
          id: frontmatter.name,
          name: frontmatter.name
            .split('-')
            .map(w => w.charAt(0).toUpperCase() + w.slice(1))
            .join(' '),
          description: frontmatter.description.slice(0, 300),
          category: category,
          tags: extractTags(frontmatter.description, frontmatter.name),
          triggers: extractTriggers(content),
          path: `skills/${category}/${folder.name}/SKILL.md`,
          dependencies: []
        };
        
        skills.push(skill);
        console.log(`✓ ${skill.id}`);
        
      } catch (err) {
        errors.push(`Error parsing ${skillPath}: ${err.message}`);
      }
    });
  });
  
  return { skills, errors };
}

function main() {
  console.log('Scanning skills...\n');
  
  const { skills, errors } = scanSkills();
  
  const registry = {
    version: '1.0.0',
    updated_at: new Date().toISOString(),
    skills: skills.sort((a, b) => a.id.localeCompare(b.id))
  };
  
  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2));
  
  console.log(`\n✅ Registry updated: ${skills.length} skills`);
  
  if (errors.length) {
    console.log(`\n⚠️  Errors (${errors.length}):`);
    errors.forEach(e => console.log(`   - ${e}`));
  }
}

main();
```

**Run it:**

```bash
node rebuild-registry.js
```

---

## Manual Workflow (No Script)

If you can't run scripts, follow this systematic process:

### 1. List All Skills

```bash
find .claude/skills -name "SKILL.md" | while read f; do
  echo "---"
  echo "FILE: $f"
  head -10 "$f"
done
```

### 2. For Each Skill, Create Entry

Read the file, extract:
- `name` from frontmatter → becomes `id`
- `description` from frontmatter
- folder path → determines `category` and `path`

### 3. Assemble JSON

Build the registry manually, one entry at a time:

```json
{
  "version": "1.0.0",
  "updated_at": "2026-01-25T12:00:00Z",
  "skills": [
    {
      "id": "bd",
      "name": "BD (Beads)",
      "description": "Backlog management with bd utility...",
      "category": "core",
      "tags": ["backlog", "tasks"],
      "triggers": ["create issue", "backlog"],
      "path": "skills/core/bd/SKILL.md",
      "dependencies": []
    }
  ]
}
```

### 4. Validate JSON

```bash
# Check JSON syntax
cat .claude/skills.json | python3 -m json.tool > /dev/null && echo "✓ Valid JSON"

# Validate against schema (if jq available)
# Or just visually verify structure
```

---

## Adding a Single Skill

When adding just one new skill:

### 1. Parse the New Skill

```bash
SKILL_PATH=".claude/skills/core/new-skill/SKILL.md"
head -20 "$SKILL_PATH"
```

### 2. Create Entry

```json
{
  "id": "new-skill",
  "name": "New Skill",
  "description": "...",
  "category": "core",
  "tags": [],
  "triggers": [],
  "path": "skills/core/new-skill/SKILL.md",
  "dependencies": []
}
```

### 3. Insert into Registry

Add to the `skills` array in `skills.json`, maintaining alphabetical order by `id`.

### 4. Update Timestamp

```json
"updated_at": "2026-01-25T12:00:00Z"
```

---

## Removing a Skill

### 1. Delete the Folder

```bash
rm -rf .claude/skills/core/old-skill
```

### 2. Remove from Registry

Delete the corresponding entry from `skills.json`.

### 3. Update Timestamp

---

## Audit / Verify

Check for inconsistencies:

```bash
# Skills on disk but not in registry
find .claude/skills -name "SKILL.md" -exec dirname {} \; | sort > /tmp/disk.txt

# Skills in registry
cat .claude/skills.json | grep '"path"' | sed 's/.*skills\///' | sed 's/\/SKILL.md.*//' | sort > /tmp/registry.txt

# Compare
diff /tmp/disk.txt /tmp/registry.txt
```

**If differences found:** Run full rebuild.

---

## Registry Entry Template

Copy this for new entries:

```json
{
  "id": "",
  "name": "",
  "description": "",
  "category": "",
  "tags": [],
  "triggers": [],
  "path": "",
  "dependencies": []
}
```

**Field guide:**

| Field | Example | Notes |
|-------|---------|-------|
| `id` | `"code-review"` | Matches folder name, lowercase-hyphen |
| `name` | `"Code Review"` | Human readable |
| `description` | `"Systematic code review. Use when reviewing PRs."` | WHAT + WHEN |
| `category` | `"core"` | One of: core, engineering, devops, documentation, research |
| `tags` | `["review", "quality"]` | Searchable keywords |
| `triggers` | `["review code", "PR review"]` | Activation phrases |
| `path` | `"skills/core/code-review/SKILL.md"` | Relative to `.claude/` |
| `dependencies` | `["git"]` | Other skill IDs needed first |

---

## Quick Reference

```
Commands:
  Full rebuild    → node rebuild-registry.js
  Find skills     → find .claude/skills -name "SKILL.md"
  Validate JSON   → python3 -m json.tool < skills.json
  Audit           → diff disk vs registry

Locations:
  Registry        → .claude/skills.json
  Schema          → .claude/skills.schema.json
  Skills          → .claude/skills/{category}/{skill-id}/SKILL.md

Process:
  1. Scan: find all SKILL.md files
  2. Parse: extract frontmatter
  3. Transform: build entry object
  4. Validate: check required fields
  5. Insert: add to skills array
  6. Save: update skills.json with timestamp
```
