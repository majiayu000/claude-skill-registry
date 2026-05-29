---
name: ref
description: Use when setting up Ref MCP server, managing API keys, or troubleshooting Ref documentation lookup issues. Also for dashboard operations (adding repos, uploading files), understanding pricing/credits, or deciding Ref vs alternatives. NOT for actually searching docs—just use ref_search_documentation directly.
---

# Ref

Documentation search MCP server. This skill covers **meta work** (setup, config, decisions)—not mainline doc searching.

> **To search docs:** Just call `ref_search_documentation` and `ref_read_url` directly. Don't invoke this skill.

## How Ref Works

### Search Philosophy

Ref uses **agentic search**: `search()` returns result overviews, then you selectively `read()` relevant pages. This matches how humans search—iterate and refine rather than batch retrieve.

### What Gets Indexed

| Source | What's Indexed |
|--------|----------------|
| Public GitHub repos | Small repos (<2k files): everything. Large repos: docs only |
| Your private repos | Same rules, synced every 5 minutes |
| Uploaded files | PDF and Markdown, chunked automatically |

**NOT indexed:** Man pages, system docs, CLI `--help` output.

### Freshness & Sync

- **GitHub repos:** Synced on 5-minute cron, incremental (compares commits)
- **Uploaded files:** Indexed immediately on upload
- **Public index:** Maintained by Ref team; request additions via [form](https://tally.so/r/nrvBY2)

### Library Versions

Ref indexes the **default branch** (usually `main`). For specific versions:
- Check if the repo tags releases with docs
- Upload version-specific docs manually if needed
- Use `ref_read_url` on a specific commit/tag URL if available

---

## Operations

### Doctor

Health check and repair for Ref setup. Handles fresh installs AND fixes drift (missing auth, outdated config, missing best practices).

Run all checks in order. Fix issues as found.

---

**Check 1: MCP Installation**

```bash
claude mcp list
```

| State | Action |
|-------|--------|
| `Ref: https://api.ref.tools/mcp (HTTP)` present | → Check 2 |
| Missing entirely | → Run Install Flow below |
| Shows as disabled | → `claude mcp enable Ref`, then Check 2 |

**Install Flow:**

1. Ask user with AskUserQuestion:
   - "I have a Ref account" → step 2
   - "I need to create one" → direct to https://ref.tools/signup, wait, then step 2

2. Tell user: "Go to https://ref.tools/install - paste the pre-populated command shown there."

3. Run the command user provides. Format:
   ```bash
   claude mcp add --transport http Ref https://api.ref.tools/mcp --header "x-ref-api-key: ref_..."
   ```

4. **Restart required.** Tell user:
   > "Restart Claude Code (Cmd+R or relaunch), then say 'continue' to resume doctor."

5. After restart, re-run Check 1.

---

**Check 2: Auth Validity**

Test the API key works:

```
ref_search_documentation: "what is ref mcp server"
```

| Result | Action |
|--------|--------|
| Results returned | → Check 3 |
| "not correctly configured" | → API key invalid. Tell user to get fresh key at https://ref.tools/keys, re-run Install Flow step 2 |
| Tool not found | → MCP not loaded. Restart Claude Code, re-run Check 1 |

---

**Check 3: Best Practices**

Reference: https://docs.ref.tools/getting-started/best-practices

**3a. Rules file exists**

Check for project rules file that mentions Ref:

```bash
# Check common locations
cat CLAUDE.md 2>/dev/null | grep -i ref || echo "NOT_FOUND"
cat AGENTS.md 2>/dev/null | grep -i ref || echo "NOT_FOUND"
cat .claude/rules/*.md 2>/dev/null | grep -i ref || echo "NOT_FOUND"
```

| State | Action |
|-------|--------|
| Ref mentioned in rules | → Check 3b |
| No Ref rule found | → Ask user with AskUserQuestion |

If no rule found, ask:
- "Add Ref rule to CLAUDE.md" (Recommended)
- "Add Ref rule to AGENTS.md" (cross-tool compatible)
- "Skip for now"

If adding, append this line to chosen file:
```
When working with libraries, check the docs with Ref.
```

**3b. Rule quality**

The rule should be simple. Per best practices, avoid:
- Over-prompting (checking docs for every interaction)
- Excessive complexity

Good: `When working with libraries, check the docs with Ref.`
Bad: `Always check Ref before any code change and verify all imports...`

If rule is overly complex, suggest simplifying.

---

**Check 4: Verification**

Final test - search Ref's own docs:

```
ref_search_documentation: "Claude Code MCP server installation"
```

Then read a result:

```
ref_read_url: <first relevant URL from results>
```

| Result | Status |
|--------|--------|
| Both tools work | ✅ Doctor complete |
| Any failure | Review earlier checks |

Report summary to user:
- MCP status
- Auth status
- Best practices status
- Test result

---

## Dashboard Operations

No API yet—these are manual steps via web UI.

### Adding a GitHub Repo

1. Go to [ref.tools/resources?tab=github](https://ref.tools/resources?tab=github)
2. Click **Add GitHub Repos**
3. Authenticate with GitHub if prompted (uses personal access token)
4. Select repos to index
5. Wait for initial sync (large repos may take a few minutes)

**What gets indexed:**
- Repos <2k files: everything (code + docs)
- Repos >2k files: docs only

**Sync:** Every 5 minutes, incremental. If you rewrite git history, remove and re-add the repo.

### Uploading PDF/Markdown

1. Go to [ref.tools/resources?tab=pdf](https://ref.tools/resources?tab=pdf)
2. Click **Add Files**
3. Upload `.pdf` or `.md` files (max 100MB each)
4. Files are chunked and indexed automatically

**Use case:** Man pages, internal docs, version-specific library docs not in public index.

### Viewing Usage

1. Go to [ref.tools/activity](https://ref.tools/activity)
2. See daily credit spend by endpoint (search, read, chat, web)
3. Filter by date range
4. Export to CSV for audits

### Managing API Keys

1. Go to [ref.tools/keys](https://ref.tools/keys)
2. Create new keys, revoke old ones
3. Each key shows last used timestamp

### Team Management

1. Go to [ref.tools/team](https://ref.tools/team)
2. Select team in workspace picker (top-left)
3. Invite members, assign roles

**Roles:**

| Role | Can Search | Can Add Content | Can Invite | Can Manage Billing |
|------|------------|-----------------|------------|-------------------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| Writer | ✅ | ✅ | ❌ | ❌ |
| Reader | ✅ | ❌ | ❌ | ❌ |

**Tip:** For public-docs-only teams, have one Admin and invite everyone else as Readers.

### Requesting Docs Be Added to Public Index

When Ref doesn't have docs for a library/tool you need:

**Form details:**
- Form ID: `nrvBY2`
- URL: https://tally.so/r/nrvBY2

**Fields:**

| Field | Content |
|-------|---------|
| What docs would you like indexed? | 1-5 sentences with context (see template below) |
| Email | User's email |

**Request template:**

```
<Tool/library name> - <what it is, 1 sentence>

<Why it's useful to index / what's currently missing, 1-2 sentences>

URL: <documentation URL>

Note: <any special notes about docs structure, size, format>
```

**Common doc URLs:**
- tmux: `https://man.openbsd.org/tmux`
- git: `https://git-scm.com/docs`

**Submission:** Use the [Tally skill](../tally/SKILL.md) with:
```
formId: nrvBY2
fields:
  - name: "What docs would you like indexed?"
    value: <drafted request>
  - name: "Email"
    value: <user email>
```

**After submitting:** Ref team reviews and adds to public index. Check back in a few days.

---

## Usage Reference

| Tool | Credits | Purpose |
|------|---------|---------|
| `ref_search_documentation` | 1 | Search docs (full sentence query) |
| `ref_read_url` | 1 | Read content from search result URL |

**Search patterns:**
- Include library name: `"Effect Schema decode unknown data validation"`
- Private docs: include `ref_src=private` in query

---

## Decision Guide: Local Docs vs Ref Upload

When you have docs that aren't in Ref's public index (e.g., man pages):

| Factor | Local `man-pages/` dir | Upload to Ref |
|--------|------------------------|---------------|
| **Setup** | Script + grep | One-time upload |
| **Search** | Grep (exact match) | Semantic search |
| **Offline** | ✅ Works | ❌ Needs internet |
| **Human browsing** | ✅ Files in repo | ❌ Web UI only |
| **CC access** | Grep local files | `ref_src=private` query |
| **Maintenance** | Re-run script on updates | Re-upload on updates |

**Recommendation:**
- **Keep local** if: humans browse the docs, offline access matters, or docs change rarely
- **Upload to Ref** if: semantic search valuable, docs are large, or you want unified search

**Both is fine:** Local for humans, Ref for CC. They serve different access patterns.

---

## Pricing & Credits

| Plan | Cost | Credits |
|------|------|---------|
| Free | $0 | 200 (never expire) |
| Basic | $9/mo | 1,000/mo |
| Additional | $9 | per 1,000 credits |

Each `search` or `read` = 1 credit. Most individual devs never hit 1,000/month.

View usage: [ref.tools/activity](https://ref.tools/activity)

### Session Caching

**Within a session (same CC conversation):**
- "Never return same link twice" — cached, no duplicate results
- "Pre-fetching" — faster reads for related content

**Across sessions (new CC conversation):**
- Unclear if cached results avoid credit charges
- New MCP session likely = fresh credit charges

**Typical burn rate estimate:**
- Light day: 10-20 credits
- Heavy day: 50-100 credits
- 1,000 credits/month = ~30-50 heavy coding days

Monitor actual usage at [ref.tools/activity](https://ref.tools/activity)

---

## Ref vs Context7

*Updated Jan 2026 — Context7 pricing has changed significantly.*

| Aspect | Ref | Context7 |
|--------|-----|----------|
| **Free tier** | 200 credits (never expire) | 1,000 calls/month |
| **Paid tier** | $9/mo = 1,000 credits | $10/seat/mo = 5,000 calls |
| **Overage** | $9 per 1,000 | $10 per 1,000 |
| **Search model** | Iterative (search → read) | Batch (resolve-library-id → get-docs) |
| **Content** | Any (prose, warnings, code) | Code snippets only |
| **Private repos** | Included | $10/seat + $15/1M tokens parsing |
| **PDF upload** | Yes | No |
| **Tokens/query** | Adaptive 500-5k | Fixed ~3k |

**When Ref wins:**
- Private repos without parsing fees
- PDF/file uploads
- Iterative search (more agentic, flexible)
- Source-of-truth access (not just snippets)

**When Context7 wins:**
- Higher volume needs (5,000 calls vs 1,000 for similar price)
- Public docs only workflows
- "use context7" prompt UX in Cursor

**Bottom line:** For typical individual usage, the model differences matter more than volume. Ref's iterative approach and private repo simplicity are worth the lower volume cap.

---

## Key URLs

| URL | Purpose |
|-----|---------|
| https://ref.tools/signup | Create account |
| https://ref.tools/install | Pre-populated install command |
| https://ref.tools/keys | Manage API keys |
| https://ref.tools/resources | Your Resources (private docs) |
| https://ref.tools/activity | View usage/credits |
| https://docs.ref.tools | Documentation |
| https://docs.ref.tools/changelog | Monthly updates |
| https://docs.ref.tools/comparison/context7 | Ref vs Context7 |
| https://docs.ref.tools/usage/credits | Credit costs |
| https://docs.ref.tools/llms.txt | Full docs index |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "not correctly configured" | API key invalid - get fresh key at ref.tools/keys |
| Tools not available | Restart Claude Code |
| Search returns nothing | Try different query terms, or content may not be indexed |
| Need specific library version | Check repo tags or upload version-specific docs |
| Docs not fresh enough | Private repos sync every 5 min; public index managed by Ref |

## Support

help@ref.tools
