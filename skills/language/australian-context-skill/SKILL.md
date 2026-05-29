---
name: australian-context
category: australian
version: 1.0.0
description: Australian English defaults, regulations, locale settings
auto_load: true
priority: 1
---

# Australian Context Skill

Ensures all output uses Australian English and references Australian context.

## Auto-Applied Settings

### Spelling (en-AU)

```
colour, favour, honour, labour, behaviour
organisation, authorisation, realisation
licence (n), license (v)
programme (general), program (computer)
metre, litre, centre, theatre
grey, cheque, catalogue, dialogue
travelling, cancelled, modelling
ageing, judgement
```

### Date/Time

```
Format: DD/MM/YYYY
Example: 05/01/2026
Time: 24-hour or 12-hour with am/pm
Timezone: AEST/AEDT (Brisbane default)
```

### Currency

```
Symbol: $
Code: AUD
Format: $1,234.56
GST: 10% (always mention if relevant)
```

### Phone Numbers

```
Mobile: 04XX XXX XXX
Landline: (0X) XXXX XXXX
Emergency: 000
SES: 132 500
```

### Addresses

```
Format:
[Street Number] [Street Name] [Street Type]
[SUBURB] [STATE] [POSTCODE]

Example:
123 Queen Street
BRISBANE QLD 4000
```

### States & Territories

```
QLD - Queensland
NSW - New South Wales
VIC - Victoria
SA - South Australia
WA - Western Australia
TAS - Tasmania
NT - Northern Territory
ACT - Australian Capital Territory
```

## Regulations & Standards

### Building & Construction

- National Construction Code (NCC)
- Australian Standards (AS/NZS)
- State-specific building requirements

### Work Health & Safety

- Work Health and Safety Act 2011
- SafeWork Australia guidelines
- State WHS regulators

### Insurance

- Insurance Council of Australia (ICA)
- Australian Financial Complaints Authority (AFCA)
- General Insurance Code of Practice

### Privacy & Compliance

- Privacy Act 1988
- WCAG 2.1 AA (accessibility)
- Australian Consumer Law

### Restoration Industry

- IICRC Standards (adopted in Australia)
- AS/NZS 3666 (HVAC hygiene)
- AS 4654 (waterproofing)

## Default Locations

When location needed but not specified:

1. Brisbane, QLD (primary)
2. Sydney, NSW
3. Melbourne, VIC

## Government Websites

```
.gov.au - Federal
.qld.gov.au - Queensland
.nsw.gov.au - New South Wales
.vic.gov.au - Victoria
```

## Never

- Use American spelling
- Reference American regulations
- Default to US locations
- Use US date format (MM/DD/YYYY)
- Use US phone format
