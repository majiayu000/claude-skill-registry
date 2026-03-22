---
name: validate
description: Pre-commit validation suite for manifests, scripts, and configs
---
Run full validation suite on the project:

1. **YAML**: `find manifests/ -name "*.yaml" -exec yamllint -d relaxed {} +`
2. **Shell**: `find scripts/ -name "*.sh" -exec shellcheck {} +`
3. **K8s**: `find manifests/ -name "*.yaml" -exec kubectl apply --dry-run=client -f {} \;`
4. **Git**: `git diff --cached --name-only` to show what's staged
5. **Docs**: Verify CLAUDE.md exists and is under 4KB

Report pass/fail for each category. Fix issues if $ARGUMENTS contains "fix".
