---
name: ad-copy
description: Write platform-compliant ad copy for Meta, Google, TikTok, LinkedIn, Pinterest, Snapchat, Amazon, or X. Loads TOS rules automatically. Shows char counts and format preview.
---

# /ad-copy — The Ad Manager

Write ad copy that's compliant with platform TOS from day one. Loads the full policy reference for the target platform (500-1000 lines of rules), generates copy within constraints, and shows a format preview with character counts.

## Arguments

Required:
- **platform**: meta | google | tiktok | linkedin | pinterest | snapchat | amazon | x
- **site**: Site key (e.g., kaicalls)
- **offer**: The offer or message in quotes

Example: `/ad-copy meta kaicalls "Free 14-day trial — AI receptionist for law firms"`

## The Skill

### Step 1: Load Platform Policy

Read the platform's TOS reference from the knowledge base:

| Platform | Policy File |
|----------|------------|
| meta | `harness/references/meta-ads-rules.md` |
| google | `harness/references/google-ads-policy-reference.md` |
| tiktok | `harness/references/tiktok-ads-policy-reference.md` |
| linkedin | `harness/references/linkedin-ads-rules.md` |
| pinterest | `harness/references/pinterest-ads-rules.md` |
| snapchat | `harness/references/snapchat-ads-policy-reference.md` |
| amazon | `harness/references/amazon-ads-policy-reference.md` |
| x | `harness/references/x-ads-policy-reference.md` |

Also load `harness/references/advertising-compliance.md` for cross-platform FTC/GDPR/CAN-SPAM rules.

### Step 2: Load Site Context

Read site proof points and persona from the brief (if exists in `~/.kai-marketing/briefs/`) or from config.

### Step 3: Generate Ad Copy

Write ad copy variants following platform-specific constraints. Generate 3 variants per ad format:

**Meta/Instagram:**
- Primary text (125 chars recommended, 2200 max)
- Headline (40 chars max)
- Description (30 chars max)
- CTA button text

**Google Ads:**
- Headlines (30 chars each, 3 required)
- Descriptions (90 chars each, 2 required)
- Display URL path

**TikTok:**
- Ad text (100 chars recommended)
- CTA text
- Note: AI content disclosure required per TOS

**LinkedIn:**
- Introductory text (150 chars recommended)
- Headline (70 chars max)
- Description (100 chars max)

### Step 4: Platform Format Preview

Show each variant with character counts and truncation warnings:

```
AD COPY — Meta/Instagram
══════════════════════════════════════

VARIANT 1:
┌─────────────────────────────────────┐
│ Primary:    Stop losing calls to    │ 118/125 chars
│             voicemail. AI answers   │
│             in 0.4 seconds.         │
│                                     │
│ Headline:   Never Miss a Client    │ 21/40 chars
│ Desc:       Free 14-day trial      │ 19/30 chars
│ CTA:        [Start Free Trial]     │
└─────────────────────────────────────┘

VARIANT 2:
...

COMPLIANCE CHECK:
  [PASS] No prohibited claims
  [PASS] No before/after imagery references
  [PASS] No personal attributes addressed
  [PASS] FTC disclosure not required (no endorsement)
  [WARN] If targeting housing/employment/credit, enable Special Ad Category
```

### Step 5: Compliance Gate

Check each variant against the platform's restricted content categories:
- Prohibited content (hard block)
- Restricted content (may need approval/certs)
- Special categories (housing, employment, credit, political)
- Required disclosures (AI content, endorsements, financial)

If any variant has compliance issues, flag them with specific TOS section references.

### Step 6: Run Quality Gate

Run the standard quality gate with a lower threshold (10/16 Four U's for ads):

```bash
kai-gate score {draft_path} --format json
```

## Error Handling

- **Unknown platform**: List valid platforms
- **Policy file missing**: Warn and generate without TOS constraints (clearly flagged)
- **Character overflow**: Show which fields exceed limits with truncation suggestions

## Chain State

**Optional reads:** `~/.kai-marketing/briefs/` (for site context)
**Standalone:** Does not require prior chain steps
