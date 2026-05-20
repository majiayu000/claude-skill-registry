---
name: script-audit
description: Audit third-party scripts on the storefront for performance and security impact
user-invocable: true
---

You are helping the team audit third-party scripts running on the Jocko Fuel storefront.

Follow these steps:

### Step 1: Identify Scripts

Delegate to the `script-investigator` agent to catalog all third-party scripts on the target page(s). For each script, capture:
- **Source domain** (e.g., googletagmanager.com, klaviyo.com)
- **Purpose** (analytics, marketing, chat widget, A/B testing, etc.)
- **Load method** (sync, async, defer)
- **File size** (KB transferred)

Ask the user which page to audit, or default to the homepage.

### Step 2: Analyze Performance Impact

For each script, delegate to the `performance-auditor` agent to measure:
- **Load time contribution** (ms added to page load)
- **Main thread blocking time** (ms of main thread occupied)
- **Network requests triggered** (cascading requests from the script)
- **Total resource footprint** (KB of JS, CSS, images loaded)

Rank scripts by total performance impact (highest impact first).

### Step 3: Check Security Concerns

Delegate to the `script-investigator` agent to evaluate:
- Are scripts loaded over HTTPS?
- Do any scripts have known vulnerabilities?
- Are there scripts from unfamiliar or untrusted domains?
- Do any scripts access sensitive data (cookies, form inputs)?
- Are Content Security Policy headers properly configured?

### Step 4: Generate Recommendations

For each script, recommend one of:
- **Keep**: Essential, well-optimized, no concerns
- **Optimize**: Needed but can be deferred, async-loaded, or version-updated
- **Review**: Purpose unclear or redundant with another script
- **Remove**: Unused, high-impact, or security risk

Present as a table with script name, purpose, impact score, security risk, and recommendation.

### Error Handling

- If the page uses a consent manager that blocks scripts, note which scripts load before/after consent
- If script sources are obfuscated, flag them for manual review
- If performance measurement tools are unavailable, provide qualitative assessment based on script analysis
