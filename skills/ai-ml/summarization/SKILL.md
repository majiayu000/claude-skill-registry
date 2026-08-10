---
name: summarization
description: Summarize text using extractive, abstractive, hierarchical, and multi-document techniques, producing concise outputs at configurable detail levels. Use when the user requests summarization or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Summarization

This skill enables an AI agent to condense long-form text into clear, accurate summaries. The agent supports multiple summarization strategies — extractive (selecting key sentences verbatim), abstractive (rewriting in new words), hierarchical (layered summaries at different detail levels), and multi-document (synthesizing across several sources). The skill is designed for technical documents, meeting notes, research papers, articles, and any text where readers need the core information without reading the full content.

## Workflow

1. **Analyze the Input:** Determine the type, length, and structure of the source material. Identify whether it is a single document or multiple documents, whether it has clear sections (headings, chapters) or is unstructured prose, and what domain it belongs to. This determines which summarization strategy to apply.

2. **Select the Summarization Strategy:** Choose the approach best suited to the input and the user's needs. Use extractive summarization for factual or legal texts where exact wording matters. Use abstractive summarization for general content where readability and brevity are priorities. Use hierarchical summarization when the user needs both a one-line TLDR and a detailed breakdown. Use multi-document summarization when synthesizing across several inputs.

3. **Identify Key Information:** Regardless of strategy, identify the core claims, findings, decisions, action items, and supporting data in the source. Rank information by importance using signals like: position in the document (introductions and conclusions carry weight), frequency of mention, explicit markers ("importantly," "in conclusion"), and relevance to the user's stated purpose.

4. **Generate the Summary:** Produce the summary at the requested length and detail level. Preserve factual accuracy — never introduce information not present in the source. Maintain the source's logical structure. For hierarchical summaries, produce three tiers: a one-sentence TLDR, a short paragraph (3-5 sentences), and a detailed section-by-section breakdown.

5. **Verify Faithfulness:** Compare the summary against the source to ensure no facts are distorted, no critical information is omitted, and no hallucinated content is introduced. Check that numerical data, proper nouns, and causal claims are accurate.

## Usage

Provide the agent with the text to summarize and optionally specify: the desired length (one-sentence, short, medium, detailed), the strategy (extractive, abstractive, hierarchical), or a specific focus area.

```
Summarize the following technical RFC into a short paragraph and a detailed
section-by-section breakdown. Focus on the proposed changes and their
backward-compatibility impact.

[paste RFC text here]
```

## Examples

### Example 1: Hierarchical Summary of a Technical Document

**User Request:**
> Summarize this document at three levels of detail.

**Source Document (excerpt):**
> The Kubernetes Gateway API is a collection of resources that model service networking in Kubernetes. It is the successor to the Ingress API and provides more expressive, extensible, and role-oriented interfaces. The API introduces three primary resource types: GatewayClass (defines a set of Gateways with common configuration), Gateway (requests a point where traffic can be translated to Services within the cluster), and HTTPRoute (defines HTTP-specific routing rules). Unlike Ingress, the Gateway API supports traffic splitting, header modification, and cross-namespace routing natively. The API reached GA status in v1.0.0, released in October 2023, with implementations available from Istio, Envoy Gateway, Cilium, and Traefik. Migration from Ingress is supported through the ingress2gateway tool, though manual review is recommended for complex configurations. Key limitations include the lack of TCP/UDP routing in the core spec (addressed by TCPRoute and UDPRoute in the experimental channel) and the varying maturity of different implementations.

**Output:**

**TLDR (1 sentence):**
The Kubernetes Gateway API is the GA successor to Ingress, introducing GatewayClass, Gateway, and HTTPRoute resources for more expressive service networking with native traffic splitting and cross-namespace routing.

**Short Summary (1 paragraph):**
The Kubernetes Gateway API, which reached GA in October 2023, replaces the Ingress API with a more expressive and extensible approach to service networking. It introduces three core resources — GatewayClass, Gateway, and HTTPRoute — that separate concerns by role (infrastructure provider, cluster operator, application developer). The API natively supports traffic splitting, header modification, and cross-namespace routing, features that required annotations or custom resources under Ingress. Implementations are available from Istio, Envoy Gateway, Cilium, and Traefik. Migration from Ingress is possible via the ingress2gateway tool, though TCP/UDP routing remains experimental and implementation maturity varies.

**Detailed Breakdown:**
- **What it is:** A collection of Kubernetes-native resources for modeling service networking, designed as the successor to the Ingress API.
- **Core resources:** GatewayClass (shared gateway configuration), Gateway (traffic entry point), HTTPRoute (HTTP routing rules).
- **Key improvements over Ingress:** Native traffic splitting, header modification, cross-namespace routing, and role-oriented resource separation — no more vendor-specific annotations.
- **Current status:** GA since v1.0.0 (October 2023). Supported by Istio, Envoy Gateway, Cilium, and Traefik.
- **Migration path:** The ingress2gateway tool automates conversion, but complex configurations require manual review.
- **Limitations:** TCP/UDP routing is still experimental. Implementation maturity varies across providers.

---

### Example 2: Multi-Document Summary of Meeting Notes

**User Request:**
> Synthesize these three meeting note documents into a single weekly digest.

**Source Documents:**

*Monday Standup (Team Alpha):*
> Discussed the v2.1 release blocker — the payment processing timeout issue. Sarah is investigating the root cause in the Stripe webhook handler. ETA for fix: Wednesday. Jake finished the new onboarding flow UI and it's in code review. Maria flagged that the staging environment SSL cert expires Friday.

*Wednesday Sprint Review:*
> Sarah resolved the payment timeout — root cause was a missing retry configuration in the webhook handler. Fix deployed to staging. QA verified it passes. Jake's onboarding flow PR received feedback on accessibility; he's addressing it. New item: product wants to add a dark mode toggle by v2.2. Estimated at 3 story points.

*Friday Retrospective:*
> Team agreed the week was productive. Payment fix shipped on time. Onboarding flow merged after accessibility fixes. SSL cert renewed by Maria on Thursday. Retro feedback: need better alerting for cert expirations. Action item: Maria to set up automated cert renewal monitoring. Looking ahead: dark mode toggle design starts Monday.

**Synthesized Weekly Digest:**

> **Week of Feb 10-14 — Team Alpha Digest**
>
> **Shipped:**
> - Payment processing timeout fix — root cause was missing retry config in Stripe webhook handler (Sarah). Deployed to staging Wednesday, QA-verified.
> - New onboarding flow UI — completed by Jake, updated after accessibility feedback, merged Friday.
> - SSL certificate renewed for staging environment (Maria, Thursday).
>
> **In Progress:**
> - Dark mode toggle added to v2.2 roadmap (3 story points). Design starts next Monday.
>
> **Action Items:**
> - Maria: Set up automated certificate renewal monitoring to prevent future near-misses.
>
> **Retro Takeaway:** The team identified cert expiration alerting as a process gap and is addressing it proactively.

## Best Practices

- **Never add information not in the source.** Summaries must be faithful to the original. If you are uncertain about a detail, omit it rather than guess.
- **Preserve numerical precision.** If the source says "37.5% increase," the summary should say "37.5% increase," not "nearly 40% increase."
- **Adjust tone to match the source.** A summary of a legal contract should be precise and formal. A summary of team chat messages can be concise and informal.
- **Front-load the most important information.** Readers of summaries often skim. Put the key takeaway in the first sentence, then add supporting detail.
- **Use the hierarchical approach for ambiguous length requests.** When the user does not specify length, provide a TLDR plus a paragraph-length summary so they can choose their preferred level.
- **Handle multi-document synthesis thematically.** Don't summarize each document separately and concatenate. Instead, identify themes that cut across documents and organize the synthesis around those themes.

## Edge Cases

- **Very short source text:** If the input is already concise (under 100 words), inform the user that further summarization may lose essential nuance, and offer to highlight the key sentence instead.
- **Source text with contradictions:** If the document contains internally contradictory statements, flag the contradiction in the summary rather than silently choosing one version.
- **Highly technical or jargon-heavy text:** If summarizing for a non-specialist audience, define key terms on first use. If summarizing for experts, preserve the technical vocabulary without over-simplifying.
- **Incomplete or cut-off documents:** If the source text appears truncated (ends mid-sentence, references sections not provided), note this and summarize only the available content, flagging that the summary may be incomplete.
- **Multiple documents with overlapping content:** In multi-document summarization, deduplicate overlapping information rather than repeating it. Note where sources agree and where they diverge.
