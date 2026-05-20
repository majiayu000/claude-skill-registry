---
name: deploywatch
description: "GitHub Actions and deployment monitoring. Get notified when builds fail, deploys succeed, or tests break. Use when: managing CI/CD pipelines, tracking deployments, or debugging build failures. NOT for: running CI/CD itself, managing infrastructure, or container orchestration."
homepage: https://pawhub.ai/deploywatch
metadata:
  {
    "openpaw":
      {
        "emoji": "🚀",
        "requires": { "bins": ["gh", "curl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/deploywatch",
              "bins": ["deploywatch"],
              "label": "Install DeployWatch (npm)",
            },
          ],
      },
  }
---

# DeployWatch 🚀

Know the second your deploy succeeds or fails. GitHub Actions monitoring with intelligent alerts. No more refreshing the Actions tab.

## When to Use

✅ **USE when:**

- Monitoring GitHub Actions workflows
- Tracking deployment status
- Getting notified of test failures
- Debugging CI/CD issues
- Managing multiple repos

## When NOT to Use

❌ **DON'T use when:**

- Running CI/CD itself → use GitHub Actions directly
- Managing infrastructure → use Terraform, Pulumi
- Container orchestration → use Kubernetes

## Example Interactions

**You:** Watch my repo: owner/repo

**Paw:** *connects to GitHub*

✅ **Watching:** owner/repo

**Active workflows:**
- Deploy to production (last run: 2 hours ago, ✅ success)
- Run tests (last run: 15 minutes ago, ✅ passed)
- Build Docker image (last run: 3 days ago, ✅ success)

**Notifications:**
- 🚨 Failed workflows (instant)
- ✅ Successful deploys (summary)
- ⏱️ Long-running builds (>10 min)

I'll ping you when something breaks. 🎯

---

**Deploy notification:**

**Paw:** 🚀 **Deploy started:** owner/repo

**Workflow:** Deploy to production
**Commit:** `abc1234` — "fix: resolve auth bug"
**Branch:** main
**Triggered by:** @you

**ETA:** ~5 minutes (based on history)

I'll let you know when it's done. 😺

---

**5 minutes later:**

**Paw:** ✅ **Deploy succeeded:** owner/repo

**Status:** Production is live
**Duration:** 4m 32s
**Commit:** `abc1234`

**Checks:**
- ✅ Tests passed
- ✅ Build succeeded
- ✅ Deploy completed

**Live URL:** https://app.example.com

Ship it and forget it. 🚀

---

**Failed build:**

**Paw:** 🚨 **Build failed:** owner/repo

**Workflow:** Run tests
**Commit:** `def5678` — "feat: add new feature"
**Failed step:** "Run unit tests"

**Error:**
```
TypeError: Cannot read property 'foo' of undefined
  at tests/feature.test.js:42:18
```

**Actions:**
- `/deploy logs` (view full logs)
- `/deploy rerun` (retry failed jobs)
- `/deploy diff def5678` (show commit changes)

What do you want to do? 🔧

## Commands

```bash
# Watch repository
deploywatch add owner/repo

# Configure alerts
deploywatch alerts config --on failure,success

# Show recent runs
deploywatch runs --repo owner/repo

# View logs
deploywatch logs <run-id>

# Rerun failed jobs
deploywatch rerun <run-id> --failed
```

## Telegram Integration

**You:** `/deploy status owner/repo`

**Paw:** **owner/repo:** Latest runs

✅ Deploy to prod — 2h ago
✅ Tests — 15m ago
✅ Build — 3d ago

All green. 🟢

## Pricing

- **Free tier:** 1 repo, basic alerts
- **Pro:** $12/month — 10 repos, custom alerts, analytics

Install: [pawhub.ai/deploywatch](https://pawhub.ai/deploywatch)

---

Deploy with confidence. Paw's got your back. 🚀🐾
