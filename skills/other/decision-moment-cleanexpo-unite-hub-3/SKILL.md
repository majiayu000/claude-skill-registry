---
name: decision-moment-skill
description: Map and optimize decision moments across Awareness, Consideration, Conversion, and Retention, then attach specific assets, visuals, and automations to each stage. Use when designing funnels, campaigns, or retention systems.
allowed-tools: Read, Write
---

# Decision Moment Skill

## Purpose
Turn raw offers and services into structured decision-moment maps that tell us exactly:
- **Where** a prospect is in their journey
- **What** they need to see/feel/understand next
- **Which** asset (page, email, video, social post) should be delivered

## Outputs
For each client/campaign:
1. **Journey Map**
   - Awareness → Problem Aware → Solution Aware → Provider Aware → Purchase → Retention
2. **Decision Moments**
   - Each moment contains:
     - Problem statement
     - Blocking objection(s)
     - Required proof
     - Recommended asset type
     - Link to asset in `social_assets` or page route
3. **Execution Map**
   - Which channel carries which moment (email, ad, social, landing page)

## Data Structures (DB)
- `decision_moment_maps` table to hold the overall map
- `decision_assets` table to join moments to specific assets

## When to Use
- After Social Playbook creation
- When designing onboarding journeys
- When improving conversion on an existing flow

## Constraints
- Always align with the No-Bluff protocol and verified value propositions.

## Decision Moment Framework

### Stage 1: Awareness
- "I have a problem but don't know what to call it"
- Asset types: Educational content, social posts, blog articles
- Goal: Get attention, define the problem

### Stage 2: Consideration
- "I know the problem, exploring solutions"
- Asset types: Comparison guides, case studies, how-to videos
- Goal: Position as the best solution

### Stage 3: Conversion
- "Ready to buy, need final push"
- Asset types: Demos, trials, testimonials, pricing pages
- Goal: Remove final objections, close deal

### Stage 4: Retention
- "Customer, keep them happy and growing"
- Asset types: Onboarding, tutorials, upsells, check-ins
- Goal: Maximize lifetime value
