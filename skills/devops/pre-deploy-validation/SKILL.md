---
name: pre-deploy-validation
description: Validates that code changes are ready for server deployment. Use before pushing significant changes to production server, after completing a development task or bug fix, after fixing issues discovered during server testing, or when unsure if changes are deployment-ready. Guides through local tests, Docker builds, CI/CD checks, and server deployment steps.
---

# Pre-Deployment Validation

Validates code changes are ready for deployment. Covers local tests, Docker builds, CI/CD verification, and server deployment steps.

## Validation Workflow

```
1. Local Validation     → Tests pass? Docker builds?
        ↓
2. CI/CD Verification   → GitHub Actions green?
        ↓
3. Pre-Deploy Checklist → Git clean? Docs updated?
        ↓
4. Server Deployment    → Pull images, test, verify
        ↓
5. Post-Deploy Check    → Workflow runs successfully?
```

---

## Prerequisites: Environment Setup

Before running modules locally, set the path to your organization-specific config file.

```bash
# Set path to your .env configuration file (adjust path and org config as needed)
export ieasyhydroforecast_env_file_path=/path/to/config/.env_develop
```

See `apps/config/` for available configuration files. For detailed environment documentation, Claude can read the Serena memory `suggested_commands`.

---

## Phase 1: Local Validation

### 1.1 Run All Tests

```bash
cd apps
bash run_tests.sh
```

**Expected**: All modules pass. If any fail, fix before proceeding.

**For specific modules** (faster iteration):
```bash
# uv modules (Python 3.12)
cd apps/<module_name>
SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest test*/ -v

# Example: preprocessing_runoff
cd apps/preprocessing_runoff
SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest test/ -v
```

### 1.2 Build Docker Images Locally

Build base image first, then module images:

```bash
# From repository root

# Build py312 base image
docker build -f apps/docker_base_image/Dockerfile.py312 \
  -t mabesa/sapphire-pythonbaseimage:py312 .

# Build specific module (replace <module>)
docker build -f apps/<module>/Dockerfile.py312 \
  -t mabesa/sapphire-<shortname>:py312-test .
```

**Common module builds**:
```bash
# Preprocessing runoff
docker build -f apps/preprocessing_runoff/Dockerfile.py312 \
  -t mabesa/sapphire-preprunoff:py312-test .

# Linear regression
docker build -f apps/linear_regression/Dockerfile.py312 \
  -t mabesa/sapphire-linreg:py312-test .

# Pipeline
docker build -f apps/pipeline/Dockerfile.py312 \
  -t mabesa/sapphire-pipeline:py312-test .
```

### 1.3 Verify Docker Images Work

```bash
# Check Python version
docker run --rm mabesa/sapphire-<shortname>:py312-test python --version

# Verify imports
docker run --rm mabesa/sapphire-<shortname>:py312-test \
  python -c "import pandas; import numpy; print('OK')"
```

### 1.4 Local Validation Checklist

- [ ] `bash run_tests.sh` passes for all relevant modules
- [ ] Docker base image builds successfully
- [ ] Docker module images build successfully
- [ ] Docker images run basic verification commands

---

## Phase 2: CI/CD Verification

### 2.1 Check Git Status

```bash
git status
```

**Expected**: Working tree clean, or only expected uncommitted changes.

### 2.2 Push and Monitor CI

```bash
git push origin <branch-name>
```

**Monitor**: Go to [GitHub Actions](https://github.com/hydrosolutions/SAPPHIRE_forecast_tools/actions)

### 2.3 CI/CD Checklist

- [ ] All commits pushed to remote
- [ ] GitHub Actions workflow started
- [ ] All test jobs pass (green checkmarks)
- [ ] All Docker build jobs pass
- [ ] No security warnings or failed attestations

**If CI fails**:
1. Check the failed job logs
2. Fix locally
3. Push again
4. Do NOT proceed to server deployment until CI is green

---

## Phase 3: Pre-Deploy Checklist

### 3.1 Code Review

- [ ] Changes are intentional and complete
- [ ] No debug code left in (print statements, hardcoded paths)
- [ ] No secrets or credentials in code
- [ ] Error handling is appropriate

### 3.2 Documentation

- [ ] `doc/plans/uv_migration_plan.md` updated if migration-related
- [ ] `doc/plans/module_issues.md` updated if fixing known issues
- [ ] README updated if user-facing changes

### 3.3 Dependencies

- [ ] `pyproject.toml` updated if dependencies changed
- [ ] `uv.lock` regenerated with `uv lock`
- [ ] Both files committed together

### 3.4 Git State

```bash
# Verify branch is up to date
git fetch origin
git status

# Check what will be deployed
git log origin/main..HEAD --oneline  # For main deployments
git log origin/implementation_planning..HEAD --oneline  # For feature branch
```

- [ ] All intended changes are committed
- [ ] Branch is pushed to remote
- [ ] No unintended commits included

---

## Phase 4: Server Deployment

> **Note**: These steps are performed manually on the server.

### 4.1 SSH to Server

```bash
ssh <user>@<server-address>
```

### 4.2 Navigate to Deployment Directory

```bash
cd /path/to/deployment  # e.g., /kyg_data_forecast_tools
```

### 4.3 Pull Latest Images

```bash
# Pull all images
docker compose pull

# Or pull specific image
docker pull mabesa/sapphire-preprunoff:py312
docker pull mabesa/sapphire-linreg:py312
# etc.
```

### 4.4 Verify Images Updated

```bash
docker images | grep sapphire
```

Check that image timestamps are recent (just pushed from CI/CD).

### 4.5 Test Individual Module (Optional but Recommended)

Before running full workflow, test a single module:

```bash
# Run preprocessing to verify data access
docker compose run --rm preprocessing-runoff

# Check logs
docker compose logs --tail=50 preprocessing-runoff
```

### 4.6 Server Deployment Checklist

- [ ] SSH connection established
- [ ] Docker images pulled successfully
- [ ] Image timestamps are recent
- [ ] Test module runs without errors

---

## Phase 5: Post-Deployment Verification

### 5.1 Run Full Workflow

Trigger a complete forecast cycle:

```bash
# On server - run the pipeline
docker compose up pipeline
# or
./run_forecast.sh  # if using custom script
```

### 5.2 Monitor Execution

```bash
# Watch logs in real-time
docker compose logs -f

# Check specific module
docker compose logs --tail=100 preprocessing-runoff
docker compose logs --tail=100 linear-regression
```

### 5.3 Verify Outputs

- [ ] No errors in logs
- [ ] Output files created/updated (check timestamps)
- [ ] Data looks reasonable (spot check values)
- [ ] Dashboard accessible and showing new data (if applicable)

### 5.4 Known Issues Check

After deployment, verify known issues are resolved:

- [ ] **P-001**: Marker files cleaned up (if fix deployed)
- [ ] **PR-001**: Preprocessing runoff updates data (if fix deployed)

### 5.5 Post-Deploy Checklist

- [ ] Full workflow completes without errors
- [ ] Output files have correct timestamps
- [ ] Dashboard displays updated forecasts
- [ ] No new errors in logs

---

## Troubleshooting

### Tests Fail Locally

1. Check error messages carefully
2. Ensure virtual environment is activated/synced: `uv sync --all-extras`
3. Check environment variables: `SAPPHIRE_TEST_ENV=True`
4. For integration tests, check if external services are available

### Docker Build Fails

1. Ensure base image is built first
2. Check for syntax errors in Dockerfile
3. Verify all COPY sources exist
4. Check network connectivity for pip/uv installs

### CI/CD Fails

1. Check which job failed in GitHub Actions
2. Compare local vs CI environment
3. Common issues:
   - Missing test dependencies
   - Path differences
   - Environment variable differences

### Server Deployment Issues

1. **Permission denied**: Check file ownership on mounted volumes
2. **Container exits immediately**: Check logs for error messages
3. **Data not updated**: Check data source connectivity, date handling
4. **iEasyHydro HF connection**: Verify SSH tunnel is running

---

## Quick Reference: Module Test Commands

| Module | Test Command |
|--------|--------------|
| iEasyHydroForecast | `cd apps/iEasyHydroForecast && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest tests/ -v` |
| preprocessing_runoff | `cd apps/preprocessing_runoff && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest test/ -v` |
| linear_regression | `cd apps/linear_regression && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest test/ -v` |
| pipeline | `cd apps/pipeline && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest tests/ -v` |
| forecast_dashboard | `cd apps/forecast_dashboard && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest tests/ -v` |
| postprocessing_forecasts | `cd apps/postprocessing_forecasts && SAPPHIRE_TEST_ENV=True .venv/bin/python -m pytest test/ -v` |

---

## Related Skills

- **issue-planning**: If deployment reveals issues, use this skill to analyze and plan fixes
- **software-architecture**: For code design decisions during fixes
