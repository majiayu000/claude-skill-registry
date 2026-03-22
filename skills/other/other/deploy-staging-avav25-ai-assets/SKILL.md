---
name: deploy-staging
description: Deploy a change to staging by reading repository deployment context, preparing the build or manifest change, and verifying the staged environment.
---

# Deploy Staging

## Workflow

1. Read root `AGENTS.md`, deployment docs, and service configs.
2. Identify the deployment mechanism for the affected service.
3. Prepare the build or manifest change.
4. Deploy to staging using the normal project path.
5. Run smoke checks and confirm health.

## Output

- Deployment summary
- Verification steps run
- Any rollback notes
