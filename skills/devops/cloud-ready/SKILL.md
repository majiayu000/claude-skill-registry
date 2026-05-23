---
name: cloud-ready
description: "Standardizes project for Cloud Sovereignty (Coolify + VPS) with Eco Mode resource limits and Professional Folder Hierarchy."
version: 1.1.0
---

# ☁️ Cloud Ready (Sovereign Deploy)

This skill forces the project into a professional, deployable state compatible with **Hetzner VPS** and **Coolify**.

## 🎯 Objective

Transform a "Local" project into a "Production" engine.

1.  **Strict Topology**: Enforces `src/`, `ops/`, `assets/`, `docs/`.
2.  **Eco Mode**: Generates `docker-compose.yml` with strict RAM/CPU limits to prevent OOM kills on cheap VPS.
3.  **Deployment Guide**: Adds `docs/COOLIFY_DEPLOY.md`.

## 🛠️ Usage

Trigger this skill when the user wants to "deploy", "go to cloud", or "standardize" the project.

```bash
# Verify structure
python -c "import os; print('✅ Ready' if os.path.exists('src') else '❌ Missing src/')"
```

## 📜 The "Golden Standard" (The Truths)

1.  **Code lives in `src/`**: No exceptions. `apps/` goes inside `src/`.
2.  **Resources live in `assets/`**: Not `rsc/`.
3.  **Infrastructure lives in `ops/`**: Firewall, Audits, Backups.
4.  **Data Persistence**: Only `/app/data` inside Docker.
5.  **Limits are Mandatory**: Every service MUST have `deploy.resources.limits`.

## 🔒 The Application of "Proof" (Verification Protocol)

Before considering a module "Cloud Ready", it must be **Inhaled** (Verified).

1.  **Create Temporary Provers**: Generate `prove_module.py` scripts at root.
2.  **Check Importability**: `from src.module import App`.
3.  **Check Integrity**: `hasattr(App, 'app')` or `hasattr(Bot, 'run')`.
4.  **Run Tests**: Fix `sys.path` in runners (`run_tests.py`) to include `src/`.

## 🧹 The "Sanitization" (Exhale Protocol)

We **never** ship the crowbar with the crate.

1.  **Delete Provers**: `del prove_*.py run_tests.py`.
2.  **Ignore Tests**: Add `tests/` and `*/tests/` to `.dockerignore`.
3.  **Sanitize Git**: Add `prove_*.py` and `*.tmp` to `.gitignore`.

> **Rule**: Production Containers contain ONLY what is needed to run. No tests, no audit tools.

## 📦 Output Artifacts

- `docker-compose.yml` (Optimized)
- `Dockerfile` (Python Slim with source mapping)
- `docs/COOLIFY_DEPLOY.md`
- `docs/SWAP_GUIDE.md`
