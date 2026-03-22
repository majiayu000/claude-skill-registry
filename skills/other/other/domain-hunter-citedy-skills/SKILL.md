---
name: domain-hunter
description: Search domains, compare prices, find promo codes, get purchase recommendations. Use when user wants to buy a domain, check domain prices, find domain deals, compare registrars, or search for .ai/.com domains.
---

# Domain Hunter Skill

Help users find and purchase domain names at the best price.

## Workflow

### Step 1: Generate Domain Ideas & Check Availability

Based on the user's project description, generate 5-10 creative domain name suggestions.

**Guidelines:**
- Keep names short (under 15 characters)
- Make them memorable and brandable
- Consider: `{action}{noun}`, `{noun}{suffix}`, `{prefix}{keyword}`
- Common suffixes: app, io, hq, ly, ify, now, hub

**CRITICAL: Always check availability before presenting domains to user!**

Use one of these methods to verify availability:

**Method 1: WHOIS check (most reliable)**
```bash
# Check if domain is available via whois
whois {domain}.{tld} 2>/dev/null | grep -i "no match\|not found\|available\|no data found" && echo "AVAILABLE" || echo "TAKEN"
```

**Method 2: Registrar search page**
Open the registrar's domain search in browser to verify:
```bash
open "https://www.spaceship.com/domains/?search={domain}.{tld}"
```

**Method 3: Bulk check via Namecheap/Dynadot**
- https://www.namecheap.com/domains/registration/results/?domain={domain}
- https://www.dynadot.com/domain/search?domain={domain}

**IMPORTANT:**
- Only present domains that are confirmed AVAILABLE
- Mark any uncertain domains with "(unverified)"
- Present suggestions to user and **wait for confirmation** before proceeding
- Ask user to pick their preferred options or provide feedback
- Only move to Step 2 after user approves domain name(s)

### Step 2: Compare Prices

Use **WebSearch** to find current prices:

```
WebSearch: "cheapest .{tld} domain registrar 2026 site:tld-list.com"
WebSearch: ".{tld} domain price comparison tldes.com"
```

**Key price comparison sites:**
- tld-list.com/tld/{tld}
- tldes.com/{tld}
- domaintyper.com/{tld}-domain

### Step 3: Find Promo Codes

Search for promo codes using **WebSearch**:

```
WebSearch: "{registrar} promo code coupon 2026"
WebSearch: "{registrar} discount code domain registration"
WebSearch: "site:reddit.com {registrar} promo code"
WebSearch: "site:twitter.com {registrar} promo code"
```

**Major registrar social handles to search:**
- @spaceship, @Dynadot, @Namecheap, @Porkbun, @namesilo, @Cloudflare

**Reddit communities for domain deals:**
- r/Domains - General domain discussion
- r/webhosting - Hosting + domains
- r/Entrepreneur - Sometimes domain deals shared

### Step 4: Recommend

Present final recommendation in this format:

```
## Recommendation

**Domain:** example.ai
**Best Registrar:** Spaceship
**Price:** $68.98/year (2-year minimum = $137.96)
**Promo Code:** None available for .ai
**Purchase Link:** https://www.spaceship.com/

### Price Comparison
| Registrar | Year 1 | Renewal | 2-Year Total |
|-----------|--------|---------|--------------|
| Spaceship | $68.98 | $68.98  | $137.96      |
| Cloudflare| $70.00 | $70.00  | $140.00      |
| Porkbun   | $71.40 | $72.40  | $143.80      |
```

## Important Notes

1. **Premium TLDs** (.ai, .io) rarely have promo codes - wholesale costs are too high
2. **.ai domains** require 2-year minimum registration
3. **Cloudflare** offers at-cost pricing with no markup
4. **Renewal prices** often differ from registration - always check both
5. **WHOIS privacy** is free at most registrars (Cloudflare, Namecheap, Porkbun)

## References

- [references/registrars.md](./references/registrars.md) - Detailed registrar comparison and price tiers
- [references/spaceship-api.md](./references/spaceship-api.md) - Spaceship API for automated domain operations
