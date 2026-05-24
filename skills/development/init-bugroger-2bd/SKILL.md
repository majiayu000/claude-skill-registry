---
name: init
description: Bootstrap or configure 2bd. Use 'fresh' to set up a new vault, 'reconnect' to link an existing vault, or 'profile' to update your user profile.
argument-hint: "[fresh --vault=/path | reconnect --vault=/path | profile]"
---

# Init Action

This action manages the connection between the 2bd engine and your vault.

## Mode Detection

Parse `$ARGUMENTS` to determine mode:

1. If contains `fresh` → **Fresh Install** (set up new vault)
2. If contains `reconnect` → **Reconnect** (link existing vault)
3. If contains `profile` → **Profile Only** (update user profile)
4. If no mode specified → Auto-detect based on current state

**Auto-detection logic:**
- If `.claude/config.md` exists and vault path is valid → offer to update profile
- If `.claude/config.md` exists but vault missing → suggest reconnect
- If no config exists → suggest fresh install

---

## Mode: Fresh Install

Set up a new vault from scratch.

### 1. Get Vault Path

Check for `--vault=` argument, otherwise ask:

"Where should I create your vault? This should be a folder that syncs (e.g., OneDrive, iCloud, Dropbox).

Example: `~/OneDrive/2bd-vault`"

Store as `$VAULT`.

### 2. Validate Path

- Ensure parent directory exists
- Warn if path is inside a git repo: "This path appears to be inside a git repository. Vaults should NOT be in git repos. Continue anyway?"
- Warn if path already has files: "This folder already has files. Should I merge the scaffold structure, or choose a different path?"

### 3. Create Vault Structure

```bash
cp -r scaffold/* "$VAULT/"
```

This copies:
- Hub files (✱ Home.md, ✱ Projects.md, ✱ People.md, ✱ Insights.md)
- Templates (Captive + Periodic + PARA)
- Directory structure with .gitkeep placeholders

### 4. Write Engine Config

Write `.claude/config.md`:

```markdown
# 2bd Engine Configuration

## Vault

vault_path: $VAULT
```

### 5. Run Profile Interview

[Execute the Profile Interview workflow below]

### 6. Confirmation

"Your vault is ready at: `$VAULT`

Next steps:
- Open the vault in Obsidian
- Run `/daily-planning` to start your first planned day
- The engine always runs from this directory (~/Code/2bd-engine)"

---

## Mode: Reconnect

Link an existing vault (e.g., after moving to a new computer).

### 1. Get Vault Path

Check for `--vault=` argument, otherwise ask:

"Where is your existing vault located?

Example: `~/OneDrive/2bd-vault`"

Store as `$VAULT`.

### 2. Validate Vault Exists

Check that these exist:
- `$VAULT/00_Brain/`
- `$VAULT/00_Brain/Systemic/Templates/`

If missing: "This doesn't look like a 2bd vault. Did you mean to run `fresh` instead?"

### 3. Write Engine Config

Write `.claude/config.md`:

```markdown
# 2bd Engine Configuration

## Vault

vault_path: $VAULT
```

### 4. Check Directives

Check if `$VAULT/00_Brain/Systemic/Directives/user-profile.md` exists:
- If yes: "Found your existing profile. You're all set!"
- If no: Ask "Would you like to set up your profile now?" → run Profile Interview if yes

### 5. Confirmation

"Reconnected to vault at: `$VAULT`

You can now run `/daily-planning` and other skills."

---

## Mode: Profile Only

Update user profile without changing vault connection.

### 1. Get Config

**Use sub-skill: `_sub/fetch/get-config`**

If no config exists, error: "No vault configured. Run `/init fresh` or `/init reconnect` first."

### 2. Check Existing Profiles

Check `$VAULT/00_Brain/Systemic/Directives/`:
- If profiles exist: "I found existing profiles. Do you want to update them? This will overwrite current settings."
- Proceed only if user confirms

### 3. Run Profile Interview

[Execute the Profile Interview workflow below]

---

## Profile Interview

Conduct a conversational interview to gather user information.

### Part 1: User Profile

Ask questions one section at a time, waiting for responses.

**Section 1: Basic Identity**

"Let's start with some basics about you."

- "What's your name?" (full name)
- "What should I call you?" (preferred name/nickname)
- "What's your current role or title?"
- "In a sentence or two, what do you do?"

**Section 2: Work Context**

"Now let's understand your work context."

- "What are your primary focus areas or responsibilities?"
- "Tell me about your team or org context—who do you work with?"
- "How would you describe your communication style? (e.g., direct, collaborative, analytical)"

**Section 3: Goals & Growth**

"Let's talk about where you're headed."

- "What are you working toward this year? (1-3 key goals)"
- "Describe the leader you're becoming—your leadership identity in 1-2 sentences"
- "Where does discomfort live for you? What's your growth edge—the stretch you're working on?"

**Section 4: Coaching Context**

"Finally, let's capture some coaching context."

- "What patterns or tendencies should I watch for—behaviors that don't serve you well?"
- "What questions help ground you or bring clarity when you're stuck?"
- "What does success look like for you this year?"

Generate `user-profile.md` using the template at `templates/user-profile.md`.
Write to: `$VAULT/00_Brain/Systemic/Directives/user-profile.md`

### Part 2: AI Personality

"Now let's customize how I should interact with you."

**Section 1: Communication Style**

- "How formal should our conversations be?" (Very formal / Professional but relaxed / Casual)
- "How direct do you want me to be?" (Very direct—don't soften / Balanced—direct but tactful / Gentle—ease into feedback)
- "How do you feel about humor in our interactions?" (Keep it serious / Occasional is fine / Bring it on)

**Section 2: Coaching Approach**

- "What balance of support vs challenge do you want?" (Mostly supportive / Balanced / Push me hard)
- "How much proactive input should I offer?" (Wait for me to ask / Suggest when relevant / Actively coach me)
- "How should I deliver feedback?" (Direct critique / Sandwich method / Through questions)

**Section 3: Interaction Patterns**

- "Should I ask questions or make suggestions?" (Mostly questions—help me think / Balanced / Mostly suggestions—save me time)
- "How much autonomy should I have when executing tasks?" (Check with me on everything / Check on important decisions / Just get it done)
- "How should I handle disagreement?" (Tell me directly / Offer alternatives / Ask questions to explore)

Generate `ai-personality.md` using the template at `templates/ai-personality.md`.
Write to: `$VAULT/00_Brain/Systemic/Directives/ai-personality.md`

### Part 3: Summary

After creating both files:

1. Summarize what was created:
   - User profile highlights (name, role, goals, growth edge)
   - AI personality settings (communication style, coaching approach)

2. Suggest next steps:
   - "Run `/daily-planning` to start your first planned day"
   - "These profiles will be loaded for all conversations to personalize your experience"
