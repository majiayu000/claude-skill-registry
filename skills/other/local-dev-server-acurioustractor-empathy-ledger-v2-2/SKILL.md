---
name: local-dev-server
description: Local dev server management — start, stop, clean restart, fix cache corruption, port conflicts. Use this skill whenever the dev server needs launching or is misbehaving.
---

# Local Dev Server

## When to Use
- Starting/stopping dev server
- "Address already in use" errors
- Infinite loading spinner / broken pages after build
- `.next` cache corruption (vendor-chunks ENOENT, 404 on static chunks)
- Server crashes and needs restart
- After major code changes or branch switches

## Standard Start (Clean)

Always prefer a clean start to avoid stale cache issues:

```bash
# 1. Kill any existing process on port 3030
lsof -ti:3030 | xargs kill -9 2>/dev/null

# 2. Clean .next cache (prevents stale vendor-chunk errors)
rm -rf .next

# 3. Start dev server in background
npx next dev -p 3030 &

# 4. Wait for ready, then verify
sleep 8 && curl -s -o /dev/null -w "%{http_code}" http://localhost:3030
```

First page load after clean start takes ~20-30s to compile. This is normal.

## Quick Restart (No Cache Clean)

Only use when you know the cache is fine (small code edits):

```bash
lsof -ti:3030 | xargs kill -9 2>/dev/null
npx next dev -p 3030 &
```

## PM2 (Persistent Server)

For long sessions where server should auto-restart on crash:

```bash
# Start
pm2 start npm --name "empathy-ledger" -- run dev

# Restart
pm2 restart empathy-ledger

# Clean restart (fixes cache issues)
pm2 stop empathy-ledger && rm -rf .next && pm2 start empathy-ledger

# Logs
pm2 logs empathy-ledger --lines 50

# Stop
pm2 stop empathy-ledger
```

## Troubleshooting

### Infinite spinner / blank page
```bash
# Cache corruption — clean restart fixes it
lsof -ti:3030 | xargs kill -9 2>/dev/null
rm -rf .next
npx next dev -p 3030 &
```

### Port already in use
```bash
lsof -ti:3030 | xargs kill -9 2>/dev/null
npx next dev -p 3030 &
```

### API returns 401 when it shouldn't
- Check browser has valid session cookies
- Try logging out and back in at `/auth/signin`
- The API auth middleware reads cookies — curl without cookies will always 401

### Vendor-chunks ENOENT / 404 on static chunks
```bash
rm -rf .next
# Restart server
```

## Verification Checklist

After starting the server, verify:
1. `curl -s -o /dev/null -w "%{http_code}" http://localhost:3030` returns `200` or `307`
2. Navigate to target page in browser
3. Check server logs for compilation errors

## Key URLs
- Homepage: http://localhost:3030
- Admin: http://localhost:3030/admin
- Data Health: http://localhost:3030/admin/data-health
- Storytellers: http://localhost:3030/admin/storytellers

## Related Skills
- `deployment-workflow` — Production deployment
- `supabase-connection` — Database setup
