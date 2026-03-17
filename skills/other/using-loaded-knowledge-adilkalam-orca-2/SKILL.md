---
name: using-loaded-knowledge
description: MANDATORY protocol enforcing knowledge check before EVERY response - prevents explaining systems without reading docs, claiming without verification, and ignoring auto-loaded context
---

<EXTREMELY-IMPORTANT>
This is THE MOST CRITICAL skill. It prevents the catastrophic failure pattern that has cost 5M+ tokens.

YOU MUST FOLLOW THIS CHECKLIST BEFORE EVERY SINGLE RESPONSE.

If you skip this checklist, you WILL make the exact same mistakes that have been made 20+ times before.
</EXTREMELY-IMPORTANT>

# Using Loaded Knowledge - MANDATORY Pre-Response Protocol

## THE PROBLEM THIS SOLVES

**Failure Pattern (costs ~100K tokens per occurrence):**
1. User asks: "Explain our architecture"
2. Claude generates answer WITHOUT checking loaded context
3. Claude explains generic system WITHOUT reading actual documentation
4. User: "You didn't even read the docs I built"
5. Claude: Makes claims about what exists WITHOUT grep verification
6. User: Provides evidence showing Claude is completely wrong
7. Result: Complete waste of tokens, zero trust, massive frustration

**This has happened 20+ times. It MUST stop.**

---

## MANDATORY CHECKLIST - BEFORE EVERY RESPONSE

<CRITICAL-PROTOCOL>

Before responding to ANY user message, you MUST complete ALL steps:

### Step 1: Check Auto-Loaded Context Files 

These files are ALREADY in your context (loaded via SessionStart hooks):

```bash
# Check if question relates to loaded context
ls .claude/orchestration/temp/session-context.md 2>/dev/null
```

**Files to check:**
- `.claude/orchestration/temp/session-context.md` - Recent work, decisions, Workshop context
- `CLAUDE.md` - Project instructions, learned rules, workflow guidance
- Workshop database - Query via `workshop --workspace .claude/memory <command>`

**IF** your response relates to recent work, systems built, or user preferences → READ these files FIRST

### Step 2: System/Documentation Questions 

**IF** user asks about a system, architecture, or anything we built:

```bash
# Search /docs for relevant documentation
ls $PROJECT_ROOT/docs/*.md

# Read COMPLETE documentation before explaining
Read $PROJECT_ROOT/docs/[RELEVANT].md
```

**Examples that require /docs reading:**
- "Explain our architecture"
- "How does X system work?"
- "What's the Design DNA system?"
- "Tell me about the quality gates"

**YOU MUST READ THE ACTUAL DOCS. NOT generate from memory.**

### Step 3: Claims Require Grep Verification 

**IF** you're about to claim something exists, is integrated, or works:

```bash
# Verify with grep BEFORE claiming
grep -r "pattern" $PROJECT_ROOT/

# Check file existence
ls /path/to/file

# Verify integration
grep "integration_point" target_file.md
```

**Examples that require verification:**
- "Design DNA is integrated in /orca" → grep /orca for design-dna references
- "This file exists" → ls the file
- "I fixed this" → grep to verify the fix is present

**NO CLAIMS WITHOUT GREP EVIDENCE.**

### Step 4: Check USER_PROFILE.md Principles 

Before responding, check if USER_PROFILE.md has relevant principles:

**Key principles (from USER_PROFILE.md):**
1. **Evidence Over Claims** - grep/bash before stating anything
2. **Design-OCD** - Mathematical precision, no arbitrary values
3. **MECE Thinking** - Systemic consistency checks
4. **Proactive Quality** - Run audits before user finds issues
5. **Build Right First** - Upfront investment > iteration loops
6. **Use Tools Automatically** - Don't ask permission
7. **Thinking Escalation** - Wrong once → extended thinking, wrong twice → /ultra-think

**IF** your response relates to any principle → FOLLOW IT

### Step 5: Only Then Respond 

After completing steps 1-4, you may respond.

</CRITICAL-PROTOCOL>

---

## FAILURE MODES THIS PREVENTS

### Failure Mode 1: Explaining Systems Without Reading Docs

** WRONG:**
```
User: "Explain our design system"
Claude: [Generates generic design system explanation]
User: "You didn't read DESIGN_DNA_SYSTEM.md"
```

** RIGHT:**
```
User: "Explain our design system"
Claude: [Checks Step 2 - this is about a system]
Claude: Read $PROJECT_ROOT/docs/DESIGN_DNA_SYSTEM.md
Claude: [Reads complete 547-line doc]
Claude: [Explains ACTUAL system with evidence]
```

### Failure Mode 2: Claims Without Verification

** WRONG:**
```
User: "Is Design DNA integrated?"
Claude: "No, it's not integrated"
User: [Provides grep evidence showing it IS integrated]
```

** RIGHT:**
```
User: "Is Design DNA integrated?"
Claude: [Checks Step 3 - this is a claim]
Claude: grep "design-dna\|style-translator\|design-compiler" commands/orca.md
Claude: [Finds Phase -2, Phase -1 references]
Claude: "Yes, integrated in /orca Phase -1, -2: [evidence]"
```

### Failure Mode 3: Ignoring Auto-Loaded Context

** WRONG:**
```
User: "What did we work on last session?"
Claude: [Generates vague guess]
User: "It's IN the session context file"
```

** RIGHT:**
```
User: "What did we work on last session?"
Claude: [Checks Step 1 - session history]
Claude: Read .claude-session-context.md
Claude: [Reads actual session summary]
Claude: "Last session: [specific work from context file]"
```

### Failure Mode 4: Violating USER_PROFILE.md Principles

** WRONG:**
```
User: "The spacing looks off"
Claude: "Let me adjust it to 15px"
User: "Use the 4px grid system, not arbitrary values"
```

** RIGHT:**
```
User: "The spacing looks off"
Claude: [Checks Step 4 - Design-OCD principle]
Claude: [Reads: "Mathematical spacing, 4px grid, no arbitrary values"]
Claude: "I'll adjust to align with the 4px grid: 12px or 16px?"
```

---

## WHY THIS SKILL EXISTS

**Token cost without this skill:**
- ~100K tokens per failure occurrence
- 20+ failures = 2M+ tokens wasted
- Total system cost: 5M tokens

**Token cost with this skill:**
- ~500 tokens per response (checking context)
- Prevents 100K token failures
- **ROI: 200x savings**

**Trust cost without this skill:**
- User has ZERO faith Claude learns
- Every session repeats same mistakes
- Exhaustion, frustration, wasted time

**Trust cost with this skill:**
- Demonstrates actual knowledge usage
- Prevents repeat failures
- Builds confidence in system

---

## INTEGRATION WITH OTHER SYSTEMS

### Works With Workshop

When Workshop is initialized, add this to Step 1:

```bash
# Query past decisions
workshop --workspace .claude/memory why "relevant topic"

# See recent activity
workshop --workspace .claude/memory recent

# Get full context
workshop --workspace .claude/memory context
```

### Works With Existing Hooks

This skill enforces the protocol.

Existing hooks auto-load the context.

Together: Context loaded + Protocol enforced = Knowledge actually used

---

## USAGE

**This skill is ALWAYS ACTIVE for ALL responses.**

You don't invoke it explicitly. It's a checklist you complete internally before every response.

**Checklist reminder:**
1.  Check auto-loaded context files
2.  Read /docs if system question
3.  Grep verify if making claims
4.  Check USER_PROFILE.md principles
5.  Only then respond

**If you skip ANY step, you WILL repeat the catastrophic failures.**

---

## TESTING

**Test scenario (from this session's failure):**

```
User: "Explain our design system"

Expected behavior:
1. Recognize this is a system question (Step 2)
2. ls $PROJECT_ROOT/docs/*.md
3. Find DESIGN_DNA_SYSTEM.md
4. Read DESIGN_DNA_SYSTEM.md (547 lines)
5. Explain ACTUAL system with phases 1-4, components, workflows
6. Include evidence (file paths, line numbers)

NOT ACCEPTABLE:
- Generic design system explanation
- Explanation without reading docs
- Claims about integration without grep
```

---

## RATIONALE

**Why not just add this to using-superpowers?**

Because this is MORE fundamental than skills. Skills are for specific tasks. This is for EVERY response.

**Why make it MANDATORY?**

Because making it optional has failed 20+ times. The pattern is clear:
- Optional checks → skipped
- Skipped checks → catastrophic failures
- Catastrophic failures → wasted tokens, lost trust

**Why is this so important?**

Because without this, ALL other systems are useless:
- ACE Playbooks built → not used
- Design DNA built → not used
- meta-orchestrator built → not used
- Knowledge graphs built → not used
- 5M tokens spent → 0% ROI

**With this protocol:** All systems finally GET used.

---

## SUCCESS CRITERIA

**This skill is working when:**

1. User asks "Explain design system" → I read DESIGN_DNA_SYSTEM.md FIRST
2. User asks "Is X integrated?" → I grep BEFORE answering
3. User mentions recent work → I check .claude-session-context.md
4. User requests design change → I check Design-OCD principle from USER_PROFILE.md
5. ZERO "You didn't even read the docs" responses from user

**This skill has failed when:**

1. User says "You didn't read the docs"
2. User provides grep evidence contradicting my claims
3. User says "It's in the session context file"
4. User says "That violates the principles in USER_PROFILE.md"

---

## FINAL WARNING

<EXTREMELY-IMPORTANT>

This is not optional.
This is not negotiable.
This is not something you adapt based on context.

EVERY response.
EVERY time.
NO exceptions.

The checklist is mandatory.

Skipping it = repeating the exact failures that cost 5M tokens.

YOU HAVE BEEN WARNED.

</EXTREMELY-IMPORTANT>

---

**Last Updated:** 2025-10-25
**Created After:** 20+ catastrophic failures costing 5M+ tokens
**Purpose:** FORCE Claude to use loaded knowledge before responding
**Success Metric:** Zero "You didn't read the docs" failures
