---
name: environment-ops
description: Skill from Parlay-Kei/stratanoble-site
---

# Environment Operations Skill

**Purpose:** Manage environment variables and configurations across all platforms
**Version:** 1.0.0
**Created:** 2025-11-06

---

## What This Skill Does

This skill provides comprehensive environment and configuration management:

- **Configuration Sync:** Keep env vars in sync across Vercel, Railway, Supabase
- **Secret Management:** Secure handling of API keys and credentials
- **Configuration Validation:** Ensure all required variables are present
- **Drift Detection:** Identify configuration mismatches
- **Auto-Correction:** Fix configuration issues automatically

---

## When to Use This Skill

Use this skill when you need to:

- ✅ Sync environment variables across platforms
- ✅ Validate configuration before deployment
- ✅ Fix missing or incorrect environment variables
- ✅ Detect configuration drift
- ✅ Rotate API keys and secrets
- ✅ Audit security configurations

---

## Key Capabilities

### 1. Environment Variable Management

**Get All Environment Variables:**
```typescript
const envVars = await getAllEnvironmentVariables();

// Returns:
{
  vercel: {
    OPENAI_API_KEY: 'sk-proj-***',
    TWILIO_ACCOUNT_SID: 'AC***',
    // ... other vars
  },
  railway: {
    OPENAI_API_KEY: 'sk-proj-***',
    PORT: '3001',
    // ... other vars
  },
  supabase: {
    SUPABASE_URL: 'https://***',
    // ... other vars
  }
}
```

**Set Environment Variable:**
```typescript
const result = await setEnvironmentVariable({
  platform: 'railway',
  key: 'OPENAI_API_KEY',
  value: 'sk-proj-new-key-here',
  encrypt: true
});

// Returns:
{
  set: true,
  platform: 'railway',
  key: 'OPENAI_API_KEY',
  requiresRestart: true
}
```

### 2. Configuration Sync

**Sync Environment Variables:**
```typescript
const sync = await syncEnvironmentVariables({
  source: '.env.production',
  targets: ['vercel', 'railway'],
  dryRun: false
});

// Returns:
{
  synced: {
    vercel: ['OPENAI_API_KEY', 'TWILIO_AUTH_TOKEN'],
    railway: ['OPENAI_API_KEY', 'SUPABASE_SERVICE_ROLE_KEY']
  },
  conflicts: [],
  requiresRestart: ['railway']
}
```

**Detect Configuration Drift:**
```typescript
const drift = await detectConfigurationDrift();

// Returns:
{
  driftDetected: true,
  differences: [
    {
      key: 'OPENAI_API_KEY',
      vercel: 'sk-proj-old',
      railway: 'sk-proj-new',
      recommendation: 'Update Vercel to match Railway'
    }
  ]
}
```

---

## Quick Reference

```bash
# CLI Commands
ops-cli env list                    # List all env vars
ops-cli env sync                    # Sync across platforms
ops-cli env validate                # Validate configuration
ops-cli env set KEY=value           # Set variable
ops-cli env rotate OPENAI_API_KEY   # Rotate key
ops-cli env audit                   # Security audit
```

---

**Last Updated:** 2025-11-06
**Maintained By:** Production Ops Team
