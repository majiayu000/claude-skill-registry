---
name: fastcode-search
description: Native Node.js semantic search for Agent. No external dependencies.
category: research-analysis
version: 2.0.0
layer: core-skill
---

# FastCode Search (Native)

> **Core Capability**: Lightning-fast codebase navigation using local Node.js indexing.
> **Zero Cost**: Runs locally. No API calls.

## 🤖 Agent Instructions (MANDATORY)

**Rule: BEFORE reading any file content to understand logic, you MUST use FastCode.**

### 1. When to use?
- User asks "Where is the login logic?"
- You need to fix a bug but don't know the exact file.
- You want to understand the project structure.

### 2. How to use?
Run the internal Node.js script. **Do not ask user to install anything.**

#### Step 1: Search
```bash
node cli/skills/fastcode.js search "your_query_here"
```

#### Step 2: Analyze Results
The script returns a JSON list of most relevant files.
- **Action**: Read ONLY the top 1-3 files returned.
- **Benefit**: Saves tokens (don't read the whole repo).

### 3. Maintenance (Auto-Index)
If search returns nothing or "Index not found", run indexing first:
```bash
node cli/skills/fastcode.js index
```

---

## 🛠️ For Humans (Optional)
You can also run this manually if you want:
`node cli/skills/fastcode.js search "auth"`
