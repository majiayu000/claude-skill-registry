---
name: ip-lookup
description: Check an IP address across multiple public geolocation and reputation sources and return a best-matched location summary.
---

# IP Lookup Skill

Purpose
- Query multiple public IP information providers and aggregate results to produce a concise, best-match location and metadata summary for an IP address.

What it does
- Queries at least four public sources (e.g. ipinfo.io, ip-api.com, ipstack, geoip-db, db-ip, ipgeolocation.io) or their free endpoints.
- Normalises returned data (country, region, city, lat/lon, org/ASN) and computes a simple match score.
- Returns a compact summary with the best-matched source and a short table of the other sources.

Notes
- Public APIs may have rate limits or require API keys for high volume; the skill falls back to free endpoints when possible.
- Geolocation is approximate; ISP/gateway locations may differ from end-user locations.

Bash example (uses curl + jq):

```bash
# Basic usage: IP passed as first arg
IP=${1:-8.8.8.8}

# Query 4 sources
A=$(curl -s "https://ipinfo.io/${IP}/json")
B=$(curl -s "http://ip-api.com/json/${IP}?fields=status,country,regionName,city,lat,lon,org,query")
C=$(curl -s "https://geolocation-db.com/json/${IP}&position=true")
D=$(curl -s "https://api.db-ip.com/v2/free/${IP}" )

# Output best-match heuristics should be implemented in script
echo "One-line summary:"
jq -n '{ip:env.IP,sourceA:A,sourceB:B,sourceC:C,sourceD:D}' --argjson A "$A" --argjson B "$B" --argjson C "$C" --argjson D "$D"
```

Node.js example (recommended):

```javascript
// ip_lookup.js
async function fetchJson(url, timeout = 8000){
  const controller = new AbortController();
  const id = setTimeout(()=>controller.abort(), timeout);
  try { const res = await fetch(url, {signal: controller.signal}); clearTimeout(id); if(!res.ok) throw new Error(res.statusText); return await res.json(); } catch(e){ clearTimeout(id); throw e; }
}

async function ipLookup(ip){
  const sources = {
    ipinfo: `https://ipinfo.io/${ip}/json`,
    ipapi: `http://ip-api.com/json/${ip}?fields=status,country,regionName,city,lat,lon,org,query`,
    geodb: `https://geolocation-db.com/json/${ip}&position=true`,
    dbip: `https://api.db-ip.com/v2/free/${ip}`
  };

  const results = {};
  for(const [k,u] of Object.entries(sources)){
    try{ results[k] = await fetchJson(u); } catch(e){ results[k] = {error: e.message}; }
  }

  // Normalise and pick best match (simple majority on country+city)
  const votes = {};
  for(const r of Object.values(results)){
    if(!r || r.error) continue;
    const country = r.country || r.country_name || r.countryCode || null;
    const city = r.city || r.city_name || null;
    const key = `${country||'?'}/${city||'?'}`;
    votes[key] = (votes[key]||0)+1;
  }
  const best = Object.entries(votes).sort((a,b)=>b[1]-a[1])[0];
  return {best: best?best[0]:null,score: best?best[1]:0,results};
}

// Usage: node ip_lookup.js 8.8.8.8
```

Agent prompt
------------

"Use the ip-lookup skill to query at least four public IP information providers for {ip}. Return a short JSON summary: best_match (country/city), score, and per-source details (country, region, city, lat, lon, org). Respect rate limits and fall back to alternate endpoints on errors."

"When creating a new skill, follow SKILL_TEMPLATE.md format and include Node.js and Bash examples." 
