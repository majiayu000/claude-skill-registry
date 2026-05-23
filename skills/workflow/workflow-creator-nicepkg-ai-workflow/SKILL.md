---
name: workflow-creator
description: Create complete Claude Code workflow directories with curated skills. Use when user wants to (1) create a new workflow for specific use case (media creator, developer, marketer, etc.), (2) set up a Claude Code project with pre-configured skills, (3) download and organize skills from GitHub repositories, or (4) generate README.md and AGENTS.md documentation for workflows. Triggers on phrases like "create workflow", "new workflow", "set up workflow", "build a xxx-workflow".
---

# Workflow Creator

Create complete workflow directories with curated skills downloaded from GitHub.

## Workflow Creation Process

### Step 1: Create directory structure

Run `scripts/create_workflow.py` to initialize:

```bash
python scripts/create_workflow.py <workflow-name> --path <output-dir>
```

Creates (with multi-AI tool support):
```
workflows/<workflow-name>-workflow/
├── README.md          # User documentation (English)
├── README_cn.md       # User documentation (Chinese)
├── AGENTS.md          # AI context (auto-loaded)
├── .claude/
│   ├── settings.json
│   └── skills/        # Skills go here (primary storage)
├── .codex/
│   └── skills -> ../.claude/skills
├── .cursor/
│   └── skills -> ../.claude/skills
├── .opencode/
│   └── skill -> ../.claude/skills
├── .agents/
│   └── skills -> ../.claude/skills
├── .kilocode/
│   └── skills -> ../.claude/skills
├── .roo/
│   └── skills -> ../.claude/skills
├── .goose/
│   └── skills -> ../.claude/skills
├── .gemini/
│   └── skills -> ../.claude/skills
├── .agent/
│   └── skills -> ../.claude/skills
├── .github/
│   └── skills -> ../.claude/skills
├── skills -> .claude/skills
├── .factory/
│   └── skills -> ../.claude/skills
└── .windsurf/
    └── skills -> ../.claude/skills
```

Symlinks enable all AI tools to use the same skills from .claude/skills/.

### Step 2: Select and download skills

1. Use the **Skill Sources** section below to find relevant skills
2. Download each skill using `scripts/download_skill.py`:

```bash
python scripts/download_skill.py <repo-url> <skill-path> --output workflows/<workflow-name>/.claude/skills/
```

**Examples:**

```bash
# Official Anthropic skills
python scripts/download_skill.py https://github.com/anthropics/skills skills/docx --output ./workflows/media-workflow/.claude/skills/

# Community skills (root level)
python scripts/download_skill.py https://github.com/gked2121/claude-skills social-repurposer --output ./workflows/media-workflow/.claude/skills/
```

### Step 3: Generate README.md (English)

**CRITICAL: Follow the exact format from `workflows/marketing-pro-workflow/README.md`**

Required structure:
```markdown
<div align="center">

# 📋 Workflow Name

### **Your AI-Powered [Domain] Team**

[← Back to AI Workflow](../../README.md)

[简体中文](./README_cn.md) | English

</div>

---

## 🎯 Who Is This For?
- **Role 1** - Use case
- **Role 2** - Use case

---

## ⚡ Quick Install
[Install commands]

---

## 📦 Skills Included (N)

### 0️⃣ Stage Name
| Skill | What It Does |
|:------|:-------------|
| `skill-name` | Description |

### 1️⃣ Next Stage
...

---

## 🔄 Complete Pipeline (N Stages)
[ASCII tree diagram]

---

## 💡 Example Workflows
[Multiple scenario examples with numbered prompts]

---

## 🔗 Skill Combinations
[Table with Goal → Skill Chain]

---

## 📄 License
MIT © [nicepkg](https://github.com/nicepkg)
```

Use `assets/templates/README.template.md` as reference.

### Step 4: Generate README_cn.md (Chinese)

Create Chinese version with:
- Same structure as English README
- Professional Chinese terminology
- Link back to `../../README_cn.md`

### Step 5: Generate AGENTS.md

Write AI instructions covering:
- Workflow overview with pipeline diagram
- Available skills grouped by stage
- Skill usage guidelines (when to use each)
- Recommended sequences for common tasks
- Output standards
- Quality gates between phases

**Important:** AGENTS.md is auto-loaded by Claude Code. Keep it concise (<500 lines) and focused on actionable instructions.

Use `assets/templates/AGENTS.template.md` as reference.

### Step 6: Update project README

After creating a workflow in the ai-workflow project, update:

1. **README.md** (English):
   - Add new workflow to the workflow table
   - Add skills list under `<details>` section
   - Update skill count (e.g., "150+ skills")

2. **README_cn.md** (Chinese):
   - Same updates in Chinese
   - Link to `README_cn.md` in workflow folder

---

## Skill Sources

### A. Skill Aggregators & Directories (for discovering skills)

| Name | Type | Scale | Best For |
|:-----|:-----|------:|:---------|
| **[Skillhub Awesome Skills](https://github.com/keyuyuan/skillhub-awesome-skills)** | GitHub curated list | 1000+ skills | Top skills by category, well-organized |
| **[Skillhub.club](https://skillhub.club)** | Online directory | 1000+ | Web UI for browsing by category |
| **[SkillsMP](https://skillsmp.com)** | Marketplace | 63,000+ | Mass search with filters (category/popularity/author) |
| **[agent-skills.md](https://agent-skills.md)** | Online directory | Large | Install commands included (`pnpm dlx add-skill ...`) |
| **[Claude Skills Hub](https://claudeskills.info)** | Online directory | Medium | Product-style browsing, good for inspiration |
| **[MCP Market Skills](https://mcpmarket.com/tools/skills)** | Online store | Medium | Product pages with About/FAQ, content creator friendly |
| **[Skills Directory](https://skillsdirectory.com)** | Online directory | Medium | Copy SKILL.md directly, good structure |
| **[Smithery Skills](https://smithery.ai/skills)** | Skill directory | Medium | Includes expected_output.json, tool-oriented |
| **[Awesome Claude Skills (ComposioHQ)](https://github.com/ComposioHQ/awesome-claude-skills)** | GitHub awesome list | High stars | Ecosystem resources, comprehensive |
| **[Awesome Claude Skills (travisvn)](https://github.com/travisvn/awesome-claude-skills)** | GitHub awesome list | 5k+ stars | Second perspective, prevents single-source bias |
| **[Awesome Agent Skills](https://github.com/heilcheng/awesome-agent-skills)** | GitHub multi-agent list | 1k+ stars | Covers Claude/Codex/Copilot/VSCode |

### B. Production-Ready Skill Repositories (for bulk import)

| Repository | Focus | Best For |
|:-----------|:------|:---------|
| **[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** | Multi-role skill packs | Content Creator suite (brand voice, SEO, platform frameworks) |
| **[gked2121/claude-skills](https://github.com/gked2121/claude-skills)** | Production workflows | Clear workflow examples (Podcast→Content→Social→SEO) |
| **[sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)** | Skill registry | Organized by role (`skills/content-creator`) |
| **[Microck/ordinary-claude-skills](https://github.com/Microck/ordinary-claude-skills)** | 600+ skills collection | skill-navigator, SEO clustering, email optimization |
| **[synapz-org/marketing-ops-hub](https://github.com/synapz-org/marketing-ops-hub)** | Marketing orchestration | Multi-skill coordination patterns |
| **[m2ai-portfolio/claude-skills](https://github.com/m2ai-portfolio/claude-skills)** | Creator/Growth suite | IG caption, YouTube script, tweet thread, blog outline |
| **[pluginagentmarketplace/custom-plugin-product-manager](https://github.com/pluginagentmarketplace/custom-plugin-product-manager)** | Product Manager suite | user-research, roadmap, requirements, analytics |
| **[lyndonkl/claude](https://github.com/lyndonkl/claude)** | Decision frameworks | prioritization, forecasting, stakeholder mapping |
| **[jamesrochabrun/skills](https://github.com/jamesrochabrun/skills)** | Mixed professional | prd-generator, technical-launch-planner |
| **[britt/claude-code-skills](https://github.com/britt/claude-code-skills)** | Writing & specs | writing-product-specs, writing-user-stories |
| **[troykelly/codex-skills](https://github.com/troykelly/codex-skills)** | Workflow management | work-intake, milestone-management |
| **[escarti/agentDevPrompts](https://github.com/escarti/agentDevPrompts)** | Feature lifecycle | feature-planning, feature-implementing |
| **[aj-geddes/useful-ai-prompts](https://github.com/aj-geddes/useful-ai-prompts)** | Sprint & agile | agile-sprint-planning, requirements-gathering |
| **[daffy0208/ai-dev-standards](https://github.com/daffy0208/ai-dev-standards)** | Multi-role standards | customer-feedback-analyzer, go-to-market-planner |

### C. Search Strategy

When the above sources lack needed skills:

1. **GitHub Search**: `"claude" "skills" "SKILL.md" <topic>`
2. **agent-skills.md Search**: Browse by tags at https://agent-skills.md/tags
3. **SkillsMP Search**: Filter by category at https://skillsmp.com
4. **Validate**: Check SKILL.md has valid YAML frontmatter with `name` and `description`

### D. Download Commands

```bash
# From GitHub repository
python scripts/download_skill.py https://github.com/<owner>/<repo> <skill-path> --output workflows/<workflow-name>/.claude/skills/

# Example: Download from alirezarezvani
python scripts/download_skill.py https://github.com/alirezarezvani/claude-skills skills/content-creator --output ./workflows/content-creator-workflow/.claude/skills/

# Example: Download from pluginagentmarketplace
python scripts/download_skill.py https://github.com/pluginagentmarketplace/custom-plugin-product-manager skills/user-research --output ./workflows/product-manager-workflow/.claude/skills/
```

---

## Output Checklist

After workflow creation, verify:
- [ ] `.claude/skills/` contains downloaded skill folders
- [ ] Each skill folder has `SKILL.md`
- [ ] All symlinks work (`.codex/skills`, `.cursor/skills`, `.opencode/skill`, `.agents/skills`, `.kilocode/skills`, `.roo/skills`, `.goose/skills`, `.gemini/skills`, `.agent/skills`, `.github/skills`, `skills`, `.factory/skills`, `.windsurf/skills`)
- [ ] `README.md` follows standard format with all sections
- [ ] `README_cn.md` created with Chinese translation
- [ ] `AGENTS.md` provides clear AI instructions (<500 lines)
- [ ] `settings.json` exists in `.claude/`
- [ ] Project README.md updated with new workflow
- [ ] Project README_cn.md updated with new workflow
- [ ] Skill counts updated in both README files
