# Professional Business Writing Skill

AI writing humanizer for professional communications. Removes AI patterns while maintaining authority. Works across Claude Code, Claude.ai, Claude Desktop, Cowork, Cursor, Windsurf, and more.

## What It Does

Transforms AI-sounding writing into clear, authoritative professional communication:

- **Removes 18 AI patterns**: "testament to," "pivotal moment," em dash overuse, promotional language, vague attributions, filler phrases, buzzwords, and more
- **Maintains authority**: Keeps professional voice strong and confident
- **Adds clarity**: Replaces vague claims with specific facts
- **Stays professional**: Direct without being stuffy OR casual

## Quick Example

**Before:**
> Our results stand as a testament to the team's dedication and serve as a pivotal moment in the project's evolution, showcasing significant growth across multiple metrics.

**After:**
> We completed Phase 2 ahead of schedule—delivered March 15 vs. March 22 target. Automation cut QA time from 40 to 12 hours per cycle.

---

## Installation

### Claude Code

**Method 1: Plugin Command (Easiest)**
```bash
/plugin install professional-business-writing@b33kman
```

**Method 2: Manual Installation**
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/b33kman/professional-business-writing-skill.git ~/.claude/skills/professional-business-writing
```

**Method 3: Copy Single File**
```bash
mkdir -p ~/.claude/skills/professional-business-writing
curl -o ~/.claude/skills/professional-business-writing/SKILL.md \
  https://raw.githubusercontent.com/b33kman/professional-business-writing-skill/main/SKILL.md
```

**Usage:**
```
/professional-business-writing

[paste your text]
```

Or simply ask:
```
Use the professional-business-writing skill to humanize this report
```

---

### Claude.ai Web (claude.ai)

1. Download this repository as ZIP:
   - Click green "Code" button → "Download ZIP"
2. Go to https://claude.ai
3. Click your profile → **Customize** → **Skills**
4. Click **"+"** button → **"Upload a skill"**
5. Select the ZIP file
6. Toggle the skill **ON**

**Usage:**
- The skill activates automatically when you write professional content
- Or request explicitly: "Use my professional writing skill to edit this"

---

### Claude Desktop App

Same as Claude.ai Web:

1. Download ZIP from GitHub
2. Open Claude Desktop
3. Settings → **Customize** → **Skills**
4. **"+"** → **"Upload a skill"** → Select ZIP
5. Toggle **ON**

---

### Cowork

Same as Claude.ai and Desktop—Cowork uses the same skill system:

1. Download ZIP from GitHub
2. Open Cowork
3. **Customize** → **Skills**
4. Upload ZIP
5. Toggle ON

The skill will activate when working on documents, emails, reports, or any professional writing.

---

### Cursor IDE

```bash
mkdir -p ~/.cursor/skills
git clone https://github.com/b33kman/professional-business-writing-skill.git ~/.cursor/skills/professional-business-writing
```

Or copy just SKILL.md:
```bash
mkdir -p ~/.cursor/skills/professional-business-writing
curl -o ~/.cursor/skills/professional-business-writing/SKILL.md \
  https://raw.githubusercontent.com/b33kman/professional-business-writing-skill/main/SKILL.md
```

---

### Windsurf IDE

```bash
mkdir -p ~/.windsurf/skills
git clone https://github.com/b33kman/professional-business-writing-skill.git ~/.windsurf/skills/professional-business-writing
```

Or copy SKILL.md:
```bash
mkdir -p ~/.windsurf/skills/professional-business-writing
curl -o ~/.windsurf/skills/professional-business-writing/SKILL.md \
  https://raw.githubusercontent.com/b33kman/professional-business-writing-skill/main/SKILL.md
```

---

### Cline

```bash
mkdir -p ~/.cline/skills
git clone https://github.com/b33kman/professional-business-writing-skill.git ~/.cline/skills/professional-business-writing
```

---

### OpenAI Custom GPTs

OpenAI doesn't support skill files directly. Instead, copy the skill content as system instructions:

1. Go to https://chat.openai.com/gpts/editor
2. Click **"Create a GPT"** or edit existing
3. Go to **"Configure"** tab
4. In **"Instructions"** field, paste the following:

```
You are a professional writing editor that removes AI-generated patterns while maintaining authority.

[Copy the entire "Professional Voice" and "AI Patterns to Remove" sections from SKILL.md]
```

Or view the full instructions at: https://raw.githubusercontent.com/b33kman/professional-business-writing-skill/main/SKILL.md

---

### Google Gemini

**Method 1: Personal Instructions (applies to all chats)**
1. Go to https://gemini.google.com
2. Click profile icon → **"Personal Intelligence Instructions"**
3. Paste key sections from SKILL.md
4. Click **"Submit"**

**Method 2: Create a Custom Gem (reusable persona)**
1. Go to https://gemini.google.com
2. Click **"Explore Gems"** → **"New Gem"**
3. Name it: "Professional Writing Editor"
4. In instructions, paste the professional voice guidelines and pattern list from SKILL.md
5. Click **"Save"**

Now you can invoke this Gem whenever you need professional writing help.

---

## What Gets Fixed

| Pattern | Before | After |
|---------|--------|-------|
| **Significance inflation** | "marking a pivotal moment..." | "Revenue grew 34% YoY" |
| **Promotional language** | "groundbreaking platform showcases..." | "Platform launched with 12 features" |
| **Vague attributions** | "Industry observers note..." | "Gartner moved us to 'Challenger'" |
| **AI vocabulary** | "Additionally... Furthermore..." | "Also... But... So..." |
| **Copula avoidance** | "serves as... functions as..." | "is... are... has..." |
| **Formulaic challenges** | "Despite challenges... continues to thrive" | "Q3 churn hit 6.2%. We're addressing it..." |
| **Generic conclusions** | "The future looks bright..." | "Launching in EMEA in Q2" |
| **Filler phrases** | "In order to... Due to the fact that..." | "To... Because..." |

---

## Use Cases

### Perfect For
- Business reports and analysis
- Project status updates
- Proposals and RFP responses
- White papers and technical documentation
- Professional articles and blog posts
- Email to clients, partners, stakeholders
- Product documentation
- Company announcements

### Works For
- Executives, managers, team leads
- Consultants and freelancers
- Writers and content creators
- Product managers and analysts
- Anyone writing professional communications

---

## How It Works

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, adapted for professional communications. The skill:

1. Scans text for 18+ AI patterns
2. Rewrites with direct, professional language
3. Replaces vague claims with specific facts
4. Removes all chatbot artifacts and filler
5. Maintains professional authority throughout

---

## Platform Compatibility

| Platform | Installation Method | Status |
|----------|---------------------|--------|
| **Claude Code** | `/plugin install` or manual | ✅ Native |
| **Claude.ai** | Upload ZIP via Skills | ✅ Native |
| **Claude Desktop** | Upload ZIP via Skills | ✅ Native |
| **Cowork** | Upload ZIP via Skills | ✅ Native |
| **Cursor** | Copy to `~/.cursor/skills/` | ✅ SKILL.md format |
| **Windsurf** | Copy to `~/.windsurf/skills/` | ✅ SKILL.md format |
| **Cline** | Copy to `~/.cline/skills/` | ✅ SKILL.md format |
| **OpenAI GPTs** | Paste as system instructions | ✅ Manual |
| **Gemini** | Personal Instructions or Gem | ✅ Manual |
| **GitHub Copilot** | N/A | ❌ No skill support |

---

## Version History

- **1.0.0** (2025-03-24) - Initial release

---

## Credits

Adapted from [blader/humanizer](https://github.com/blader/humanizer) by @blader.  
Modified for professional business writing by Mark Beekman.

Original humanizer based on Wikipedia's "Signs of AI writing" maintained by WikiProject AI Cleanup.

---

## License

MIT

---

## Contributing

Issues and pull requests welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Keywords

AI writing, AI detection, humanizer, professional writing, business communications, AI patterns, writing assistant, Claude skills, Claude Code, content editing, writing tool, AI humanizer, professional voice, business writing, technical writing
