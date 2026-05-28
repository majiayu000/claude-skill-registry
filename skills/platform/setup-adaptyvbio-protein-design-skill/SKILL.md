---
name: setup
description: >
  First-time setup for protein design tools. Use this skill when:
  (1) User is new and hasn't run any tools yet,
  (2) Commands fail with "file not found" or "modal: command not found",
  (3) Modal authentication errors occur,
  (4) User asks how to get started or set up the environment,
  (5) biomodals directory is missing or tools aren't working.
license: MIT
category: utilities
tags: [setup, onboarding, installation]
---

# Setup Guide

Help users get their environment ready to run protein design tools.

## Quick checklist

Run through this checklist when a user encounters setup issues:

| Step | Check | Fix |
|------|-------|-----|
| 1. Modal CLI | `modal --version` | `pip install modal` |
| 2. Modal auth | `modal token show` | `modal setup` |
| 3. biomodals | `ls biomodals/modal_*.py` | `git clone https://github.com/hgbrian/biomodals` |
| 4. Test | `cd biomodals && modal run modal_boltzgen.py --help` | See troubleshooting |

## Diagnosing issues

### Error: "modal: command not found"

**Cause**: Modal CLI not installed.

**Fix**:
```bash
pip install modal
```

Then restart the terminal or run `hash -r`.

### Error: "Permission denied" or "Unauthorized"

**Cause**: Modal not authenticated.

**Fix**:
```bash
modal setup
```

This opens a browser. Click "Authorize" to complete authentication.

### Error: "No such file or directory: modal_boltzgen.py"

**Cause**: biomodals repository not cloned or not in correct directory.

**Fix**:
```bash
git clone https://github.com/hgbrian/biomodals
cd biomodals
```

### Error: "uvx: command not found"

**Cause**: `uvx` is an optional wrapper from the `uv` package. It's not required.

**Fix**: Run modal directly (recommended):
```bash
modal run modal_boltzgen.py --help
```

Or install uv if you prefer using uvx:
```bash
pip install uv
```

## Full setup steps

### Step 1: Install Modal CLI

```bash
pip install modal
```

Verify: `modal --version`

### Step 2: Authenticate Modal

```bash
modal setup
```

This opens a browser. Click "Authorize".

Verify: `modal token show`

### Step 3: Clone biomodals

```bash
git clone https://github.com/hgbrian/biomodals
cd biomodals
```

Verify: `ls modal_*.py` should show files like `modal_boltzgen.py`

### Step 4: Test the Setup

```bash
cd biomodals
modal run modal_boltzgen.py --help
```

Expected: Usage instructions appear showing `--input-yaml`, `--protocol`, `--num-designs` options.

## Common workflows after setup

Once setup is complete, users can:

```bash
cd biomodals

# Design binders with BoltzGen (requires YAML config)
modal run modal_boltzgen.py --input-yaml binder.yaml --protocol protein-anything --num-designs 50

# Generate backbones with RFdiffusion
modal run modal_rfdiffusion.py --pdb target.pdb --contigs "A1-150/0 70-100" --num-designs 100

# Validate with Chai
modal run modal_chai1.py --input-faa designs.fasta
```

## GPU selection

Set GPU with environment variable:

```bash
GPU=A10G modal run modal_rfdiffusion.py --pdb target.pdb --contigs "A1-100/0 50-80" --num-designs 10
GPU=L40S modal run modal_boltzgen.py --input-yaml config.yaml --num-designs 50
GPU=A100 modal run modal_chai1.py --input-faa complex.fasta
```

| GPU | VRAM | Best For |
|-----|------|----------|
| T4 | 16GB | ProteinMPNN, ESM |
| A10G | 24GB | RFdiffusion, Chai |
| L40S | 48GB | BoltzGen, BindCraft |
| A100 | 40-80GB | Large complexes |

## Modal free tier

Modal offers $30/month in free credits - enough for:
- ~500 BoltzGen designs
- ~2000 RFdiffusion backbones
- ~1000 Chai predictions

---

**Full documentation**: See [Installation Guide](../../docs/installation.md)
