---
name: increment
description: Plan new Product Increment. Use when starting new features, hotfixes, or development work that needs specification.
hooks:
  PreToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/interview-enforcement-guard.sh
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/spec-template-enforcement-guard.sh
  PostToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: bash plugins/specweave/hooks/v2/guards/increment-duplicate-guard.sh
---

# Plan Product Increment

**Orchestrator for increment planning** - handles pre-flight checks, then delegates to `sw:increment-planner` skill.

## Workflow

```
Step 0A: Discipline Check (BLOCKING)
Step 0B: WIP Enforcement
Step 0C: Tech Stack Detection
Step 1:  Call sw:increment-planner skill
```

## Step 0A: Discipline Check (MANDATORY)

**Cannot start N+1 until N is DONE.**

```bash
if ! specweave check-discipline; then
  echo "❌ Cannot create new increment! Close existing work first."
  echo "💡 Run: /sw:done <id>"
  exit 1
fi
```

## Step 0B: WIP Enforcement

Default: 1 active increment (focus). Allow 2 for emergencies.

```typescript
const active = MetadataManager.getAllActive();
const limits = config.limits || { maxActiveIncrements: 1, hardCap: 3 };

if (active.length >= limits.hardCap) {
  // BLOCK - ask user to complete/pause existing
  console.log("⚠️ WIP LIMIT REACHED");
  console.log("Options: /sw:done <id> | /sw:pause <id>");
}

if (active.length >= limits.maxActiveIncrements) {
  // SOFT WARNING - hotfix/bug can bypass
  const isEmergency = ['hotfix', 'bug'].includes(incrementType);
  if (!isEmergency) {
    // Prompt: complete, pause, or continue anyway
  }
}
```

**Type-Based Limits:**
- Hotfix/Bug: Unlimited (emergency)
- Feature/Change-Request: Max 2
- Refactor: Max 1
- Experiment: Unlimited

## Step 0C: Tech Stack Detection

Auto-detect from project files:

| File | Language |
|------|----------|
| package.json | TypeScript/JavaScript |
| requirements.txt | Python |
| go.mod | Go |
| Cargo.toml | Rust |
| pom.xml | Java |
| *.csproj | C#/.NET |

If detection fails, ask user.

## Step 1: Activate Increment Planner

**MUST use Skill tool:**

```typescript
Skill({
  skill: "sw:increment-planner",
  args: "--id=XXXX-name --description=\"...\" --project=my-project"
});
```

The skill handles:
- Project/board selection
- TDD mode detection
- Template creation
- Living docs sync

## Step 2: Post-Creation Sync

After skill completes:

```bash
/sw:sync-specs {increment-id}
/sw-github:sync {increment-id}  # If configured
```

## Output

```
✅ Created increment 0003-user-authentication

   Tech stack: TypeScript, NextJS, PostgreSQL
   Location: .specweave/increments/0003-user-authentication/

   Files: spec.md, plan.md, tasks.md, metadata.json

   Next: /sw:do 0003 (start implementation)
```

## Error Handling

- `.specweave/` not found: "Run specweave init first"
- Vague description: Ask clarifying questions
- Skill fails: Fall back to keyword prompts for PM/Architect skills

---

**This command is the main entry point for creating new work in SpecWeave.**
