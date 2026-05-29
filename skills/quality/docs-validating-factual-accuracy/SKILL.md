---
description: Universal methodology for verifying factual correctness in documentation using WebSearch and WebFetch tools. Covers command syntax verification, version checking, code example validation, API correctness, confidence classification system ([Verified], [Error], [Outdated], [Unverified]), source prioritization, and update frequency rules. Essential for maintaining factual accuracy in technical documentation and educational content
---

# Factual Validation Methodology Skill

## Purpose

This Skill provides a universal methodology for verifying factual correctness in technical documentation, educational content, and code examples using WebSearch and WebFetch tools.

**When to use this Skill:**

- Verifying command syntax and flags
- Checking version numbers and compatibility
- Validating code examples compile/run correctly
- Confirming API methods and signatures
- Verifying external claims and references
- Classifying confidence levels for documentation
- Maintaining factual accuracy in tutorials

## Core Concepts

### What is Factual Validation?

**Factual validation** is the systematic process of verifying objective, verifiable claims in documentation against authoritative sources using web search and retrieval tools.

**Validates**:

- Command syntax (bash, npm, git commands)
- Software version numbers
- API method names and signatures
- Code example correctness
- Configuration file formats
- Library/package availability
- External factual claims

**Does NOT validate**:

- Subjective quality assessments
- Narrative flow or writing style
- Architectural decisions or opinions
- Future predictions or speculation

### The Four Confidence Classifications

All validation findings use one of four confidence labels:

**[Verified]** - Objectively correct according to authoritative sources

- Command syntax matches official documentation
- Version number confirmed via package registry
- Code example compiles/runs as shown
- API method exists with correct signature

**[Error]** - Objectively incorrect, breaks functionality

- Command syntax wrong (fails when executed)
- Code example won't compile/run
- API method doesn't exist or has wrong signature
- Incorrect version number that doesn't exist

**[Outdated]** - Was correct but now superseded by newer version

- References old major version with breaking changes
- Uses deprecated API (still works but replacement exists)
- Command syntax changed in recent release
- Configuration format updated

**[Unverified]** - Cannot confirm correctness (insufficient evidence)

- No authoritative source found
- Multiple conflicting sources
- Documentation ambiguous or incomplete
- Claim too specific to verify externally

## Validation Workflow

### Step-by-Step Process

**1. Identify Claims to Validate**

Extract objective, verifiable claims from content:

```markdown
Content: "Install using `npm install --save-deps prettier`"
Claim: npm flag "--save-deps" is valid syntax
Type: Command syntax
```

**2. Determine Source Priority**

Use authoritative sources in priority order:

1. **Official documentation** (docs.npmjs.com, official GitHub repos)
2. **Package registries** (npmjs.com, pypi.org, crates.io)
3. **Official release notes** (CHANGELOG, GitHub releases)
4. **Well-maintained community sources** (Stack Overflow official answers, MDN)

**3. Execute Web Search**

```
WebSearch query: "npm install flags official documentation"
Target: Find official npm CLI documentation
```

**4. Fetch Authoritative Content**

```
WebFetch: https://docs.npmjs.com/cli/v9/commands/npm-install
Extract: List of valid flags and their purposes
```

**5. Compare and Classify**

```
Claim: "--save-deps" flag
Source: Official npm docs list "--save-dev" (NOT "--save-deps")
Classification: [Error]
Confidence: HIGH (official docs contradict claim)
```

**6. Document Finding**

```markdown
**File**: `docs/tutorials/tu__quick-start.md:42`
**Verification**: [Error] - Command syntax incorrect
**Criticality**: CRITICAL - Breaks user quick start experience
**Category**: Factual Error - Command Syntax

**Finding**: Installation command uses incorrect npm flag `--save-deps` (should be `--save-dev`)

**Impact**: Users following tutorial get command error, cannot complete setup

**Recommendation**: Change `npm install --save-deps prettier` to `npm install --save-dev prettier`

**Verification Source**:
Official npm documentation confirms `--save-dev` is correct flag
https://docs.npmjs.com/cli/v9/commands/npm-install

**Confidence**: HIGH
```

## Source Prioritization

### Tier 1: Official Documentation (Highest Authority)

**Examples**:

- Official language documentation (docs.python.org, docs.oracle.com/javase)
- Official package documentation (npmjs.com package pages, PyPI)
- Official CLI references (git-scm.com, docs.npmjs.com)
- Official API documentation (developer.mozilla.org, official SDK docs)

**Characteristics**:

- Maintained by project creators
- Canonical source of truth
- Version-specific
- Updated with releases

**When to use**: For syntax, commands, API signatures, version numbers

### Tier 2: Package Registries (Version Truth)

**Examples**:

- npmjs.com (JavaScript/Node.js packages)
- pypi.org (Python packages)
- crates.io (Rust crates)
- rubygems.org (Ruby gems)
- maven.org (Java packages)

**Characteristics**:

- Authoritative version numbers
- Availability confirmation
- Dependency information
- Release dates

**When to use**: For version verification, package availability, dependency checks

### Tier 3: Official Release Notes (Change Truth)

**Examples**:

- GitHub Releases pages
- CHANGELOG.md files in official repos
- Official blog announcements
- Migration guides

**Characteristics**:

- Documents changes between versions
- Breaking change identification
- Deprecation notices
- Migration paths

**When to use**: For outdated content detection, breaking change verification

### Tier 4: Well-Maintained Community (Supplementary)

**Examples**:

- Stack Overflow accepted answers (with high votes)
- MDN Web Docs (Mozilla Developer Network)
- Official tutorial sites (RustByExample, GoByExample)

**Characteristics**:

- Community-verified
- Practical examples
- Context-dependent correctness
- May lag behind latest versions

**When to use**: For practical patterns, edge cases, when official docs insufficient

## Common Validation Patterns

### Pattern 1: Command Syntax Validation

**Claim Type**: Bash/shell command syntax

**Validation Steps**:

1. Extract command and flags from content
2. WebSearch: "[command-name] official documentation"
3. WebFetch: Official CLI reference page
4. Compare: Flags, argument order, option names
5. Classify: [Verified] if exact match, [Error] if wrong

**Example**:

```
Content: "git commit -am 'message'"
WebSearch: "git commit flags official documentation"
WebFetch: https://git-scm.com/docs/git-commit
Verify: -a flag exists, -m flag exists, combined -am valid
Result: [Verified]
```

### Pattern 2: Version Number Validation

**Claim Type**: Software/package version reference

**Validation Steps**:

1. Extract package name and version number
2. WebSearch: "[package-name] [version] release"
3. WebFetch: Package registry page (npmjs.com, pypi.org)
4. Compare: Version exists in registry
5. Check: Latest version, deprecation status
6. Classify: [Verified], [Outdated], or [Error]

**Example**:

```
Content: "Install React 17.0.2"
WebSearch: "react 17.0.2 npmjs"
WebFetch: https://www.npmjs.com/package/react
Verify: 17.0.2 exists in version list
Check: Latest is 18.2.0 (major version ahead)
Result: [Outdated] - Breaking changes exist in v18
```

### Pattern 3: Code Example Validation

**Claim Type**: Code snippet correctness

**Validation Steps**:

1. Extract code example from content
2. Identify language and version
3. WebSearch: "[language] [concept] official examples"
4. WebFetch: Official documentation or tutorial
5. Compare: Syntax, method signatures, patterns
6. If possible: Run code locally to verify execution
7. Classify: [Verified], [Error], or [Outdated]

**Example**:

````
Content:
```python
import asyncio
async def main():
    await asyncio.sleep(1)
asyncio.run(main())
```

WebSearch: "python asyncio.run documentation"
WebFetch: https://docs.python.org/3/library/asyncio-task.html
Verify: asyncio.run() syntax correct, requires Python 3.7+
Check: No syntax errors, runnable code
Result: [Verified]
````

### Pattern 4: API Method Validation

**Claim Type**: API method existence and signature

**Validation Steps**:

1. Extract API method name, parameters, return type
2. WebSearch: "[library] [method] official api documentation"
3. WebFetch: Official API reference
4. Compare: Method name, parameter types, return type
5. Check: Deprecation status
6. Classify: [Verified], [Error], or [Outdated]

**Example**:

```
Content: "Use fs.readFileSync(path, 'utf-8')"
WebSearch: "node.js fs.readFileSync official documentation"
WebFetch: https://nodejs.org/api/fs.html#fsreadfilesyncpath-options
Verify: Method exists, parameters match (path, options)
Check: 'utf-8' encoding valid
Result: [Verified]
```

## Update Frequency Rules

### When to Re-validate Content

**MANDATORY re-validation triggers**:

- **6 months since last validation** - Standard refresh cycle
- **Major version release** of referenced software/library
- **Breaking change announced** in official release notes
- **User reports error** in documentation
- **Deprecation notice** for used API/method

**OPTIONAL re-validation triggers**:

- Minor version updates (if content specific to that version)
- Patch releases (usually safe to skip)
- Community feedback about potential issues
- Regular documentation review cycles

### Validation Metadata Storage

**Location**: `docs/metadata/external-links-status.yaml`

**Format**:

```yaml
factual-validations:
  - file: "docs/tutorials/tu__quick-start.md"
    claim: "npm install --save-dev prettier"
    verification-status: "[Verified]"
    last-checked: "2025-12-27T10:00:00+07:00"
    source: "https://docs.npmjs.com/cli/v9/commands/npm-install"
    expires: "2026-06-27T10:00:00+07:00" # 6 months later
```

## Integration with Checker Agents

### Dual-Label Pattern

Factual validation findings require BOTH verification label AND criticality level:

```markdown
### 1. [Error] - Command Syntax Incorrect in Installation Guide

**File**: `docs/tutorials/tu__quick-start.md:42`
**Verification**: [Error] - Command syntax verified incorrect via WebSearch
**Criticality**: CRITICAL - Breaks user quick start experience
**Category**: Factual Error - Command Syntax

**Finding**: [description]
**Impact**: [consequences]
**Recommendation**: [fix]
**Verification Source**: [URL]
**Confidence**: HIGH
```

**Why dual labels?**

- **Verification** ([Verified]/[Error]/[Outdated]/[Unverified]) describes FACTUAL STATE
- **Criticality** (CRITICAL/HIGH/MEDIUM/LOW) describes URGENCY/IMPORTANCE

Both dimensions provide complementary information.

### Confidence Assessment

**HIGH confidence** when:

- Official documentation clearly contradicts claim
- Package registry shows version doesn't exist
- Code example fails to compile (verified locally)
- Multiple authoritative sources agree

**MEDIUM confidence** when:

- Sources partially contradict (some say yes, some say no)
- Claim is version-specific but version unclear
- Documentation ambiguous or incomplete
- Cannot find definitive authoritative source

### Factual Validation Agents

Three agents implement this methodology:

- **docs\_\_checker** - Validates documentation factual accuracy
- **docs\_\_tutorial-checker** - Validates tutorial factual accuracy
- **apps\_\_ayokoding-web\_\_facts-checker** - Validates ayokoding-web factual accuracy

All use same validation workflow and confidence classification.

## Common Mistakes

### ❌ Mistake 1: Using outdated sources

**Wrong**: Citing 5-year-old blog post for current syntax

**Right**: Check official documentation for latest version

### ❌ Mistake 2: Missing version context

**Wrong**: "React hooks were introduced recently"

**Right**: "React hooks were introduced in React 16.8 (February 2019)"

### ❌ Mistake 3: Trusting unofficial sources

**Wrong**: Using random Stack Overflow answer as sole source

**Right**: Verify with official docs, use SO for supplementary context

### ❌ Mistake 4: Not documenting verification source

**Wrong**: Marking [Verified] without citing source

**Right**: Always include verification source URL in finding

### ❌ Mistake 5: Conflating verification with subjective quality

**Wrong**: [Error] for "code style not following best practices"

**Right**: Use [Error] only for objective incorrectness (won't compile, wrong syntax)

## Best Practices

### Validation Checklist

Before marking content as validated:

- [ ] Identified all objective, verifiable claims
- [ ] Used authoritative sources (official docs, registries)
- [ ] Documented verification source URLs
- [ ] Applied correct confidence classification
- [ ] Recorded validation date and expiry
- [ ] Classified criticality level
- [ ] Provided clear remediation steps for errors

### Batch Validation Workflow

1. **Extract claims**: Scan content for all verifiable claims
2. **Group by type**: Commands, versions, code examples, APIs
3. **Prioritize**: Critical paths first (install commands, quick starts)
4. **Validate systematically**: One claim type at a time
5. **Document findings**: Use standardized format
6. **Update metadata**: Record validation dates and sources

### Tool Usage Pattern

```
Step 1: WebSearch to find authoritative source
  Query: "npm install flags official documentation"
  Result: Multiple sources, identify official docs

Step 2: WebFetch to retrieve content
  URL: https://docs.npmjs.com/cli/v9/commands/npm-install
  Extract: Flag list, examples, usage patterns

Step 3: Compare and classify
  Claim vs Source → Determine classification
  Document finding with source citation
```

## Reference Documentation

**Primary Convention**: [Factual Validation Convention](../../../../governance/conventions/content/factual-validation.md)

**Related Conventions**:

- [Content Quality Principles](../../../../governance/conventions/content/quality.md) - Universal content standards
- [Criticality Levels](../../../../governance/development/quality/criticality-levels.md) - Severity classification system
- [Timestamp Format](../../../../governance/conventions/formatting/timestamp.md) - Validation metadata timestamps

**Related Skills**:

- `criticality-confidence-system` - Understanding dual-label system and priority matrix

**Related Agents**:

- `docs__checker` - Documentation factual validation
- `docs__tutorial-checker` - Tutorial factual validation
- `apps__ayokoding-web__facts-checker` - ayokoding-web factual validation

---

This Skill packages critical factual validation methodology for maintaining accuracy in technical documentation. For comprehensive details, consult the primary convention document.

## References

**Primary Convention**: [Factual Validation Convention](../../../../governance/conventions/content/factual-validation.md)

**Related Conventions**:

- [Content Quality Principles](../../../../governance/conventions/content/quality.md) - Universal content standards
- [Criticality Levels](../../../../governance/development/quality/criticality-levels.md) - Severity classification
- [Timestamp Format](../../../../governance/conventions/formatting/timestamp.md) - Validation metadata timestamps

**Related Skills**:

- `wow__assessing-criticality-confidence` - Understanding dual-label system and priority matrix
