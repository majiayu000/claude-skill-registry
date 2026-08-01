---
name: hippocampus
description: 'Search hippocampus knowledge base for documentation, conventions, patterns,
  and how-to guides (discovery: requirements-clarity). Evaluate at requirements-clarity
  when user asks "how do I...", "find my'
---

---
name: hippocampus
description: Search hippocampus knowledge base for documentation, conventions, patterns, and how-to guides (discovery: requirements-clarity). Evaluate at requirements-clarity when user asks "how do I...", "find my...", "what's my convention for...", "continue working on...", or wants to create/edit persistent documentation. All markdown files must go to hippocampus - none created elsewhere.
---

# Hippocampus Knowledge Base

## Core Rule

**ALL markdown → hippocampus. No exceptions.**

- Never create .md files in project directories
- Never create .md files in /tmp or elsewhere
- Everything goes to `~/.claude/hippocampus/` (global or project tier)

## Authority Model

- **AI autonomy:** Search and present options (no approval needed)
- **User authority:** Tier selection, phantom node choice, edit vs create
- **Pattern:** AI finds, user classifies

## Determine Intent

- **Finding resource?** → Discovery path
- **Creating/editing markdown?** → Create/Edit path
- **Adding binary files?** (auto-detect: .png, .jpg, .pdf, .opus, .mp3, .mp4, etc.) → Binary Asset path

---

## Discovery Path

### Step 1: Search Hippocampus
- Use Task tool with `subagent_type=Explore` to search hippocampus
- Path: `~/.claude/hippocampus/`
- Search query based on user's request

### Step 2: Present Paths for Selection
- Show found file paths via AskUserQuestion with `multiSelect: true`
- User selects which files to read
- Only read selected files (saves context window)

### Step 3: Return Content
- Read only the user-selected files
- Return relevant content to user

---

## Create/Edit Path

### Step 1: Search First
- Use Task tool with `subagent_type=Explore` to search hippocampus
- Path: `~/.claude/hippocampus/`
- Check if similar content already exists
- **If found:** Present paths via AskUserQuestion → user picks to edit or create new
- **If not found:** Continue to Step 2

### Step 2: Tier Selection
AskUserQuestion with options:
- **Global** (`~/.claude/hippocampus/global/`): Cross-project content (ADRs, patterns, business ops)
  - Phantom nodes: Topic-based (e.g., `[[docker-deployment]]`, `[[prompt-engineering]]`)
- **Project** (`~/.claude/hippocampus/project/{name}/`): Client-specific content
  - Phantom nodes: Client-based (e.g., `[[client-archibus]]`, `[[client-iitr]]`)

### Step 3: Phantom Node Selection
- Use Explore agent to search for existing phantom nodes in hippocampus
- Present found options to user via AskUserQuestion
- User picks existing or creates new `[[phantom-node]]`
- Convention: Use tier-appropriate phantom node type (topic-based for global, client-based for project)

### Step 4: Publishing Decision
AskUserQuestion:
- **Publish to GitHub Pages?**
- Options: Yes / No
- If Yes: Add `publish: true` to frontmatter
- Result: File will be mirrored to public-wilsch-ai-pages repo on push
- **Return link:** `https://mariuswilsch.github.io/public-wilsch-ai-pages/{tier}/{filename}` (without .md extension)

### Step 5: Create File
- Path: `~/.claude/hippocampus/{tier}/filename.md`
- Include selected phantom node wikilink on Line 2-3, after `# Title`
- Use descriptive filename (no prefixes needed)

### Step 6: Git Commit
- Commit changes with descriptive message
- Git tracks all document evolution

---

## Binary Asset Path

For non-markdown files (images, PDFs, audio, video, etc.)

### Step 1: Tier + Folder Selection
- Same as Create/Edit path: Global or Project tier
- Files go to: `~/.claude/hippocampus/{tier}/{folder}/`

### Step 2: Move Binary Files
- Move files to selected hippocampus folder
- Keep original filenames (or rename if requested)

### Step 3: Create Minimal Index
Create `index.md` with: title, phantom node, then one line per file:

```markdown
# {Descriptive Title}
[[phantom-node]]
![Image description](image.png)
[Document description](document.pdf)
[Audio description](audio.opus)
```

**Format by file type:**
- Images: `![Description](file.png)`
- Documents: `[Description](file.pdf)`
- Audio/Video: `[Description](file.opus)`

One index per folder. Add lines as files are added.

### Step 4: Git Commit
- Commit binary files + index.md together
- Message: "feat: add {description} to hippocampus"
