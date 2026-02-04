---
name: fact-check
description: Verify factual claims against database sources
category: verification
---

# Fact-Checking Skill

Verify factual claims in manuscript against ingested sources.

## Usage

```bash
/fact-check --section section_123
/fact-check --chapter 3
/fact-check --claim "SOE training lasted six weeks"
```

## How It Works

1. **Extract Claims**: Identify factual statements
2. **Source Lookup**: Find relevant sources in database
3. **Verification**: Compare claim to source content
4. **Reliability Check**: Assess source quality
5. **Report**: Flag unsupported or conflicting claims

## Claim Categories

### Verifiable
- Dates and timelines
- Statistics and numbers
- Historical events
- Technical specifications
- Geographic information
- Names and titles

### Subjective
- Opinions and interpretations
- Character motivations (fiction)
- Artistic choices

## Verification Levels

✅ **Verified**: 2+ high-reliability sources agree
⚠️ **Partially Verified**: 1 source, or medium reliability
❌ **Unverified**: No source support
⚡ **Conflicting**: Sources disagree

## Example Report

```
FACT-CHECK REPORT - Section 3.2

✅ "SOE training center at Beaulieu"
   Sources: [High] SOE Official History
            [High] Beaulieu Archives

⚠️ "Training lasted six weeks"
   Sources: [Medium] Memoir - Agent testimony
   Note: Duration varied by agent specialty

❌ "All agents carried cyanide capsules"
   Sources: None found
   Recommendation: Research or remove/hedge claim

⚡ "Over 400 agents deployed to France"
   Conflicting: [High] Official records say 393
                [Medium] Historian estimates 420+
   Recommendation: Cite range or specific source
```

## Integration

Runs automatically during `/bookstrap-edit-path`
Can be run manually on specific sections
