---
name: new-product
description: Generate comprehensive Enterprise AI Product White Papers using existing product documentation from Google Drive as source material. Use when users request "create a product white paper", "generate a white paper for [product]", or similar requests for enterprise-grade product documentation for SaaS, hardware, or service offerings.
---

# Product White Paper

Generate enterprise-grade product white papers that serve as strategic assets for educating buyers and presenting research-backed solutions to complex business problems.

## Workflow

Follow these steps to generate a product white paper:

1. **Understand the Product:** Clarify which product requires a white paper and identify the target audience (C-suite executives, technical decision-makers, or both)

2. **Gather Source Material:** Search Google Drive for existing product documentation, including:
   - Product specifications and feature descriptions
   - Technical architecture documentation
   - Customer case studies or testimonials
   - Competitive analysis
   - ROI data or success metrics
   - Implementation guides
   - Governance and compliance documentation

3. **Read the Structure Guide:** Load `references/white-paper-essentials.md` to understand the required structure and tone

4. **Generate the White Paper:** Create the white paper following the six-section structure, incorporating information from the gathered source material

5. **Present in Chat:** Output the complete white paper in the chat window formatted in markdown for easy copy-paste

## Search Strategy

When searching Google Drive for source material, use multiple targeted searches:

**For product information:**
```
name contains '[product-name]' and (mimeType = 'application/vnd.google-apps.document' or mimeType = 'application/pdf')
```

**For technical documentation:**
```
fullText contains '[product-name]' and (fullText contains 'architecture' or fullText contains 'technical' or fullText contains 'specification')
```

**For business value content:**
```
fullText contains '[product-name]' and (fullText contains 'ROI' or fullText contains 'value' or fullText contains 'benefit' or fullText contains 'case study')
```

Cast a wide net initially, then narrow based on relevance. Review multiple documents to synthesize comprehensive content.

## White Paper Structure

The white paper must follow this six-section structure (detailed in `references/white-paper-essentials.md`):

1. **Executive Summary** - High-impact summary of strategic and technical takeaways
2. **The Strategic Imperative** - Problem articulation, market context, and business justification
3. **The Solution Blueprint** - Product features, capabilities, and operational benefits
4. **Building Trust** - Governance, assurance, explainability, and risk mitigation
5. **Enterprise Value and ROI** - Multi-dimensional value framework and workforce augmentation
6. **Implementation and Next Steps** - Roadmap, change management, and clear call-to-action

## Tone and Quality Standards

Adhere to these principles:

- **Educational, not promotional:** Establish expertise through depth and research, avoid overt sales language
- **Formal and auditable:** Use engineering/legal-grade formality with verifiable claims
- **Research-backed:** Ground all assertions in evidence from source materials
- **Executive-relevant:** Balance technical depth with strategic business value
- **Conversion-oriented:** Include clear takeaways and actionable next steps

## Output Format

Present the white paper directly in the chat window using markdown formatting:
- Use proper heading hierarchy (# for title, ## for main sections, ### for subsections)
- Bold key terms and concepts for scannability
- Include bullet points for lists of features or benefits
- Maintain professional formatting for easy copy-paste into document editors

## Key References

- **Detailed structure and requirements:** See `references/white-paper-essentials.md` for comprehensive guidance on each section's purpose, required elements, and tone