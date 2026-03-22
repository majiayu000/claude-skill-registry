---
name: k8s-templates
description: Provide starter files for a Kubernetes operator dev loop, including Tilt, Kustomize dev overlays, Make targets, and a minimal Dockerfile. Use when Codex needs to create or refresh local scaffolding around a Kubebuilder-style operator.
---

# Kubernetes Operator Templates

Copy or adapt the boilerplate under `assets/` into the target repo.

## Included Files

- `assets/Makefile`
- `assets/Tiltfile`
- `assets/Dockerfile`
- `assets/config/dev/kustomization.yaml`
- `assets/config/dev/manager_dev_patch.yaml`

## Adaptation Rules

- Change image names, module paths, and package paths to match the target repo.
- Keep the dev overlay on one replica with leader election disabled.
- Keep `allow_k8s_contexts(...)` restricted to the intended local kind context.
- Adjust the `go build` package path in `Tiltfile` if the main package is not under `./cmd`.
- If the container process is not PID 1, replace the live-update restart command with whatever actually restarts the manager.

## Usage

1. Copy the template files into the target repo.
2. Copy the helper scripts from `$k8s-workflow` into the target repo or replace the Make targets with inline commands.
3. Update paths, image names, and namespace assumptions.
4. Run `$k8s-workflow` to use the templates in a full operator loop.
5. Read `references/template-notes.md` before changing the live-update behavior or overlay layout.
