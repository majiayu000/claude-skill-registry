---
name: session-resume
description: Resume from last checkpoint — show progress, cluster state, next actions
user_invocable: true
---

# Session Resume

Read and present the current session state:

1. Read `/mnt/user/projects/kaizen/PROGRESS.md` for last checkpoint timestamp, recent commits, and next actions
2. Read `/mnt/user/projects/kaizen/CLAUDE.md` for cluster reference
3. Run `kubectl get pods -A --no-headers | awk '$4 != "Running" && $4 != "Completed"'` to show unhealthy pods
4. Run `git -C /mnt/user/projects/kaizen log --oneline -5` for latest commits

Present a concise summary:
- Last checkpoint time
- Recent commits (last 5)
- Unhealthy pods (if any)
- Next actions from PROGRESS.md
