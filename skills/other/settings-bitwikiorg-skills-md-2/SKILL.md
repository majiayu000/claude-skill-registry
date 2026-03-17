---
description: Imported skill settings from agentskills
name: settings
signature: 27cbfc6ea7cd19b519a71a5caa60ff8e39750bee623c5554284bd767dc11a751
source: /a0/tmp/skills_research/agentskills/.claude/settings.json
---

{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
