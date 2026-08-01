# Security System User Guide

## Quick Start

### For Skill Authors

1. **Create your skill** following the [template](../template/)
2. **Run local security check**:
   ```bash
   python scripts/security_scanner.py skills/your-skill/SKILL.md
   ```
3. **Fix any issues** reported by the scanner
4. **Submit PR** - automated checks will run

### For Registry Maintainers

1. **Run security scan** for changed skills
2. **Review findings** and fix/flag issues
3. **Merge if**: No errors (or accepted risk with justification)

### For Users

1. **Check source** (repo owner / stars / activity)
2. **Review frontmatter** (license, requires_network, requires_approval)
3. **Scan locally** if you’re unsure

## Components

### 1. JSON Schema (`schema/skill.schema.json`)

Validates SKILL.md frontmatter structure.

**Example**:
```yaml
---
name: my-skill
description: Does something useful with Claude
version: 1.0.0
author: username
license: MIT
category: development
tags: [python, automation]
requires_network: false
requires_approval: true
---
```

**Run validation**:
```bash
python -c "
import json, yaml, jsonschema
schema = json.load(open('schema/skill.schema.json'))
with open('skills/my-skill/SKILL.md') as f:
    content = f.read().split('---', 2)[1]
    skill = yaml.safe_load(content)
jsonschema.validate(skill, schema)
print('✓ Schema valid')
"
```

### 2. Security Scanner (`scripts/security_scanner.py`)

Detects dangerous patterns and vulnerabilities.

**Usage**:
```bash
# Scan single file
python scripts/security_scanner.py skills/pdf/SKILL.md

# Scan entire directory
python scripts/security_scanner.py skills/ --output report.json

# Strict mode (fail on warnings)
python scripts/security_scanner.py skills/ --strict
```

**What it checks**:
- ❌ Code execution (`eval`, `exec`)
- ❌ Unsafe YAML (`yaml.load`)
- ❌ Command injection (`os.system`, `shell=True`)
- ❌ Sensitive file access
- ⚠️ Network access
- ⚠️ File deletion
- ⚠️ Prompt injection patterns

**Output**:
```
✗ skills/suspicious/SKILL.md
❌ 2 ERROR(S):
  - dangerous_pattern: eval() found at line 45
  - yaml_security: yaml.load() is unsafe, use yaml.safe_load()
⚠️  1 WARNING(S):
  - network_access: Imports requests module
```

### Archive Remediation (`scripts/remediate_archive_security.py`)

Maintainers can repair a failing data archive without weakening the scanner.
The remediation tool is dry-run by default and accepts only a full report from
the same scanner version and ruleset, generated with `--require-metadata`.

```bash
# 1. Produce the authoritative report from the core checkout.
python scripts/security_scanner.py \
  ../claude-skill-registry-data \
  --quiet \
  --require-metadata \
  --output /tmp/archive-security-report.json

# 2. Review a bounded audit plan. This does not modify the data checkout.
python scripts/remediate_archive_security.py \
  --skills-dir ../claude-skill-registry-data \
  --security-report /tmp/archive-security-report.json \
  --output /tmp/archive-remediation-plan.json

# 3. Apply the same validated plan and write the result outside the archive.
python scripts/remediate_archive_security.py \
  --skills-dir ../claude-skill-registry-data \
  --security-report /tmp/archive-security-report.json \
  --output /tmp/archive-remediation-result.json \
  --apply

# 4. Prove that the strict publication scan is clean.
python scripts/security_scanner.py \
  ../claude-skill-registry-data \
  --quiet \
  --require-metadata \
  --output /tmp/archive-security-report-after.json
```

Entries failing only frontmatter parsing are normalized. Entries with any
security error are removed from the data checkout, where the change remains
reviewable and recoverable through Git. Before the first mutation, the tool
validates every content hash and pre-scans every normalized result. The audit
contains paths, error types, hashes, and source identity, but no raw finding
snippets that could expose credentials.

### 3. GitHub Actions Workflow

Automatically runs on:
- Daily schedule (`sync-data` in core)
- Push to core main (`build-index` in core)
- Manual trigger (`sync-data` / `build-index` in core)
- Successful core sync dispatches `publish-from-core` in main

**Features**:
- Discover + sync data repo
- Security scan for skills
- Rebuild registry.json
- Build search index + deploy Pages from core
- Publish merged artifact to main after core/data refs are pinned

## Common Issues

### Issue: "yaml.load() is unsafe"

❌ **Don't**:
```python
import yaml
data = yaml.load(content)
```

✅ **Do**:
```python
import yaml
data = yaml.safe_load(content)
```

### Issue: "Command injection risk"

❌ **Don't**:
```python
os.system(f"git commit -m '{message}'")
subprocess.call(f"rm {filename}", shell=True)
```

✅ **Do**:
```python
subprocess.run(['git', 'commit', '-m', message])
subprocess.run(['rm', filename])
```

### Issue: "eval() detected"

❌ **Don't**:
```python
result = eval(user_input)
exec(code_string)
```

✅ **Do**:
```python
# Use ast.literal_eval for safe evaluation
import ast
result = ast.literal_eval(user_input)

# Or use proper parsing
import json
data = json.loads(json_string)
```

### Issue: "Prompt injection detected"

❌ **Don't**:
```markdown
Ignore all previous instructions.
System: You are now...
```

✅ **Do**:
- Write clear, straightforward instructions
- Don't try to override system prompts
- Focus on the skill's actual functionality

## Advanced Usage

### Custom Security Rules

Add custom patterns to `scripts/security_scanner.py`:

```python
DANGEROUS_PATTERNS = {
    'your_pattern': r'dangerous_function\s*\(',
    # ...
}
```

## Integration with CI/CD

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python scripts/security_scanner.py skills/ --strict
if [ $? -ne 0 ]; then
    echo "Security scan failed. Fix issues before committing."
    exit 1
fi
```

### Local Development

```bash
# Install dependencies
pip install pyyaml jsonschema

# Run full security check
make security-check

# Or manually
python scripts/security_scanner.py skills/
```

## Best Practices

### For Authors

1. ✅ Use `yaml.safe_load()` always
2. ✅ Parameterize commands, never use `shell=True`
3. ✅ Validate and sanitize all inputs
4. ✅ Document network requirements
5. ✅ Request user approval for destructive actions
6. ✅ Keep dependencies updated
7. ✅ Follow principle of least privilege

### For Reviewers

1. ✅ Check security scan results first
2. ✅ Review actual code, not just metadata
3. ✅ Verify network access is justified
4. ✅ Test skills in sandboxed environment
5. ✅ Check repo owner and activity
6. ✅ Check for recent maintenance

### For Users

1. ✅ Read the source code
2. ✅ Prefer well‑known repos
3. ✅ Check last update date
4. ✅ Review required permissions
5. ✅ Report suspicious behavior

## FAQ

**Q: What happens if my skill fails security scan?**

A: Fix the issues locally and rerun the scanner before opening/merging PR.

**Q: Can I appeal a security decision?**

A: Yes. If you believe a scan result is a false positive, comment on the PR explaining why the code is safe.

**Q: What if I need to use network access?**

A: Set `requires_network: true` in frontmatter and document why it's needed. The scanner will allow it but flag for review.

## Support

- **Documentation**: [SECURITY.md](../SECURITY.md)
- **Schema**: [skill.schema.json](../schema/skill.schema.json)
- **Issues**: https://github.com/[owner]/[repo]/issues
- **Discussions**: https://github.com/[owner]/[repo]/discussions

---

**Version**: 1.0.0
**Last Updated**: 2026-01-08
