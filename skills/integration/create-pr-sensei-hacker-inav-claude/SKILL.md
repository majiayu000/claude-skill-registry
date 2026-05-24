---
description: Create pull requests for PrivacyLRS and INAV projects
triggers:
  - create pr
  - make pr
  - create pull request
  - submit pr
  - new pull request
---

# Pull Request Creation

## Which repository are you working on?

**IMPORTANT:** The PR workflow differs significantly between repositories.

**Read the appropriate guide:**

### For INAV or inav-configurator
📖 **Read:** `.claude/skills/create-pr/INAV-PR.md`

**Use this for:**
- Flight controller firmware (`inav/`)
- Configuration GUI (`inav-configurator/`)

---

### For PrivacyLRS
📖 **Read:** `.claude/skills/create-pr/PRIVACYLRS-PR.md`

**Use this for:**
- Privacy-focused Long Range System (`PrivacyLRS/`)

---

## Quick Decision Helper

**Check your current directory:**
```bash
pwd
```

- Contains `/inav/` or `/inav-configurator/` → Read `INAV-PR.md`
- Contains `/PrivacyLRS/` → Read `PRIVACYLRS-PR.md`

---

## 🚨 Universal Critical Rules (All Repos)

1. **Testing is MANDATORY** - untested code can brick hardware
2. **NEVER work directly on production branches** (secure_01, master, main)
3. **NEVER target `master`** for PRs
4. **Read this first:** `claude/developer/guides/CRITICAL-BEFORE-PR.md`

---

**After identifying your repository, read the appropriate detailed guide above.**
