---
name: skill-snitch
description: Security auditing for MOOLLM skills - static analysis and runtime surveillance
license: MIT
tier: 1
allowed-tools:
  - read_file
  - list_dir
related: [cursor-mirror, deep-snitch, k-lines, sister-script]
tags: [moollm, security, audit, patterns, surveillance]
---

# Skill Snitch Protocol

Skill Snitch audits MOOLLM skills for security issues through static analysis and runtime surveillance. It's **prompt-driven** - no Python code, just orchestration via LLM tool calls.

## Skill Type Detection

skill-snitch distinguishes between skill types and applies appropriate requirements:

### MOOLLM Skills (Strict Requirements)

MOOLLM skills are identified by:
- Presence of `CARD.yml` and/or `SKILL.md`
- Tags containing "moollm"
- References to other `skills/*` or `PROTOCOLS.yml`
- Use of K-lines/K-refs

**Required files:**
- `CARD.yml` - Interface, methods, tools, advertisements
- `SKILL.md` - Protocol documentation
- `README.md` - GitHub-facing documentation

### Anthropic/Generic Skills (Flexible)

Non-MOOLLM skills (Anthropic MCP skills, generic tools) have no strict file requirements:
- May use `.mdc` files (Anthropic format)
- Often standalone with no cross-references
- No CARD.yml/SKILL.md required

### Classification Output

```yaml
classification:
  type: moollm      # moollm | anthropic | generic | hybrid
  confidence: high
  missing_requirements:
    - README.md     # If MOOLLM but missing
  recommendations:
    - "Add README.md for GitHub visibility"
```

### Hybrid Skills

Skills with some MOOLLM elements but incomplete structure:
- Has CARD.yml but no SKILL.md
- References MOOLLM protocols but lacks proper structure
- Flagged for review

## Auto-Initialize / Heal

On first invocation, check for and create missing user files:

```
.moollm/skill-snitch/
├── config.yml          # User preferences
├── ignore.yml          # Patterns/paths to skip
├── trust-overrides.yml # Manual trust level overrides
├── scan-history.yml    # Log of past scans
├── last-scan.yml       # Most recent scan results
└── trust-cache.yml     # Cached trust assessments
```

### INIT Protocol

```markdown
1. Check if .moollm/skill-snitch/ exists
   - If not: mkdir -p .moollm/skill-snitch/
   
2. For each required file, check existence:
   - config.yml
   - ignore.yml  
   - trust-overrides.yml
   - scan-history.yml
   
3. Create missing files from templates (see below)

4. Report: "skill-snitch initialized" or "skill-snitch healed: created X files"
```

## File Templates

### config.yml

```yaml
# skill-snitch configuration
version: 1

startup_scan:
  enabled: false
  min_severity: medium
  
scan_defaults:
  include_examples: false
  follow_dependencies: true
  max_depth: 3
  
trust_defaults:
  unknown_skill: yellow
  no_card_yml: orange
  external_network: orange
  shell_commands: yellow
```

### ignore.yml

```yaml
# Patterns and paths to ignore during scans
version: 1

paths:
  - "skills/cursor-mirror/scripts/cursor_mirror.py"  # Contains pattern definitions
  - "**/*_test.py"
  - "**/examples/**"
  
patterns:
  - name: "pattern_definition"
    description: "Regex pattern definitions (not actual secrets)"
    match: 'AuditPattern\(|r".*\(\?i\)|PATTERN_REGISTRY'
    
  - name: "documentation_example"
    description: "Examples in docs"
    match: '```.*\n.*password.*\n.*```'
    
categories_to_skip:
  - info  # Skip INFO-level findings
```

### trust-overrides.yml

```yaml
# Manual trust level overrides
version: 1

overrides:
  # Example:
  # skills/trusted-skill/:
  #   trust: green
  #   reason: "Reviewed by Don on 2026-01-15"
  #   expires: 2026-07-15
```

### scan-history.yml

```yaml
# Scan history (append-only)
version: 1
scans: []
# Entries added automatically:
# - date: 2026-01-15T20:30:00Z
#   skill: skills/adventure/
#   findings: 3
#   trust: yellow
```

## Scan Protocol

```markdown
## SCAN Protocol

When asked to scan a skill:

1. **INIT** - Ensure .moollm/skill-snitch/ exists

2. **Load ignore list**
   - Read .moollm/skill-snitch/ignore.yml
   - Merge with skill's own .snitch-ignore if present
   
3. **Read skill metadata**
   - Read {skill_path}/CARD.yml
   - Note: tools, dependencies, methods
   
4. **Static scan**
   For each file in skill:
   - Skip if matches ignore patterns
   - Look for:
     - Shell commands (curl, wget, ssh, nc)
     - External URLs
     - Encoded content (base64, hex)
     - File access outside workspace
     - Undeclared dependencies
   
5. **Output K-REFs**
   For each finding:
   - Emit: {path}:{line} # {pattern} | {severity} - {description}
   
6. **Log scan**
   - Append to .moollm/skill-snitch/scan-history.yml
```

## Fetch-Scan Protocol (Remote URL)

```markdown
## FETCH-SCAN Protocol

Scan a skill directly from a URL without downloading or installing.

1. **Receive URL**
   - User provides any URL: GitHub repo, directory, file, blog post, README
   
2. **Resolve what it points to**
   - GitHub repo URL → list contents via GitHub API or raw.githubusercontent.com
   - GitHub directory URL → that's a skill directory, fetch its files
   - GitHub file URL → fetch and scan that single file
   - Blog post / README → read it, follow links to find skill files (CARD.yml, SKILL.md, *.py)
   - Organization / user URL → list repos, identify ones that look like skills
   
3. **Fetch skill files**
   - Fetch via raw.githubusercontent.com (no git clone, no filesystem writes)
   - Priority: CARD.yml first (sniffable interface), then SKILL.md, then scripts
   - Follow the Semantic Image Pyramid: GLANCE → CARD → SKILL → README → code
   
4. **Run scan on fetched content**
   - Apply same patterns, surfaces, analyzers as local SCAN
   - Surface type: "remote" (fetched content, not local files)
   - All pattern matching works on content strings, not file paths
   
5. **Report**
   - Trust tier assessment
   - Findings with line numbers (relative to fetched content)
   - Recommendation: CLONE / REVIEW FIRST / DO NOT INSTALL
   - Link back to source URL for manual review

6. **Nothing written to filesystem**
   - No clone, no download, no temp files
   - The skill was audited in memory
   - You decide whether to install AFTER seeing the report
```

**Usage:**
- `FETCH-SCAN https://github.com/someone/their-skill` — scan a whole skill repo
- `FETCH-SCAN https://github.com/someone/repo/tree/main/skills/cool-skill` — scan one skill directory
- `FETCH-SCAN https://github.com/someone/repo/blob/main/SKILL.md` — scan a single file
- `FETCH-SCAN https://someone.com/blog/my-new-agent-skill` — read the blog, follow links, scan what you find

In WIMP terms: drag and drop a URL onto skill-snitch. It's happy to dive in, find all the skills, and snitch on every one of them. The npm audit before npm install — except you don't even need to install to audit.

## Snitch Protocol (Runtime)

```markdown
## SNITCH Protocol

When asked to snitch on a skill's runtime behavior:

1. **Get composer ID**
   - User provides, or find most recent for this skill
   
2. **Call cursor-mirror's sister script**
   python3 skills/cursor-mirror/scripts/cursor_mirror.py deep-snitch --composer {id} --yaml
   
3. **Load skill's declared behavior**
   - From CARD.yml: tools, dependencies
   
4. **Compare declared vs actual**
   - Tools used but not declared?
   - Paths accessed outside workspace?
   - Network calls made?
   
5. **Output discrepancies**
   DECLARED: tools: [read_file, write_file]
   OBSERVED: tools: [read_file, write_file, Shell, WebSearch]
   UNDECLARED: [Shell, WebSearch]
```

## Observe Protocol (Deep Runtime)

```markdown
## OBSERVE Protocol

Full runtime observation with cursor-mirror. Requires user cooperation.

1. **User exercises the skill**
   - User must actually invoke and use the skill
   - Test various features, edge cases, inputs
   - This requires trusting the skill enough to run it

2. **Gather runtime data via cursor-mirror's sister script**
   (skill-snitch invokes these internally)
   
   python3 skills/cursor-mirror/scripts/cursor_mirror.py tools <composer> --yaml
   python3 skills/cursor-mirror/scripts/cursor_mirror.py context-sources <composer> --yaml
   python3 skills/cursor-mirror/scripts/cursor_mirror.py timeline <composer> --yaml
   python3 skills/cursor-mirror/scripts/cursor_mirror.py deep-snitch --composer <id> --yaml

3. **Analyze captured activity**
   
   Tool Analysis:
   - All tools called vs CARD.yml declared
   - Flag undeclared usage
   - Check parameters (paths, URLs, commands)
   
   File Analysis:
   - All reads/writes — within workspace?
   - Any ~/.ssh, ~/.aws, .env, credentials access?
   
   Network Analysis:
   - WebSearch, WebFetch, curl, wget?
   - Known services or suspicious endpoints?
   
   Secret Scanning:
   - API key patterns in tool results
   - Tokens, passwords in output
   - Base64-encoded sensitive data

4. **Generate runtime report**
   
   RUNTIME OBSERVATION: skills/target-skill/
   Session: <composer-id>
   
   TOOL CALLS:
   - read_file: 12 (DECLARED)
   - Shell: 2 (UNDECLARED!)
   
   FILES ACCESSED:
   - skills/target-skill/*.yml (expected)
   - ~/.ssh/config (SUSPICIOUS!)
   
   VERDICT: YELLOW - undeclared Shell usage
```

Like Little Snitch watches your network, skill-snitch watches skill behavior via cursor-mirror.

## Trust Assessment

Trust tiers:
- 🟢 **GREEN** - Verified safe, all checks pass
- 🔵 **BLUE** - Trusted source, minor warnings
- 🟡 **YELLOW** - Caution, review recommended  
- 🟠 **ORANGE** - Suspicious, manual review required
- 🔴 **RED** - Dangerous, do not use

```markdown
## TRUST Protocol

1. Run SCAN (static)
2. Run SNITCH (runtime) if composer provided
3. Check trust-overrides.yml for manual override
4. Calculate trust tier:
   
   RED if:
     - Any CRITICAL finding
     - Reverse shell pattern
     - Undeclared network + secrets access
     
   ORANGE if:
     - HIGH findings without explanation
     - Undeclared shell commands
     - No CARD.yml
     
   YELLOW if:
     - MEDIUM findings
     - Undeclared dependencies
     - External URLs
     
   BLUE if:
     - Only LOW/INFO findings
     - All tools declared
     - Known publisher
     
   GREEN if:
     - No findings
     - Consistency check passes
     - Trust override from user
     
5. Cache result in trust-cache.yml
6. Output assessment with K-REFs to concerns
```

## Consistency Check

```markdown
## CONSISTENCY Protocol

Verify all parts of skill agree:

1. **INDEX.yml ↔ CARD.yml**
   - Skill listed in skills/INDEX.yml?
   - Path correct?
   - Description matches?
   
2. **CARD.yml ↔ SKILL.md**
   - All methods documented?
   - Tools match?
   
3. **CARD.yml ↔ Implementation**
   - Declared dependencies imported?
   - Declared tools used?
   - Undeclared tools/deps?
   
4. **SKILL.md ↔ README.md**
   - Examples current?
   - No deprecated features mentioned?

Output drift findings as K-REFs.
```

## Startup Scan (Optional)

If enabled in config.yml:

```markdown
## SKILL-SCAN Advertisement

On session start:

1. Check config.yml: startup_scan.enabled
2. If enabled:
   - List all skills in skills/
   - Quick scan each (CARD.yml + *.py only)
   - Report summary:
   
   🔍 SKILL-SCAN: 12 skills scanned
   ✅ 10 clean
   ⚠️ 2 warnings:
      skills/untrusted/ - no CARD.yml
      skills/fetcher/ - undeclared network
```

## Integration with cursor-mirror

skill-snitch composes with cursor-mirror. The LLM orchestrates both skills together — you invoke skill-snitch by prompting:

```
"Snitch on skills/adventure/ in session abc123"
"Observe what skills/target-skill/ did"
```

Internally, the skill uses cursor-mirror's sister script:

```bash
# Deep audit
python3 skills/cursor-mirror/scripts/cursor_mirror.py deep-snitch --composer ID --yaml

# Pattern scan
python3 skills/cursor-mirror/scripts/cursor_mirror.py audit --patterns secrets,shell_exfil --yaml

# Tool usage
python3 skills/cursor-mirror/scripts/cursor_mirror.py tools ID --yaml
```

The skill abstracts the CLI — you don't need to remember the syntax.

## Scan Methodology

See [SCAN-METHODOLOGY.md](./SCAN-METHODOLOGY.md) for the two-phase approach:

1. **Phase 1: Bash Scripts** — Fast structural scan of ALL skills
   - Structure check (CARD.yml, SKILL.md, README.md)
   - Script detection (.py, .js files)
   - Pattern grep (exec, eval, password, etc.)
   - Tool tier extraction

2. **Phase 2: LLM Batched Review** — Deep read in batches of 5
   - Actually READ files, don't just grep
   - Scripts get full code review
   - Context determines if patterns are dangerous
   - Trust assessment per skill

**Golden Rule:** *Grep finds. LLM understands.*
