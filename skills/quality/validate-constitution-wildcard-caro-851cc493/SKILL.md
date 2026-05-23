---
name: "validate-constitution"
description: "Validates code changes against the project's consolidated knowledge and configuration rules. Use on push to catch violations of agreed-upon standards like installation scripts, linking patterns, and configuration consistency."
version: "1.0.0"
allowed-tools: "Bash, Read, Grep, Glob, Task"
license: "AGPL-3.0"
---

# Constitution Validation Skill

## What This Skill Does

This skill validates code changes against the caro project's **consolidated knowledge and configuration rules** (the "constitution"). It catches violations of agreed-upon standards before they are pushed to the repository.

**Key Responsibilities:**
- Validate installation script references use the canonical format
- Check internal page linking follows conventions
- Ensure configuration consistency across the codebase
- Report violations with clear fix suggestions

## When to Use This Skill

This skill is **automatically triggered** via the PostPush hookify hook. It can also be manually invoked when:

- You want to validate changes before committing
- Reviewing a PR for constitutional compliance
- Checking if documentation follows standards

**Automatic Triggers:**
- Every `git push` operation (via hookify PostPush)

**Manual Triggers:**
- "Validate my changes against the constitution"
- "Check if these files follow our standards"
- "Run constitution validation"

## Constitutional Rules

### Rule 1: Canonical Installation Script

**The ONLY authorized installation command is:**

```bash
bash <(curl --proto '=https' --tlsv1.2 -sSfL https://setup.caro.sh)
```

**Why this specific format?**
- `bash <()` - Process substitution is more secure than pipe
- `--proto '=https'` - Enforces HTTPS-only connections
- `--tlsv1.2` - Requires TLS 1.2 minimum for security
- `-sSfL` - Silent, show errors, fail on HTTP errors, follow redirects

**FORBIDDEN patterns:**
```bash
# These are all WRONG:
curl -sSL https://caro.sh/install.sh | bash
curl https://caro.sh/install.sh | bash
curl ... | sh
wget ... | bash
```

### Rule 2: Internal Page Linking

When referencing other pages within the website, always link properly:

| When mentioning... | Link to... |
|-------------------|------------|
| installation guide, download | `/#download` |
| FAQ | `/faq` |
| telemetry, privacy | `/telemetry` |
| support | `/support` |
| roadmap | `/roadmap` |
| credits | `/credits` |

**Example Violation:**
```html
<!-- WRONG: No link -->
For other options, see our installation guide.

<!-- CORRECT: Proper link -->
For other options, see our <a href="/#download">installation guide</a>.
```

### Rule 3: Configuration Consistency

Single source of truth for all configuration:

| Configuration | Location |
|--------------|----------|
| Site config | `website/src/config/site.ts` |
| CLI version | `Cargo.toml` |
| Install URL | `https://setup.caro.sh` (only) |

**FORBIDDEN:**
- Hardcoding version numbers in content
- Multiple different install script URLs
- Duplicating config values across files

## Validation Workflow

When triggered, the skill:

1. **Identifies changed files** via `git diff` or staged changes
2. **Scans for pattern violations** using grep/regex
3. **Reports findings** with file:line, violation type, and fix
4. **Returns status** (PASS/FAIL) for hookify

## Using the Sub-Agent

For comprehensive validation, invoke the constitution-validator agent:

```
Task: constitution-validator
Prompt: "Validate the staged changes against constitutional rules. Check for:
1. Installation script violations
2. Missing internal page links
3. Configuration consistency issues

Report all violations with file paths and suggested fixes."
```

## Integration with Hookify

This skill is integrated with hookify via the `PostPush` hook. The hook:

1. Runs after `git push` is executed
2. Invokes the constitution-validator agent
3. Reports any violations found
4. Warns the developer to fix issues

**Hook Configuration** (in `.claude/settings.json`):
```json
{
  "hooks": {
    "PostPush": [{
      "hooks": [{
        "type": "command",
        "command": "./.claude/hooks/validate-constitution.sh"
      }]
    }]
  }
}
```

## Manual Validation

To manually validate before pushing:

```bash
# Check specific files
grep -rn "caro.sh/install.sh" website/

# Check for missing links
grep -rn "see our installation guide" website/ | grep -v "href="

# Full validation via agent
# Use: /skill validate-constitution
```

## Remediation Guide

### Fixing Installation Script Violations

**Find violations:**
```bash
grep -rn "curl.*caro.sh/install.sh" .
grep -rn "curl.*|.*bash" .
```

**Replace with canonical command:**
```bash
bash <(curl --proto '=https' --tlsv1.2 -sSfL https://setup.caro.sh)
```

### Fixing Missing Links

**Find violations:**
```bash
grep -rn "see our installation guide" . | grep -v "href="
grep -rn "see the FAQ" . | grep -v "href="
```

**Add proper links:**
```html
<a href="/#download">installation guide</a>
<a href="/faq">FAQ</a>
```

## Files to Validate

Priority order for validation:
1. `website/src/pages/*.astro` - User-facing content
2. `website/src/components/*.astro` - Reusable components
3. `README.md` - Project entry point
4. `docs/**/*.md` - Documentation
5. `CLAUDE.md` - AI guidance
6. `.claude/**/*.md` - Claude configuration

## Remember

- The constitution is non-negotiable
- All violations must be fixed before merge
- When in doubt, check the canonical source:
  - Install command: `website/src/components/Download.astro`
  - Site config: `website/src/config/site.ts`

---

*This skill ensures consistency across all caro project documentation and code, preventing drift from agreed-upon standards.*
