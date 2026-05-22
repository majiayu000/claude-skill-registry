---
name: agent-skills-expert
description: Expert for creating and managing Claude Code Agent Skills. Create skills with git submodule + sparse-checkout for source references, write SKILL.md with proper frontmatter, and follow best practices. Use when creating new skills, adding source references to skills, or managing skill configurations.
---

# Agent Skills Expert

Expert for creating and managing Claude Code Agent Skills. Helps create skills that follow official specifications, including using Git Submodule + Sparse Checkout for source code references.

## 📚 Core Concepts

### What is an Agent Skill?

Agent Skill is an extensible capability module for Claude Code, containing:
- `SKILL.md` - Skill definition file (required)
- Supporting files - Documentation, scripts, templates, etc. (optional)
- `source/` - Source code reference directory (optional, using git submodule)

### Skill Storage Locations

- **Personal Skills**: `~/.claude/skills/skill-name/`
- **Project Skills**: `.claude/skills/skill-name/`

## 🔧 Skill Creation Workflow

### 1. Basic Skill Structure

```
skill-name/
├── SKILL.md              # Required: Skill definition
├── examples.md           # Optional: Example code
├── quick-reference.md    # Optional: Quick reference
├── SOURCE_STRUCTURE.md   # Optional: Source structure documentation
├── scripts/              # Optional: Helper scripts
└── source/               # Optional: Source code references
    └── repo-name/        # Git Submodule
```

### 2. SKILL.md Specification

```yaml
---
name: skill-name                    # Required: lowercase letters, numbers, hyphens, max 64 chars
description: Brief description...   # Required: Skill description, max 1024 chars
allowed-tools: Read, Grep, Glob     # Optional: Restrict available tools
---

# Skill Name

## Instructions
Clear usage instructions...

## Examples
Concrete usage examples...
```

**Description Best Practices**:
- Explain what the skill does
- Explain when to use the skill
- Include keywords for Claude to discover

### 3. Adding Source References (Git Submodule + Sparse Checkout)

#### Step 1: Add Submodule

```bash
cd ~/.claude/skills
git submodule add https://github.com/org/repo.git skill-name/source/repo-name
```

#### Step 2: Configure Sparse Checkout

```bash
cd skill-name/source/repo-name

# Initialize sparse-checkout
git sparse-checkout init --no-cone

# Set content to keep
git sparse-checkout set \
    /README.md \
    /docs/ \
    /src/ \
    /examples/
```

#### Step 3: Create SOURCE_STRUCTURE.md

Document the source structure, including:
- Sparse checkout configuration
- Directory structure explanation
- Key file locations
- Maintenance guide

## 📋 Sparse Checkout Configuration Guide

### Principles for Selecting Content to Keep

1. **Core source code** - Main API implementation
2. **Documentation** - README, docs directory
3. **Examples** - examples directory
4. **Configuration files** - pyproject.toml, package.json, etc.
5. **Tests** - Test cases showing usage patterns

### Content to Exclude

- Large resource files (images, videos)
- Build artifacts
- CI/CD configuration (usually not needed)
- Historical release notes

### Common Sparse Checkout Patterns

**Python Projects:**
```bash
git sparse-checkout set \
    /README.md \
    /LICENSE \
    /src/ \
    /docs/ \
    /examples/ \
    /tests/ \
    /pyproject.toml
```

**JavaScript/TypeScript Projects:**
```bash
git sparse-checkout set \
    /README.md \
    /LICENSE \
    /src/ \
    /docs/ \
    /examples/ \
    /package.json \
    /tsconfig.json
```

**Rust Projects:**
```bash
git sparse-checkout set \
    /README.md \
    /LICENSE \
    /src/ \
    /docs/ \
    /examples/ \
    /Cargo.toml
```

## 🛠️ Maintenance Operations

### Update Submodule

```bash
cd skill-name/source/repo-name
git pull origin main
```

### Modify Sparse Checkout Configuration

```bash
cd skill-name/source/repo-name

# Add new directory
git sparse-checkout add /new-dir/

# Reconfigure
git sparse-checkout set /dir1/ /dir2/ /file.md
```

### View Configuration

```bash
cd skill-name/source/repo-name
git sparse-checkout list
du -sh .  # Check size
```

### Troubleshooting Recovery

```bash
# Completely reset submodule
cd ~/.claude/skills
git submodule deinit -f skill-name/source/repo-name
rm -rf .git/modules/skill-name/source/repo-name
git submodule update --init skill-name/source/repo-name

# Reconfigure sparse-checkout
cd skill-name/source/repo-name
git sparse-checkout init --no-cone
git sparse-checkout set /directories-to-keep/
```

## 📝 Template Files

### SKILL.md Template

See [templates/SKILL_TEMPLATE.md](templates/SKILL_TEMPLATE.md)

### SOURCE_STRUCTURE.md Template

See [templates/SOURCE_STRUCTURE_TEMPLATE.md](templates/SOURCE_STRUCTURE_TEMPLATE.md)

## ✅ Checklist

### Creating New Skill

- [ ] Create skill directory `mkdir -p ~/.claude/skills/skill-name`
- [ ] Create SKILL.md (with correct frontmatter)
- [ ] Write clear description (include trigger keywords)
- [ ] Add usage instructions and examples
- [ ] Test that skill is correctly discovered

### Adding Source References

- [ ] Add git submodule
- [ ] Configure sparse-checkout
- [ ] Verify reasonable size (typically <100MB)
- [ ] Create SOURCE_STRUCTURE.md
- [ ] Update source access instructions in SKILL.md
- [ ] Commit all changes

### Maintenance

- [ ] Regularly update submodule
- [ ] Check if sparse-checkout configuration is still appropriate
- [ ] Update documentation to reflect latest structure

## 🔗 Related Resources

- [GIT_SPARSE_CHECKOUT_TUTORIAL.md](../GIT_SPARSE_CHECKOUT_TUTORIAL.md) - Detailed Sparse Checkout tutorial
- [CLAUDE_CODE_SKILL_TUTORIAL.md](../CLAUDE_CODE_SKILL_TUTORIAL.md) - Official skill tutorial
- [Agent Skills Official Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

## 📊 Existing Skills Reference

| Skill | Source Reference | Sparse Checkout |
|-------|------------------|-----------------|
| langgraph-python-expert | ✅ | ✅ (~66MB) |
| lib-slint-expert | ✅ | ❌ |
| vscode-extension-builder | ✅ | ✅ |
| uv-expert | ✅ | ❌ |
| rust-cli-tui-developer | ✅ | ❌ |

---

*Last updated: 2024-12-23*
