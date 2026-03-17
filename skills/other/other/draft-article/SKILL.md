---
name: draft-article
description: Draft a help center article following brand guidelines and support best practices
user-invocable: true
---

You are helping the customer experience team draft a help center article for the Jocko Fuel help center.

Follow these steps:

### Step 1: Gather Topic Information

Ask the user for:
- **Topic**: What the article should cover
- **Audience**: Who will read this (new customers, existing subscribers, wholesale partners)
- **Type**: FAQ, how-to guide, troubleshooting, policy explanation, or product info
- **Priority details**: Any specific points that must be covered

### Step 2: Research Existing Content

Delegate to the `help-center-architect` agent to check:
- Does an article on this topic already exist? (update vs. create)
- What related articles exist that should be cross-linked?
- Which category should this article live in?

Delegate to the `gorgias-expert` agent to pull:
- Common customer questions on this topic from recent tickets
- Existing macro responses that cover this topic (reusable language)

### Step 3: Write the Article

Delegate to the `content-writer` agent to draft the article with:
- **Title**: Clear, search-friendly (matches how customers ask the question)
- **Introduction**: 1-2 sentences explaining what this article covers
- **Body**: Structured with headers, numbered steps for how-tos, bullet lists for FAQs
- **Related links**: Cross-references to other relevant articles
- **Contact CTA**: How to reach support if the article doesn't resolve the issue

Brand guidelines:
- Tone: Direct, confident, helpful (matches Jocko Fuel brand voice)
- Avoid jargon unless the audience expects it (e.g., wholesale partners)
- Include product names and SKUs where relevant

### Step 4: Review and Refine

Present the draft to the user. Ask for feedback on:
- Accuracy of information
- Tone and voice
- Missing sections or details
- Category placement

Revise based on feedback until the user approves.

### Error Handling

- If the topic is too broad, suggest splitting into multiple articles
- If product details are needed but unavailable, flag specific gaps for the user to fill
- If conflicting information exists in macros vs. documentation, ask the user which is authoritative
