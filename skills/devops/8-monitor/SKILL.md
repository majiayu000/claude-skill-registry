---
name: monitor
description: Track production app health and catch issues before users complain. Use after deploying, to check app status, or when investigating user reports. Covers error tracking, uptime monitoring, and metrics for non-technical founders.
---

# Monitor

## Monitoring Checklist

```
Basic Monitoring:
- [ ] Uptime monitoring (is site up?)
- [ ] Error tracking (are errors happening?)
- [ ] Performance monitoring (is it slow?)
- [ ] User activity (are people using it?)
- [ ] Critical alerts configured
- [ ] Check dashboard daily
```

See [MONITORING-SETUP.md](MONITORING-SETUP.md) for implementation.

---

## Why Monitor?

**Without monitoring:**
- Users hit errors, you don't know
- Site goes down, you find out from Twitter
- Slow performance, users leave silently
- Security issues, no alert

**With monitoring:**
- Errors show in dashboard immediately
- Get text when site goes down
- See performance degradation
- Catch issues before users complain

**Goal: Know about problems before users tell you.**

---

## Three Essential Monitors

### 1. Is It Up?

**Uptime monitoring** - Pings your app every minute

**Free tools:**
- UptimeRobot (free, 50 monitors)
- Pingdom (limited free tier)
- Vercel/Netlify (built-in for deployed apps)

**Setup:**
```
1. Sign up for UptimeRobot
2. Add monitor for https://yourapp.com
3. Add your email for alerts
4. Get texted if site is down
```

### 2. Are There Errors?

**Error tracking** - Captures JavaScript errors and API failures

**Free tools:**
- Sentry (free tier: 5k errors/month)
- LogRocket (limited free)
- Vercel/Netlify logs (for deployed apps)

**Setup:**
```
Tell AI:
"Add Sentry error tracking:
- Capture all frontend errors
- Capture all API errors
- Include user context
- Send to Sentry dashboard"
```

### 3. Is It Slow?

**Performance monitoring** - Tracks page load times

**Free tools:**
- Vercel Analytics (built-in)
- Google PageSpeed Insights (free)
- Cloudflare Analytics (free tier)

**Setup:**
- Usually automatic with hosting platform
- Check dashboard weekly

---

## What to Monitor

### Critical Metrics

**Must monitor:**
- Site uptime (99%+)
- Error rate (< 1% of requests)
- API response time (< 500ms)
- Page load time (< 3s)

**Nice to have:**
- Active users
- Feature usage
- Conversion rates
- User paths

**For MVP:** Focus on the "must monitor" only.

---

## Setting Up Alerts

**Configure alerts for:**

**Critical (text me immediately):**
- Site is down
- Error rate spike (10x normal)
- Database connection lost
- Payment processing failing

**Important (email within hour):**
- API slow (>2 seconds)
- Error rate elevated (2x normal)
- Disk space low (>80%)

**Informational (daily digest):**
- New errors discovered
- Performance trending down
- Traffic patterns

**Tell AI:**
```
Configure monitoring alerts:
- Critical: Text to [phone]
- Important: Email to [email]
- Send summary: Daily at 9am
```

---

## Daily Monitoring Routine

**5-minute morning check:**

```
Daily Check:
1. Open monitoring dashboard
2. Check uptime (should be 100% yesterday)
3. Check error count (any spikes?)
4. Check performance (slower than usual?)
5. Review any alerts from overnight
```

**If all green:** You're done, 5 minutes.

**If red:** Investigate using debug skill.

---

## Reading Monitoring Dashboards

### Uptime Dashboard

**Green:** Site responding  
**Red:** Site down or slow to respond

**What to check:**
- Uptime percentage (target: 99%+)
- Response time (target: <500ms)
- Recent downtime incidents

### Error Dashboard

**Look for:**
- Error count spikes (sudden jump)
- New error types (didn't see before)
- Affected users (how many hit this?)
- Error frequency (happening a lot?)

**Priority:**
- Affecting many users → High priority
- Blocking key features → High priority
- Edge case error → Lower priority

### Performance Dashboard

**Look for:**
- Load time trending up (getting slower)
- Slow endpoints (which API calls)
- Slow pages (which routes)
- Geographic differences (slow in specific regions)

---

## Error Investigation

**When errors spike:**

```
1. Open error tracking dashboard (Sentry)
2. Find the most frequent error
3. Read error message and stack trace
4. Note: How many users affected?
5. Note: Started when?
6. Check: Did we deploy recently?
```

**Give to AI:**
```
Error in production:
[Paste error message and stack trace]

Affected: [X] users in last [Y] hours
Started: [timestamp]
Recent deploys: [any?]

Please:
1. Explain what's wrong
2. Propose hotfix
3. How to test before deploying
```

---

## User-Reported Issues

**When user reports problem:**

```
User Report Investigation:
1. Can you reproduce it?
2. Check monitoring for errors at that time
3. Check logs for that user
4. Check if others affected
5. Determine severity

Then use debug skill to fix.
```

**Tell AI:**
```
User reported: [issue description]
User: [email or ID]
Timestamp: [when it happened]

Check monitoring and logs for this user at this time.
What errors or issues do you see?
```

---

## Proactive Monitoring

**Catch issues before users:**

**Weekly checks:**
```
Weekly Review:
- [ ] Error trends (going up or down?)
- [ ] Performance trends (slower?)
- [ ] New error types introduced
- [ ] Uptime issues resolved
- [ ] Alert noise (too many false alerts?)
```

**Monthly checks:**
```
Monthly Health:
- [ ] Compare to last month
- [ ] Any degradation?
- [ ] Any improvements?
- [ ] Monitoring gaps (what's not tracked?)
```

---

## Free Monitoring Stack

**Recommended for MVP:**

**Uptime:**
- UptimeRobot (free) - 50 monitors

**Errors:**
- Sentry (free) - 5k errors/month

**Performance:**
- Vercel Analytics (free on Vercel)
- Cloudflare Analytics (free)

**Logs:**
- Platform logs (Vercel, Netlify, Railway)

**Cost: $0/month until you need more.**

---

## When to Upgrade Monitoring

**Upgrade when:**
- Hitting free tier limits
- Need more detailed analytics
- Need faster alert response
- Need advanced features (session replay, etc.)

**Paid tiers (typically $20-50/mo):**
- Sentry Pro ($26/mo)
- LogRocket ($99/mo - session replay)
- DataDog ($15/host/mo)

**For < 1000 users:** Free tiers sufficient.

---

## Common Monitoring Mistakes

| Mistake | Fix |
|---------|-----|
| No monitoring set up | Set up before launch |
| Alert fatigue (too many alerts) | Only alert on critical issues |
| Checking once a month | Check daily (5 minutes) |
| Ignoring trends | Watch for degradation over time |
| No alerts configured | Set up text alerts for downtime |
| Monitoring but not acting | Use monitoring to find and fix issues |

---

## Interpreting Trends

**Good trends:**
- Errors decreasing
- Performance improving
- Uptime stable at 99.9%+

**Warning trends:**
- Errors slowly increasing
- Performance slowly degrading
- Uptime dipping below 99%

**Critical trends:**
- Sudden error spike
- Sudden performance drop
- Multiple downtime incidents

**Action:** Address warning trends before they become critical.

---

## Logging vs Monitoring

**Logging:**
- Records what happened
- For debugging specific issues
- Detailed, verbose
- Review when investigating

**Monitoring:**
- Tracks overall health
- For catching issues early
- High-level metrics
- Review daily

**Both needed:** Monitoring alerts you, logs help debug.

---

## Setting Up Logging

**Tell AI:**
```
Add application logging:
- Log all errors with context
- Log API requests/responses
- Log slow operations (>1s)
- Log authentication events
- Don't log sensitive data

Format: JSON with timestamp, level, message, context
Send to: [Platform logs or external service]
```

**Log levels:**
- ERROR: Something broke
- WARN: Something concerning
- INFO: Normal operations
- DEBUG: Detailed debugging info

**Production:** Log ERROR and WARN only.

---

## Monitoring Integrations

**Third-party services:**

**Payments (Stripe):**
- Failed payments alert
- Refund requests alert
- Subscription cancellations (daily digest)

**Email (SendGrid):**
- Delivery failures alert
- Bounce rate elevated alert
- Spam complaints alert

**Database:**
- Connection pool exhausted
- Slow queries (>1s)
- Disk space low

**Tell AI:**
```
Add monitoring for [service]:
- Alert on failures
- Track success rate
- Log errors with context
```

---

## Incident Response

**When alerts fire:**

```
Incident Response:
1. Acknowledge alert (mark as seen)
2. Assess severity:
   - Critical: Site down, payments failing
   - High: Errors affecting many users
   - Medium: Isolated issues
3. Immediate action:
   - Critical: Hotfix or rollback
   - High: Fix within hours
   - Medium: Fix in next deploy
4. Update users if needed
5. Post-mortem after resolved
```

**Critical incidents:**
```
1. Assess impact (how many affected?)
2. Quick fix or rollback
3. Deploy hotfix
4. Verify fixed
5. Monitor closely for hour
6. Update status page if you have one
```

---

## Success Looks Like

✅ Know about issues before users report them  
✅ Uptime >99.9%  
✅ Errors caught and fixed quickly  
✅ Performance trends stable or improving  
✅ Daily monitoring routine (5 minutes)  
✅ Alerts configured and actionable  
✅ Issues resolved proactively