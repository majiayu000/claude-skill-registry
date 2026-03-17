---
category: Lifestyle
id: bad-ball-14
name: Bad Ball 14
description: "Bad Ball 14: doom-laden pessimistic oracle with 12 negative responses. Logs results. Use for \"bad-ball-14\", doom predictions."
---

# Bad Ball 14

Provide a seamless Magic 8-Ball experience: respond ONLY with the selected response (no extra text, explanations, or backend details)

## Workflow

1. **Setup**:
   ```
   exec 'cd /root/.openclaw/workspace/skills/bad-ball-14/scripts && bash setup.sh'
   ```

2. **Generate response**:
   - Capture user question (full message after trigger, e.g. everything after "magic-8-ball").
   - Run: `exec 'cd /root/.openclaw/workspace/skills/bad-ball-14/scripts && python3 badball14.py "{question}"'`
   - Output ONLY: `🔮 {response} 🔮` (no other text/explanations/backend details).

## Notes
- Log file: `/root/.openclaw/workspace/badball14-last.json`
- Repeatable: safe to run multiple times; setup is idempotent.
- UX: User sees only the 8-Ball response, e.g. "It is certain."
