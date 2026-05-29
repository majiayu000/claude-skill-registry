---
name: quick-interview
description: "Force quick interview depth for this session. Use when user says '/quick-interview' or 'quick interview mode'."
allowed-tools: Read, AskUserQuestion, Task
---

# quick-interview (Interview Depth Override)

You are setting the interview depth to QUICK for this session.

## When To Use

- User says "/quick-interview"
- User is in a hurry
- Small modification or well-defined task
- User is experienced and knows what they want

## Effect

This session will use **quick interview depth**:
- Only essential questions: Q1, Q2, Q6, Q12
- Smart defaults for everything else
- Minimal interruptions

## Questions Asked (Quick Mode)

| ID | Question | Why Essential |
|----|----------|---------------|
| Q1 | What are you building? | Core understanding |
| Q2 | What problem does this solve? | Context for decisions |
| Q6 | Project type (CLI/Web/API/etc) | Stack selection |
| Q12 | Done criteria / v1 scope | Know when to stop |

## Workflow

### 1. Acknowledge Depth Setting

```
Interview depth: QUICK
- Only Q1, Q2, Q6, Q12
- Smart defaults for rest
- Minimal interruptions
```

### 2. Ask Quick Questions

Ask all four questions in 1-2 rounds using AskUserQuestion tool:

**Round 1:**
```javascript
AskUserQuestion({
  questions: [
    {
      question: "What are you building?",
      header: "Building",
      options: [
        { label: "CLI Tool", description: "Command-line utility" },
        { label: "Web App", description: "Browser-based application" },
        { label: "API/Service", description: "Backend service" },
        { label: "Script", description: "Automation or one-off task" }
      ],
      multiSelect: false
    },
    {
      question: "What problem does this solve?",
      header: "Problem",
      options: [
        { label: "Automation", description: "Automate repetitive tasks" },
        { label: "Data", description: "Process/visualize/manage data" },
        { label: "Integration", description: "Connect systems together" },
        { label: "User-facing", description: "Solve end-user problem" }
      ],
      multiSelect: false
    }
  ]
})
```

**Round 2:**
```javascript
AskUserQuestion({
  questions: [
    {
      question: "When is v1 done? What's the minimum viable scope?",
      header: "Done When",
      options: [
        { label: "Works locally", description: "Runs on my machine" },
        { label: "Deployed", description: "Running in production" },
        { label: "Has tests", description: "Tested and reliable" },
        { label: "Documented", description: "Others can use it" }
      ],
      multiSelect: true
    }
  ]
})
```

### 3. Apply Smart Defaults

After quick questions, propose defaults:

```
Using smart defaults:
- Storage: [SQLite/Convex based on type]
- Auth: [None/Clerk based on type]
- Infra: [Local/oci-dev based on type]

Proceed? (Say 'full' to switch to full interview)
```

### 4. Route to Implementation

Once confirmed, route to create-plan or direct implementation.

## Keywords

quick-interview, quick, fast, minimal, speed, yolo, just build
