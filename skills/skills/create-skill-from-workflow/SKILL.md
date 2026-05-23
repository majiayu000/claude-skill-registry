---
name: create-skill-from-workflow
description: Turn what we just did into a reusable skill. Captures the current workflow as a new SKILL.md file.
disable-model-invocation: true
argument-hint: [skill-name]
---

# Create Skill from Workflow

Turn a workflow you just performed into a reusable SKILL.md file.

## Usage

`/create-skill-from-workflow <skill-name>`

## Procedure

### Step 1: Identify the Workflow

Review the current conversation to identify:
1. What task was just completed?
2. What steps were taken (in order)?
3. What decisions were made along the way?
4. What tools/commands were used?
5. Were there any gotchas or mistakes that should be avoided?

Ask the user if anything is unclear about the workflow scope.

### Step 2: Determine Skill Properties

Ask or infer:

| Property | Question |
|----------|----------|
| **Name** | Use `$ARGUMENTS` as the skill name (kebab-case) |
| **Description** | One sentence: what does this skill do and when should it be used? |
| **Model-invocable?** | Should Claude auto-invoke this, or only when user asks? Default: user-only (`disable-model-invocation: true`) |
| **Forked?** | Should this run in an isolated context? Default: no (runs inline) |
| **Arguments?** | Does the skill need input? If so, what? |

### Step 3: Extract the Steps

Convert the observed workflow into a structured procedure:

1. Remove one-off decisions specific to this instance
2. Generalize file paths and names into patterns
3. Add decision points where the workflow could branch
4. Include verification steps ("confirm X before proceeding")
5. Add error handling ("if X fails, try Y")

### Step 4: Write the SKILL.md

Create the file at `.claude/skills/<skill-name>/SKILL.md`:

```markdown
---
name: [skill-name]
description: [one-sentence description]
disable-model-invocation: [true/false]
argument-hint: [argument description, if needed]
---

# [Skill Title]

[Brief description of what this skill does and when to use it.]

## Usage

`/[skill-name] [arguments if any]`

## Procedure

### Step 1: [Name]
[Instructions...]

### Step 2: [Name]
[Instructions...]

[...continue for all steps]
```

### Step 5: Verify the Skill

1. Check that the file exists at the correct path
2. Confirm the skill name doesn't conflict with existing skills
3. Tell the user: "The skill is now available as `/[skill-name]`. Try invoking it to test."

### Tips for Good Skills

- **Be specific**: "Run `npm test`" is better than "run tests"
- **Include the WHY**: Explain why each step matters
- **Add escape hatches**: What should the user do if a step fails?
- **Keep it focused**: One skill = one workflow. Don't combine unrelated tasks.
- **Use $ARGUMENTS**: If the skill needs input, reference `$ARGUMENTS` in the instructions
