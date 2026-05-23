---
name: optimization-mastery
description: 2026-grade Cross-Domain Optimization. Expertise in Interaction to Next Paint (INP), Partial Hydration, UUIDv7 indexing, and AI Token Stewardship. Performance is a feature, not an afterthought.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
<domain_overview>
# ⚡ OPTIMIZATION MASTERY: THE VELOCITY CORE
> **Philosophy:** Efficiency is the highest form of quality. Minimal overhead, maximum impact. Performance-First is the only law.
**INTERACTION HYGIENE MANDATE (CRITICAL):** Never prioritize synthetic benchmarks over real-world interaction smoothness. AI-generated code often misses Interaction to Next Paint (INP) bottlenecks caused by synchronous main-thread blocking. You MUST use `scheduler.yield()` or `requestAnimationFrame` for any complex DOM or state updates triggered by user events. Any implementation that risks "Layout Thrashing" or exceeds the 200ms INP threshold must be rejected.
</domain_overview>
<frontend_velocity>
## 🎨 PROTOCOL 1: FRONTEND PRECISION (INP & BUNDLE)
Aesthetics must be fast. Refer to `frontend-design` for visuals, but enforce these for speed.
1. **The INP Threshold:**
    *   **Core Metric:** Interaction to Next Paint (INP) MUST be < 200ms.
    *   **Action:** Yield to main thread for heavy logic. Use `scheduler.yield()` or `requestIdleCallback`.
2. **Hydration Strategies:**
    *   **Mandatory:** Use **Partial Hydration** or **Resumability** (e.g. Qwik/Astro patterns).
    *   **Forbidden:** Massive "Full Hydration" of static content.
3. **Asset Governance:**
    *   Images: Modern formats (AVIF/WebP) with `srcset` are mandatory.
    *   Fonts: Only `wght` variable fonts; subsetted.
</frontend_velocity>
<backend_velocity>
## 🏗️ PROTOCOL 2: BACKEND VELOCITY (QUERY & DATA)
The backend must be a fortress of speed. Refer to `backend-design` for architecture.
1. **Identifier Strategy:**
    *   **Mandatory:** Use **UUIDv7** for all primary keys in high-insert tables.
    *   **Rationale:** Time-sortable IDs prevent B-tree fragmentation and boost insert speed by ~30%.
2. **Query Budget:**
    *   **Max Latency:** Sub-100ms for OLTP queries.
    *   **Action:** Every index MUST be a "Covering Index" for critical read paths.
3. **Edge compute:**
    *   Offload logic to Edge Functions (Vercel/Cloudflare) to reduce Time-to-First-Byte (TTFB).
</backend_velocity>
<ai_token_stewardship>
## 🤖 PROTOCOL 3: AI TOKEN STEWARDSHIP (RESOURCE OPS)
AIs are expensive/slow. Optimize the "thought" itself.
1. **Context Window Management:**
    *   **Action:** Use "Context Folding" (summarizing history) to keep prompts under 4k tokens if possible.
2. **Credit-Based Execution:**
    *   Assign a "Token Budget" to complex tool calling phases.
3. **Caching:** 
    *   Implement Semantic Caching for repetitive LLM queries.
</ai_token_stewardship>
<audit_and_reference>
## 📂 COGNITIVE AUDIT CYCLE
1. Is INP < 200ms?
2. Are primary keys UUIDv7?
3. Is hydration partial/resumable?
4. Is the token budget justified for this request?
</audit_and_reference>
