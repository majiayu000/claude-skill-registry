---
name: medical-specialty-briefs
description: Generate daily or on-demand medical research briefs for any medical specialty. Searches latest research from top-tier journals, delivers concise summaries with 1-sentence takeaways, images when available, and direct links. Use when user asks for medical news, research updates, journal briefs, or specialty-specific medical updates for specialties like endocrinology, cardiology, oncology, neurology, etc.
---

# Medical Specialty Briefs

Generate curated medical research briefs for any medical specialty in a Google News-style format.

## When to Use This Skill

- User asks for "medical news" or "research updates" for a specific specialty
- User wants a "daily brief" for their medical field
- User mentions journal names (NEJM, JAMA, Lancet, etc.) with research queries
- User is a clinician seeking specialty-specific updates

## Output Format

Each brief item should include:

1. **Headline** - Clear, concise title
2. **One-Sentence Summary** - Key takeaway for clinicians
3. **Source** - Journal name + publication date
4. **Image** - Include if available from source
5. **Link** - Direct URL to original article
6. **Clinical Relevance Badge** - One of:
   - 🔴 High Impact (practice-changing)
   - 🟡 Moderate (consider for practice)
   - 🟢 Low (awareness only)

## Search Strategy

### Priority Journals (in order)
1. New England Journal of Medicine (NEJM)
2. The Lancet
3. JAMA (Journal of the American Medical Association)
4. Specialty-specific top journals
5. BMJ (British Medical Journal)
6. Nature / Nature Medicine
7. Journal of Clinical Endocrinology & Metabolism (JCEM)
8. Endocrine Practice
9. Thyroid
10. Specialty-specific top journals

### Search Parameters
- Time window: Last 7 days (configurable)
- Content: Clinical research, guidelines, AI/ML applications, drug approvals, device approvals
- Exclude: Case reports, preprints (unless high impact), non-peer reviewed

## Workflow

1. **Identify Specialty** - Ask if not specified
2. **Set Time Window** - Default 7 days, ask if different needed
3. **Search** - Query priority journals for specialty + date range
4. **Filter** - Remove duplicates, prioritize clinical relevance
5. **Format** - Generate Google News-style cards
6. **Deliver** - Present to user with specialty header

## Example Queries by Specialty

| Specialty | Example Search |
|-----------|----------------|
| Endocrinology | "Weight loss medication" "thyroid nodule ultrasound" |
| Cardiology | "heart failure SGLT2" "AFib catheter ablation" |
| Oncology | "immunotherapy checkpoint inhibitor" "liquid biopsy" |
| Neurology | "Alzheimer lecanemab" "stroke thrombectomy" |

## Usage
User: "Give me today's cardiology brief"
→ Search cardiology journals from last 7 days
→ Return 3-5 formatted brief items
User: "Weekly neurology update"
→ Search neurology journals from last 7 days
→ Return formatted brief


## Notes

- If no new articles found, state: "No new high-impact articles found for [specialty] in the last [time window]."
- Track delivered articles to avoid repeats in subsequent briefs
- Prioritize articles with clinical utility metrics (sensitivity/specificity, AUC, hazard ratios)