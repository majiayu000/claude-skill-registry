---
name: domain-name-generator
description: Generate creative domain names and check availability for branding, startups, and web projects
---

# Domain Name Generator Skill

Generate creative, brandable domain names and verify availability.

## When to Use
- Startup naming
- Product launches
- Rebranding projects
- Portfolio websites

## Core Capabilities
- Creative name generation
- Domain availability checking
- Alternative TLD suggestions (.com, .io, .ai, etc.)
- Brandability scoring
- SEO-friendly suggestions
- Trademark conflict checking

## Generation Strategies
- Compound words (DropBox, YouTube)
- Portmanteaus (Pinterest = Pin + Interest)
- Prefixes/Suffixes (Shopify, Spotify)
- Misspellings (Flickr, Tumblr)
- Made-up words (Kodak, Xerox)

## Availability Check
```bash
# Using whois
whois example.com

# Using dig
dig example.com

# Bulk check with Python
import whois
domain = whois.whois('example.com')
print(domain.status)
```

## Evaluation Criteria
- Short and memorable
- Easy to spell
- Pronounceable
- No trademark conflicts
- Available on social media
- .com availability (preferred)

## Resources
- Namecheap: https://www.namecheap.com/
- Instant Domain Search: https://instantdomainsearch.com/
