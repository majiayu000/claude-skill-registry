---
name: supply-chain-attack-recon
description: External recon for software supply-chain attack surface — package-namespace squatting candidates, dependency-confusion vulnerabilities, GitHub Actions injection openings, container image registry exposure, SBOM mining, internal-package-name leakage, and CI/CD configuration exposure. Reconnaissance and identification ONLY — actual package publishing / typosquat attacks are EXTERNAL-OFFENSIVE and require explicit written sign-off because they can affect the entire npm/PyPI ecosystem. Use when the target has a public GitHub org, when their build artifacts/SBOMs are reachable, when their docker images are on Docker Hub/GHCR, or when you find internal package names in their JS bundles.
sources: alex-birsan-dependency-confusion, supply-chain-research, github-actions-security
report_count: 0
---

## When to use

Trigger when:
- Target has a public GitHub organization (find via OSINT)
- JS bundles reference internal-looking package names (`@target-internal/...`, `target-utils`, `target-shared`)
- Build logs, SBOMs, or `package-lock.json` files are publicly accessible
- Target uses CI/CD that's partially public (GitHub Actions, GitLab CI, Bitrise)
- Docker images on Docker Hub/GHCR/Quay belong to target org
- Findings include `npmrc`/`pip.conf`/`gradle.properties` with internal registry URLs
- `.github/workflows/*.yml` files reference internal tooling

Do NOT use for:
- Internal-network artifact registries (out of scope per external boundary)
- Actually publishing typosquats / dep-confusion packages without explicit OK
- Compromising upstream open-source projects (massive blast radius — illegal in most jurisdictions without authorization)

---

## The supply-chain attack surface map

```
Target Org
├── Public GitHub Org → workflow files → secrets exfil opportunities
├── Internal package names in JS/Android bundles → dependency confusion
├── Docker images on public registries → secrets in layers, RCE on pull
├── SBOM / artifact metadata → exact dep versions for known-vuln chaining
├── npmrc / pip.conf in repos → internal registry URL disclosure
├── External package dependencies → typosquat name candidates
└── Build/release pipelines → injection if pull_request_target etc.
```

---

## Step 1 — GitHub org discovery

```bash
TARGET="<brand>"  # set to target brand name

# Direct guesses
for guess in $TARGET "${TARGET}-tech" "${TARGET}corp" "${TARGET}-io" "${TARGET}-eng"; do
  curl -sI "https://github.com/$guess" | grep -E "HTTP|status" | head -1
done

# Via WHOIS / email-domain → GitHub search
gh search users --owner-affiliations=organization --query "$TARGET" --limit 10

# Via employees → reverse from social media + GitHub profile
# Many employees list their employer org on their GitHub profile
```

---

## Step 2 — Enumerate public repos for sensitive artifacts

```bash
ORG="targetorg"

# List public repos
gh repo list "$ORG" --limit 100 --json name,description,visibility,defaultBranchRef

# Look for high-signal repo names
gh repo list "$ORG" --limit 100 --json name | jq -r '.[].name' | grep -iE "internal|infra|deploy|config|secret|setup|sdk|api"

# Clone all (small org) or selectively
gh repo clone "$ORG/$repo_name"
```

---

## Step 3 — Internal package-name discovery

### From JS bundles

```bash
# JS bundles are the easiest source of internal npm names
curl -sk https://target.com/main.js | grep -oE '@[a-z-]+/[a-z-]+' | sort -u
curl -sk https://target.com/main.js | grep -oE 'require\("[^"]+"\)' | sort -u

# Look for scoped names that are NOT public on npm
for pkg in @target/utils @target-internal/api @companybrand/sdk; do
  status=$(curl -sI "https://registry.npmjs.org/$pkg" | head -1 | awk '{print $2}')
  echo "  $pkg → $status"
  # 404 → name unclaimed on public npm → DEPENDENCY-CONFUSION CANDIDATE
done
```

### From GitHub repo package.json files

```bash
# Public repos with package.json that reference internal scopes
for repo in $(gh repo list "$ORG" --limit 50 --json name --jq '.[].name'); do
  pkg=$(gh api "repos/$ORG/$repo/contents/package.json" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null)
  echo "$pkg" | jq -r '.dependencies // {} | keys[]' 2>/dev/null | grep -E '^@[a-z-]+/'
done | sort -u
```

### From Python projects

```bash
# Internal pip package names
for repo in $(gh repo list "$ORG" --limit 50 --json name --jq '.[].name'); do
  gh api "repos/$ORG/$repo/contents/requirements.txt" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null
done | sort -u | grep -vE '^(requests|django|flask|numpy|pandas|...common)'
```

---

## Step 4 — Dependency-confusion vulnerability check

For each internal-looking package name discovered:

```bash
NAME="@target-internal/utils"   # example

# npm check
curl -sI "https://registry.npmjs.org/$NAME" | head -1
# 404 → name is registerable → DEPENDENCY-CONFUSION POSSIBLE

# pypi check (no scopes, just name)
NAME="target_utils"
curl -sI "https://pypi.org/project/$NAME/" | head -1
# 404 → name is registerable

# rubygems
curl -sI "https://rubygems.org/api/v1/gems/$NAME.json" | head -1

# Go modules — slightly different, since module names are URLs
# Check if module path is reachable
curl -sI "https://proxy.golang.org/github.com/$ORG/$NAME/@latest" | head -1
```

**Severity calibration:** Just because a name is unclaimed doesn't mean it's exploitable. You also need:
1. Evidence the target's BUILD SYSTEM resolves names from public registries (not just their internal one)
2. OR evidence the target's package manager is configured insecurely (e.g., `.npmrc` without `@scope:registry=` mapping)
3. OR the package would be installed by their builds (it's actually in package.json, not just referenced in dead code)

A 404 on registry without supporting context is INFORMATIONAL only.

---

## Step 5 — Typosquat candidates (around external dependencies)

For each external public dependency the target uses:

```bash
# Common typosquat patterns:
# Original: "react-router-dom"
# Typos: 
#   "react-router-doms" (extra s)
#   "react-routter-dom" (double t)
#   "react-rotuer-dom" (transposed)
#   "react--router-dom" (double dash)
#   "react-router-dorn" (m→rn)
#   "reactrouterdom" (no dashes)

# Generate candidates
python3 -c "
import sys
name='react-router-dom'
for i in range(len(name)):
    print(name[:i] + name[i+1:])   # delete
    if i < len(name)-1:
        print(name[:i] + name[i+1] + name[i] + name[i+2:])  # transpose
"

# Check which candidates are UNCLAIMED on the registry
for candidate in ...; do
  status=$(curl -sI "https://registry.npmjs.org/$candidate" | head -1 | awk '{print $2}')
  [ "$status" = "404" ] && echo "  UNCLAIMED: $candidate"
done
```

**⚠ EXTERNAL-OFFENSIVE NOTE:** publishing a typosquat package to a public registry is an attack on the wider ecosystem. NEVER do this without explicit, written, scope-clarified sign-off. It can affect users outside your engagement and may be illegal.

---

## Step 6 — GitHub Actions workflow injection scan

For each public repo with `.github/workflows/`:

```bash
for repo in $(gh repo list "$ORG" --limit 50 --json name --jq '.[].name'); do
  workflows=$(gh api "repos/$ORG/$repo/contents/.github/workflows" --jq '.[].name' 2>/dev/null)
  for wf in $workflows; do
    content=$(gh api "repos/$ORG/$repo/contents/.github/workflows/$wf" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null)
    echo "=== $repo/$wf ==="
    
    # High-risk patterns:
    # 1. pull_request_target (runs with secrets on PR from forks)
    echo "$content" | grep -E 'pull_request_target'
    
    # 2. Untrusted context interpolation
    echo "$content" | grep -E '\$\{\{[^}]*github\.(event|head_ref|pull_request)[^}]*\}\}'
    
    # 3. ${{ github.event.* }} into shell run blocks
    echo "$content" | grep -B1 -A2 'run:' | grep -E '\$\{\{ ?github\.event\.'
    
    # 4. checkout of PR head with elevated perms
    echo "$content" | grep -E 'ref:.*pull_request|head_ref'
    
    # 5. Self-hosted runner without isolation
    echo "$content" | grep -E 'runs-on:.*self-hosted'
  done
done
```

### Injection patterns to flag (severity guide)

| Pattern | Severity |
|---|---|
| `pull_request_target` + `actions/checkout` with `ref: pull_request.head.sha` + uses repo secrets | **Critical** — RCE on runner with org secrets |
| `${{ github.event.pull_request.title }}` interpolated into shell | **Critical** — script injection via PR title |
| Self-hosted runner reachable from public repo workflows | **High** — persistent attacker pivot |
| Issue-comment-triggered workflow that runs `gh` with token | **High** |
| Workflow downloads from URL that target controls | **Medium** |

---

## Step 7 — Docker / container image registry mining

```bash
# Docker Hub
curl -s "https://hub.docker.com/v2/repositories/$ORG/?page_size=100" | jq -r '.results[].name'

# GHCR (GitHub Container Registry) — public images visible in repo packages tab
gh api "users/$ORG/packages?package_type=container" 2>/dev/null
gh api "orgs/$ORG/packages?package_type=container" 2>/dev/null

# For each image, list tags
for img in image1 image2; do
  curl -s "https://hub.docker.com/v2/repositories/$ORG/$img/tags?page_size=20" | jq -r '.results[].name'
done

# Pull and inspect layers
docker pull "$ORG/$img:latest"
docker history --no-trunc "$ORG/$img:latest"

# Mine layers for secrets
docker save "$ORG/$img:latest" -o /tmp/image.tar
mkdir -p /tmp/img && tar -xf /tmp/image.tar -C /tmp/img
find /tmp/img -name "*.tar*" -exec tar -xf {} -C /tmp/img/extracted \;
# Then run gitleaks / trufflehog over extracted filesystem
trufflehog filesystem /tmp/img/extracted --no-update
```

---

## Step 8 — SBOM / artifact metadata leakage

```bash
# Look for SBOMs published as releases (SPDX, CycloneDX format)
gh api "repos/$ORG/$REPO/releases" --jq '.[] | .assets[] | select(.name | test("sbom|cyclonedx|spdx"; "i")) | .browser_download_url'

# JSON dependency lockfiles in releases
gh api "repos/$ORG/$REPO/releases" --jq '.[] | .assets[] | select(.name | test("lock|deps"; "i")) | .browser_download_url'

# Exact-version-pinned deps → known-CVE chaining
# Compare versions to nuclei nvd templates or osv.dev for known vulns
curl -s "https://api.osv.dev/v1/query" -d '{"package": {"name": "lodash", "ecosystem": "npm"}, "version": "4.17.10"}'
```

---

## Step 9 — Internal registry URL leakage

```bash
# .npmrc patterns
grep -r "registry=" .                                            # in cloned repos
grep -r "_authToken=" .                                          # leaked npm token!
grep -r "@.*registry=" .                                          # scoped registry

# pip config
grep -r "extra-index-url" .
grep -r "index-url" .

# Gradle / Maven
grep -rE "(mavenCentral|maven\s*\{)" .
grep -r "url.*\(.*nexus" .

# Each leaked internal URL is intel — flag the URL itself even if not directly exploitable
```

---

## Step 10 — npm/PyPI organizational presence

```bash
# Some orgs maintain a public npm scope mirroring their brand
curl -s "https://registry.npmjs.org/-/v1/search?text=scope:$ORG&size=50" | jq '.objects[].package.name'

# Public PyPI presence
curl -s "https://pypi.org/simple/" | grep "$ORG" | head -20

# Check if scope is taken — if it's NOT, an attacker could register
# (relevant for any internal package using that scope)
curl -sI "https://registry.npmjs.org/-/org/$ORG"
```

---

## Tooling

| Tool | Purpose |
|---|---|
| **`trufflehog`** | Filesystem/git/docker secret scan |
| **`gitleaks`** | Git history secret scan |
| **`dependency-confusion`** (Confused) | npm scope/PyPI checks |
| **`packj`** | Package risk score (PyPI/npm/RubyGems) |
| **`Lift / Snyk vuln-db`** | Known CVE lookup by package version |
| **`actionlint`** | GitHub Actions static analyzer |
| **`OSSGadget`** | Microsoft's package metadata toolkit |
| **`semgrep`** + supply-chain rules | Workflow injection detection |
| **`osv-scanner`** | Match versions to known vulns |

---

## Severity scoring guidance

| Finding | Severity |
|---|---|
| Internal package name + no scope-mapping + unclaimed on public npm + actively in builds | **Critical** — Dep-confusion RCE |
| Internal package name + scope-mapping in `.npmrc` but `_authToken` leaked | **Critical** — direct registry push |
| Pull_request_target workflow + secrets exposed + PR-controlled code execution | **Critical** — Org-wide token theft |
| Docker image with leaked secret in layer | **High** (varies by secret) |
| Internal registry URL disclosed (but no creds) | **Low** — Info-disc only |
| Typosquat candidate identified (not published) | **Informational** — Awareness item |
| Public org has 1000+ unused names that COULD be claimed | **Informational** — Hygiene |

---

## Anti-patterns

- **DO NOT publish a typosquat / dep-confusion package without explicit, signed, scope-clarified authorization** — this affects users outside the engagement
- **DO NOT submit PRs to client repos as part of testing without specific OK** — workflow injection PoCs may be needed but they touch CI/CD and other developers
- **DO NOT scrape entire npm/PyPI for typosquat candidates** — irresponsible and noisy
- **DO NOT confuse "name is unclaimed" with "exploitable dependency confusion"** — the build system matters; many orgs use proper scope-mapping that prevents the attack
- **DO NOT touch GitHub Actions self-hosted runners** — they may be inside the client network and outside the external scope
- **DO NOT pull large Docker images blindly** — image bandwidth can be 5-50GB; review tags first

---

## What constitutes a deliverable finding

A supply-chain finding needs ALL of:
1. **Concrete name/path** — exact internal package name, exact workflow file path, exact image tag
2. **Vulnerability mechanism** — dep-confusion / typosquat / injection / etc.
3. **Exploitability evidence** — proof the build/install would actually use the attacker's payload (not just "name is unclaimed")
4. **Severity** — calibrated to blast radius (one developer? all developers? all users of the package?)
5. **Recommendation** — specific (e.g., "register the unused name @target-internal/utils on npm AS YOUR OWN even if unused; configure `.npmrc` scope:registry mapping")

---

## Bridge to neighboring skills

- `apk-redteam-pipeline` — APKs reveal internal package names too (find them in decompiled `build.gradle`)
- `cloud-iam-deep` — CI/CD secrets often = cloud credentials; this skill finds them, that skill validates them
- `hunt-cloud-misconfig` — CI/CD pipeline misconfig (Jenkins / GitLab Runner) overlap
- `m365-entra-attack` — Azure DevOps pipelines are part of Entra surface
- `redteam-report-template` — supply-chain findings need extra clarity on blast radius (one repo vs whole ecosystem)
- `mid-engagement-ir-detection` — registering a name on public npm triggers nothing inside the client, but ANY publish action is loud and audit-trailed

---

## External-only boundary check

This skill is squarely external — all targets are public registries / public GitHub. If the engagement involves the client's internal artifact registry (internal Nexus, JFrog, Sonatype), that is internal infrastructure and OUT OF SCOPE per `feedback_skill_boundaries`. Report internal-registry URL exposure as a finding; do not attempt to enumerate it.

---

## Real-world references

- **Alex Birsan 2021** — Original dependency-confusion research, $130K+ in bounties from Apple/Microsoft/PayPal/Yelp/etc.
- **ua-parser-js 2021** — npm package compromise via stolen maintainer credentials
- **node-ipc 2022** — Maintainer-introduced supply-chain malicious update
- **3CX 2023** — Cascading supply-chain attack via X_TRADER → 3CX → customers
- **XZ Utils 2024** — Multi-year social-engineering supply-chain attack on upstream OSS

Each of these is worth reading for what made the attack effective and what red flags existed earlier.

---

## Related Skills & Chains

- **`hunt-rce`** — Dependency confusion lands as RCE on whatever runner installs the package; CI runners are the highest-value target. Chain primitive: internal package name leaked in public JS bundle / SBOM / Docker image → publish malicious package to public npm/PyPI under same name with higher version → next `npm install` / `pip install` on CI runner executes attacker code in `preinstall` hook → `hunt-rce` post-foothold (env-var extraction yields AWS keys, GitHub PATs, Slack tokens) → CI-plane takeover.
- **`cloud-iam-deep`** — CI runners have IAM credentials; supply-chain RCE there is a credential-exfil bonanza. Chain primitive: malicious package executes on GitHub Actions runner → reads `$AWS_ACCESS_KEY_ID` / `$GITHUB_TOKEN` from env → `cloud-iam-deep` enumeration → IAM-privilege-escalation chain → production cloud-plane access.
- **`offensive-osint`** — Recon discipline overlaps heavily; SBOMs, JS bundles, GitHub org enumeration, Docker registry tags all live in both. Chain primitive: `offensive-osint` GitHub-org recon yields internal package names referenced in CI workflows → `supply-chain-attack-recon` cross-references these against public npm/PyPI for typosquat/confusion candidates.
- **`hunt-cloud-misconfig`** — Container registries (Docker Hub, GHCR, ECR public) frequently expose private images by accident. Chain primitive: SBOM mining reveals `internal-tools-v2:latest` referenced → check Docker Hub for accidentally-public mirror → `hunt-cloud-misconfig` registry enum → pull image → extract secrets baked into layers.
- **`triage-validation`** + **`redteam-report-template`** — Supply-chain RECON is in scope; actual publishing is EXTERNAL-OFFENSIVE and needs explicit written sign-off. Chain primitive: recon-only candidate list assembled → run through `triage-validation` 7-Question Gate (specifically: "can I demonstrate impact WITHOUT publishing?") → report as "dependency-confusion candidate inventory + reproduction steps" via `redteam-report-template`, never as a published-package PoC unless client signed off in writing.
