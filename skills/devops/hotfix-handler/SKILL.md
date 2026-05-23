---
name: hotfix-handler
description: Emergency hotfix and bug resolution skill for Fixlify. Automatically activates when dealing with production bugs, critical issues, emergency fixes, or incident response. Provides systematic approach to rapid bug resolution.
version: 1.0.0
author: Fixlify Team
tags: [hotfix, bugfix, emergency, incident, debugging, production]
---

# Hotfix Handler Skill

You are a senior engineer responding to production incidents and critical bugs for Fixlify.

## Incident Response Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. ASSESS (2 min)                                          │
│     └── Understand impact and scope                         │
│                                                              │
│  2. COMMUNICATE (1 min)                                     │
│     └── Notify stakeholders if severe                       │
│                                                              │
│  3. ISOLATE (5 min)                                         │
│     └── Identify affected code/data                         │
│                                                              │
│  4. FIX (varies)                                            │
│     └── Implement minimal fix                               │
│                                                              │
│  5. VERIFY (5 min)                                          │
│     └── Test fix thoroughly                                 │
│                                                              │
│  6. DEPLOY (10 min)                                         │
│     └── Push to production                                  │
│                                                              │
│  7. MONITOR (30 min)                                        │
│     └── Watch for regression                                │
│                                                              │
│  8. POST-MORTEM (later)                                     │
│     └── Document and prevent recurrence                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Severity Classification

| Severity | Impact | Response Time | Examples |
|----------|--------|---------------|----------|
| **P0** | System down | Immediate | Auth broken, DB down |
| **P1** | Major feature broken | < 1 hour | Payments failing, SMS not sending |
| **P2** | Feature degraded | < 4 hours | Slow queries, UI glitches |
| **P3** | Minor issue | Next sprint | Typos, cosmetic issues |

## Quick Diagnostic Commands

### Check Application Health
```bash
# Check if app is responding
curl -I https://fixlify.app

# Check Supabase
curl -I https://mqppvcrlvsgrsqelglod.supabase.co/rest/v1/

# Check edge function
curl https://mqppvcrlvsgrsqelglod.supabase.co/functions/v1/health
```

### Check Logs
```bash
# Vercel logs (requires CLI)
vercel logs --follow

# Supabase function logs
supabase functions logs send-sms --tail

# Database logs
supabase db logs
```

### Check Recent Deployments
```bash
# Vercel deployments
vercel ls

# Recent commits
git log --oneline -10

# Compare with production
git diff main..HEAD
```

## Debugging Strategies

### 1. Reproduce the Issue
```typescript
// Create minimal reproduction
describe('BUG-XXX: [Description]', () => {
  it('reproduces the issue', async () => {
    // Steps to reproduce
    const result = await functionUnderTest(badInput);
    expect(result).toBe(unexpectedValue); // This should fail showing the bug
  });
});
```

### 2. Binary Search for Breaking Commit
```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>

# Git will checkout commits, test each one
npm test
git bisect good  # or git bisect bad

# Find the culprit
git bisect reset
```

### 3. Database Investigation
```sql
-- Check recent data changes
SELECT * FROM jobs
WHERE updated_at > NOW() - INTERVAL '1 hour'
ORDER BY updated_at DESC
LIMIT 20;

-- Check for data anomalies
SELECT status, COUNT(*)
FROM jobs
GROUP BY status;

-- Check for null values
SELECT COUNT(*)
FROM clients
WHERE organization_id IS NULL;
```

### 4. Frontend Debugging
```typescript
// Add debug logging
console.log('[DEBUG] Component state:', {
  data,
  isLoading,
  error,
  user: user?.id,
  org: organization?.id,
});

// Check React Query state
const queryClient = useQueryClient();
console.log('Query cache:', queryClient.getQueryData(['key']));
```

## Common Bug Patterns

### 1. Organization Isolation Bug
```typescript
// ❌ BUG: Missing organization filter
const { data } = await supabase.from('jobs').select('*');

// ✅ FIX: Add organization filter
const { data } = await supabase
  .from('jobs')
  .select('*')
  .eq('organization_id', organization?.id);
```

### 2. Race Condition
```typescript
// ❌ BUG: Race condition in state update
setItems([...items, newItem]);
saveToDatabase(items); // Uses old items!

// ✅ FIX: Use callback or await
setItems(prev => {
  const updated = [...prev, newItem];
  saveToDatabase(updated);
  return updated;
});
```

### 3. Null/Undefined Error
```typescript
// ❌ BUG: No null check
const name = user.profile.name;

// ✅ FIX: Optional chaining + fallback
const name = user?.profile?.name ?? 'Unknown';
```

### 4. Async/Await Error
```typescript
// ❌ BUG: Missing await
const data = supabase.from('jobs').select('*');
console.log(data); // Promise, not data!

// ✅ FIX: Add await
const { data } = await supabase.from('jobs').select('*');
```

### 5. RLS Policy Bug
```sql
-- ❌ BUG: Policy references wrong column
CREATE POLICY "test" ON jobs
  USING (user_id = auth.uid()); -- Wrong! Jobs don't have user_id

-- ✅ FIX: Use correct organization check
CREATE POLICY "test" ON jobs
  USING (
    organization_id = (
      SELECT organization_id FROM profiles WHERE id = auth.uid()
    )
  );
```

## Hotfix Workflow

### 1. Create Hotfix Branch
```bash
# From main (production)
git checkout main
git pull origin main
git checkout -b hotfix/BUG-XXX-description
```

### 2. Make Minimal Fix
- Only fix the bug
- No refactoring
- No "while we're at it" changes
- Keep diff as small as possible

### 3. Test Thoroughly
```bash
# Run affected tests
npm test -- --grep "BUG-XXX"

# Type check
npm run build

# Manual verification
npm run dev
```

### 4. Deploy
```bash
# Commit with bug reference
git add -A
git commit -m "fix: [BUG-XXX] description of fix"

# Push and create PR
git push origin hotfix/BUG-XXX-description

# If P0/P1, merge immediately after review
# Then deploy
```

### 5. Rollback if Needed
```bash
# Vercel rollback
vercel rollback

# Database rollback (if migration was involved)
# Run rollback SQL from migration file
```

## Post-Mortem Template

```markdown
# Incident Post-Mortem: [Title]

## Summary
- **Date**: YYYY-MM-DD
- **Duration**: X hours
- **Severity**: P0/P1/P2
- **Impact**: [Number of users affected, functionality impacted]

## Timeline
- HH:MM - Issue reported
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Issue resolved

## Root Cause
[Technical explanation of what went wrong]

## Resolution
[What was done to fix it]

## Lessons Learned
### What went well
- [Item 1]

### What could be improved
- [Item 1]

## Action Items
- [ ] [Action 1] - Owner - Due date
- [ ] [Action 2] - Owner - Due date

## Prevention
[How to prevent this from happening again]
```

## Emergency Contacts

- **Primary On-Call**: [Contact info]
- **Supabase Support**: support@supabase.io
- **Vercel Support**: support@vercel.com
- **Stripe Support**: [Dashboard support]

## Quick Reference

### Rollback Commands
```bash
# Vercel rollback
vercel rollback

# Git revert last commit
git revert HEAD
git push origin main

# Revert specific commit
git revert <commit-hash>
```

### Feature Flag (Emergency Disable)
```typescript
// Quick feature toggle
const FEATURE_FLAGS = {
  SMS_ENABLED: false, // Disable temporarily
  EMAIL_ENABLED: true,
};

// Usage
if (FEATURE_FLAGS.SMS_ENABLED) {
  await sendSMS(message);
}
```

### Emergency Maintenance Mode
```typescript
// Add to App.tsx for emergency
const MAINTENANCE_MODE = false;

if (MAINTENANCE_MODE) {
  return <MaintenancePage />;
}
```
