---
name: seo-aeo-audit
description: 'Use when asked to improve SEO, optimize for search, fix meta tags, add structured data, or improve AEO visibility. Runs a full technical, page, structured-data, and AEO audit and returns a prioritized markdown report. Not for tasks requiring source or remote-system changes.'
---

# SEO / AEO audit

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Improve SEO, optimize for search, fix meta tags, add structured data, or improve AEO visibility. |
| Authority | Read-only: no file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | None: audit report only; no files are written, no services are modified. |
| Done | Report lists critical/high/medium issues, includes validated JSON-LD recommendations, and provides re-verification steps using Lighthouse, PageSpeed, and Search Console. |

## Inputs

- URL(s) (required): The target page or site URL(s) to audit.
- Focus area (optional): Narrow the audit to one or more of: `technical`, `page`, `structured-data`, `aeo`. Default: all four.
- JSON-LD template (optional): A caller-supplied local template used to validate structured-data recommendations.

## Procedure

1. **Confirm URL and scope.** Require at least one target URL. Parse the scope argument or default to all four areas. **Done when:** the URL and scope are confirmed.
2. **Run technical SEO checks.** Execute Lighthouse against the target URL. Parse the output for: crawlability signals, indexability, HTTP status, canonical tags, robots directives, hreflang, sitemap presence, and Core Web Vitals. Record every violation as critical, high, or medium. **Done when:** technical SEO violations are recorded with severity.
3. **Audit on-page elements.** Fetch the page HTML. Parse title tags, meta descriptions, heading hierarchy (H1-H6), image alt attributes, internal/external link distribution, and content keyword density. Flag duplicate, missing, truncated, or over-stuffed elements. **Done when:** on-page element violations are recorded.
4. **Audit structured data.** Extract all `<script type="application/ld+json">` blocks from the fetched page. Validate each against the appropriate JSON-LD schema type (Article, BreadcrumbList, FAQPage, Product, Organization, LocalBusiness, HowTo, SpeakableSpecification, or others). Report malformed, missing, or conflicting markup. If JSON-LD templates are available, compare the live markup against the recommended template for each detected type. **Done when:** structured-data violations are recorded with corrected JSON-LD blocks.
5. **Audit AEO visibility.** Assess the page for answer-engine optimization signals: clear entity definitions in the first 100 words, FAQ or HowTo blocks, SpeakableSpecification in structured data, passage-level relevance, and citation eligibility signals. Do not fabricate rankings or citations. **Done when:** AEO visibility findings are recorded.
6. **Synthesize the report.** Combine findings from steps 2-5. Assign every issue a severity: critical (blocks indexing), high (major ranking factor impact), or medium (improvement opportunity). Group under the four sections. For every structured-data finding, include the corrected JSON-LD block with the corrected fields shown. **Done when:** the report is synthesized with all findings grouped and severity-assigned.
7. **Add re-verification steps.** After the findings, append a Verification section with step-by-step instructions using Lighthouse (command-line command to re-run the audit), PageSpeed Insights API (curl command to fetch the pagespeed API result), and Google Search Console (URL Inspection API steps to verify index status). **Done when:** the Verification section is appended.
8. **Return the report.** Output the complete markdown report to the user. Do not write any file. **Done when:** the report is returned to the user.

## Failure and recovery

- No URL provided: stop. Return `"error": "url_required"` with the message "Audit requires a target URL."
- Page unreachable: stop. Return `"error": "page_unreachable"` with the URL and the response code or error text.
- Script execution failure: catch the error. Return `"error": "tool_execution_failed"` with the script name and error output.
- Malformed JSON-LD detected: flag as a critical finding in the report. Include the raw block and the parsing error. Do not halt the audit.
- Zero findings in a category: state "No issues detected in this category" explicitly in the report rather than omitting the section.
- Partial tool results: include whatever data the tool returned. Mark any missing fields as `"status": "unavailable"` in the tool output block.

## Output

A markdown audit report with a header (target URL, audit timestamp, scope), four sections (Technical SEO, On-Page SEO, Structured Data, AEO Visibility) each with severity-labeled issues and fixes, validated JSON-LD code blocks for every structured-data fix, a Verification section with exact re-verification commands, and a summary table with issue count by severity.
