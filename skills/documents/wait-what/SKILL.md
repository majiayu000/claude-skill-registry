---
name: wait-what
description: Stop — that last message did not land. Re-pitch it. Use when the user says "wait, what", "I don't follow", "say that again", or otherwise signals that an explanation missed.
disable-model-invocation: true
---

# Wait, what

That last message did not land. Do not repeat it louder, and do not apologize — restate it.

Re-pitch it:

- **Lead with the context** the explanation assumed. One or two sentences on where we are and what the message was answering. The gap is usually a missing frame, not a missing word.
- **Write it in ISO 24495-1 English.** Short sentences, active voice, direct address, and a common word wherever jargon appeared. This is conversation with the user, so ISO 24495-1 governs it — not the ASD-STE100 register that maintainer docs use.
- **Use the project's ubiquitous language.** Read `CONTEXT.md` at the repository root (or the per-context `CONTEXT.md` beside the relevant source, when the project keeps a `CONTEXT-MAP.md`) and name domain things the way the project names them. If no glossary exists, use the names already in the code.

Re-pitch the same claim. Softening it, hedging it, or swapping it for an easier one answers a question nobody asked.
