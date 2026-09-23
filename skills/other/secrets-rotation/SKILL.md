---
name: secrets-rotation
description: What to do the moment a secret is exposed — pasted into chat, committed, logged, shown in a transcript or a screenshot. The secret is compromised; only revoking and rotating it helps. Turns it into one tracked task with an escalation, not a reminder repeated every session. Use when you see a key, token, password or private key anywhere it should not be ("ключ в чате", "токен в логах", "закоммитил .env"). Loaded by security-officer, l3-support, devops.
when_to_use: |
  Apply when:
  - a key, token, password or private key appears in a message, a commit, a log, a transcript, a screenshot or a context file
  - the operator pastes a credential into the conversation
  - a secret scanner (scripts/hooks/secret-scan.mjs, gitleaks) reports a finding
  - a session log carries "rotate the X key" forward from an earlier session
  Do NOT apply to:
  - test fixtures that are assembled at runtime and match no live account
effort: low
allowed-tools: Read, Bash, Grep
---

# secrets-rotation — an exposed secret is spent

Deleting the message, rewriting git history or redacting the log does not un-expose a
secret: the transcript, the remote, the backup and the provider's own logs already hold
it. The only fix is to make the exposed value worthless — **revoke it and issue a new one**.

What went wrong on real projects is not ignorance of that. It is that the rotation was
**remembered instead of tracked**: "rotate the exchange API keys" was carried forward
through seven session logs; "keys that passed through chat" appeared in seven summaries
of another project; a monitoring token pasted in plain text was never rotated. Each
session wrote the reminder again and nobody owned it.

## The moment you see one

1. **Never repeat the value.** Not in your answer, not in a task title, not in a log, not
   in a commit message. Name its **kind** and **where it is**: "OpenRouter API key, in the
   operator's message of 22.09, 14:10". `scripts/lib/secret-patterns.mjs` names the kind.
2. **Say it plainly, first line:** this key is compromised; revoking it is the only fix.
3. **Open one task, not a note** — in Beads if the project has it:

   ```bash
   bd create "Rotate <kind> exposed in <where> on <date>" -t bug -p 0 \
     -d "Exposed: <where>. Revoke at <provider console>, issue new, store in <secret store>, redeploy <consumers>, prove the old one is rejected."
   ```

   Priority 0 for a production credential or anything that moves money; 1 otherwise.
4. **If you can rotate it, rotate it** — the operator asked you to handle it, or your
   task covers that system. If it needs the operator (a provider console you cannot
   reach, a hardware token), the task's first line says exactly what they must click.

## Done means the old value is refused

A rotation is closed with evidence, not with "rotated":

- the new value is in the secret store the code reads — never in `CLAUDE.md`,
  `preferences.md`, memory files, a README or any file that is loaded into a model's
  context (one key in a preferences file reached 605 transcripts);
- every consumer was redeployed and uses it (`deploy-landed`, config check);
- **a call with the old value fails** — 401/403 from the provider. That is the proof.

## Carrying it forward

An open rotation task older than 48 hours goes to the top of the next session's report
and of `/inbox`, with its age. Do not re-list it in the session log as a fresh item —
link the task. Re-writing a reminder is how the seven-session carry-over happened.
