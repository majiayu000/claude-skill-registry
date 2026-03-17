---
name: npm-publish
description: Publish @autumnsgrove/groveengine to npm with proper registry swap workflow. Use when releasing a new version of the engine package to npm.
user_invocable: true
---

# npm Publish Skill

Publish `@autumnsgrove/groveengine` to npm while keeping the default registry as GitHub Packages.

## When to Activate

Activate this skill when:
- User says "publish to npm"
- User says "release to npm"
- User says "bump and publish"
- User says "/npm-publish"

## The Workflow

**CRITICAL**: The package.json uses GitHub Packages by default. You MUST swap to npm, publish, then swap BACK.

```
1. Bump version in packages/engine/package.json
2. Swap publishConfig to npm registry
3. Build the package
4. Publish to npm
5. Swap publishConfig BACK to GitHub Packages
6. Commit the version bump
7. Push to remote
```

## Step-by-Step Execution

### Step 1: Bump Version

Edit `packages/engine/package.json`:

```json
"version": "X.Y.Z",  // Increment appropriately
```

Use semantic versioning:
- **MAJOR** (X): Breaking changes
- **MINOR** (Y): New features, backwards compatible
- **PATCH** (Z): Bug fixes, backwards compatible

### Step 2: Swap to npm Registry

**BEFORE** (GitHub Packages - default):
```json
"publishConfig": {
  "registry": "https://npm.pkg.github.com"
},
```

**AFTER** (npm - for publishing):
```json
"publishConfig": {
  "registry": "https://registry.npmjs.org",
  "access": "public"
},
```

### Step 3: Build Package

```bash
cd /Users/autumn/Documents/Projects/GroveEngine/packages/engine
pnpm run package
```

### Step 4: Publish to npm

```bash
npm publish --access public
```

The `prepublishOnly` script runs `pnpm run package` automatically, so this may rebuild.

Verify success with:
```
+ @autumnsgrove/groveengine@X.Y.Z
```

### Step 5: Swap BACK to GitHub Packages

**CRITICAL - DO NOT FORGET THIS STEP**

Change `packages/engine/package.json` back to:

```json
"publishConfig": {
  "registry": "https://npm.pkg.github.com"
},
```

### Step 6: Commit Version Bump

```bash
cd /Users/autumn/Documents/Projects/GroveEngine
git add packages/engine/package.json
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

## Quick Reference Commands

```bash
# From project root:

# 1. Edit version in packages/engine/package.json
# 2. Edit publishConfig to npm registry

# 3. Build and publish
cd packages/engine
pnpm run package
npm publish --access public

# 4. Edit publishConfig back to GitHub

# 5. Commit and push (from project root)
git add packages/engine/package.json
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

## Verification

After publishing, verify on npm:

```bash
npm view @autumnsgrove/groveengine version
```

Or visit: https://www.npmjs.com/package/@autumnsgrove/groveengine

## Troubleshooting

### OTP/2FA Error
```
npm error code EOTP
npm error This operation requires a one-time password
```

**Solution**: Create a granular access token with "Bypass 2FA" enabled:
1. Go to https://www.npmjs.com/settings/autumnsgrove/tokens
2. Generate New Token → Granular Access Token
3. Enable "Bypass 2FA"
4. Set token: `npm config set //registry.npmjs.org/:_authToken=npm_YOUR_TOKEN`

See `AgentUsage/npm_publish.md` for detailed token setup.

### Package Already Published
```
npm error 403 - You cannot publish over the previously published versions
```

**Solution**: You forgot to bump the version. Increment it and try again.

### Wrong Registry in Commit
If you accidentally committed with npm registry, fix it:

```bash
# Edit publishConfig back to GitHub
git add packages/engine/package.json
git commit --amend --no-edit
git push --force-with-lease origin main
```

## Registry Swap Reference

| Registry | publishConfig |
|----------|---------------|
| **GitHub** (default) | `"registry": "https://npm.pkg.github.com"` |
| **npm** (for publish) | `"registry": "https://registry.npmjs.org", "access": "public"` |

## Checklist

Before starting:
- [ ] Decided on new version number
- [ ] All changes committed and pushed

During publish:
- [ ] Version bumped in package.json
- [ ] publishConfig swapped to npm
- [ ] Package built successfully
- [ ] Published to npm (see `+ @autumnsgrove/groveengine@X.Y.Z`)
- [ ] publishConfig swapped BACK to GitHub
- [ ] Version bump committed
- [ ] Pushed to remote

## Related

- `AgentUsage/npm_publish.md` - Token setup and 2FA workaround
- `packages/engine/package.json` - Package configuration
