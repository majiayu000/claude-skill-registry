---
name: sobriety-tools-guardian
description: Performance optimization and continuous improvement for sobriety.tools recovery app. Use for load time optimization, offline capability, crisis detection, performance monitoring, automated issue detection. Activate on "sobriety.tools", "recovery app perf", "crisis detection", "offline meetings", "HALT check-in", "sponsor contacts". NOT for general Next.js help, unrelated Cloudflare Workers, or non-recovery apps.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,Task,WebFetch
---

# Sobriety Tools Guardian

**Mission**: Keep sobriety.tools fast enough to save lives. A fentanyl addict in crisis has seconds, not minutes. The app must load instantly, work offline, and surface help before they ask.

## Why Performance Is Life-or-Death

```
CRISIS TIMELINE:
0-30 seconds:  User opens app in distress
30-60 seconds: Looking for sponsor number or meeting
60-120 seconds: Decision point - call someone or use
2+ minutes:    If still searching, may give up

EVERY SECOND OF LOAD TIME = LIVES AT RISK
```

**Core truth**: This isn't a business app. Slow performance isn't "bad UX" - it's abandonment during crisis. The user staring at a spinner might be deciding whether to live or die.

## Stack-Specific Optimization Knowledge

### Architecture (Know This Cold)
```
Next.js 15 (static export) → Cloudflare Pages
    ↓
Supabase (PostgREST + PostGIS)
    ↓
Cloudflare Workers:
  - meeting-proxy (KV cached, geohash-based)
  - meeting-harvester (hourly cron)
  - claude-api (AI features)
```

### Critical Performance Paths

**1. Meeting Search (MUST be &lt;500ms)**
```
User location → Geohash (3-char ~150km cell)
    → KV cache lookup (edge, ~5ms)
    → Cache HIT: Return immediately
    → Cache MISS: Supabase RPC find_current_meetings
        → PostGIS ST_DWithin query
        → Store in KV, return
```
**Bottleneck**: Cold Supabase queries. **Fix**: Pre-warm top 30 metros via /warm endpoint.

**2. Sponsor/Contact List (MUST be &lt;200ms)**
```
User opens contacts → Local IndexedDB first
    → Show cached contacts instantly
    → Background sync with Supabase
    → Update UI if changes
```
**Anti-pattern**: Waiting for network before showing contacts. In crisis, show stale data immediately.

**3. Check-in Flow (MUST be &lt;100ms to first input)**
```
Open check-in → Pre-rendered form shell
    → Load previous patterns async
    → Submit optimistically
```

### Offline-First Requirements (NON-NEGOTIABLE)

```typescript
// Service Worker must cache:
const CRISIS_CRITICAL = [
  '/contacts',           // Sponsor phone numbers
  '/safety-plan',        // User's safety plan
  '/meetings?saved=true', // Saved meetings list
  '/crisis',             // Crisis resources page
];

// These MUST work with zero network:
// 1. View sponsor contacts
// 2. View safety plan
// 3. View saved meetings (even if stale)
// 4. Record check-in (sync when online)
```

## Crisis Detection Patterns

### Journal Sentiment Signals
```typescript
// RED FLAGS (surface help proactively):
const CRISIS_INDICATORS = {
  anger_spike: 'HALT angry score jumps 3+ points',
  ex_mentions: 'Mentions ex-partner 3+ times in week',
  isolation: 'No check-ins for 3+ days after daily streak',
  time_distortion: 'Check-ins at unusual hours (2-5am)',
  negative_spiral: 'Consecutive declining mood scores',
};

// When detected: Surface sponsor contact, safety plan link
// DO NOT: Be preachy or alarming. Gentle nudge only.
```

### Check-in Analysis
```sql
-- Detect concerning patterns
SELECT user_id,
  AVG(angry_score) as avg_anger,
  AVG(angry_score) FILTER (WHERE created_at > NOW() - INTERVAL '3 days') as recent_anger,
  COUNT(*) FILTER (WHERE EXTRACT(HOUR FROM created_at) BETWEEN 2 AND 5) as late_night_checkins
FROM daily_checkins
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY user_id
HAVING AVG(angry_score) FILTER (WHERE created_at > NOW() - INTERVAL '3 days') >
       AVG(angry_score) + 2;
```

## Performance Monitoring & Logging

### Key Metrics to Track
```typescript
// Client-side (log to analytics)
const PERF_METRICS = {
  ttfb: 'Time to First Byte',
  fcp: 'First Contentful Paint',
  lcp: 'Largest Contentful Paint',
  tti: 'Time to Interactive',

  // App-specific critical paths
  contacts_visible: 'Time until sponsor list renders',
  meeting_results: 'Time until first meeting card shows',
  checkin_interactive: 'Time until check-in form accepts input',
};

// Log slow paths
if (contactsVisibleTime > 500) {
  logPerf('contacts_slow', { duration: contactsVisibleTime, network: navigator.connection?.effectiveType });
}
```

### Automated Performance Regression Detection
```bash
# scripts/perf-audit.sh - Run in CI
lighthouse https://sobriety.tools/meetings --output=json --output-path=./perf.json
SCORE=$(jq '.categories.performance.score' perf.json)
if (( $(echo "$SCORE < 0.9" | bc -l) )); then
  echo "Performance regression: $SCORE"
  # Create GitHub issue automatically
fi
```

## Automated Issue Detection & Filing

### Background Performance Scanner
```typescript
// Run hourly via Cloudflare Worker cron
async function performanceAudit() {
  const checks = [
    checkMeetingCacheHealth(),
    checkSupabaseQueryTimes(),
    checkStaticAssetSizes(),
    checkServiceWorkerCoverage(),
  ];

  const issues = await Promise.all(checks);
  const problems = issues.flat().filter(i => i.severity === 'high');

  for (const problem of problems) {
    await createGitHubIssue({
      title: `[Auto] Perf: ${problem.title}`,
      body: problem.description + '\n\n' + problem.suggestedFix,
      labels: ['performance', 'automated'],
    });
  }
}
```

## Common Anti-Patterns

### 1. Network-Blocking Contact Display
**Symptom**: Contacts page shows spinner while fetching
**Problem**: User in crisis sees loading state instead of sponsor number
**Solution**:
```typescript
// WRONG
const { data: contacts } = useQuery(['contacts'], fetchContacts);

// RIGHT
const { data: contacts } = useQuery(['contacts'], fetchContacts, {
  initialData: () => getCachedContacts(), // IndexedDB
  staleTime: Infinity, // Never refetch automatically
});
```

### 2. Uncached Meeting Searches
**Symptom**: Every search hits Supabase
**Problem**: 200-500ms latency on every search
**Solution**: Geohash-based KV caching (already implemented in meeting-proxy)

### 3. Large Bundle Blocking Interactivity
**Symptom**: High TTI despite fast TTFB
**Problem**: JavaScript bundle blocks main thread
**Solution**:
```typescript
// Lazy load non-critical features
const JournalAI = dynamic(() => import('./JournalAI'), { ssr: false });
const Charts = dynamic(() => import('./Charts'), { loading: () => <ChartSkeleton /> });
```

### 4. Synchronous Check-in Submission
**Symptom**: Button stays disabled during network request
**Problem**: User thinks it didn't work, closes app
**Solution**: Optimistic UI + background sync queue

## Performance Optimization Checklist

### Before Every Deploy
- [ ] Bundle size delta &lt; 5KB
- [ ] No new synchronous network calls in critical paths
- [ ] Lighthouse performance score &gt;= 90
- [ ] Offline mode tested (disable network in DevTools)

### Weekly Audit
- [ ] Review slow query logs in Supabase
- [ ] Check KV cache hit rate (should be &gt;80%)
- [ ] Analyze Real User Metrics (RUM) for P95 load times
- [ ] Test on 3G throttled connection

### Monthly Deep Dive
- [ ] Profile React renders (why did this re-render?)
- [ ] Audit third-party scripts
- [ ] Review and prune unused dependencies
- [ ] Test crisis flows end-to-end on real device

## Scripts Available

| Script | Purpose |
|--------|---------|
| `scripts/perf-audit.ts` | Run Lighthouse + custom checks, file issues |
| `scripts/cache-health.ts` | Check KV cache hit rates and staleness |
| `scripts/crisis-path-test.ts` | Automated test of crisis-critical flows |
| `scripts/bundle-analyzer.ts` | Track bundle size over time |

## Integration Points

### With meeting-harvester
- After harvest, warm cache for top metros
- Monitor harvest duration and meeting counts
- Alert if harvest fails (stale data = wrong meeting times)

### With check-in system
- Analyze patterns for crisis detection
- Track submission success rate
- Monitor offline queue depth

### With contacts/sponsors
- Ensure offline availability
- Track time-to-display
- Monitor sync failures

## When to Escalate

**File GitHub issue immediately if:**
- Lighthouse score drops below 85
- P95 meeting search > 1 second
- Contacts page has any loading state > 200ms
- Service Worker fails to cache crisis pages
- Any user-reported "couldn't load" during crisis hours (evenings/weekends)

**This is a recovery app. Performance isn't a feature - it's the difference between someone getting help and someone dying alone.**
