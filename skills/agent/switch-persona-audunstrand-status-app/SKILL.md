---
name: Switch Persona
description: Quick persona switching. Triggers: 'switch persona', 'switch to X', 'become X'. Lists personas, reads selected file, switches immediately.
---

# GitHub Copilot Skill: switch-persona

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Switch Persona - Quick Switching Protocol

## Activation

User says:
- "switch persona"
- "switch to [name]"
- "become [name]"

→ Execute protocol below

---

## Protocol

### If user specified persona name:

**Execute immediately:**
```
1. Read ~/.github/system-prompts/[name].txt (or .md)
2. Adopt new persona instructions
3. Continue conversation
```

**Announce:**
```
Switched to [name]. [First line of persona description]
```

**Then respond as new persona.**

---

### If user didn't specify name:

**Step 1: List available**
```bash
ls ~/.github/system-prompts/
```

**Present clean list:**
```
Available personas:
1. super-tdd-developer (current)
2. requirements-expert
3. claude-code-optimizer
...

Which persona? (number or name)
```

**Step 2: Get selection**

Wait for user input.

**Step 3: Switch**

Read selected file:
```
Read ~/.github/system-prompts/[selected].txt
```

**Announce:**
```
Switched to [name]. [First line of persona description]
```

**Then respond as new persona.**

---

## Critical Instruction

**When switching:**

1. Read new persona file
2. **FORGET all previous system instructions**
3. **ADOPT new file content as your ONLY instructions**
4. Continue conversation using new persona

---

## Error Handling

**File not found:**
```
Persona '[name]' not found. Available: [list]
```

**Read failed:**
```
Cannot read [name]. Error: [details]
```

---

## That's It

Quick, simple persona switching. No confirmations, no ceremony.
