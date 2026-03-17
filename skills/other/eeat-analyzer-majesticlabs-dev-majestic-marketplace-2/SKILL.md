---
name: eeat-analyzer
description: Analyze and optimize E-E-A-T signals (Experience, Expertise, Authority, Trust) for content credibility.
---

# E-E-A-T Analyzer

Frameworks for analyzing and improving Experience, Expertise, Authority, and Trust signals.

## E-E-A-T Signal Framework

### Experience Signals

| Signal | Implementation | Priority |
|--------|----------------|----------|
| First-hand experience | "I tested...", "In my experience..." | High |
| Case studies | Detailed client/project examples | High |
| Original research | Surveys, data analysis, experiments | High |
| Behind-the-scenes | Process documentation, workflows | Medium |
| Real examples | Screenshots, videos, specific details | Medium |

### Expertise Signals

| Signal | Implementation | Priority |
|--------|----------------|----------|
| Author credentials | Degrees, certifications, years experience | High |
| Technical depth | Industry terminology, detailed explanations | High |
| Comprehensive coverage | Address all subtopics, FAQ sections | High |
| Expert quotes | Interviews, cited experts | Medium |
| Accuracy | Fact-checked, current information | High |

### Authority Signals

| Signal | Implementation | Priority |
|--------|----------------|----------|
| External citations | Links from authoritative sources | High |
| Brand mentions | Unlinked mentions in industry | Medium |
| Industry recognition | Awards, speaking engagements | Medium |
| Published research | Whitepapers, studies, reports | High |
| Media features | Press coverage, interviews | Medium |

### Trust Signals

| Signal | Implementation | Priority |
|--------|----------------|----------|
| Contact accessibility | Clear contact info, response time | High |
| Privacy policy | GDPR compliance, clear terms | High |
| SSL/security | HTTPS, security badges | High |
| Reviews/testimonials | Verified customer feedback | High |
| Editorial policy | Fact-checking process, corrections | Medium |
| Transparency | Author bios, update history | Medium |

## Audit Scorecard

| Dimension | Score (1-10) | Evidence | Improvements |
|-----------|--------------|----------|--------------|
| Experience | | | |
| Expertise | | | |
| Authority | | | |
| Trust | | | |
| **Overall** | | | |

## Author Bio Template

```
[Name] is a [title/role] with [X] years of experience in [industry/domain].
[He/She/They] holds [credentials/certifications] and has [notable achievement].

[Name] has [authority indicator: published/spoken/advised] on [topic] for
[notable clients/publications/events]. [His/Her/Their] work has been featured
in [media mentions].

Connect with [Name]: [LinkedIn] | [Twitter] | [Professional site]
```

## Trust Signal Checklist

### Essential (Must Have)
- [ ] Clear author identification with bio
- [ ] Contact page with multiple methods
- [ ] Privacy policy and terms of service
- [ ] SSL certificate (HTTPS)
- [ ] Physical address (if applicable)

### Recommended
- [ ] Customer reviews/testimonials
- [ ] Industry certifications displayed
- [ ] Security badges (payment, data)
- [ ] About page with team bios
- [ ] Editorial/fact-check policy

### Advanced
- [ ] Third-party review integration
- [ ] Professional credentials verification
- [ ] Update/correction log
- [ ] Methodology transparency
- [ ] Conflict of interest disclosure

## Content E-E-A-T Enhancement

For each content piece, add:

1. **Author box** - Credentials, photo, links
2. **Sources section** - Citations with links
3. **Methodology note** - How information was gathered
4. **Last updated** - Date with change summary
5. **Expert review** - "Reviewed by [Expert]" badge

## Schema Implementation

```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "jobTitle": "Role",
    "alumniOf": "Institution",
    "sameAs": ["LinkedIn", "Twitter"]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Company"
  },
  "datePublished": "2024-01-01",
  "dateModified": "2024-06-01"
}
```
