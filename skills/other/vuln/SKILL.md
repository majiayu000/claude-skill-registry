---
name: vuln
description: Look up a vulnerability by ID or list all vulnerabilities for a package
argument-hint: <vuln-id or package-name>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
---

# Vulnetix Vulnerability Lookup Skill

This skill serves two purposes based on the argument provided:

- **Vuln ID argument** (CVE-*, GHSA-*, PYSEC-*, etc.) --> retrieves detailed vulnerability intelligence and assesses its impact against the current repository
- **Package name argument** (express, lodash, log4j-core, etc.) --> lists all known vulnerabilities for that package and identifies which ones affect your installed version

**This skill does not modify application code** -- it only updates `.vulnetix/memory.yaml` to track findings. Use `/vulnetix:fix` for remediation, `/vulnetix:exploits` for exploit analysis, or `/vulnetix:remediation` for a context-aware remediation plan.

## Argument Detection

Determine the mode from the argument:

**Vuln lookup mode** -- argument matches any known vulnerability identifier pattern:
- `CVE-*` (e.g., CVE-2021-44228)
- `GHSA-*` (e.g., GHSA-jfh8-3a1q-hjz9)
- `PYSEC-*`, `GO-*`, `RUSTSEC-*`, `EUVD-*`, `OSV-*`, `GSD-*`, `VDB-*`, `GCVE-*`
- `SNYK-*`, `ZDI-*`, `MSCVE-*`, `MSRC-*`, `RHSA-*`, `TALOS-*`, `EDB-*`
- `WORDFENCE-*`, `PATCHSTACK-*`, `MFSA*`, `JVNDB-*`, `CNVD-*`, `BDU:*`, `HUNTR-*`
- `DSA-*`, `DLA-*`, `USN-*`, `ALSA-*`, `RLSA-*`, `MGASA-*`, `OPENSUSE-*`, `FreeBSD-*`, `BIT-*`

The VDB accepts **78+ identifier formats** in total.

**Package vulns mode** -- argument does not match any vuln-id pattern. Treat it as a package name.

If ambiguous, prefer vuln lookup mode (vuln IDs are more structured). If the vuln lookup returns an error or empty response, fall back to package vulns mode automatically.

## Vulnerability Memory (.vulnetix/memory.yaml)

This skill reads and updates the `.vulnetix/memory.yaml` file in the repository root. This file is shared with `/vulnetix:fix`, `/vulnetix:exploits`, `/vulnetix:package-search`, `/vulnetix:exploits-search`, and `/vulnetix:remediation`.

### Schema

The canonical schema is defined in `/vulnetix:fix`. This skill creates or updates base vulnerability fields: `aliases`, `package`, `ecosystem`, `discovery`, `versions`, `severity`, `safe_harbour`, and `status`. It does not modify `threat_model` or `cwss` (owned by `/vulnetix:exploits`).

### Reading Prior State and SBOMs

**At the start of every invocation:**

1. Use **Glob** to check if `.vulnetix/memory.yaml` exists in the repo root
2. If it exists, use **Read** to load it
3. Use **Glob** for `.vulnetix/scans/*.cdx.json` -- if CycloneDX SBOMs exist from prior scans, cross-reference for additional context
4. **Vuln lookup mode**: check for the vuln ID or any aliases in memory. If found:
   ```
   Previously seen: <vulnId> -- <developer-friendly status> (as of <date>)
   Priority: <P1/P2/P3/P4> (<score>) -- "<priority description>" (if cwss data exists)
   Last decision: <developer-friendly decision> -- "<reason>"
   Dependabot: <alert state, PR state if available>
   ```
5. **Package vulns mode**: find all entries referencing the queried package name. If found:
   ```
   Known history for <package>:
   - CVE-2021-44228 -- Fixed (2024-01-15), P1 (87.5)
   - CVE-2023-1234 -- Investigating (2024-03-01)
   ```

### Writing Updated State

**Vuln lookup mode (after Step L6):**

1. If no entry exists, create one with `status: under_investigation`, `decision.choice: investigating`, `discovery.source: user`
2. If an entry exists, merge aliases, update `severity` and `safe_harbour` if newer. **Do NOT change `status` or `decision`.**
3. Append to `history`: `event: lookup`

**Package vulns mode (after Step P7):**

For each vulnerability that **affects the installed version** and is **not already tracked**:
1. Create a minimal stub entry with `status: under_investigation`, `decision.choice: investigating`, `discovery.source: scan`, `decision.reason: "Discovered via /vulnetix:vuln <package>"`
2. Append to `history`: `event: discovered`

For existing entries, do **not** change `status` or `decision` -- only update `severity` if newer.

### VEX Status Mapping

Use developer-friendly language when surfacing status:
- `not_affected` --> "Not affected"
- `affected` --> "Vulnerable"
- `fixed` --> "Fixed"
- `under_investigation` --> "Investigating"

## Dependabot Integration

When `gh` CLI is available (check with `gh auth status 2>/dev/null`), query Dependabot alerts to enrich the output.

**Vuln lookup mode:** Query alerts matching the vuln ID:
```bash
gh api repos/{owner}/{repo}/dependabot/alerts --jq '[.[] | select(.security_advisory.cve_id == "'"$ARGUMENTS"'" or .security_advisory.ghsa_id == "'"$ARGUMENTS"'")] | first'
```

**Package vulns mode:** Query alerts for the package:
```bash
gh api repos/{owner}/{repo}/dependabot/alerts?state=open --jq '[.[] | select(.dependency.package.name == "'"$PACKAGE_NAME"'")] | length'
```

---

## Vuln Lookup Mode Workflow

Use this workflow when the argument matches a vulnerability identifier pattern.

### Step L1: Load Vulnerability Memory

Check for and load `.vulnetix/memory.yaml` as described in "Reading Prior State" above. Display any prior state before proceeding.

### Step L2: Fetch Vulnerability Data

```bash
vulnetix vdb vuln "$ARGUMENTS" -o json
```

**CLI Reference** (from `vulnetix vdb vuln` docs):
- Accepts any of the 78+ identifier formats
- `-o json` returns machine-readable output
- Response includes: identifier and aliases, description, published/modified dates, CVSS scores (v2, v3, v4), references/advisories, affected products/versions, EPSS probability, KEV status

Extract: identity, aliases, description, dates, CVSS vectors/scores, EPSS, KEV status/deadline, CWE IDs, affected products with version ranges and fixed versions, reference URLs.

### Step L3: Enrich with Metrics

```bash
vulnetix vdb metrics "$ARGUMENTS" -o json
```

**CLI Reference** (from `vulnetix vdb metrics` docs):
- Returns structured metric objects by type (CVSS v2, v3.1, v4, EPSS, etc.)
- Each metric includes: source, type, score, vector string, timestamp

Merge with Step L2 data. If this call fails, continue with Step L2 data alone.

### Step L4: Analyze Repository Impact

Use **Glob** and **Grep** to assess repo impact:

1. **Detect manifest files:**
   - `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` --> **npm**
   - `go.mod`, `go.sum` --> **go**
   - `Cargo.toml`, `Cargo.lock` --> **cargo**
   - `requirements.txt`, `pyproject.toml`, `Pipfile`, `poetry.lock`, `uv.lock` --> **pypi**
   - `Gemfile`, `Gemfile.lock` --> **rubygems**
   - `pom.xml`, `build.gradle`, `gradle.lockfile` --> **maven**
   - `composer.json`, `composer.lock` --> **packagist**

2. **Search for affected packages** from VDB response using **Grep** in manifests/lockfiles
3. **Determine installed version** (lockfile --> manifest --> installed artifacts --> unknown). Report source transparently.
4. **Assess dependency relationship** -- direct vs transitive, whether installed version is in vulnerable range
5. **Cross-reference CycloneDX SBOMs** in `.vulnetix/scans/*.cdx.json`

### Step L5: Present Structured Summary

**Identity:**
```
<Vuln ID> (<alias1>, <alias2>, ...)
<Description -- first 2-3 sentences>
Published: <date>  |  Modified: <date>
```

**Severity Table:**

| Metric | Score | Vector |
|--------|-------|--------|
| CVSS v3.1 | 10.0 (Critical) | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H |
| CVSS v4.0 | 10.0 (Critical) | ... |
| EPSS | 0.97 (97% chance of exploitation within 30 days) | -- |
| CISA KEV | Listed (deadline: YYYY-MM-DD) | -- |

**Affected Packages:**

| Package | Ecosystem | Vulnerable Range | Fixed In |
|---------|-----------|-----------------|----------|
| log4j-core | maven | < 2.17.1 | 2.17.1 |

**Repository Impact:**

| Package | Installed Version | Source | Affected? | Relationship |
|---------|------------------|--------|-----------|-------------|
| log4j-core | 2.14.1 | lockfile: pom.xml | Yes (in range) | Direct |

If no affected packages found: **"No affected packages detected in this repository."**

**References:** List top advisory and reference URLs.

**Next Steps:**
- "Run `/vulnetix:exploits $ARGUMENTS` for exploit intelligence and threat modeling"
- "Run `/vulnetix:fix $ARGUMENTS` for fix intelligence and manifest edits"
- "Run `/vulnetix:remediation $ARGUMENTS` for a context-aware remediation plan"
- "Run `/vulnetix:exploits-search --ecosystem <eco>` to discover related exploited vulnerabilities"

### Step L6: Update Vulnerability Memory

Update `.vulnetix/memory.yaml` as described in "Writing Updated State" above. If the user provides a decision during the conversation, record it using the risk treatment categories defined in `/vulnetix:exploits`.

---

## Package Vulns Mode Workflow

Use this workflow when the argument does not match a vulnerability identifier pattern.

### Step P1: Load Vulnerability Memory

Check for and load `.vulnetix/memory.yaml`. Display any known history for the queried package before proceeding.

### Step P2: Detect Repository Ecosystems

Use **Glob** to identify manifest files (same manifest list as Step L4 above). Determine which ecosystems the repository uses.

### Step P3: Detect Installed Version

Determine if the queried package is installed. Resolve using the priority chain:

1. **User-supplied version** -- explicitly stated in the user's message
2. **Lockfile** -- most authoritative:
   - **npm**: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **pypi**: `poetry.lock`, `Pipfile.lock`, `uv.lock`
   - **go**: `go.sum`
   - **cargo**: `Cargo.lock`
   - **rubygems**: `Gemfile.lock`
   - **maven**: `gradle.lockfile`
   - **packagist**: `composer.lock`
3. **Manifest file** -- declared version constraint (less precise)
4. **Installed artifacts** -- query installed state (e.g., `node_modules/<pkg>/package.json`, `pip show <pkg>`)

If not installed: **"Not currently installed -- no existing version detected."**

**Version Source Label**: `4.17.1 (from lockfile: package-lock.json)`, `^4.17.0 (from manifest: package.json -- constraint, not exact)`, `Not installed`

### Step P4: Fetch Package Vulnerabilities

```bash
vulnetix vdb vulns "$ARGUMENTS" -o json
```

**CLI Reference** (from `vulnetix vdb vulns` docs):
- Retrieves all known vulnerabilities for a specific package
- **Flags:**
  - `--limit int` -- Maximum results (default 100)
  - `--offset int` -- Results to skip for pagination (default 0)
  - `-o, --output string` -- Output format: `json` or `pretty` (default "pretty")
- **Response includes:** total count, vulnerability identifiers, severity, CVSS, affected version ranges, fixed versions, descriptions, references, pagination info

**Pagination modifiers** -- parse user message:
- "first 20" / "top 20" / "limit 20" --> `--limit 20`
- "next page" / "more" / "page 2" --> `--offset <previous_offset + limit>`
- "all" --> `--limit 500`

### Step P5: Filter and Enrich

1. **Filter by repo ecosystems** -- discard vulns from ecosystems not in the repo
2. **Cross-reference with memory** -- note prior status, decision, CWSS priority, PoC count for each
3. **Determine "Affects You?"** -- compare installed version against each vuln's affected range:
   - **Yes** -- installed version in vulnerable range
   - **No** -- installed version outside range
   - **Unknown** -- version undetermined or range data incomplete

### Step P6: Present Vulnerability List

```
Vulnerabilities for <package>@<version> (<version source>)
Total: N known vulnerabilities (M affect your version)

| # | ID              | Severity | Affects You? | Fixed In | Status       | EPSS  |
|---|-----------------|----------|-------------|----------|--------------|-------|
| 1 | CVE-2024-XXXXX  | critical | Yes         | 4.18.3   | --           | 0.45  |
| 2 | CVE-2023-YYYYY  | high     | Yes         | 4.17.3   | Fixed        | 0.12  |
| 3 | CVE-2022-ZZZZZ  | medium   | No (>=4.17) | 4.17.0   | --           | 0.03  |
```

**Summary:** `M of N affect your version -- X critical, Y high, Z medium`

**Pagination info** (if truncated): `Showing 1-20 of 47. Say "next page" or "page 3" for more.`

**Actionable recommendations:**
- Critical/high affecting installed version: `"Run /vulnetix:fix <vuln-id> to remediate"` or `"Run /vulnetix:remediation <vuln-id> for a context-aware remediation plan"`
- Vulns with exploit signals: `"Run /vulnetix:exploits <vuln-id> for exploit analysis"`
- Any vuln: `"Run /vulnetix:vuln <vuln-id> for detailed vulnerability info"`
- Broad discovery: `"Run /vulnetix:exploits-search --ecosystem <eco> to find exploited vulnerabilities in your ecosystem"`

### Step P7: Update Vulnerability Memory

Update `.vulnetix/memory.yaml` as described in "Writing Updated State" above. Only create stub entries for vulns that **affect the installed version** to prevent memory file bloat.

---

## Error Handling

**Vuln lookup mode:**
- If `vdb vuln` returns error/empty, try falling back to package vulns mode (the argument might be a package name)
- If `vdb metrics` fails, continue with `vdb vuln` data alone
- If no manifest files found, note repo impact analysis is inconclusive
- If vuln ID not found, suggest alternative formats (GHSA if CVE fails, etc.)

**Package vulns mode:**
- If `vdb vulns` returns error, suggest checking `vulnetix vdb status`
- If no vulns found: "No known vulnerabilities found for <package>. This doesn't guarantee safety -- the package may not be indexed yet."
- If package not found in repo ecosystems, suggest `/vulnetix:package-search`
- If manifest files missing, "Affects You?" shows "Unknown"

**Both modes:**
- If `.vulnetix/memory.yaml` cannot be written, warn but do not block

## Important Reminders

1. This skill **does not modify application code** -- use `/vulnetix:fix` or `/vulnetix:remediation` for that
2. This skill **does not fetch or analyze exploits** -- use `/vulnetix:exploits` for single-vuln analysis or `/vulnetix:exploits-search` for broad discovery
3. EPSS display: "X% chance of exploitation within 30 days" in vuln mode, decimal (0.45) in table columns
4. Safe Harbour scores: convert API integer (0-100) to decimal (0.00-1.00)
5. **Always update `.vulnetix/memory.yaml`** after the lookup
6. Version source transparency is mandatory
7. Prior data serves as baseline on re-invocation -- update, don't restart
