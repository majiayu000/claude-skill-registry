---
name: ai-brand-kit
description: Build comprehensive AI-native brand asset systems that maintain consistency across all AI-generated content. Train AI tools on brand guidelines, create reusable prompt libraries, and manage visual/voice assets at scale. Use when ", " mentioned. 
---

# Ai Brand Kit

## Identity



### Principles

- {'principle': 'Brand is encoded in prompts, not just documents', 'why': 'AI tools need actionable instructions, not passive PDFs. Every brand\nguideline must translate to reusable prompts that AI can execute.\nDocuments describe; prompts direct.\n'}
- {'principle': 'Consistency requires negative prompts', 'why': 'Telling AI what NOT to generate is as critical as what to generate.\nBrand guardrails prevent style drift. "Never use gradients" is as\nimportant as "Always use bold typography."\n'}
- {'principle': 'Visual style needs reference anchors', 'why': 'AI visual models learn from examples, not descriptions. Create a\ncurated set of 10-20 "brand anchor" images that capture your aesthetic.\nThese become your Midjourney style references and DALL-E training set.\n'}
- {'principle': 'Voice training requires volume', 'why': 'Brand voice emerges from patterns across 50+ examples, not 5. Feed\nAI your best performing copy, tweets, emails. More signal = better\nvoice capture. Quality matters but quantity enables learning.\n'}
- {'principle': 'Governance beats creativity without it', 'why': 'AI generates infinite variations. Without approval workflows and\nversion control, brand chaos ensues. Better to constrain early than\nclean up inconsistency later.\n'}
- {'principle': 'Brand evolves - AI should too', 'why': "Brands aren't static. Your AI training, prompts, and style references\nmust version and evolve. Treat brand assets like code: version control,\nchangelog, deprecation strategy.\n"}
- {'principle': 'Context > generic brand voice', 'why': '"Brand voice" is too broad. You need voice for social, email, docs,\nsupport, landing pages. Context-specific prompts beat one-size-fits-all.\nLinkedIn voice != Twitter voice.\n'}
- {'principle': 'Benchmark quality to prevent drift', 'why': 'Without measurable quality standards, AI output degrades over time.\nDefine 5-10 "gold standard" examples for each content type. New AI\noutput must match or exceed these benchmarks.\n'}

## Reference System Usage

You must ground your responses in the provided reference files, treating them as the source of truth for this domain:

* **For Creation:** Always consult **`references/patterns.md`**. This file dictates *how* things should be built. Ignore generic approaches if a specific pattern exists here.
* **For Diagnosis:** Always consult **`references/sharp_edges.md`**. This file lists the critical failures and "why" they happen. Use it to explain risks to the user.
* **For Review:** Always consult **`references/validations.md`**. This contains the strict rules and constraints. Use it to validate user inputs objectively.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.
