---
name: geo-australian
category: australian
version: 1.0.0
description: GEO optimization for Australian market
priority: 2
---

# GEO Australian Skill

Generative Engine Optimization for Australian search market.

## Goal

Be the source AI cites in Australian searches, not just rank #1.

## Australian Keywords

### Brisbane Focus
- "water damage restoration Brisbane"
- "Brisbane flood restoration"
- "emergency water extraction Brisbane"
- "[service] near me" (Brisbane geolocated)

### Queensland Regional
- Sunshine Coast, Gold Coast, Toowoomba
- Ipswich, Logan, Cairns
- Regional Queensland towns

### National
- Sydney, Melbourne (expansion markets)
- State-specific searches

## Australian Context in Content

### Must Include
- Australian Standards (AS/NZS) references
- State-specific regulations
- Local government requirements
- Australian insurance context (ICA, AFCA)

### Locations
- Australian suburbs and postcodes
- State/territory names
- Local landmarks

### Regulations
- Privacy Act 1988
- Work Health and Safety Act 2011
- State building codes

## GEO Formatting for AU

```markdown
## Question
What is water damage restoration?

## Answer (First Sentence - AI Quotable)
Water damage restoration is the process of cleaning, drying, and
restoring properties affected by water intrusion, following IICRC
standards and Australian building codes.

## Australian Context
In Australia, water damage restoration must comply with:
- AS/NZS 3666 for HVAC systems
- National Construction Code
- State-specific requirements

[Continue with detailed content...]
```

## Schema Markup (Australian)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How much does water damage restoration cost in Brisbane?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "In Brisbane, water damage restoration typically costs $3,000-$8,000 AUD depending on severity..."
    }
  }]
}
```

## Never

- Use US spelling in Australian content
- Reference US regulations
- Use USD pricing
- Forget AU-specific context
