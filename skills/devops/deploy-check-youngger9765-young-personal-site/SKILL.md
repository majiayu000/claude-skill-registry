---
name: deploy-check
description: |
  Pre-deployment verification for young-personal-site.
  Ensures build success, TypeScript, i18n sync, and functionality.
allowed-tools: [Bash, Read, Grep]
activation-keywords: [deploy, 部署, push, 推送, publish, 發布, 上線, vercel, build, release]
priority: critical
---

# Deploy Check

## Purpose
Prevent shipping broken code to production.

**Checks**:
- ✅ Build succeeds
- ✅ TypeScript compiles
- ✅ i18n synchronized (zh-TW ↔ en)
- ✅ No critical errors

---

## Quick Checklist

### 1. Build Verification
```bash
npm run build
```

**Must pass**:
- [ ] Build completes (no errors)
- [ ] No TypeScript errors
- [ ] All routes generated

**Common issues**:
- Type errors → Fix TypeScript types
- Module not found → Check imports
- Image optimization → Check file sizes

---

### 2. TypeScript Check
```bash
npx tsc --noEmit
```

**Must pass**:
- [ ] Zero type errors
- [ ] All components typed correctly

---

### 3. i18n Synchronization
```bash
# Invoke i18n-sync skill
Skill(skill="i18n-sync")
```

**Must pass**:
- [ ] messages/zh-TW.json valid
- [ ] messages/en.json valid
- [ ] All keys synchronized
- [ ] No missing translations

**Auto-fix**:
If i18n-sync fails, it will report missing keys. Fix before deploying.

---

### 4. Route Accessibility

**Test both locales**:
```
zh-TW:
- [ ] /zh-TW (home)
- [ ] /zh-TW/projects
- [ ] /zh-TW/speaking
- [ ] /zh-TW/about

en:
- [ ] /en (home)
- [ ] /en/projects
- [ ] /en/speaking
- [ ] /en/about
```

**Quick test**:
```bash
npm run dev
# Visit each route manually
```

---

### 5. Responsive Design

**Test viewports**:
- [ ] Mobile (375px)
- [ ] Tablet (768px)
- [ ] Desktop (1440px)

**Key checks**:
- Navigation works on all sizes
- Images scale correctly
- Text readable (no overflow)

---

## Deployment Flow

```yaml
1. Pre-deployment checks:
   - Run this skill (deploy-check)
   - Fix any failures

2. Commit and push:
   - git add .
   - git commit -m "feat: description"
   - git push

3. Vercel auto-deploys:
   - Monitor build logs
   - Check deployment URL

4. Post-deployment:
   - Verify production site
   - Test both languages
   - Check all critical pages
```

---

## Integration

**Works with**:
- `i18n-sync` - Translation validation
- `content-update` - Content changes
- Git hooks - Auto-check before push

**Invoked by**:
- BeforePush hook (recommended)
- Manual: `/deploy-check` command
- Auto: Keywords (deploy, push, 部署)

---

## Common Failures

### Build Fails
```
Error: Type 'X' is not assignable to type 'Y'
→ Fix TypeScript types
→ Re-run: npm run build
```

### i18n Mismatch
```
Missing in en.json: projects.newproject.title
→ Add translation key
→ Re-run: Skill(skill="i18n-sync")
```

### Route 404
```
Page /speaking/event-slug not found
→ Check dynamic routes
→ Verify slug naming
```

---

## Emergency Skip

**ONLY if absolutely necessary**:
```bash
# Skip pre-deployment checks (NOT RECOMMENDED)
git push --no-verify
```

**When to skip**:
- ⚠️ Hotfix for critical production bug
- ⚠️ Content-only change (no code)
- ⚠️ Emergency security patch

**Never skip for**:
- ❌ New features
- ❌ Refactoring
- ❌ Dependencies update

---

## Success Output

```
✅ Deploy Check: PASS

Build: ✅ Success (3.2s)
TypeScript: ✅ No errors
i18n: ✅ Synchronized (zh-TW ↔ en)
Routes: ✅ All accessible

🚀 Ready to deploy!
```

---

**Version**: 2.0 (Simplified)
**Project**: young-personal-site
**Last Updated**: 2024-12-31
