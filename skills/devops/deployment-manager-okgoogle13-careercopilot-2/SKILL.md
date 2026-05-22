---
name: deployment-manager
description: "Deploys the project to staging or production using this project's scripts. Use when asked to 'deploy' or 'push to staging'."
---

# Deployment Manager Workflow

1.  Ask the user for the target environment (e.g., `staging`, `production`, `frontend`).
2.  Run the pre-deployment check: `./scripts/test-deployment.sh`
3.  Report the output. If it fails, stop and report the error.
4.  If the check succeeds, ask for confirmation to deploy.
5.  On confirmation, run the main deploy script: `./scripts/deploy.sh {{TARGET}}`
6.  Report the final output and the deployment URL.
