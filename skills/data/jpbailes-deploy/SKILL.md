---
description: Deploy jpbailes.com to GCP Cloud Run or trigger Render failover
user_invocable: true
arguments:
  - name: action
    description: "Action: deploy, failover, status, rollback"
    required: false
    default: "deploy"
---

# jpbailes.com Deployment & DR Runbook

## Quick Reference

| Action | Command |
|--------|---------|
| Deploy to GCP | `/jpbailes-deploy deploy` |
| Check status | `/jpbailes-deploy status` |
| Failover to Render | `/jpbailes-deploy failover` |
| Rollback to GCP | `/jpbailes-deploy rollback` |

---

## Standard Deployment (GCP Cloud Run)

### Prerequisites
- gcloud CLI authenticated
- Project: support-forge
- Region: us-central1

### Deploy Steps

1. Navigate to project:
```bash
cd ~/me.jbailes.com
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy jpbailes \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --project support-forge
```

3. Verify deployment:
```bash
curl -I https://jpbailes-301352865144.us-central1.run.app
curl -I https://jpbailes.com
```

---

## Status Check

Check all endpoints:
```bash
echo "=== GCP Cloud Run ==="
curl -sI https://jpbailes-301352865144.us-central1.run.app | head -1

echo "=== Render Backup ==="
curl -sI https://jpbailes.onrender.com | head -1

echo "=== Production Domain ==="
curl -sI https://jpbailes.com | head -1
```

---

## Failover to Render.com

**Use when**: GCP Cloud Run is down or unresponsive

### Step 1: Verify Render is healthy
```bash
curl -I https://jpbailes.onrender.com
```

### Step 2: Update GoDaddy DNS
1. Go to https://dcc.godaddy.com/manage/jpbailes.com/dns
2. Delete A records (216.239.x.x)
3. Add CNAME: @ → jpbailes.onrender.com
4. Wait 5-10 minutes for propagation

### Step 3: Verify failover
```bash
nslookup jpbailes.com
curl -I https://jpbailes.com
```

---

## Rollback to GCP (After Failover)

**Use when**: GCP is restored and you want to return to primary

### Step 1: Verify GCP is healthy
```bash
curl -I https://jpbailes-301352865144.us-central1.run.app
```

### Step 2: Update GoDaddy DNS
1. Go to https://dcc.godaddy.com/manage/jpbailes.com/dns
2. Delete CNAME record
3. Add A records:
   - 216.239.32.21
   - 216.239.34.21
   - 216.239.36.21
   - 216.239.38.21

### Step 3: Verify rollback
```bash
nslookup jpbailes.com
curl -I https://jpbailes.com
```

---

## Local Development

```bash
cd ~/me.jbailes.com
npm run dev     # Start dev server at localhost:3000
npm run build   # Build production
npm run lint    # Run ESLint
```

---

## Troubleshooting

### Build fails on Cloud Run
- Check Dockerfile syntax
- Ensure next.config.ts has `output: 'standalone'`
- Review build logs: `gcloud builds log [BUILD_ID]`

### DNS not resolving
- Check GoDaddy DNS settings
- Verify A records or CNAME is correct
- Wait for TTL to expire (check current TTL)
- Test with: `dig jpbailes.com`

### Contact form broken
- AWS SES may be suspended
- Fallback: Direct users to {YOUR_EMAIL}
- TODO: Implement SendGrid backup

---

## Related Files
- Codebase: `~/me.jbailes.com/`
- DR Plan: `~/me.jbailes.com/JPbailes_DR_Plan.md`
- Project docs: `~/me.jbailes.com/CLAUDE.md`
