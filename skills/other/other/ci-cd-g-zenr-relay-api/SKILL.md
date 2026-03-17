---
name: ci-cd
description: Set up or update GitHub Actions CI/CD pipeline (Marcus Chen's workflow)
disable-model-invocation: true
---

Set up CI/CD: $ARGUMENTS

## Step 1 — Create Workflow Directory
```bash
mkdir -p .github/workflows
```

## Step 2 — CI Workflow (tests + type check on every push/PR)
Create `.github/workflows/ci.yml`:
- Trigger on push/PR to main
- Matrix strategy for supported language versions (see project config)
- Install dependencies from the dependency file (see project config)
- Run the test command with mock/dev mode enabled
- Run the type-check command

## Step 3 — Docker Build Workflow (verify Dockerfile on every PR)
Create `.github/workflows/docker.yml`:
- Trigger on PR to main
- Build the Docker image using the Docker build command (see project config)
- Run the container with mock/dev mode enabled
- Verify the health endpoint responds

## Step 4 — Release Workflow (on tag push)
Create `.github/workflows/release.yml`:
- Trigger on tag push matching `v*`
- Create GitHub Release with auto-generated release notes

## Step 5 — Add CI Badge to README
Add the CI workflow badge to the project README.

## Step 6 — Verify
```bash
git add .github/
git commit -m "ci: add GitHub Actions workflows"
git push
```
Check the Actions tab on GitHub to verify the workflow runs.

## Rules
- Always test with mock/dev mode enabled in CI (no hardware)
- Test on multiple language versions per project config
- Docker build test ensures Dockerfile stays valid
- Never store secrets in workflow files — use GitHub Secrets