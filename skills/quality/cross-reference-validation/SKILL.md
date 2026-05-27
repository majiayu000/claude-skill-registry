---
name: cross-reference-validation
description: Validates all documentation references - file paths, links, line numbers, code examples
version: 1.0.0
category: validation
auto_invoke: false
---

# Cross-Reference Validation Skill

**Purpose**: Ensure all documentation references (file paths, links, line numbers) are accurate and up-to-date.

---

## What This Skill Validates

### 1. File Path References

**Pattern**: References to files in documentation

**Example**:

```markdown
# docs/guide.md:45

See the implementation in ./scripts/debug/test.sh
```

**Validation**: Does `./scripts/debug/test.sh` exist?

### 2. Relative Links

**Pattern**: Markdown links to other docs

**Example**:

```markdown
# README.md:67

For details, see [Architecture](docs/ARCHITECTURE.md)
```

**Validation**: Does `docs/ARCHITECTURE.md` exist?

### 3. File:Line References

**Pattern**: References to specific code lines

**Example**:

```markdown
# docs/guide.md:89

Implementation: src/convert.ts:450
```

**Validation**:

- Does `src/convert.ts` exist?
- Does it have at least 450 lines?

### 4. Code Examples

**Pattern**: Code blocks with language tags

**Example**:

````markdown
# docs/api.md:120

```typescript
import { Server } from "./server";
```
````

**Validation**: Does `./server` export `Server`?

### 5. Issue/PR References

**Pattern**: GitHub issue/PR mentions

**Example**:

```markdown
# CHANGELOG.md:45

Fixed in #123
```

**Validation**: Does issue #123 exist and is it closed?

---

## Workflow

### Phase 1: Extract All References

#### Step 1.1: Find File Path References

```bash
# Search for common file path patterns
grep -rn '\./[a-zA-Z0-9_/-]*\.\(sh\|ts\|js\|py\|md\)' *.md docs/

# Patterns to match:
# - ./script.sh
# - ./src/file.ts
# - scripts/debug/test.sh
# - ../relative/path.md
```

**Create reference map**:

```json
{
  "docs/guide.md:45": {
    "type": "file_path",
    "reference": "./scripts/debug/test.sh",
    "context": "See the implementation in",
    "line": 45
  }
}
```

#### Step 1.2: Find Markdown Links

```bash
# Extract all markdown links
grep -rn '\[.*\](.*\)' *.md docs/ | grep -v 'http'

# Pattern: [Link Text](path/to/file.md)
```

**Parse format**:

```json
{
  "README.md:67": {
    "type": "markdown_link",
    "text": "Architecture",
    "reference": "docs/ARCHITECTURE.md",
    "line": 67
  }
}
```

#### Step 1.3: Find File:Line References

```bash
# Pattern: filename:line_number
grep -rn '[a-zA-Z0-9_/-]*\.\(ts\|js\|py\|sh\):[0-9]\+' *.md docs/

# Examples:
# - src/convert.ts:450
# - lib/utils.py:89
```

**Parse format**:

```json
{
  "docs/guide.md:89": {
    "type": "file_line_reference",
    "file": "src/convert.ts",
    "line": 450,
    "doc_line": 89
  }
}
```

#### Step 1.4: Find Code Imports

````bash
# Extract code blocks
awk '/```typescript/,/```/ {print}' docs/**/*.md

# Look for import statements
grep -A 5 "^import"
````

**Parse imports**:

```json
{
  "docs/api.md:120": {
    "type": "code_import",
    "import": "{ Server } from './server'",
    "file": "./server",
    "exports": ["Server"]
  }
}
```

---

### Phase 2: Validate File Paths

#### Step 2.1: Check File Existence

```bash
# For each file path reference
REFERENCE="./scripts/debug/test.sh"

if [ -f "$REFERENCE" ]; then
  echo "✅ Valid: $REFERENCE"
else
  echo "❌ Broken: $REFERENCE not found"

  # Try to find similar files
  BASENAME=$(basename "$REFERENCE")
  find . -name "$BASENAME" -type f
fi
```

**Output for broken reference**:

```
❌ BROKEN FILE PATH: docs/guide.md:45
   Referenced: ./scripts/debug/test.sh
   Status: File not found

   Possible matches:
   - ./scripts/test/test.sh (moved?)
   - ./debug-test.sh (renamed?)

   Suggested fix:
   Update reference to: ./scripts/test/test.sh
```

#### Step 2.2: Check for File Moves

```bash
# Check git history for file move
REFERENCE="./debug-local.sh"

git log --all --follow --name-status -- "*$(basename $REFERENCE)"

# Output might show:
# R100  debug-local.sh  scripts/debug/debug-local.sh
```

**If move detected**:

````
⚠️ FILE MOVED: docs/guide.md:45
   Old path: ./debug-local.sh
   New path: ./scripts/debug/debug-local.sh
   Moved: 3 days ago (commit abc123)

   Auto-fix available: YES

   Suggested fix:
   ```markdown
   See: ./scripts/debug/debug-local.sh
````

````

---

### Phase 3: Validate Markdown Links

#### Step 3.1: Resolve Relative Links

```bash
# For link in README.md:67
LINK="docs/ARCHITECTURE.md"
DOC_DIR=$(dirname "README.md")  # .
FULL_PATH="$DOC_DIR/$LINK"      # ./docs/ARCHITECTURE.md

if [ -f "$FULL_PATH" ]; then
  echo "✅ Valid link"
else
  echo "❌ Broken link: $FULL_PATH"
fi
````

#### Step 3.2: Find Renamed Files

```bash
# If link is broken
LINK="docs/ARCHITECTURE.md"

# Search for similar files
find docs/ -name "*ARCHITECTURE*" -o -name "*architecture*"

# Common renames:
# - ARCHITECTURE.md → system-design.md
# - ARCHITECTURE.md → architecture/overview.md
```

**Output**:

```
❌ BROKEN LINK: README.md:67
   Links to: docs/ARCHITECTURE.md
   Status: File not found

   Possible matches:
   - docs/architecture/system-design.md
   - docs/SYSTEM-ARCHITECTURE.md

   Context: [Architecture](docs/ARCHITECTURE.md)

   Suggested fix:
   [Architecture](docs/architecture/system-design.md)
```

---

### Phase 4: Validate File:Line References

#### Step 4.1: Check File and Line Number

```bash
# Reference: src/convert.ts:450
FILE="src/convert.ts"
LINE=450

# Check file exists
if [ ! -f "$FILE" ]; then
  echo "❌ File not found: $FILE"
  exit 1
fi

# Check line count
LINE_COUNT=$(wc -l < "$FILE")

if [ $LINE_COUNT -lt $LINE ]; then
  echo "❌ Line $LINE doesn't exist (file has $LINE_COUNT lines)"
else
  echo "✅ Valid reference"
  # Show the referenced line
  sed -n "${LINE}p" "$FILE"
fi
```

**Output for invalid line**:

```
❌ INVALID LINE REFERENCE: docs/guide.md:89
   References: src/convert.ts:450
   Problem: File only has 412 lines

   Last modification: 3 hours ago (commit 2e8237c)
   Likely cause: Code was refactored/removed

   Options:
   1. Remove line reference (just reference file)
   2. Find new location of code
   3. Update to correct line number

   Suggested fix:
   Implementation: src/convert.ts (search for function)
```

#### Step 4.2: Verify Referenced Code Exists

```bash
# If line reference is valid, check context
FILE="src/convert.ts"
LINE=450

# Get referenced line
REFERENCED_LINE=$(sed -n "${LINE}p" "$FILE")

# Show context in documentation
echo "Referenced line: $REFERENCED_LINE"
echo "Documentation context: {context from docs}"

# Verify they match
```

**Example**:

```
✅ VALID REFERENCE: docs/guide.md:89
   References: src/convert.ts:450

   Referenced line (450):
   controller.enqueue({ type: "input_json_delta", ... });

   Documentation context:
   "Tool parameters are streamed via input_json_delta (line 450)"

   Status: Accurate reference ✅
```

---

### Phase 5: Validate Code Examples

#### Step 5.1: Extract Imports from Code Blocks

````bash
# Find TypeScript code blocks
awk '/```typescript/,/```/ {print}' docs/api.md > /tmp/code_block.ts

# Extract imports
grep "^import" /tmp/code_block.ts

# Example: import { Server } from './server';
````

#### Step 5.2: Verify Exports Exist

```bash
# For import: { Server } from './server'
IMPORT_FROM="./server"
IMPORT_NAME="Server"

# Find the file (relative to doc location or src/)
# Try: ./server.ts, ./server/index.ts, src/server.ts

find . -name "server.ts" -o -name "index.ts" | while read file; do
  # Check if it exports Server
  grep "export.*Server" "$file"
done
```

**Output for broken import**:

````
⚠️ CODE EXAMPLE MAY BE OUTDATED: docs/api.md:120
   Import: { Server } from './server'
   Problem: No 'Server' export found in ./server.ts

   Actual exports in ./server.ts:
   - export class APIServer
   - export { createServer }

   Possible fix:
   ```typescript
   import { APIServer } from './server';
````

```

---

### Phase 6: Generate Report

#### Output Format

```

🔗 Cross-Reference Validation Report

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
Total references: 47
✅ Valid: 42 (89%)
⚠️ Warnings: 3 (6%)
❌ Broken: 2 (4%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BROKEN REFERENCES (CRITICAL)

❌ BROKEN FILE PATH: docs/DEBUG-GUIDE.md:39
Referenced: ./debug-local.sh
Status: File not found
Last seen: 3 days ago (moved to scripts/debug/)

Auto-fix available: YES

Fix:

- Current: ./debug-local.sh
- Update to: ./scripts/debug/debug-local.sh

Git detected move in commit abc123

❌ BROKEN LINK: README.md:35
Links to: docs/ARCHITECTURE.md
Status: File not found

Possible matches:

- docs/architecture/system-design.md (closest match)
- docs/SYSTEM-ARCH.md

Fix:
[Architecture](docs/architecture/system-design.md)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WARNINGS (REVIEW RECOMMENDED)

⚠️ INVALID LINE REFERENCE: docs/guide.md:89
References: src/convert.ts:450
Problem: File only has 412 lines

Possible causes:

- Code was refactored
- Lines were removed
- Reference needs update

Suggested fix:
Reference file without line number, or find new location

⚠️ CODE EXAMPLE OUTDATED: docs/api.md:120
Import: { Server } from './server'
Problem: No 'Server' export found

Actual exports:

- APIServer (renamed?)
- createServer

Suggested update:
import { APIServer } from './server';

⚠️ RELATIVE PATH UNCLEAR: docs/troubleshooting.md:56
Referenced: ../config.json
Context: "Edit ../config.json to configure"
Problem: Relative paths confusing from docs/

Suggested fix:
Use absolute path: ./config.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VALID REFERENCES (Sample)

✅ docs/guide.md:15 → ./scripts/test/test-auth.sh
✅ README.md:45 → docs/guides/getting-started.md
✅ docs/api.md:67 → src/server.ts:125 (accurate)
✅ CONTRIBUTING.md:89 → .github/PULL_REQUEST_TEMPLATE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTO-FIX SUMMARY

✅ Can auto-fix (2 references):

1. docs/DEBUG-GUIDE.md:39 (file move detected)
2. docs/DEBUG-LMSTUDIO.md:96 (same file move)

Run: /align-project → Option 2 (Fix interactively)
→ Phase 2 will apply these fixes

⚠️ Needs manual review (3 references):

1. Invalid line reference (code refactored)
2. Code example import (export renamed)
3. Relative path clarity (user preference)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED BREAKDOWN

File Path References: 18 total
✅ Valid: 16
❌ Broken: 2

Markdown Links: 15 total
✅ Valid: 14
❌ Broken: 1

File:Line References: 8 total
✅ Valid: 7
⚠️ Invalid line: 1

Code Examples: 6 total
✅ Valid: 5
⚠️ Outdated: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTIONS

Immediate (Fix Today):

1. Update 2 file paths after move to scripts/debug/
2. Fix broken link to architecture docs

Review (This Week): 3. Update invalid line reference in guide.md 4. Verify code example imports in api.md

Optional (Next Sprint): 5. Consider using absolute paths instead of relative

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

````

---

## Auto-Fix Capabilities

### Can Auto-Fix

**File moves detected by git**:
```bash
# Detect move
git log --follow --name-status -- "debug-local.sh"
# R100  debug-local.sh  scripts/debug/debug-local.sh

# Auto-update all references
find . -name "*.md" -exec sed -i 's|./debug-local.sh|./scripts/debug/debug-local.sh|g' {} \;
````

**Broken links with obvious match**:

```bash
# Find closest match using fuzzy search
BROKEN="docs/ARCHITECTURE.md"
BASENAME=$(basename "$BROKEN")

# Look for similar
find docs/ -name "*architecture*" -o -name "*arch*"
# If only one match → auto-fix
```

### Needs Manual Review

- **Multiple possible matches**: User chooses correct path
- **Code examples**: User verifies updated import is correct
- **Line references**: Code may have moved, need context
- **Ambiguous relative paths**: User preference for absolute vs relative

---

## Integration with File Move Hook

When files are moved, trigger cross-reference validation:

```bash
# Post-file-move hook
OLD_PATH="$1"
NEW_PATH="$2"

# Find all references to old path
REFERENCES=$(grep -r "$OLD_PATH" --include="*.md" .)

if [ -n "$REFERENCES" ]; then
  echo "📝 Found $(echo "$REFERENCES" | wc -l) references to moved file"
  echo ""
  echo "Auto-update? [Y/n]"
  read RESPONSE

  if [[ "$RESPONSE" =~ ^[Yy] ]]; then
    # Update all references
    find . -name "*.md" -exec sed -i "s|$OLD_PATH|$NEW_PATH|g" {} \;
    echo "✅ Updated all references"
  fi
fi
```

---

## Success Criteria

After validation:

- ✅ All file path references checked for existence
- ✅ All markdown links verified or flagged
- ✅ File:line references validated against actual line count
- ✅ Code examples checked for accurate imports
- ✅ Auto-fix suggestions provided for broken references
- ✅ Completes in < 15 seconds for medium projects

---

## Edge Cases

### Case 1: Intentional External Reference

```markdown
# docs/guide.md:45

For comparison, see: https://github.com/other-project/file.ts:123
```

**Detection**: External URL, not local reference
**Action**: Skip (can't validate external references)

### Case 2: Glob Pattern in Reference

```markdown
# docs/build.md:67

All test files in tests/\*_/_.test.ts
```

**Detection**: Glob pattern, not specific file
**Action**: Validate pattern matches at least one file

```bash
# Check glob
if ls tests/**/*.test.ts 1> /dev/null 2>&1; then
  echo "✅ Pattern matches files"
else
  echo "⚠️ No files match pattern"
fi
```

### Case 3: Line Reference to Comments

```markdown
# docs/guide.md:89

See comment at src/convert.ts:450
```

```typescript
// src/convert.ts:450
// TODO: This needs refactoring
```

**Validation**: Line exists but is a comment
**Action**: Still valid (user may reference comments intentionally)

---

## Performance Optimization

For large projects (100+ documentation files):

**Batch file existence checks**:

```bash
# Instead of checking each file individually
# Create temp file with all references
cat references.txt | while read ref; do
  [ -f "$ref" ] || echo "BROKEN: $ref"
done > broken_refs.txt
```

**Cache git history**:

```bash
# Get all file moves once
git log --follow --name-status --diff-filter=R > /tmp/git_moves.txt

# Parse once, reference many times
```

**Parallel validation**:

```bash
# Split references into chunks
# Validate each chunk in parallel using & backgrounding
```

---

**This skill ensures documentation references stay accurate as code evolves, preventing link rot and reference decay.**
