# Mounting the Loa Framework

You are installing the Loa framework onto a repository. This is the first step before the Loa can ride through the codebase.

> *"The Loa mounts the repository, preparing to ride."*

## Core Principle

```
MOUNT once → RIDE many times
```

Mounting installs the framework. Riding analyzes the code.

---

## Pre-Mount Checks

### 1. Verify Git Repository

```bash
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "❌ Not a git repository. Initialize with 'git init' first."
  exit 1
fi
echo "✓ Git repository detected"
```

### 2. Check for Existing Mount

```bash
if [[ -f ".loa-version.json" ]]; then
  VERSION=$(jq -r '.framework_version' .loa-version.json 2>/dev/null)
  echo "⚠️ Loa already mounted (v$VERSION)"
  echo "Use '/update-loa' to sync framework, or continue to remount"
  # Use AskUserQuestion to confirm remount
fi
```

### 3. Verify Dependencies

```bash
command -v jq >/dev/null || { echo "❌ jq required"; exit 1; }
echo "✓ Dependencies satisfied"
```

---

## Mount Process

### Step 1: Configure Upstream Remote

```bash
LOA_REMOTE_URL="${LOA_UPSTREAM:-https://github.com/0xHoneyJar/loa.git}"
LOA_REMOTE_NAME="loa-upstream"
LOA_BRANCH="${LOA_BRANCH:-main}"

if git remote | grep -q "^${LOA_REMOTE_NAME}$"; then
  git remote set-url "$LOA_REMOTE_NAME" "$LOA_REMOTE_URL"
else
  git remote add "$LOA_REMOTE_NAME" "$LOA_REMOTE_URL"
fi

git fetch "$LOA_REMOTE_NAME" "$LOA_BRANCH" --quiet
echo "✓ Upstream configured"
```

### Step 2: Install System Zone

```bash
echo "Installing System Zone (.claude/)..."
git checkout "$LOA_REMOTE_NAME/$LOA_BRANCH" -- .claude 2>/dev/null || {
  echo "❌ Failed to checkout .claude/ from upstream"
  exit 1
}
echo "✓ System Zone installed"
```

### Step 3: Initialize State Zone

```bash
echo "Initializing State Zone..."

# Create structure (preserve if exists)
mkdir -p grimoires/loa/{context,reality,legacy,discovery,a2a/trajectory}
mkdir -p .beads

# Initialize structured memory
if [[ ! -f "grimoires/loa/NOTES.md" ]]; then
  cat > grimoires/loa/NOTES.md << 'EOF'
# Agent Working Memory (NOTES.md)

> This file persists agent context across sessions and compaction cycles.

## Active Sub-Goals

## Discovered Technical Debt

## Blockers & Dependencies

## Session Continuity
| Timestamp | Agent | Summary |
|-----------|-------|---------|

## Decision Log
| Date | Decision | Rationale | Decided By |
|------|----------|-----------|------------|
EOF
  echo "✓ Structured memory initialized"
else
  echo "✓ Structured memory preserved"
fi
```

### Step 4: Create Version Manifest

```bash
cat > .loa-version.json << EOF
{
  "framework_version": "0.6.0",
  "schema_version": 2,
  "last_sync": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "zones": {
    "system": ".claude",
    "state": ["grimoires/loa", ".beads"],
    "app": ["src", "lib", "app"]
  },
  "migrations_applied": ["001_init_zones"],
  "integrity": {
    "enforcement": "strict",
    "last_verified": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  }
}
EOF
echo "✓ Version manifest created"
```

### Step 5: Generate Checksums (Anti-Tamper)

```bash
echo "Generating integrity checksums..."

CHECKSUMS_FILE=".claude/checksums.json"
checksums='{"generated":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","algorithm":"sha256","files":{'

first=true
while IFS= read -r -d '' file; do
  hash=$(sha256sum "$file" | cut -d' ' -f1)
  relpath="${file#./}"
  [[ "$first" == "true" ]] && first=false || checksums+=','
  checksums+='"'"$relpath"'":"'"$hash"'"'
done < <(find .claude -type f ! -name "checksums.json" ! -path "*/overrides/*" -print0 | sort -z)

checksums+='}}'
echo "$checksums" | jq '.' > "$CHECKSUMS_FILE"
echo "✓ Checksums generated"
```

### Step 6: Create User Config

```bash
if [[ ! -f ".loa.config.yaml" ]]; then
  cat > .loa.config.yaml << 'EOF'
# Loa Framework Configuration
# This file is yours - framework updates will never modify it

persistence_mode: standard  # standard | stealth
integrity_enforcement: strict  # strict | warn | disabled
drift_resolution: code  # code | docs | ask

disabled_agents: []

memory:
  notes_file: grimoires/loa/NOTES.md
  trajectory_dir: grimoires/loa/a2a/trajectory
  trajectory_retention_days: 30
  auto_restore: true

edd:
  enabled: true
  min_test_scenarios: 3
  trajectory_audit: true
  require_citations: true

compaction:
  enabled: true
  threshold: 5

integrations:
  - github
EOF
  echo "✓ Config created"
else
  echo "✓ Config preserved"
fi
```

### Step 7: Initialize beads_rust (Optional)

```bash
if command -v br &> /dev/null; then
  if [[ ! -f ".beads/beads.db" ]]; then
    br init --quiet 2>/dev/null && echo "✓ beads_rust initialized"
  else
    echo "✓ beads_rust already initialized"
  fi
else
  echo "⚠️ beads_rust (br) not found - skipping (install: .claude/scripts/beads/install-br.sh)"
fi
```

### Step 8: Create Overrides Directory

```bash
mkdir -p .claude/overrides
[[ -f .claude/overrides/README.md ]] || cat > .claude/overrides/README.md << 'EOF'
# User Overrides

Files here are preserved across framework updates.
Mirror the .claude/ structure for any customizations.
EOF
```

---

## Post-Mount Output

Display completion message:

```markdown
╔═════════════════════════════════════════════════════════════════╗
║  ✓ Loa Successfully Mounted!                                    ║
╚═════════════════════════════════════════════════════════════════╝

Zone structure:
  📁 .claude/          → System Zone (framework-managed)
  📁 .claude/overrides → Your customizations (preserved)
  📁 grimoires/loa/     → State Zone (project memory)
  📄 grimoires/loa/NOTES.md → Structured agentic memory
  📁 .beads/           → Task graph

Next steps:
  1. Run 'claude' to start Claude Code
  2. Issue '/ride' to analyze this codebase
  3. Or '/plan-and-analyze' for greenfield development

⚠️ STRICT ENFORCEMENT: Direct edits to .claude/ will block execution.
   Use .claude/overrides/ for customizations.

The Loa has mounted. Issue '/ride' when ready.
```

---

## Stealth Mode

If `--stealth` flag or `persistence_mode: stealth` in config:

```bash
echo "Applying stealth mode..."
touch .gitignore

for entry in "grimoires/loa/" ".beads/" ".loa-version.json" ".loa.config.yaml"; do
  grep -qxF "$entry" .gitignore 2>/dev/null || echo "$entry" >> .gitignore
done

echo "✓ State files added to .gitignore"
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Not a git repository" | No `.git` directory | Run `git init` first |
| "jq required" | Missing jq | Install jq (`brew install jq` / `apt install jq`) |
| "Failed to checkout .claude/" | Network/auth issue | Check remote URL and credentials |
| "Loa already mounted" | `.loa-version.json` exists | Use `/update-loa` or confirm remount |

---

## Trajectory Logging

Log mount action to trajectory:

```bash
MOUNT_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TRAJECTORY_FILE="grimoires/loa/a2a/trajectory/mounting-$(date +%Y%m%d).jsonl"

echo '{"timestamp":"'$MOUNT_DATE'","agent":"mounting-framework","action":"mount","status":"complete","version":"0.6.0"}' >> "$TRAJECTORY_FILE"
```

---

## NOTES.md Update

After successful mount, add entry to NOTES.md:

```markdown
## Session Continuity
| Timestamp | Agent | Summary |
|-----------|-------|---------|
| [now] | mounting-framework | Mounted Loa v0.6.0 on repository |
```
