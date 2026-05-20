---
name: remediation
description: Get a context-aware remediation plan for a vulnerability with fix verification steps
argument-hint: <vuln-id>
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
model: sonnet
---

# Vulnetix Remediation Plan Skill

This skill generates a comprehensive, context-aware remediation plan for a specific vulnerability using the VDB V2 remediation API. It auto-detects your repository's ecosystem, package manager, installed versions, container images, and OS to provide targeted fix guidance including registry upgrades, source patches, distribution advisories, workarounds, CWE-specific remediation strategies, and verification commands.

**How this differs from `/vulnetix:fix`:** The existing `/vulnetix:fix` skill fetches V1 fix data and proposes manual manifest edits. This skill uses the V2 `remediation plan` endpoint which provides **context-aware** guidance (ecosystem, version, OS, container), **CWE remediation strategies**, **CrowdSec threat intelligence** (live exploitation data), **workaround effectiveness scoring**, **SSVC decision support**, and **verification commands** per package manager.

## Vulnerability Memory (.vulnetix/memory.yaml)

This skill reads and updates the `.vulnetix/memory.yaml` file in the repository root. This file is shared with `/vulnetix:fix`, `/vulnetix:exploits`, `/vulnetix:package-search`, `/vulnetix:vuln`, and `/vulnetix:exploits-search`.

### Schema

The canonical schema is defined in `/vulnetix:fix`. This skill updates base fields and appends remediation plan events to the history log.

### Reading Prior State

**At the start of every invocation:**

1. Use **Glob** to check if `.vulnetix/memory.yaml` exists in the repo root
2. If it exists, use **Read** to load it and check for the vuln ID or aliases
3. Use **Glob** for `.vulnetix/scans/*.cdx.json` -- cross-reference for component data
4. If a prior entry exists, display:
   ```
   Previously seen: <vulnId> -- <developer-friendly status> (as of <date>)
   Priority: <P1/P2/P3/P4> (<score>) (if cwss data exists)
   Last decision: <developer-friendly decision> -- "<reason>"
   ```

### Writing Updated State

**After completing the remediation plan (Step 7):**

1. If no entry exists, create one with `status: under_investigation`, `discovery.source: user`
2. If an entry exists, update `severity`, `safe_harbour`, and `versions.fixed_in` from the remediation plan data. Merge aliases.
3. **Do NOT change `status` or `decision`** unless the user explicitly makes a decision during the conversation
4. Append to `history`: `event: remediation-plan`, detail: summary of fix options found (registry fixes, source fixes, workarounds, distribution patches)
5. Confirm to the user

### VEX Status Mapping

- `not_affected` --> "Not affected"
- `affected` --> "Vulnerable"
- `fixed` --> "Fixed"
- `under_investigation` --> "Investigating"

## Dependabot Integration

When `gh` CLI is available (check with `gh auth status 2>/dev/null`), query Dependabot alerts for the vuln ID to cross-reference with the remediation plan.

1. Query alerts matching this vuln ID
2. If a Dependabot PR exists, note it in the output: `"Dependabot PR #N proposes this upgrade -- consider reviewing and merging it"`
3. Update the `dependabot` section in the memory entry

## Workflow

### Step 1: Load Memory and Detect Repository Context

1. Load `.vulnetix/memory.yaml` as described above
2. Use **Glob** to detect manifest files and determine:
   - **Ecosystem** -- npm, pypi, maven, go, cargo, rubygems, packagist
   - **Package manager** -- npm, yarn, pnpm, pip, poetry, uv, cargo, go, maven, gradle, bundler, composer
3. If the vuln ID is already in memory with a `package` field, use that package name
4. If not, run a quick lookup to get affected products:
   ```bash
   vulnetix vdb vuln "$ARGUMENTS" -o json
   ```
   Extract affected package names and ecosystems from the response.
5. For each affected package found in the repo, detect the installed version using the priority chain: lockfile --> manifest --> installed artifacts --> unknown

### Step 2: Auto-Populate Context Flags

Build the CLI flags automatically from repository state:

| Flag | Source | How to detect |
|------|--------|---------------|
| `--ecosystem` | Manifest files | From Step 1 ecosystem detection |
| `--package-name` | VDB response or memory | Affected package name matching repo |
| `--current-version` | Lockfile/manifest | Installed version from Step 1 |
| `--package-manager` | Manifest file type | `package-lock.json` --> npm, `yarn.lock` --> yarn, `poetry.lock` --> pip/poetry, etc. |
| `--purl` | Constructed | If ecosystem + name + version are known, construct `pkg:<eco>/<name>@<version>` |
| `--container-image` | Containerfile/Dockerfile | Use **Glob** for `Containerfile`, `Dockerfile`, `*.dockerfile`. If found, **Read** and extract `FROM` image reference (e.g., `node:18-alpine`) |
| `--os` | OS detection | Check for `/etc/os-release` or infer from container base image |
| `--vendor` | VDB response | From affected products vendor field |
| `--product` | VDB response | From affected products product field |

Always set:
- `--include-guidance` -- includes CWE-specific remediation strategies
- `--include-verification-steps` -- includes per-package-manager verification commands

If no package context can be determined (no manifests, no memory), run the command without package-specific flags -- the API will still return general remediation guidance.

### Step 3: Execute Remediation Plan Query

```bash
vulnetix vdb remediation plan "$ARGUMENTS" -V v2 --include-guidance --include-verification-steps -o json [context flags]
```

**CLI Reference** (from `vulnetix vdb remediation plan` docs):

| Flag | Type | Description |
|------|------|-------------|
| `--ecosystem` | string | Package ecosystem (npm, pypi, maven, go, cargo, etc.) |
| `--package-name` | string | Package name |
| `--current-version` | string | Currently installed version (enables version-specific guidance) |
| `--package-manager` | string | Package manager (npm, pip, cargo, maven, etc.) |
| `--purl` | string | Package URL (overrides ecosystem + package-name) |
| `--container-image` | string | Container image reference (e.g., node:18-alpine) |
| `--os` | string | OS identifier (e.g., ubuntu:22.04, debian-11) |
| `--vendor` | string | Vendor name for CPE matching |
| `--product` | string | Product name for CPE matching |
| `--registry` | string | Registry filter (npm, pypi, maven-central) |
| `--include-guidance` | bool | Include CWE-specific markdown guidance |
| `--include-verification-steps` | bool | Include verification commands per package manager |
| `-V` | string | API version -- must be `v2` |
| `-o, --output` | string | Output format: `json` or `pretty` |

Examples:
```bash
# Basic remediation plan
vulnetix vdb remediation plan CVE-2021-44228 -V v2 --include-guidance --include-verification-steps -o json

# With full package context
vulnetix vdb remediation plan CVE-2021-44228 -V v2 \
  --ecosystem maven --package-name log4j-core --current-version 2.14.1 \
  --package-manager maven --include-guidance --include-verification-steps -o json

# Using PURL
vulnetix vdb remediation plan CVE-2021-44228 -V v2 \
  --purl "pkg:maven/org.apache.logging.log4j/log4j-core@2.14.1" \
  --include-guidance --include-verification-steps -o json

# With container context
vulnetix vdb remediation plan CVE-2024-XXXXX -V v2 \
  --ecosystem npm --package-name express --current-version 4.17.1 \
  --container-image "node:18-alpine" --include-guidance --include-verification-steps -o json
```

**Response structure** (from V2 OAS):

The response includes:
- `cveId`, `state`, `title`, `aliases`, `description`
- `descriptions[]` -- multi-source descriptions with language and source attribution
- `crowdSecSummary` -- live threat intelligence:
  - `totalSightings`, `uniqueIPs`, `isActive`
  - `firstSeen`, `lastSeen`
  - `topSourceCountries`, `topTargetCountries`
  - `mitreTechniques`, `behaviors`
- `cvssDetails` -- parsed CVSS vector components (attackVector, attackComplexity, privilegesRequired, userInteraction, scope, impact metrics)
- `agent_prompt` -- AI-optimized remediation context string
- Registry fixes, source fixes, distribution patches, workarounds, CWE guidance, verification steps (context-dependent based on flags provided)

### Step 4: Present the Remediation Plan

Render a structured remediation report with the following sections:

**Vulnerability Summary:**
```
<CVE ID> -- <title>
<description -- first 2-3 sentences>
Severity: <CVSS score> (<level>)  |  EPSS: <score>
```

**Threat Activity** (from CrowdSec data, if present):
```
Live Exploitation: <Active/Inactive>
Sightings: <totalSightings> from <uniqueIPs> unique IPs
Last seen: <lastSeen>
Source countries: <top 3>
MITRE techniques: <techniques in developer language>
```

If no CrowdSec data, skip this section.

**Registry Fixes** (version upgrades per ecosystem):

| Ecosystem | Package | Current | Fix Version | Verified | Confidence | Registry |
|-----------|---------|---------|-------------|----------|------------|----------|
| maven | log4j-core | 2.14.1 | 2.17.1 | Yes | High | Maven Central |

For each fix, report Safe Harbour confidence:
- **High** (> 0.90): patch-level bump, official registry release
- **Reasonable** (0.35-0.90): minor version bump, backward-compatible
- **Low** (< 0.35): major version bump, significant API changes

**Source Fixes** (upstream commits/PRs, if available):

```
Upstream fix: <commit URL>
  SHA: <sha>
  Author: <author>
  Message: <commit message>
  Repository health: <commit frequency, contributor count>
```

**Distribution Patches** (if `--os` or `--container-image` was set):

| Distro | Patch ID | Affected Packages | Priority |
|--------|----------|-------------------|----------|
| Ubuntu 22.04 | USN-XXXX-X | liblog4j2-java | High |

**Workarounds** (interim mitigations, if no immediate fix):

```
Workaround: <description>
  Effectiveness: <score>/100
  Applicable versions: <range>
  Requires restart: <Yes/No>
  Verification: <steps>
```

**CWE Guidance** (weakness-specific remediation strategies):

```
CWE-<id>: <title>
Remediation strategy:
<markdown guidance from API>

Verification guidance:
<markdown from API>
```

**Verification Steps** (per package manager):

```
Verify the fix:
  npm: npm audit --json | jq '.vulnerabilities["<package>"]'
  maven: mvn dependency:tree | grep <package>
  pip: pip show <package> | grep Version
```

### Step 5: Cross-Reference with Dependabot and Memory

1. If Dependabot PR exists for this upgrade, note: `"Dependabot PR #N already proposes this upgrade -- consider reviewing and merging"`
2. If a prior `/vulnetix:exploits` analysis exists in memory (threat_model, cwss), surface the priority: `"Prior exploit analysis: P1 (87.5) -- Act now"`
3. If a prior `/vulnetix:fix` analysis exists, note what was previously proposed

### Step 6: Present Actionable Next Steps

Based on the remediation plan, present concrete actions:

1. **If registry fix available:** Show exact manifest edit (same diff format as `/vulnetix:fix`) with the fix version from the remediation plan. Offer to apply it.
2. **If source fix only (no registry release):** Note that the fix requires building from source or waiting for a release. Link to the commit/PR.
3. **If workaround only:** Present the workaround steps with effectiveness score. Note: "No patch available yet -- workaround is interim mitigation."
4. **If distribution patch:** Provide the package manager command (e.g., `apt-get update && apt-get install --only-upgrade <package>`)
5. **Test commands:** Suggest running tests after applying the fix
6. **Re-scan:** Suggest `vulnetix vdb vuln <vuln-id>` to verify the fix resolved the vulnerability
7. **Rollback guidance:** If the fix introduces breaking changes, note the backup/rollback approach

**Cross-references:**
- `"Run /vulnetix:exploits $ARGUMENTS for exploit intelligence and threat modeling"`
- `"Run /vulnetix:vuln $ARGUMENTS for full vulnerability details"`
- `"Run /vulnetix:exploits-search --ecosystem <eco> to discover related exploited vulnerabilities"`

### Step 7: Update Vulnerability Memory

1. Use **Read** to load the current memory file
2. Create or update the entry:
   - `versions.fixed_in` -- from the registry fix data
   - `versions.fix_source` -- registry name and version
   - `severity` -- from CVSS data
   - `safe_harbour` -- computed from fix confidence
   - `aliases` -- merge any newly discovered aliases
   - `dependabot` -- if gathered in Step 5
3. Append to `history`: `event: remediation-plan`, detail: summary of fix options (e.g., "Registry fix: 2.17.1 (Maven Central, High confidence). 2 workarounds available. CWE-502 guidance provided.")
4. Use **Write** to save
5. Confirm to the user

**If the user applies a fix or makes a decision:**
- Record using the risk treatment categories from `/vulnetix:exploits`
- Set `status: fixed` and `decision.choice: fix-applied` if they apply the fix
- Append `event: fix-applied` with detail including the version change

## Error Handling

- If `vulnetix vdb remediation plan` returns an error, fall back to `vulnetix vdb fixes "$ARGUMENTS" -o json` (V1 endpoint) and present basic fix data. Note that V2 enrichment (workarounds, CWE guidance, verification steps) is unavailable.
- If the vuln ID is not found, suggest checking the format and provide examples
- If no package context can be determined from the repo, run without context flags and note that guidance is generic rather than repo-specific
- If no fixes, workarounds, or patches are available, state clearly: "No remediation options are currently available for this vulnerability. Consider risk acceptance or component removal."
- If `.vulnetix/memory.yaml` cannot be written, warn but do not block

## Important Reminders

1. This skill **proposes code changes** (manifest edits) but **always asks before applying** -- same guardrail as `/vulnetix:fix`
2. **Auto-populate context flags** from the repo -- the V2 API returns better results with more context. Always detect ecosystem, package name, current version, and package manager.
3. **Container detection is important** -- if a Containerfile/Dockerfile exists, extract the base image for OS-specific distribution patches
4. Safe Harbour scores: compute from fix confidence tiers, display as 0.00-1.00
5. Version source transparency is mandatory -- always disclose how the current version was determined
6. **CrowdSec data is live threat intelligence** -- if sightings are active, flag prominently
7. The `agent_prompt` field in the response contains AI-optimized context -- use it to inform your analysis but do not display it raw to the user
8. **Always update `.vulnetix/memory.yaml`** after generating the plan
9. If Dependabot already has a PR for this fix, prefer merging that PR over manual edits
10. The V2 remediation endpoint is the most comprehensive single endpoint -- it aggregates data from registry fixes, source fixes, distribution patches, workarounds, CWE guidance, and KEV data into one response
