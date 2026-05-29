---
name: dependency
description: Dependency management and technology selection. Apply when introducing new libraries, choosing technologies, or managing package versions.
---

# Dependency Management & Technology Selection

## Build vs Buy Decision Tree

```
┌─ Is this core business logic?
│  ├─ Yes → Build (keep control)
│  └─ No → ↓
│
├─ Is there a mature, well-maintained library?
│  ├─ Yes → Use library
│  └─ No → ↓
│
├─ Would building it take > 2 days?
│  ├─ Yes → Find alternative or build
│  └─ No → Build (simpler than integrating)
```

**Golden Rule**: Only build when you need competitive advantage. Everything else, use proven solutions.

## Library Evaluation Criteria

Before adding ANY dependency, verify:

1. **Maintenance Health**
   - ✅ Last commit within 6 months
   - ✅ Issues are being addressed
   - ✅ No major open bugs related to your use case

2. **Ecosystem Health**
   - ✅ GitHub stars > 100 (for general libs)
   - ✅ Weekly downloads > 10k (for npm)
   - ✅ No known security vulnerabilities (run `npm audit` or `snyk`)

3. **Bundle Size**
   - ⚠️ Is this library adding > 50KB minified?
   - ⚠️ Does it have tree-shaking support?
   - ⚠️ Can you use a smaller alternative?

4. **API Stability**
   - ✅ Has stable v1.0+ release
   - ❌ Avoid libraries with 0.x.x versions (unstable)

## Dependency Categories

| Type | Strategy |
|------|----------|
| **Utility libraries** (lodash, date-fns) | Use, but prefer modern alternatives (native APIs, smaller libs) |
| **UI frameworks/components** (React, shadcn/ui) | Standardize, don't mix |
| **Backend SDKs** (Stripe, AWS SDK) | Use official SDKs, never unofficial |
| **Dev dependencies** | Minimize, remove unused |
| **Polyfills** | Avoid, target modern browsers |

## Version Management

1. **Use semantic versioning strictly**
   - `^1.2.3` → Accept 1.x.x updates (patch + minor)
   - `~1.2.3` → Accept 1.2.x updates (patch only)
   - `1.2.3` → Exact version (for critical deps)

2. **Lock files are sacred**
   - Commit `package-lock.json`, `yarn.lock`, `poetry.lock`
   - Never manually edit lock files
   - Same lock file across all environments

3. **Update strategy**
   ```bash
   # Monthly: Check for security updates
   npm audit

   # Quarterly: Minor version updates
   npm update

   # Yearly: Major version updates (requires testing)
   # Example: Upgrade React 18 → 19
   ```

## When to Avoid Dependencies

❌ **Don't add if**:
- It's 5 lines of code you can write yourself
- You only use 10% of a large library
- There's no clear migration path if it's abandoned
- It adds unnecessary complexity

✅ **Do add if**:
- It's a well-solved problem (date parsing, validation)
- It's security-sensitive (crypto, auth)
- It has active community and documentation

## Security Checklist

Before merging any PR with new dependencies:

- [ ] Run security audit: `npm audit` / `pip-audit`
- [ ] Check for known CVEs in the package
- [ ] Verify maintainer identity (avoid typosquatting)
- [ ] Review license compatibility (MIT, Apache 2.0, BSD preferred)
- [ ] Check if package has been compromised (replaced)

## Package.json Best Practices

```json
{
  "dependencies": {
    "react": "^19.0.0",           // Standard deps
    "@stripe/stripe-js": "^3.0.0" // Scoped packages for official SDKs
  },
  "devDependencies": {
    "typescript": "^5.0.0",       // Dev tools
    "prettier": "^3.0.0"
  },
  "overrides": {
    "minimist": "^1.2.8"         // Force security patch
  },
  "engines": {
    "node": ">=18.0.0"           // Minimum version
  }
}
```

## Removal Strategy

Quarterly dependency audit:
1. List all dependencies: `npm list --depth=0`
2. Identify unused: `npx depcheck`
3. Check each against actual usage in codebase
4. Remove unused: `npm uninstall <package>`
5. Test thoroughly after removal
