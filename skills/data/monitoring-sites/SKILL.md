---
name: monitoring-sites
description: Use this skill for monitoring website health, checking uptime, SSL certificates, performance, or managing client site portfolio. Runs health checks across all managed sites, alerts on issues, and tracks site status. Invoke for site monitoring, health checks, uptime verification, or portfolio status reviews.
---

# Site Monitoring System

Monitor health and status of all managed client sites.

## Managed Sites Portfolio

| Site | Platform | Hosting | Profile | Status Page |
|------|----------|---------|---------|-------------|
| support-forge.com | Next.js | GCP Cloud Run | support-forge | - |
| vineyardvalais.com | Next.js | Amplify | default | - |
| witchsbroomcleaning.com | Static | S3/CloudFront | default | - |
| sweetmeadow-bakery.com | Next.js | Amplify | sweetmeadow | - |
| homebasevet.com | Static | S3 | default | - |
| jpbailes.com | Next.js | GCP Cloud Run | support-forge | - |

## Quick Health Check

### All Sites Status
```bash
# Quick ping check for all sites
for site in support-forge.com vineyardvalais.com witchsbroomcleaning.com sweetmeadow-bakery.com homebasevet.com jpbailes.com; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "https://$site")
  echo "$site: $status"
done
```

### Individual Site Check
```bash
# Full health check for single site
SITE="support-forge.com"

# HTTP Status
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "https://$SITE"

# Response time
curl -s -o /dev/null -w "Response Time: %{time_total}s\n" "https://$SITE"

# SSL Check
echo | openssl s_client -servername $SITE -connect $SITE:443 2>/dev/null | openssl x509 -noout -dates

# DNS Check
nslookup $SITE
```

## Health Check Checklist

### Daily Checks (Automated)
```
□ All sites responding (200 OK)
□ SSL certificates valid
□ Response time < 3 seconds
□ No error pages
```

### Weekly Checks
```
□ SSL expiry > 14 days
□ Domain expiry checked
□ Backup verification
□ Performance review
□ Error log review
```

### Monthly Checks
```
□ Full performance audit
□ Security scan
□ Content freshness
□ Analytics review
□ Hosting costs review
```

## Site-Specific Details

### support-forge.com
```
Type: Next.js Monorepo (Docker)
Hosting: GCP Cloud Run
Project: support-forge
Region: us-central1
Direct URL: https://support-forge-301352865144.us-central1.run.app

Deploy:
cd ~/support-forge-app
gcloud run deploy support-forge --source . --region us-central1 --allow-unauthenticated --project support-forge

Health Endpoints:
- https://support-forge.com (main)
- https://support-forge.com/client-setup/index.html

DR Backup: EC2 ({LEGACY_EC2_IP}) - Legacy, deprecated
DR Plan: ~/support-forge-app/Support_Forge_DR_Plan.pdf
```

### vineyardvalais.com
```
Type: Next.js
Hosting: AWS Amplify
Profile: default
App ID: [check Amplify console]

Deploy: Push to main branch (auto-deploy)

Check Status:
aws amplify list-apps --profile default
```

### witchsbroomcleaning.com
```
Type: Static HTML
Hosting: S3 + CloudFront
Profile: default
Bucket: [check S3]

Deploy: aws s3 sync ./dist s3://[bucket] --profile default
Invalidate: aws cloudfront create-invalidation --distribution-id [id] --paths "/*"
```

### sweetmeadow-bakery.com
```
Type: Next.js
Hosting: AWS Amplify
Profile: sweetmeadow
App ID: dqa0p0t9xllsd

Deploy: Push to main branch (auto-deploy)

Check Status:
aws amplify get-app --app-id dqa0p0t9xllsd --profile sweetmeadow
```

### homebasevet.com
```
Type: Static
Hosting: S3
Profile: default
Bucket: homebasevet-staging

Deploy: aws s3 sync ./dist s3://homebasevet-staging --profile default
```

### jpbailes.com / me.jbailes.com
```
Type: Next.js
Hosting: GCP Cloud Run
Project: support-forge
Region: us-central1
Service: jpbailes
Direct URL: https://jpbailes-301352865144.us-central1.run.app

Deploy:
cd ~/me.jbailes.com
gcloud run deploy jpbailes --source . --region us-central1 --allow-unauthenticated --project support-forge

DR Backup: Render.com (jpbailes.onrender.com)
DR Plan: ~/me.jbailes.com/JPbailes_DR_Plan.md
```

## SSL Certificate Monitoring

### Check SSL Expiry
```bash
# Check single site
echo | openssl s_client -servername support-forge.com -connect support-forge.com:443 2>/dev/null | openssl x509 -noout -enddate

# Check all sites
for site in support-forge.com vineyardvalais.com witchsbroomcleaning.com sweetmeadow-bakery.com homebasevet.com jpbailes.com; do
  expiry=$(echo | openssl s_client -servername $site -connect $site:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$site: $expiry"
done
```

### SSL Renewal
- **Amplify sites**: Auto-renewed by AWS
- **S3/CloudFront**: ACM auto-renews
- **EC2 (support-forge.com)**: Let's Encrypt via certbot
  ```bash
  # On EC2 server
  sudo certbot renew
  docker-compose restart nginx
  ```

## Performance Monitoring

### PageSpeed Check
```
Sites to check monthly:
1. https://pagespeed.web.dev/analysis?url=https://support-forge.com
2. https://pagespeed.web.dev/analysis?url=https://vineyardvalais.com
3. https://pagespeed.web.dev/analysis?url=https://witchsbroomcleaning.com
4. https://pagespeed.web.dev/analysis?url=https://sweetmeadow-bakery.com
5. https://pagespeed.web.dev/analysis?url=https://homebasevet.com
```

### Target Metrics
| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time | < 1s | 1-3s | > 3s |
| TTFB | < 200ms | 200-600ms | > 600ms |
| LCP | < 2.5s | 2.5-4s | > 4s |
| PageSpeed Score | > 90 | 70-90 | < 70 |

## Uptime Monitoring (Free Tools)

### UptimeRobot (Recommended)
- **URL**: https://uptimerobot.com
- **Free tier**: 50 monitors, 5-min intervals
- **Setup**: Add all sites with email alerts

### Freshping
- **URL**: https://www.freshworks.com/website-monitoring/
- **Free tier**: 50 monitors, 1-min intervals

### StatusCake
- **URL**: https://www.statuscake.com
- **Free tier**: 10 monitors

## Error Monitoring

### Check Error Logs

**EC2 (support-forge.com)**:
```bash
ssh -i ~/.ssh/support-forge-key.pem ubuntu@{LEGACY_EC2_IP}
docker-compose logs --tail=100 web
docker-compose logs --tail=100 nginx
```

**Amplify Sites**:
```bash
# Check build logs
aws amplify list-jobs --app-id [APP_ID] --branch-name main --profile [PROFILE]
```

### Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Site down | 502/503 error | Restart containers/services |
| SSL error | Certificate warning | Renew SSL cert |
| Slow load | > 3s response | Check server resources, optimize |
| 404 errors | Broken links | Fix links or add redirects |
| Build failed | Amplify error | Check build logs, fix code |

## Incident Response

### Site Down Protocol
```
1. VERIFY
   - Check from multiple locations
   - Confirm not local network issue

2. IDENTIFY
   - Check server status
   - Review error logs
   - Check recent deployments

3. COMMUNICATE
   - Notify client if extended outage
   - Update status if applicable

4. RESOLVE
   - Apply fix
   - Verify site is back

5. DOCUMENT
   - Log incident
   - Root cause analysis
   - Prevention measures
```

### Quick Restart Commands

**EC2 Docker (support-forge.com)**:
```bash
ssh -i ~/.ssh/support-forge-key.pem ubuntu@{LEGACY_EC2_IP}
cd /home/ubuntu/support-forge-app
docker-compose restart
# or full rebuild:
docker-compose down && docker-compose up -d --build
```

**Amplify (trigger redeploy)**:
```bash
aws amplify start-job --app-id [APP_ID] --branch-name main --job-type RELEASE --profile [PROFILE]
```

## Status Dashboard Template

```
SITE STATUS DASHBOARD
=====================
Last Updated: [Timestamp]

SITE                      STATUS    RESPONSE   SSL EXPIRY
─────────────────────────────────────────────────────────
support-forge.com         ✓ UP      0.8s       45 days
vineyardvalais.com        ✓ UP      1.2s       90 days
witchsbroomcleaning.com   ✓ UP      0.5s       60 days
sweetmeadow-bakery.com    ✓ UP      1.1s       90 days
homebasevet.com           ✓ UP      0.4s       30 days
jpbailes.com              ✓ UP      0.9s       90 days

RECENT INCIDENTS
────────────────
[Date] - [Site] - [Issue] - [Resolution]

UPCOMING MAINTENANCE
────────────────────
[Date] - [Site] - [Planned work]
```

## Quick Commands

**"Check all sites"**
→ Run health check on entire portfolio

**"Status of [domain]"**
→ Detailed status for single site

**"SSL expiry check"**
→ Check SSL certificates for all sites

**"Restart [site]"**
→ Restart/redeploy specific site

**"Performance report"**
→ Run PageSpeed checks on all sites
