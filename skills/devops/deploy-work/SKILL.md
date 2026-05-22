---
name: deploy-work
description: Deployment workflow for company repos (pre/pro) using CI, ECR, and Helm.
---

# Deploy Work Skill

Standard deployment workflow for company repositories with CI/CD -> ECR -> Helm.

## When to Use

- Deploying to pre or pro for company repos.
- Ensuring CI has produced an image tag before helm upgrade.
- Running a controlled deploy with explicit confirmation.

## Core Rules

- Always use `--set image.tag=<SHA>` for helm upgrades.
- Do NOT edit or commit `values-pre.yaml` or `values-pro.yaml`.
- Verify CI completion and ECR push before helm upgrade.
- Ask for confirmation before `helm upgrade`.

## Repo Detection

Use any of:
- `git remote get-url origin`
- repo folder name
- presence of `ci/helm-package-new`

### Naturgy Special Case

- `values-pre.yaml` and `values-pro.yaml` under `ci/helm-package-new` only apply to the `naturgy-web` repo.
- If release is `naturgy-web-new` (or `naturgy-web-pre-naturgy-web-new`) use:
  - `./ci/helm-package-new/values-pre.yaml` or `./ci/helm-package-new/values-pro.yaml`.
- Otherwise use:
  - `./ci/helm-package/values-pre.yaml` or `./ci/helm-package/values-pro.yaml`.

## Pre Deployment Workflow

1. Ensure branch/PR has CI green.
   - `gh pr checks <id> --watch`
   - or `gh run list --branch <branch> --workflow ci.yml -L 1`

2. Get the SHA with CI green.
   - `gh run list --branch <branch> --workflow ci.yml -L 1 --json headSha,conclusion,status`

3. Verify ECR image push in logs.
   - `gh run view <run_id> --log`
   - Look for tags containing `<SHA>`.

4. Confirm cluster context and detect release/namespace.
   - `kubectl config current-context`
   - `kubectl get ns | rg <ns>`
   - `kubectl get deployments -A | rg <app>`
   - `helm list -A | rg <app>`

5. Confirm chart path and helm upgrade (confirm first).
   - Common chart path: `./ci/helm-package` or `./ci/helm-package-new`
   - `helm upgrade <release> -f <values-pre.yaml> <chart-path> --namespace <ns> --set image.tag=<SHA>`

## Pro Deployment Workflow

1. Merge PR to `master`.
   - `gh pr merge <id> --merge`

2. Wait for CI on `master`.
   - `gh run list --branch master --workflow ci.yml -L 1`

3. Get SHA and verify ECR push.
   - Same as pre.

4. Confirm cluster context and detect release/namespace.
   - `kubectl config current-context`
   - `kubectl get ns | rg <ns>`
   - Same as pre.

5. Confirm chart path and helm upgrade (confirm first).
   - Common chart path: `./ci/helm-package` or `./ci/helm-package-new`
   - `helm upgrade <release> -f <values-pro.yaml> <chart-path> --namespace <ns> --set image.tag=<SHA>`

## Safety

- No destructive cluster commands.
- Read-only until user confirms helm upgrade.
- Record release, namespace, and revision after deploy.
