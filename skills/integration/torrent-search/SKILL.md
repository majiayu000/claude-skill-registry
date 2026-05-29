---
name: torrent-search
description: "Search for torrents by title or IMDB ID via a Torznab-compatible API. Use when: (1) User asks to find a torrent for a movie or show, (2) You need a magnet link for a given title, or (3) User provides an IMDB ID and wants download options."
---

# Torrent Search

Search any Torznab-compatible indexer (e.g. bitmagnet) for torrents by title or IMDB ID. Returns magnet links, file sizes, seeders, resolution, and codec.

## When to use

- User asks to find a torrent for a movie, TV show, or any other content
- User provides an IMDB ID (e.g. `tt1234567`) and wants download options
- You need to programmatically retrieve a magnet link for a given title
- User asks to compare available qualities (720p, 1080p, 2160p) for a release

## Required tools / APIs

- `curl` — HTTP requests (pre-installed on most systems)
- `jq` — JSON parsing (used after XML→JSON conversion)
- `xmllint` — XML parsing (optional, from `libxml2-utils`)
- A running Torznab endpoint — examples use `https://bitmagnetfortheweebs.midnightignite.me/torznab/api`

Install options:

```bash
# Ubuntu/Debian
sudo apt-get install -y curl jq libxml2-utils

# macOS
brew install curl jq libxml2

# Node.js (no extra packages — uses native fetch + DOMParser via fast-xml-parser)
npm install fast-xml-parser
```

## Skills

### search_by_title

Search for torrents using a free-text title query.

```bash
TORZNAB_URL="https://bitmagnetfortheweebs.midnightignite.me/torznab/api"
QUERY="Breaking Bad"

curl -fsS --max-time 15 \
  "${TORZNAB_URL}?t=search&q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")" \
  | xmllint --xpath "//item" - 2>/dev/null \
  | grep -oP '(?<=<title>).*?(?=</title>)'
```

Full extraction with magnet links:

```bash
TORZNAB_URL="https://bitmagnetfortheweebs.midnightignite.me/torznab/api"
QUERY="Inception 2010"

xml=$(curl -fsS --max-time 15 \
  "${TORZNAB_URL}?t=search&q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")")

# Print title + magnet for each result
echo "$xml" | python3 - << 'EOF'
import sys, xml.etree.ElementTree as ET

data = sys.stdin.read()
root = ET.fromstring(data)
ns = {'torznab': 'http://torznab.com/schemas/2015/feed'}

for item in root.findall('.//item'):
    title = item.findtext('title', '')
    size  = item.findtext('size', '0')
    enc   = item.find('enclosure')
    magnet = enc.get('url') if enc is not None else ''

    attrs = {a.get('name'): a.get('value') for a in item.findall('torznab:attr', ns)}
    seeders    = attrs.get('seeders', '?')
    resolution = attrs.get('resolution', '')
    codec      = attrs.get('video', '')

    size_gb = round(int(size) / 1_073_741_824, 2)
    print(f"{title}")
    print(f"  Size: {size_gb} GB  Seeders: {seeders}  {resolution} {codec}")
    print(f"  Magnet: {magnet[:80]}...")
    print()
EOF
```

**Node.js:**

```javascript
import { XMLParser } from 'fast-xml-parser';

const TORZNAB_URL = 'https://bitmagnetfortheweebs.midnightignite.me/torznab/api';

async function searchTorrents(query) {
  const url = `${TORZNAB_URL}?t=search&q=${encodeURIComponent(query)}`;
  const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const xml = await res.text();
  const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: '@_' });
  const doc = parser.parse(xml);

  const items = doc?.rss?.channel?.item ?? [];
  const list = Array.isArray(items) ? items : [items];

  return list.map(item => {
    const attrs = {};
    const rawAttrs = item['torznab:attr'] ?? [];
    const attrList = Array.isArray(rawAttrs) ? rawAttrs : [rawAttrs];
    for (const a of attrList) attrs[a['@_name']] = a['@_value'];

    return {
      title:      item.title,
      sizeBytes:  Number(item.size ?? 0),
      sizeGB:     +(Number(item.size ?? 0) / 1_073_741_824).toFixed(2),
      magnet:     item.enclosure?.['@_url'] ?? attrs.magneturl ?? '',
      infohash:   attrs.infohash ?? '',
      seeders:    Number(attrs.seeders ?? 0),
      leechers:   Number(attrs.leechers ?? 0),
      resolution: attrs.resolution ?? '',
      codec:      attrs.video ?? '',
      year:       attrs.year ?? '',
      imdb:       attrs.imdb ? `tt${attrs.imdb}` : '',
    };
  });
}

// Usage
searchTorrents('Inception 2010').then(results => {
  results.forEach(r => {
    console.log(`${r.title}`);
    console.log(`  ${r.sizeGB} GB | ${r.resolution} ${r.codec} | ${r.seeders} seeders`);
    console.log(`  ${r.magnet.slice(0, 80)}...`);
    console.log();
  });
});
```

---

### search_by_imdb_id

Search by exact IMDB ID to get all available releases for a specific title.

```bash
TORZNAB_URL="https://bitmagnetfortheweebs.midnightignite.me/torznab/api"
IMDB_ID="tt12735488"   # Kalki 2898 AD

curl -fsS --max-time 15 \
  "${TORZNAB_URL}?t=search&q=${IMDB_ID}" \
  | python3 - << 'EOF'
import sys, xml.etree.ElementTree as ET

root = ET.fromstring(sys.stdin.read())
ns = {'torznab': 'http://torznab.com/schemas/2015/feed'}

for item in root.findall('.//item'):
    title = item.findtext('title', '')
    size  = int(item.findtext('size', '0'))
    enc   = item.find('enclosure')
    magnet = enc.get('url') if enc is not None else ''
    attrs = {a.get('name'): a.get('value') for a in item.findall('torznab:attr', ns)}

    print(f"[{attrs.get('resolution','?'):6}] {round(size/1e9,1):5.1f}GB  "
          f"S:{attrs.get('seeders','?'):>3}  {title}")
EOF
```

**Node.js:**

```javascript
import { XMLParser } from 'fast-xml-parser';

const TORZNAB_URL = 'https://bitmagnetfortheweebs.midnightignite.me/torznab/api';

async function searchByImdb(imdbId) {
  // imdbId format: 'tt1234567' or just '1234567'
  const id = imdbId.startsWith('tt') ? imdbId : `tt${imdbId}`;
  const url = `${TORZNAB_URL}?t=search&q=${id}`;

  const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const xml = await res.text();
  const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: '@_' });
  const doc = parser.parse(xml);

  const items = doc?.rss?.channel?.item ?? [];
  const list = Array.isArray(items) ? items : [items];

  return list.map(item => {
    const attrs = {};
    const rawAttrs = item['torznab:attr'] ?? [];
    for (const a of Array.isArray(rawAttrs) ? rawAttrs : [rawAttrs]) {
      attrs[a['@_name']] = a['@_value'];
    }
    return {
      title:      item.title,
      sizeGB:     +(Number(item.size ?? 0) / 1_073_741_824).toFixed(2),
      magnet:     item.enclosure?.['@_url'] ?? attrs.magneturl ?? '',
      infohash:   attrs.infohash ?? '',
      seeders:    Number(attrs.seeders ?? 0),
      resolution: attrs.resolution ?? '',
      codec:      attrs.video ?? '',
      year:       attrs.year ?? '',
    };
  });
}

// Usage — find all releases for a specific IMDB title
searchByImdb('tt12735488').then(results => {
  // Sort by seeders descending, then by size descending
  results.sort((a, b) => b.seeders - a.seeders || b.sizeGB - a.sizeGB);
  results.forEach(r =>
    console.log(`[${r.resolution || '?':>6}] ${r.sizeGB}GB  S:${r.seeders}  ${r.title}`)
  );
});
```

---

### pick_best_result

Filter and rank results by quality preference (resolution priority + seeder count).

**Node.js:**

```javascript
function pickBest(results, { preferResolution = '1080p', minSeeders = 1 } = {}) {
  const resolutionRank = { '2160p': 4, '1080p': 3, '720p': 2, '480p': 1 };
  const preferred = resolutionRank[preferResolution] ?? 3;

  return results
    .filter(r => r.seeders >= minSeeders)
    .sort((a, b) => {
      const ra = resolutionRank[a.resolution] ?? 0;
      const rb = resolutionRank[b.resolution] ?? 0;
      // Exact preferred resolution first, then by seeders
      const aMatch = ra === preferred ? 1 : 0;
      const bMatch = rb === preferred ? 1 : 0;
      if (bMatch !== aMatch) return bMatch - aMatch;
      return b.seeders - a.seeders;
    })[0] ?? null;
}

// Usage
const results = await searchByImdb('tt12735488');
const best = pickBest(results, { preferResolution: '1080p', minSeeders: 1 });
if (best) {
  console.log(`Best pick: ${best.title}`);
  console.log(`Magnet: ${best.magnet}`);
}
```

## Output format

Each result object contains:

- `title` — string — release name as indexed (e.g. `"Inception.2010.1080p.BluRay.x264"`)
- `sizeGB` — number — file size in gigabytes (e.g. `3.15`)
- `magnet` — string — full magnet URI starting with `magnet:?xt=urn:btih:...`
- `infohash` — string — 40-char hex SHA-1 info hash
- `seeders` — number — active seeders at index time (may be stale)
- `leechers` — number — active leechers at index time
- `resolution` — string — `"720p"`, `"1080p"`, `"2160p"`, or `""` if unknown
- `codec` — string — `"x264"`, `"x265"`, `"XviD"`, `"AV1"`, or `""` if unknown
- `year` — string — release year (e.g. `"2024"`)
- `imdb` — string — IMDB ID in `tt` format (e.g. `"tt12735488"`)

Error shape:

```json
{ "error": "HTTP 503", "fix": "Indexer is down — retry in 30s or use a different endpoint" }
```

## Rate limits / Best practices

- The public endpoint has no documented rate limit; add a 1-second delay between batch queries
- IMDB ID search (`?q=tt...`) is more precise than title search — prefer it when you have the ID
- Seeder counts in the index may lag reality by hours — always surface them to the user but don't rely on them for availability
- Sort results by seeders descending before presenting to the user
- Filter out results with 0 seeders unless no others exist
- Cache results for at least 5 minutes — the index is not real-time
- For batch lookups, space requests at least 1 second apart

## Agent prompt

```text
You have torrent-search capability via a Torznab API.
When a user asks to find a torrent for something:

1. If they provide an IMDB ID (tt...), use search_by_imdb_id for precise results.
2. Otherwise use search_by_title with the title and year if known.
3. Parse the XML response and extract: title, sizeGB, seeders, resolution, magnet link.
4. Sort results by seeders descending. Filter out 0-seeder results unless nothing else exists.
5. Present the top 3–5 results with: title, size, resolution, seeder count.
6. Ask the user which one they want, then return the full magnet link.
7. Never auto-start a download without user confirmation.

Torznab endpoint: https://bitmagnetfortheweebs.midnightignite.me/torznab/api
```

## Troubleshooting

**Empty results / no `<item>` elements:**
- Symptom: The XML response has a `<channel>` but no `<item>` children
- Solution: The indexer has no matches. Try a shorter query (just the title, no year). Try searching by IMDB ID instead.

**`xmllint` not found:**
- Symptom: `xmllint: command not found`
- Solution: `sudo apt-get install -y libxml2-utils` (Linux) or `brew install libxml2` (macOS). Alternatively use the Python `xml.etree` approach which needs no extra tools.

**`fast-xml-parser` not available:**
- Symptom: `Cannot find module 'fast-xml-parser'`
- Solution: `npm install fast-xml-parser`. As a zero-dependency alternative, use the Bash + Python script path which only needs the standard library.

**Endpoint unreachable (connection refused / timeout):**
- Symptom: `curl: (7) Failed to connect` or `curl: (28) Operation timed out`
- Solution: The specific public instance may be offline. Self-host bitmagnet (`docker run -d ghcr.io/bitmagnet-io/bitmagnet`) and point `TORZNAB_URL` to your local instance.

**Magnet link is empty:**
- Symptom: `enclosure url` is missing or blank for some items
- Solution: Reconstruct from infohash: `magnet:?xt=urn:btih:<infohash>&dn=<encoded-title>`

## See also

- [../using-youtube-download/SKILL.md](../using-youtube-download/SKILL.md) — Download videos from YouTube with yt-dlp
- [../anonymous-file-upload/SKILL.md](../anonymous-file-upload/SKILL.md) — Upload files without an account (IPFS / transfer.sh)
