---
name: phone-specs-scraper
description: "Scrape phone specifications from GSM Arena, PhoneDB, and alternative sites. Use when: (1) Comparing smartphone specs, (2) Researching device features, or (3) Building phone comparison tools."
---

# Phone Specifications Scraper

Extract detailed smartphone specs from popular phone database websites for comparison and research.

## When to use

- User asks to compare phone specifications
- Researching device features before purchase
- Building phone comparison tools or databases
- Finding detailed technical specifications

## Required tools / APIs

- No external API required
- Web scraping tools: curl, wget, or Playwright/Puppeteer
- HTML parsing: BeautifulSoup (Python), cheerio (Node.js), or grep/sed (bash)

## Phone Spec Websites

### Primary Sources

**1. GSM Arena (gsmarena.com)**
- Largest phone database with detailed specs
- URL pattern: `https://www.gsmarena.com/[brand]_[model]-[id].php`
- Example: `https://www.gsmarena.com/google_pixel_9-13242.php`

**2. PhoneDB (phonedb.net)**
- Detailed device specifications database
- URL pattern: `https://phonedb.net/index.php?m=device&s=query&d=[device-name]`

**3. PhoneArena (phonearena.com)**
- Phone reviews and comparisons
- URL pattern: `https://www.phonearena.com/phones/[brand]-[model]`

**4. MK Mobile Arena (mkmobilearena.com)**
- Side-by-side phone comparisons
- URL pattern: `https://mkmobilearena.com/phone-compare/[phone1]-vs-[phone2]`

**5. TechRadar (techradar.com)**
- Phone reviews with spec comparisons
- URL pattern: `https://www.techradar.com/phones/[brand]-[model]`

**6. DeviceBeast (devicebeast.com)**
- Comprehensive device specs
- URL pattern: `https://devicebeast.com/phones/[brand]-[model]`

**7. Comparigon (comparigon.com)**
- Side-by-side comparisons
- URL pattern: `https://comparigon.com/phones/[brand]-[model]`

**8. SpecsBattle (specsbattle.com)**
- Detailed phone comparisons
- URL pattern: `https://specsbattle.com/phones/[brand]-[model]`

## Skills

### scrape_gsmarena_specs

Scrape phone specs from GSM Arena using curl and grep.

```bash
# Get phone specs from GSM Arena
PHONE_URL="https://www.gsmarena.com/google_pixel_9-13242.php"

# Download page and extract key specs
curl -s "$PHONE_URL" | grep -oP '(?<=<td class="ttl">)[^<]+' | head -20

# Extract specifications table
curl -s "$PHONE_URL" | grep -A2 'class="specs-cp"' | grep -oP '(?<=<td>)[^<]+'
```

**Node.js with cheerio:**

```javascript
const cheerio = require('cheerio');

async function scrapeGSMArenaSpecs(url) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);
  
  const specs = {};
  
  // Extract basic info
  specs.name = $('h1.specs-phone-name').text().trim();
  specs.released = $('.specs-cp .specs-cp-release').text().trim();
  specs.weight = $('.specs-cp .specs-cp-weight').text().trim();
  
  // Extract all specification tables
  $('.specs-cp table').each((i, table) => {
    const category = $(table).find('th').text().trim();
    specs[category] = {};
    
    $(table).find('tr').each((j, row) => {
      const key = $(row).find('td.ttl').text().trim();
      const value = $(row).find('td.nfo').text().trim();
      if (key && value) {
        specs[category][key] = value;
      }
    });
  });
  
  return specs;
}

// Usage
// scrapeGSMArenaSpecs('https://www.gsmarena.com/google_pixel_9-13242.php').then(console.log);
```

### search_phone_specs

Search for phone specs across multiple sources.

```bash
# Search using SearXNG for phone comparison pages
QUERY="Google Pixel 9 vs Pixel 10 specs comparison"
INSTANCE="https://searx.party"

curl -s "${INSTANCE}/search?q=${QUERY}&format=json" | jq -r '.results[] | select(.url | contains("gsmarena\|phonedb\|mkmobilearena")) | {title, url}'
```

**Node.js:**

```javascript
async function searchPhoneSpecs(phone1, phone2) {
  const query = `${phone1} vs ${phone2} specs comparison`;
  const searxInstances = [
    'https://searx.party',
    'https://searx.tiekoetter.com',
    'https://searx.ninja'
  ];
  
  for (const instance of searxInstances) {
    try {
      const params = new URLSearchParams({
        q: query,
        format: 'json',
        language: 'en'
      });
      
      const res = await fetch(`${instance}/search?${params}`, { timeout: 10000 });
      const data = await res.json();
      
      // Filter for phone spec sites
      const specSites = data.results.filter(r => 
        r.url.includes('gsmarena.com') ||
        r.url.includes('mkmobilearena.com') ||
        r.url.includes('techradar.com') ||
        r.url.includes('phonedb.net')
      );
      
      if (specSites.length > 0) {
        return specSites;
      }
    } catch (err) {
      console.warn(`Instance ${instance} failed: ${err.message}`);
    }
  }
  
  throw new Error('No working search instances found');
}

// Usage
// searchPhoneSpecs('Google Pixel 9', 'Google Pixel 10').then(console.log);
```

### compare_two_phones

Compare specifications between two phones with highlighted differences.

```javascript
async function comparePhones(phone1Specs, phone2Specs) {
  const comparison = {
    matches: [],
    differences: [],
    upgrades: [],
    downgrades: []
  };
  
  // Compare key specs
  const keyFields = [
    'chipset', 'display', 'battery', 'mainCamera', 
    'ram', 'storage', 'weight', 'releaseDate'
  ];
  
  for (const field of keyFields) {
    const val1 = phone1Specs[field];
    const val2 = phone2Specs[field];
    
    if (val1 === val2) {
      comparison.matches.push({ field, value: val1 });
    } else {
      comparison.differences.push({
        field,
        phone1: val1,
        phone2: val2
      });
      
      // Detect upgrades (simplified logic)
      if (field === 'battery' || field === 'ram' || field === 'storage') {
        const num1 = parseInt(val1);
        const num2 = parseInt(val2);
        if (!isNaN(num1) && !isNaN(num2) && num2 > num1) {
          comparison.upgrades.push({ field, from: val1, to: val2 });
        }
      }
    }
  }
  
  return comparison;
}

// Usage example with formatted output
function formatComparison(comparison) {
  let output = '## Phone Comparison\n\n';
  
  output += '### ✅ Same Specs\n';
  comparison.matches.forEach(m => {
    output += `- ${m.field}: ${m.value}\n`;
  });
  
  output += '\n### 🔄 Differences\n';
  comparison.differences.forEach(d => {
    output += `- **${d.field}**:\n`;
    output += `  - Phone 1: ${d.phone1}\n`;
    output += `  - Phone 2: ${d.phone2}\n`;
  });
  
  output += '\n### ⬆️ Upgrades\n';
  comparison.upgrades.forEach(u => {
    output += `- ${u.field}: ${u.from} → ${u.to}\n`;
  });
  
  return output;
}
```

### scrape_comparison_site

Scrape pre-formatted comparison from sites like MK Mobile Arena.

```bash
# Get comparison from MK Mobile Arena
COMPARISON_URL="https://mkmobilearena.com/phone-compare/google-pixel-9-vs-google-pixel-10"

# Extract comparison table
curl -s "$COMPARISON_URL" | grep -oP '(?<=<td[^>]*>)[^<]+' | head -50
```

**Node.js:**

```javascript
async function scrapeComparisonSite(url) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);
  
  const comparison = {
    phone1: {},
    phone2: {},
    differences: []
  };
  
  // Extract phone names
  comparison.phone1.name = $('table tr:first-child td:nth-child(2) h3').text().trim();
  comparison.phone2.name = $('table tr:first-child td:nth-child(3) h3').text().trim();
  
  // Extract specs row by row
  $('table tr').each((i, row) => {
    const specName = $(row).find('td:first-child').text().trim();
    const phone1Value = $(row).find('td:nth-child(2)').text().trim();
    const phone2Value = $(row).find('td:nth-child(3)').text().trim();
    
    if (specName && phone1Value && phone2Value) {
      comparison.phone1[specName] = phone1Value;
      comparison.phone2[specName] = phone2Value;
      
      if (phone1Value !== phone2Value) {
        comparison.differences.push({
          spec: specName,
          phone1: phone1Value,
          phone2: phone2Value
        });
      }
    }
  });
  
  return comparison;
}
```

## Rate limits / Best practices

- Respect robots.txt - check `/robots.txt` before scraping
- Rate limit: 1 request per second maximum
- Cache results for at least 1 hour to avoid redundant requests
- Use rotating User-Agent strings
- Handle JavaScript-rendered sites with Playwright/Puppeteer when needed
- Some sites block scrapers - use fallback sources

## Agent prompt

```text
You can scrape phone specifications from GSM Arena and other sources. When a user asks to compare phones:

1. First try MK Mobile Arena or similar comparison sites that show side-by-side specs
2. If not available, scrape individual phone pages from GSM Arena
3. Extract key specs: display, chipset, battery, cameras, RAM, storage, release date
4. Highlight differences and upgrades between models
5. Format output with clear sections: Same Specs, Differences, Upgrades

Always cite the source URL and respect site terms of service.
```

## Troubleshooting

**Error: "403 Forbidden"**
- Site is blocking scrapers
- Solution: Try alternative sources (PhoneDB, PhoneArena, TechRadar)

**Error: "Empty results"**
- Page structure changed or phone not found
- Solution: Verify phone name spelling and model number

**Error: "JavaScript required"**
- Site uses client-side rendering
- Solution: Use Playwright/Puppeteer instead of curl

**Rate limited**
- Too many requests to the site
- Solution: Add delays (sleep 2) between requests

## See also

- [using-web-scraping](../using-web-scraping/SKILL.md) — General web scraping techniques
- [web-search-api](../web-search-api/SKILL.md) — Find phone comparison pages via search
