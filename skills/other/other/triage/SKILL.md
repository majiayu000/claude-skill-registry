---
name: doctor-triage
license: MIT
description: |
  Perform breadth-first hypothesis surfacing and prioritization across all
  ownership zones, without commitment. This is not diagnosis and not investigation.
metadata:
  author: Jordan Godau
  references:
    - 01_PURPOSE.md
    - 02_SCOPE.md
    - 03_BEHAVIOR.md
    - 04_OUTPUT.md
  assets:
    - TRIAGE_REPORT.md
  scripts:
    - evidence.sh
  keywords:
    - triage
    - hypothesis
    - breadth
    - prioritization
    - zones
    - likelihood
---

# doctor-triage

Perform **breadth-first hypothesis surfacing and prioritization** across all ownership zones.

## Purpose

Assume the problem may live in a layer the user is ignoring. Prefer "possible and boring" over "clever and narrow."

This is **not** diagnosis and **not** investigation.

## Epistemic Stance

- The problem may originate outside the layer where symptoms manifest
- Early confidence is a warning sign, not a virtue
- Multiple hypotheses are better than one "obvious" answer

## Scope of Consideration (Always Include)

- Backend application code
- Frontend build/runtime
- CI/CD pipelines
- Container build & images
- Kubernetes manifests (ingress, services, probes, RBAC, secrets)
- Cloud infrastructure (IaC, identity, networking, storage)
- Configuration & environment variables
- Dependencies and versions

## You MUST

- Enumerate plausible causes across ALL zones
- Rank them by likelihood with explanation
- Cite lightweight evidence pointers (file paths, grep hits, manifest locations)
- Explicitly call out assumptions under dispute
- Recommend which suspect(s) merit focused exam next

## You MUST NOT

- Investigate deeply
- Open large files unnecessarily
- Collapse uncertainty into a single answer
- Propose fixes

## Output

A completed **Triage Report** using the template at `../.resources/assets/TRIAGE_REPORT.md`.

## Scripts

- `evidence.sh` — Lightweight grep-based evidence pointer gathering
