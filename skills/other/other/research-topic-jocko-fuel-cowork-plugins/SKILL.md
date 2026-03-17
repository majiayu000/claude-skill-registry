---
name: research-topic
description: Research a topic for content creation
user-invocable: true
---

You are helping the marketing team research a topic for upcoming content.

Follow these steps:

### Step 1: Define Research Scope

Ask the user for:
- **Topic** — the subject to research
- **Purpose** — blog post, product page, email campaign, social content, or general knowledge
- **Depth** — quick overview (5-10 key points) or deep dive (comprehensive brief)
- **Angle** — what perspective or focus the eventual content will take

### Step 2: Conduct Research

Delegate to the research-agent to:
- Search for authoritative sources on the topic
- Gather scientific/clinical evidence (especially for ingredient or health topics)
- Identify key facts, statistics, and talking points
- Find relevant Jocko Fuel product connections
- Note any claims that will require DSHEA compliance review

### Step 3: Compile Research Brief

Present a structured research brief:

**Topic Summary** — 2-3 sentence overview

**Key Points:**
- Numbered list of main findings with source attribution

**Claims Requiring Compliance Review:**
- Any health-related claims flagged for DSHEA review

**Product Connections:**
- Relevant Jocko Fuel products that relate to the topic

**Suggested Content Angles:**
- 2-3 possible angles for content based on findings

**Sources:**
- List of credible sources found during research

### Step 4: Next Steps

Offer the user follow-up actions:
- Proceed to content creation (`/jf-content-creative:create-blog`)
- Deep-dive on a specific subtopic
- Cross-reference with product intelligence (`/jf-product-intelligence:research-ingredient`)
- Save the brief for later use

### Error Handling

- If research yields limited results, suggest broadening or refocusing the topic
- If the topic is outside Jocko Fuel's domain, note the limitation and research what's available
- If health claims are complex, recommend consulting the product-intelligence plugin
