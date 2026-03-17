---
name: deployment-validator
description: Validates application readiness for Render/production deployment. Auto-runs when user mentions deployment. Prevents "works locally, fails in production" issues. Always run this BEFORE any deployment.
triggers: ["deploy", "render", "production", "staging", "push to render", "ready to deploy", "deployment", "going live"]
version: 1.0.0
created: 2025-10-19
auto_invoke: true
---

# Deployment Validator Skill

**Purpose**: Systematically validate the application is ready for production deployment, catching common "works locally, fails on Render" issues BEFORE they happen.

## When to Use

This skill MUST be invoked when:
- User mentions deploying to Render, production, or staging
- User says "ready to deploy" or "push to production"
- Any git push to main/production branches
- After significant routing or static file changes
- Before creating deployment documentation

## Common Issues We've Learned (Hard-Won Lessons)

### Issue 1: Static File Path Mismatches
**Problem**: Files served from wrong directory (projectRoot vs publicDir)
**Symptom**: Works locally, 404 in production
**Root Cause**: Express static middleware serves from different base paths

**Example**:
```typescript
// BAD - File in /public but served from projectRoot
app.use(express.static(projectRoot));
// Accessing /demo-scenario-picker.html serves from projectRoot/demo-scenario-picker.html
// But file is actually in projectRoot/public/demo-scenario-picker.html

// GOOD - Serve public files from publicDir
app.use(express.static(publicDir));
// Accessing /demo-scenario-picker.html serves from publicDir/demo-scenario-picker.html
```

**Fix Pattern**:
1. Identify which directory the file is ACTUALLY in
2. Ensure static middleware serves from that directory
3. Update all references to match the served path

### Issue 2: Route Precedence Overriding Static Middleware
**Problem**: Explicit routes defined AFTER static middleware override file serving
**Symptom**: 404 for HTML files even though they exist
**Root Cause**: Express matches routes in order - explicit routes win over static middleware

**Example**:
```typescript
// BAD - Explicit route overrides static middleware
app.use(express.static(publicDir)); // Line 199
app.get('/demo-scenario-picker.html', (req, res) => { // Line 450
  res.sendFile(path.join(projectRoot, 'demo-scenario-picker.html')); // WRONG PATH!
});

// GOOD - Remove explicit route, let static middleware handle it
app.use(express.static(publicDir)); // Line 199
// No explicit route needed - static middleware serves it automatically
```

**Fix Pattern**:
1. Check for duplicate routes (explicit routes + static middleware)
2. Remove explicit routes if static middleware already handles the file
3. If explicit route is needed, ensure it uses correct path (publicDir, not projectRoot)

### Issue 3: Missing Files in Production
**Problem**: Files exist locally but not committed/pushed
**Symptom**: git status shows untracked files, Render can't find them
**Root Cause**: File moved to new directory but git not updated

**Example**:
```bash
# File moved from projectRoot to /public but not tracked
$ git status
?? public/demo-scenario-picker.html

# File not in repo, so Render can't access it
```

**Fix Pattern**:
1. Always check `git status` after moving files
2. `git add` newly created/moved files
3. Verify file is in repo before deploying

### Issue 4: Hardcoded Local Paths
**Problem**: Paths work on developer machine but not in production
**Symptom**: ENOENT errors in production logs
**Root Cause**: Absolute paths specific to local filesystem

**Example**:
```typescript
// BAD - Hardcoded local path
const filePath = '/Users/developer/project/public/file.html';

// GOOD - Relative to project structure
const filePath = path.join(__dirname, '..', 'public', 'file.html');
```

**Fix Pattern**:
1. Search codebase for hardcoded paths (/Users/, C:\, etc.)
2. Replace with path.join() using __dirname or process.cwd()
3. Use environment variables for external paths

### Issue 5: Environment Variable Mismatches
**Problem**: Different env vars locally vs production
**Symptom**: Features work locally, fail in production
**Root Cause**: .env file not synced with Render dashboard

**Example**:
```bash
# Local .env
PORT=3000
NODE_ENV=development

# Render dashboard (missing vars)
PORT=10000
# NODE_ENV not set - defaults incorrectly
```

**Fix Pattern**:
1. Document all required env vars
2. Verify Render dashboard has all vars set
3. Use fallback values: `process.env.VAR || 'default'`

## Validation Checklist

Run this checklist BEFORE every deployment:

### Step 1: Static File Validation
```bash
# Check which files are in /public
ls -la public/

# Verify files are tracked in git
git status

# Search for explicit routes that might override static middleware
grep -n "app.get.*\.html" src/index.ts

# Check static middleware configuration
grep -A5 "express.static" src/index.ts
```

**Expected Results**:
- All HTML files in /public are tracked by git (not in `?? untracked`)
- No explicit routes for files served by static middleware
- Static middleware serves from correct directory (publicDir for /public files)

### Step 2: Route Precedence Check
```bash
# Find all app.get() routes in index.ts
grep -n "^app.get" src/index.ts

# Check order: static middleware should be BEFORE explicit routes
# Line numbers should be: static middleware (low) -> explicit routes (high)
```

**Expected Results**:
- Static middleware defined early (around line 199-244)
- Explicit routes defined later (after line 275)
- No duplicate routes (same path in static middleware + explicit route)

### Step 3: Path Validation
```bash
# Search for hardcoded paths
grep -r "\/Users\/" src/
grep -r "C:\\\\" src/
grep -r "projectRoot" src/index.ts | grep -v "const projectRoot"

# Verify path.join usage for all file operations
grep -n "sendFile" src/index.ts
```

**Expected Results**:
- No hardcoded user-specific paths
- All sendFile() calls use path.join() with __dirname or projectRoot/publicDir
- Correct base directory (publicDir for /public files, projectRoot for root files)

### Step 4: Git Status Validation
```bash
# Check for untracked files
git status --porcelain | grep "^??"

# Check for uncommitted changes
git status --porcelain | grep "^ M"

# Verify critical files are tracked
git ls-files public/ | wc -l
```

**Expected Results**:
- No untracked files in /public (unless intentionally gitignored)
- All changes committed
- All production files present in git repository

### Step 5: Environment Variable Check
```bash
# List all env vars used in code
grep -r "process.env" src/ | grep -v node_modules | cut -d: -f2 | grep -o "process.env\['[^']*'\]" | sort -u

# Compare with .env.example (if exists)
cat .env.example
```

**Expected Results**:
- All required env vars documented
- Render dashboard configured with all necessary vars
- Fallback values for non-critical vars

### Step 6: Build Validation
```bash
# Clean build
npm run build

# Check for build errors
echo $?  # Should be 0

# Verify dist/ directory created
ls -la dist/
```

**Expected Results**:
- Build succeeds without errors
- dist/ directory contains compiled JavaScript
- No TypeScript errors

### Step 7: Local Production Simulation
```bash
# Run in production mode locally
NODE_ENV=production npm start

# Test critical endpoints
curl http://localhost:3000/health
curl http://localhost:3000/demo-scenario-picker.html
curl http://localhost:3000/api/v1/requirements
```

**Expected Results**:
- Server starts successfully
- All endpoints return 200 (not 404)
- HTML files serve correctly

## Automated Validation Script

Create this script at `/scripts/validate-deployment.sh`:

```bash
#!/bin/bash
# Deployment Validation Script
# Run this BEFORE every deployment

set -e  # Exit on first error

echo "=== Project Conductor Deployment Validator ==="
echo ""

# Step 1: Git Status
echo "1. Checking git status..."
UNTRACKED=$(git status --porcelain | grep "^??" || true)
if [ -n "$UNTRACKED" ]; then
  echo "❌ FAIL: Untracked files found:"
  echo "$UNTRACKED"
  exit 1
fi
echo "✅ PASS: No untracked files"

UNCOMMITTED=$(git status --porcelain | grep "^ M" || true)
if [ -n "$UNCOMMITTED" ]; then
  echo "⚠️  WARNING: Uncommitted changes found:"
  echo "$UNCOMMITTED"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Step 2: Check for duplicate routes
echo ""
echo "2. Checking for duplicate routes..."
DUPLICATES=$(grep -n "app.get.*\.html" src/index.ts | wc -l)
if [ "$DUPLICATES" -gt 5 ]; then
  echo "⚠️  WARNING: Found $DUPLICATES explicit HTML routes"
  echo "    Review for conflicts with static middleware"
  grep -n "app.get.*\.html" src/index.ts
fi

# Step 3: Check for hardcoded paths
echo ""
echo "3. Checking for hardcoded paths..."
HARDCODED=$(grep -r "\/Users\/" src/ 2>/dev/null | grep -v node_modules || true)
if [ -n "$HARDCODED" ]; then
  echo "❌ FAIL: Hardcoded paths found:"
  echo "$HARDCODED"
  exit 1
fi
echo "✅ PASS: No hardcoded paths"

# Step 4: Validate static file configuration
echo ""
echo "4. Validating static file configuration..."
PUBLIC_FILES=$(ls -1 public/*.html 2>/dev/null | wc -l)
echo "   Found $PUBLIC_FILES HTML files in /public"

# Check if publicDir is used correctly
PUBLICDIR_USAGE=$(grep -c "express.static(publicDir)" src/index.ts || true)
if [ "$PUBLICDIR_USAGE" -lt 1 ]; then
  echo "⚠️  WARNING: publicDir static middleware not found"
fi

# Step 5: Build test
echo ""
echo "5. Running build test..."
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "✅ PASS: Build successful"
else
  echo "❌ FAIL: Build failed"
  exit 1
fi

# Step 6: Check required files
echo ""
echo "6. Checking required files..."
REQUIRED_FILES=(
  "src/index.ts"
  "package.json"
  "tsconfig.json"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ FAIL: Missing required file: $file"
    exit 1
  fi
done
echo "✅ PASS: All required files present"

# Summary
echo ""
echo "=== Deployment Validation Complete ==="
echo "✅ Ready to deploy to Render"
echo ""
echo "Next steps:"
echo "  1. git add ."
echo "  2. git commit -m 'Ready for deployment'"
echo "  3. git push origin main"
echo "  4. Monitor Render deployment logs"
```

Make it executable:
```bash
chmod +x scripts/validate-deployment.sh
```

## Usage

### Automatic Invocation
When user says: "ready to deploy", "push to render", "deploy to production"

**Your Response**:
```
🛡️ Running deployment validation first...

[Run validation checklist steps 1-7]

Results:
✅ Static files validated
✅ Route precedence correct
✅ No hardcoded paths
✅ Git status clean
✅ Environment variables documented
✅ Build successful
✅ Local production test passed

All checks passed! Ready to deploy.
```

### Manual Invocation
User can explicitly call:
```bash
npm run validate:deploy
# or
./scripts/validate-deployment.sh
```

## Fix Patterns Reference

### Pattern 1: File in /public, served from projectRoot
**Detection**: File exists in /public but 404 in production
**Fix**:
```typescript
// Before (WRONG)
app.get('/file.html', (req, res) => {
  res.sendFile(path.join(projectRoot, 'file.html')); // File not here!
});

// After (CORRECT)
// Remove explicit route, let static middleware handle it
app.use(express.static(publicDir)); // This serves /public files at root
```

### Pattern 2: Explicit route overrides static middleware
**Detection**: grep shows both static middleware AND explicit route for same file
**Fix**:
```typescript
// Before (CONFLICT)
app.use(express.static(publicDir)); // Line 199
app.get('/file.html', ...); // Line 450 - OVERRIDES!

// After (RESOLVED)
app.use(express.static(publicDir)); // Line 199
// Removed explicit route - static middleware handles it
```

### Pattern 3: File moved but not tracked
**Detection**: `git status` shows `?? public/file.html`
**Fix**:
```bash
git add public/file.html
git commit -m "Add file to public directory"
git push origin main
```

### Pattern 4: Wrong path in sendFile
**Detection**: ENOENT error in production logs
**Fix**:
```typescript
// Before (WRONG)
res.sendFile(path.join(projectRoot, 'file.html')); // File is in /public!

// After (CORRECT)
res.sendFile(path.join(publicDir, 'file.html')); // Correct base dir
```

## Integration with package.json

Add these scripts:
```json
{
  "scripts": {
    "validate:deploy": "./scripts/validate-deployment.sh",
    "predeploy": "npm run validate:deploy",
    "deploy": "git push origin main"
  }
}
```

Now `npm run deploy` automatically validates before pushing.

## Skill Improvement Tracking

**Version History**:
- 1.0.0 (2025-10-19): Initial creation from deployment debugging session
  - Captured static file path mismatch issue
  - Captured route precedence issue
  - Captured git tracking issue
  - Created automated validation checklist

**Future Enhancements**:
- [ ] Add automated fix suggestions (not just detection)
- [ ] Integrate with CI/CD pipeline
- [ ] Add Render-specific log monitoring
- [ ] Database migration validation
- [ ] Environment variable auto-sync with Render

## Success Metrics

This skill is successful if:
1. **Zero "works locally, fails on Render" incidents** after deployment
2. **Validation catches issues before git push** (not after)
3. **New developers can deploy confidently** using this checklist
4. **Production deployments succeed on first try** (no rollbacks)

## Related Skills
- `validation`: General validation workflow (tests, linting)
- `scout`: Find deployment best practices from external sources

## References
- Express.js static middleware docs: https://expressjs.com/en/starter/static-files.html
- Render deployment guide: https://render.com/docs/deploy-node-express-app
- Path module docs: https://nodejs.org/api/path.html

---

**Remember**: This skill was created from REAL debugging pain. Every check in this list prevented an actual production issue. Use it religiously.
