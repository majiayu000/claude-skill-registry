---
name: research
description: Find authoritative answers from official docs, RFCs, standards, and academic sources — never from blogs or opinions
triggers: [research, find, how to, unknown, best practice, which library, official docs, RFC, spec, standard, look this up]
context_cost: medium
---

# Research Skill

## Goal
Find accurate, current answers from authoritative sources only. Prevent API hallucination, deprecated usage, and wrong regulatory interpretation. All findings stored in semantic memory for reuse.

## Authoritative Source Tiers

| Tier | Sources | Trust Level |
|---|---|---|
| **Tier 1 (Primary)** | Official language docs (MDN, nodejs.org, laravel.com, docs.python.org), Official specs (RFC.editor.org, W3C, ECMA), Security standards (OWASP, NIST, CIS, CVE.mitre.org) | Highest |
| **Tier 2 (Academic/Official)** | arXiv.org, IEEE Xplore, ACM Digital Library, Official GitHub repos (github.com/[org]/[repo]), Official changelogs/release notes | High |
| **Tier 3 (Verified Industry)** | Anthropic docs, AWS docs, GCP docs, Azure docs, Microsoft Docs | Medium |
| **NOT Acceptable** | Blog posts, Medium, Reddit, StackOverflow opinions, Dev.to | Do not cite |

## Steps

1. **Formulate the precise research question**
   - Include: exact library/framework name + version number
   - Include: what you need to know (API signature, behavior, requirements)
   - Example: "What are the valid values for the SameSite attribute in Set-Cookie header per RFC 6265?"

2. **Use Context-7 MCP first** (for library/SDK questions)
   ```
   # Context-7 provides up-to-date, version-specific library documentation
   # Use it to avoid hallucinating deprecated or non-existent API methods
   context7: resolve-library-id "express"
   context7: get-library-docs "/expressjs/express" topic="routing"
   ```

3. **Search with authoritative source filter**

   Using Brave Search MCP or Tavily MCP:
   ```
   # Add site: filter to restrict to official sources
   query: "JWT signature verification site:nodejs.org OR site:rfc-editor.org"
   query: "GDPR article 17 right to erasure site:gdpr-info.eu OR site:eur-lex.europa.eu"
   query: "bcrypt cost factor recommendation site:owasp.org"
   ```

4. **Verify the source is current version**
   - Check: does this documentation apply to the version we're using?
   - Check: is there a newer version of this API that deprecates this approach?
   - If version mismatch found: flag to human — do NOT assume old behavior applies

5. **Cross-reference with at least 2 Tier 1/2 sources**
   - A single source is insufficient for security decisions
   - If 2 sources conflict: flag as "uncertain, requires human validation"
   - If only 1 Tier 1 source found: note as "single source — verify before implementing"

6. **Never guess or extrapolate**
   ```
   If authoritative source not found:
     DO NOT assume behavior
     DO NOT use knowledge cutoff info for rapidly evolving topics
     DO: Report "authoritative source not found" + propose alternatives:
       a) Use known alternative with documented behavior
       b) Human provides authoritative reference
       c) Skip feature until verified
   ```

7. **Store finding in semantic memory**
   - Append to: `agents/memory/semantic/PROJECT_KNOWLEDGE_TEMPLATE.md`
   - Format:
     ```markdown
     ### [Topic] — verified [DATE]
     **Question:** [what was researched]
     **Finding:** [what was found]
     **Source:** [exact URL to official doc]
     **Applies to version:** [library@version]
     **Expires:** [date or "review at next major version"]
     ```

8. **Return the answer with citation**
   - Always include the source URL in your response
   - Always state which version the answer applies to
   - Always note if there are known future changes planned

## Constraints
- NEVER cite blog posts, Medium, or StackOverflow as the authority on a technical question
- If only Tier 3 sources found: flag as "vendor documentation — verify against official spec"
- For security decisions: require Tier 1 source (OWASP, NIST, or official RFC)
- For regulatory requirements: require official government or standards body source

## Output Format
Finding with: answer, source URL (Tier 1/2), version applicability, confidence level (High/Medium/Low based on source tier).
