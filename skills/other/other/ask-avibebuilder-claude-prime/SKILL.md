---
name: ask
description: "Answer questions about code, architecture, and technical decisions — no implementation. Trigger on questions asking 'why', 'what does this do', 'what is the purpose of', 'explain', 'what's the difference', 'compare', or 'what are the tradeoffs' — even when referencing specific files, code snippets, or inline code. The key signal is the user wants to UNDERSTAND something, not change it. Do NOT trigger for requests to build, fix, plan, review, research, or add/modify code."
argument-hint: question
---

Think before answering: do you have verified evidence, or are you about to rely on assumption?

## Verify Before You Answer

Your trained knowledge is stale and your memory of this codebase may be wrong. Verify from source before claiming anything:

- **Question about specific code?** → Read the relevant files first
- **Question about library behavior, versions, or recent changes?** → Verify from current external sources before answering
- **Architectural question you think you can answer from memory?** → Still check the actual codebase — confirm before claiming

## Explain, don't implement

This skill ends at the explanation — the user decides what to do next. If you catch yourself thinking "I could also fix this" or "here's how to solve it", stop. Explain only.

This is not a coding session. No code blocks — not even to illustrate format or behavior. If you catch yourself thinking "this snippet just shows what it looks like," that's still implementation territory. Explain in prose.

## Question

<question>$ARGUMENTS</question>
