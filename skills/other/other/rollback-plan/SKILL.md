---
name: vibe-rollback-plan
description: Documents rollback procedures before making risky changes. Covers what's changing, verification steps, rollback procedures, and blast radius assessment.
user-invocable: true
---

# vibe-rollback-plan

The time to plan a rollback is BEFORE you need one.

## When to Use This Skill

- Database migrations (especially destructive ones)
- API breaking changes
- Infrastructure changes (networking, permissions, DNS)
- Large dependency upgrades
- Any change where "undo" isn't obvious

## When NOT to Use This Skill

- Safe, easily reversible changes (adding a new file, adding a feature flag)
- Changes with automated rollback (CI/CD with rollback built in)
- Local development changes

## Steps

1. **Document the change**:
   - What is being changed?
   - Why is it being changed?
   - What systems are affected?

2. **Define success criteria**:
   - How do we know the change worked?
   - What metrics to watch?
   - How long to monitor before declaring success?

3. **Assess blast radius**:
   - What breaks if this fails?
   - Which users/services are affected?
   - Is there data loss risk?

4. **Write rollback procedure**:
   - Step-by-step commands to reverse the change
   - Expected time to rollback
   - Who needs to be notified?

5. **Pre-change checklist**:
   - [ ] Rollback procedure documented
   - [ ] Rollback tested (if possible)
   - [ ] Monitoring in place
   - [ ] Team notified
   - [ ] Backup taken

## Output Format

### Rollback Plan: [Change Name]

**Change**: [Description]
**Risk Level**: Low / Medium / High / Critical
**Blast Radius**: [What's affected]
**Estimated Recovery Time**: [Time to rollback]

### Success Criteria
1. [How to verify the change worked]

### Rollback Procedure
```bash
# Step 1: [Description]
[command]
# Step 2: [Description]
[command]
```

### Pre-Change Checklist
- [ ] Backup taken
- [ ] Rollback tested
- [ ] Monitoring active
- [ ] Team notified
