---
name: npmrc
description: Conditionally generates .npmrc for GitHub Packages registry configuration. Maps organization scope to registry endpoint when component library is requested. Token stored in ~/.npmrc only.
---

# NPM RC Skill

## Purpose
Generate `.npmrc` file for GitHub Packages registry configuration when component library is requested.

## ⚠️ CONDITIONAL SKILL - READ CAREFULLY

**Execute this skill ONLY if**: `include_component_library: yes`

**If `include_component_library: no`**: 
- **SKIP this skill entirely**
- Do not generate `.npmrc` file
- Do not include in file generation checklist
- Move to next skill

## 🚨 MANDATORY FILE COUNT
**Expected Output**: **1 file** (only if component library requested)
- `.npmrc` (standard format)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

**STEP 0 - Conditional Check**:
```javascript
if (include_component_library !== 'yes') {
  console.log('⏭️  SKIPPING npmrc skill - Component library not requested');
  return; // Exit this skill
}
```

Perform these checks in order before generating the file:

1. **Verify GitHub Registry URL**: Confirm current GitHub Packages registry endpoint
   - **Check documentation**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry
   - **Current URL**: `https://npm.pkg.github.com` (verify this is still correct)
   - **If changed**: Use updated registry URL from GitHub docs
   - **GitHub Enterprise**: Check if organization uses custom domain

2. **Token Configuration Check**: Verify user has configured GitHub authentication
   - **DO NOT read token value** - Security risk to access `~/.npmrc` contents
   - **Check file exists only**: `test -f ~/.npmrc && echo "Config exists" || echo "Config missing"`
   - **User responsibility**: Assume users have configured their own GitHub PAT
   - **If concerns exist**: 
     - ⚠️ **INFORM USER**: "Ensure GitHub token is configured in ~/.npmrc with read:packages scope"
     - **Documentation link**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry#authenticating-with-a-personal-access-token
     - **Action**: Continue generation and document token requirements in README

3. **Token Permission Verification**: Check if token has required scope
   - **Required scope**: `read:packages`
   - **Cannot verify programmatically**: Token is in home directory (inaccessible to agent)
   - **Document requirement**: Note in output that token must have `read:packages` scope
   - **Test authentication**: Run `npm whoami --registry=https://npm.pkg.github.com` (optional)

4. **Component Library Package Detection**: Verify package name and latest version
   - **Default package**: `@RoyalAholdDelhaize/pdl-spectrum-component-library-web`
   - **Check if specified**: Look for custom package name in configuration
   - **Fetch version**: Run `npm view @RoyalAholdDelhaize/pdl-spectrum-component-library-web version --registry=https://npm.pkg.github.com`
   - **If fails**: Token authentication issue or package doesn't exist

5. **Verify .npmrc Format**: Check if npm still supports current format
   - **Current format**: `@scope:registry=https://npm.pkg.github.com`
   - **Run**: `npm config get @RoyalAholdDelhaize:registry` to test format
   - **Alternative formats**: Check npm documentation for any new syntax
   - **Backward compatibility**: Ensure format works with npm 8+, 9+, 10+

6. **Gitignore Verification**: Ensure `.npmrc` will NOT be committed with tokens
   - **Check `.gitignore`**: Verify `.npmrc` is listed (if tokens were to be embedded)
   - **Current approach**: `.npmrc` uses home directory token (no local token storage)
   - **Safe to commit**: File only contains registry configuration, not tokens
   - **Validation**: `.npmrc` should NOT contain `_authToken` line

7. **Organization Scope Detection**: Verify organization scope is correct
   - **Default**: `@RoyalAholdDelhaize`
   - **Check configuration**: Look for `project_scope` parameter
   - **Derive from package name**: Extract organization from component library package
   - **Example**: `@RoyalAholdDelhaize/package-name` → scope is `@RoyalAholdDelhaize`

## Execution Checklist

Execute in this order:

- [ ] 0. **CONDITIONAL CHECK**: Verify `include_component_library: yes` (EXIT if no)
- [ ] 1. Verify GitHub Packages registry URL is current (`https://npm.pkg.github.com`)
- [ ] 2. Check if token exists in `~/.npmrc` (warn if missing)
- [ ] 3. Document required token scope (`read:packages`)
- [ ] 4. Verify component library package exists and is accessible
- [ ] 5. Confirm `.npmrc` format is still supported by npm
- [ ] 6. Verify `.npmrc` will not contain embedded tokens (safe to commit)
- [ ] 7. Detect organization scope from configuration or package name
- [ ] 8. Generate `.npmrc` with registry configuration only
- [ ] 9. Run validation script to confirm file format and accessibility

## Output

### Primary Format: `.npmrc`

**For @RoyalAholdDelhaize Organization** (default):
```
@RoyalAholdDelhaize:registry=https://npm.pkg.github.com
```

**For Custom Organization** (adapt as needed):
```
@YourOrganization:registry=https://npm.pkg.github.com
```

**For Multiple Scopes** (advanced):
```
@RoyalAholdDelhaize:registry=https://npm.pkg.github.com
@AnotherOrg:registry=https://npm.pkg.github.com
```

**⚠️ CRITICAL - What NOT to Include:**
```
# ❌ NEVER include authToken in project .npmrc
# //npm.pkg.github.com/:_authToken=${TOKEN}  # WRONG - Security risk!

# ✅ Token should ONLY be in ~/.npmrc (user home directory)
```

## 🛑 BLOCKING VALIDATION - MUST RUN AFTER FILE GENERATION

### Validation Script

Run this script after generating `.npmrc` to verify correctness:

```bash
#!/bin/bash
# NPM RC Validation Script

echo "🔍 Validating .npmrc..."

# Check if file exists
if [ ! -f ".npmrc" ]; then
  echo "❌ BLOCKING ERROR: .npmrc file not found"
  exit 1
fi

# Check if file is not empty
if [ ! -s ".npmrc" ]; then
  echo "❌ BLOCKING ERROR: .npmrc is empty"
  exit 1
fi

# Check for GitHub registry URL
if ! grep -q "npm.pkg.github.com" .npmrc; then
  echo "❌ BLOCKING ERROR: GitHub Packages registry URL not found"
  exit 1
fi

# Check for organization scope
if ! grep -qE "@[a-zA-Z0-9_-]+:registry=" .npmrc; then
  echo "❌ BLOCKING ERROR: Organization scope not configured"
  exit 1
fi

# CRITICAL: Verify no embedded tokens in file
if grep -q "_authToken" .npmrc; then
  echo "❌ BLOCKING ERROR: Token found in .npmrc - SECURITY RISK!"
  echo "⚠️  Tokens should only be in ~/.npmrc, not project .npmrc"
  exit 1
fi
# Check if ~/.npmrc exists (without reading contents)
if [ ! -f ~/.npmrc ]; then
  echo "⚠️  WARNING: ~/.npmrc file not found"
  echo "ℹ️  Component library installation may fail"
  echo "ℹ️  Configure GitHub PAT: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry"
else
  echo "ℹ️  ~/.npmrc exists - assuming GitHub authentication configured"
  echo "ℹ️  Ensure token has 'read:packages' scope"
fi

# Test npm config reading
REGISTRY=$(npm config get @RoyalAholdDelhaize:registry)
if [ "$REGISTRY" != "https://npm.pkg.github.com" ] && [ "$REGISTRY" != "https://npm.pkg.github.com/" ]; then
  echo "⚠️  WARNING: Registry configuration not detected by npm"
fi

echo "✅ .npmrc validation passed"
exit 0
```

**Usage**: `bash validate-npmrc.sh`

### Manual Verification

After generation, manually verify:

1. **Home config exists**: `test -f ~/.npmrc && echo "Configured" || echo "Not configured"`
2. **Content check**: `cat .npmrc` (should only show registry, no tokens)
3. **No tokens embedded**: `grep "_authToken" .npmrc` (should return nothing)
4. **Registry config**: `npm config get @RoyalAholdDelhaize:registry` (should return GitHub URL)
5. **Test authentication**: `npm whoami --registry=https://npm.pkg.github.com` (should show username)

## Template
See: `examples.md` in this directory for complete examples and adaptation guide.

## Key Features
- **Conditional Execution**: Only runs when component library is requested
- **Token-Free**: Uses home directory token (`~/.npmrc`), not embedded in project
- **Safe to Commit**: File contains only registry configuration
- **Organization-Specific**: Configured for @RoyalAholdDelhaize but easily adaptable
- **Multi-Scope Support**: Can configure multiple GitHub organizations
- **Security-First**: Never stores tokens in project files

### Token Security
- **Home Directory Only**: Token stored in `~/.npmrc` (user-level)
- **Never Commit Tokens**: Project `.npmrc` has no authentication credentials
- **Required Scope**: `read:packages` for installing private packages
- **Token Validation**: Cannot verify home token programmatically (security by design)
- **User Responsibility**: Users must configure their own GitHub PAT

### Configuration Strategy
- **Registry Only**: Project `.npmrc` maps scope to registry endpoint
- **Authentication Separate**: npm automatically uses `~/.npmrc` token for authentication
- **No Environment Variables**: Token not needed in .env files

### Organization Adaptation
To adapt for different organizations:
```
# Change from:
@RoyalAholdDelhaize:registry=https://npm.pkg.github.com

# To your organization:
@YourOrgName:registry=https://npm.pkg.github.com
```

Extract organization from `project_scope` or component library package name.

### Integration Considerations
- **npm install**: Automatically uses configured registry for scoped packages
- **CI/CD**: Requires GitHub token in pipeline secrets (separate configuration)
- **Team Setup**: Each developer needs personal access token in `~/.npmrc`
- **Package Resolution**: Unscoped packages still use public npm registry

### Maintenance Considerations
- **GitHub URL Changes**: Verify registry URL hasn't changed (rare but possible)
- **npm Format Updates**: Check if scope syntax changes in npm major versions
- **Token Rotation**: Users must update `~/.npmrc` when rotating PATs
- **Package Migration**: If component library moves, update organization scope
