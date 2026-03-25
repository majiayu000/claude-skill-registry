---
name: dep-check
description: Check for outdated, deprecated, or vulnerable dependencies with upgrade suggestions
disable-model-invocation: true
allowed-tools: Read, Bash
---

Check all project dependencies for issues.

## Steps

1. **Detect package manager**
   - package.json → npm/yarn/pnpm
   - requirements.txt / pyproject.toml → pip
   - go.mod → Go modules
   - Cargo.toml → Cargo
   - Gemfile → Bundler

2. **Check for outdated packages**
   ```
   npm outdated 2>/dev/null
   pip list --outdated 2>/dev/null
   ```

3. **Check for vulnerabilities**
   ```
   npm audit 2>/dev/null
   pip audit 2>/dev/null
   ```

4. **Check for deprecated packages**
   - Read package.json/requirements.txt
   - Flag packages known to be deprecated or unmaintained

5. **Output report:**

   ```
   ## Dependency Report

   ### Vulnerable (fix immediately)
   | Package | Current | Issue | Fix |
   |---------|---------|-------|-----|
   | [name] | [ver] | [CVE/issue] | [upgrade to] |

   ### Outdated (major version behind)
   | Package | Current | Latest | Breaking Changes |
   |---------|---------|--------|-----------------|
   | [name] | [ver] | [ver] | [yes/no + notes] |

   ### Outdated (minor/patch)
   | Package | Current | Latest |
   |---------|---------|--------|
   | [name] | [ver] | [ver] |

   ### Healthy
   - [X] packages are up to date
   ```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
