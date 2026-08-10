---
name: terms-of-service-generation
description: Draft Terms of Service documents for web applications, SaaS platforms, and digital marketplaces. Use when the user requests terms of service generation or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Terms of Service Generation

Draft comprehensive Terms of Service (ToS) documents tailored to web applications, SaaS platforms, and digital marketplaces. This skill produces enforceable, jurisdiction-aware terms covering user rights and restrictions, acceptable use, liability, warranties, dispute resolution, and platform-specific concerns like content moderation, subscription billing, and API usage.

## Workflow

1. **Understand Business Model** — Determine the platform type (SaaS, marketplace, social platform, API service), revenue model (subscription, freemium, transaction fees, advertising), user types (consumers, businesses, or both), and the core value proposition. Identify whether the service handles payments, user content, third-party integrations, or regulated data. These factors dictate which ToS sections are essential.

2. **Define User Rights and Restrictions** — Establish what users are permitted to do (acceptable use) and explicitly prohibited from doing (abuse, scraping, reverse engineering, circumventing access controls). Define account creation requirements including age minimums, accurate information obligations, and account security responsibilities. Specify the license granted to users and any usage limits tied to subscription tiers.

3. **Draft Liability and Warranty Sections** — Craft disclaimers of warranties (AS-IS/AS-AVAILABLE), limitations of liability with monetary caps, and exclusions for consequential damages. Include specific carve-outs required by consumer protection laws in key jurisdictions. Address service availability commitments or explicitly disclaim uptime guarantees if no SLA exists.

4. **Add Dispute Resolution Mechanisms** — Define the governing law and jurisdiction, include arbitration clauses with class action waivers where enforceable, specify small claims court exceptions, and outline informal dispute resolution steps that must precede formal proceedings. Consider whether B2B users should have different dispute terms than consumers.

5. **Review Enforceability** — Audit the draft for unconscionable terms that courts routinely strike down, ensure conspicuous presentation of material terms (auto-renewal, arbitration), verify compliance with platform-specific requirements (app store guidelines), and confirm that modification and termination provisions are reasonable and provide adequate notice.

## Usage

Describe your platform, business model, user base, and any specific concerns. Mention if you handle user-generated content, process payments, or operate in regulated industries.

**Example prompt:**
```
Generate Terms of Service for "CloudDeploy", a freemium SaaS platform for deploying web applications. Free tier has resource limits, paid tiers are monthly subscriptions. Users deploy their own code. We're a US Delaware company with global users.
```

## Examples

### Example 1: Freemium SaaS Platform

**Input:** CloudDeploy — a web application deployment platform. Delaware C-Corp. Free tier (3 projects, 1GB bandwidth), Pro tier ($29/mo), Team tier ($99/mo). Users deploy their own code and static assets. Integrates with GitHub.

**Output (key sections):**

**1. Acceptance of Terms**

By creating an account or using CloudDeploy, you agree to these Terms of Service and our Privacy Policy. If you use CloudDeploy on behalf of an organization, you represent that you have authority to bind that organization to these terms.

**2. Account and Subscription Terms**

Free tier accounts are subject to the resource limits published on our pricing page, which we may adjust with 30 days' notice. Paid subscriptions are billed monthly in advance. You may upgrade or downgrade at any time — upgrades take effect immediately with prorated charges, downgrades take effect at the next billing cycle. We will attempt to charge your payment method automatically; after two failed attempts, we may suspend your account after 7 days' written notice.

**3. User Responsibilities and Acceptable Use**

You are responsible for all code, content, and data you deploy through CloudDeploy ("User Content"). You must not deploy content that: (a) violates any law or regulation, (b) infringes third-party intellectual property, (c) contains malware or is designed to disrupt other users' deployments, (d) operates as an open proxy or relay, (e) mines cryptocurrency, or (f) exceeds your tier's resource allocation through circumvention. We reserve the right to suspend deployments that threaten platform stability without prior notice.

**4. Limitation of Liability**

TO THE MAXIMUM EXTENT PERMITTED BY LAW, CLOUDDEPLOY'S TOTAL LIABILITY FOR ANY CLAIMS ARISING FROM THESE TERMS OR YOUR USE OF THE SERVICE SHALL NOT EXCEED THE GREATER OF (A) THE FEES YOU PAID IN THE 12 MONTHS PRECEDING THE CLAIM OR (B) $100. THIS CAP DOES NOT APPLY TO CLOUDDEPLOY'S INDEMNIFICATION OBLIGATIONS OR WILLFUL MISCONDUCT.

### Example 2: Marketplace with User-Generated Content

**Input:** ArtVault — a digital art marketplace. Artists upload and sell digital artwork. Platform takes 15% commission. Users can leave reviews. DMCA compliance needed.

**Output (key sections):**

**Content Ownership and License**

Artists retain full ownership of their uploaded artwork. By listing content on ArtVault, you grant us a non-exclusive, worldwide license to display, reproduce, and distribute thumbnails and previews of your artwork solely for operating and promoting the marketplace. This license terminates 30 days after you remove the content, except for copies already purchased by buyers.

**Content Moderation**

ArtVault reserves the right to remove content that violates these terms or our Content Guidelines. We use a combination of automated scanning and human review. Content may be removed without prior notice if it depicts illegal activity, non-consensual intimate imagery, or child exploitation. For other violations, we will notify the creator and provide 48 hours to appeal before removal, except where immediate removal is required by law.

**DMCA and Copyright Infringement**

If you believe content on ArtVault infringes your copyright, submit a DMCA takedown notice to our designated agent at dmca@artvault.example with: (1) identification of the copyrighted work, (2) identification of the infringing material with URL, (3) your contact information, (4) a statement of good faith belief, (5) a statement under penalty of perjury that the information is accurate, and (6) your physical or electronic signature. Counter-notices may be filed within 10 business days. We implement a repeat infringer policy and will terminate accounts with three substantiated strikes.

**Transaction Terms**

Sellers set their own prices. ArtVault collects payment from buyers and remits the net amount (sale price minus 15% commission) to sellers within 14 business days via the seller's chosen payout method. All sales are final unless the delivered file is materially different from the listing or is corrupted. Dispute resolution between buyers and sellers is facilitated by ArtVault for 30 days post-purchase, after which disputes must be resolved directly between the parties.

## Best Practices

- Use a layered approach: lead with a plain-language summary of key terms, then provide the full legal text. Courts increasingly favor clarity.
- Make material terms conspicuous — auto-renewal, arbitration clauses, and limitation of liability should not be buried in boilerplate.
- Include a severability clause so that if one provision is struck down, the remaining terms survive.
- Version your ToS with a date and maintain an archive of previous versions for transparency.
- Distinguish between terms for different user types (free vs. paid, consumers vs. business) where obligations differ materially.
- Specify a reasonable notice period (at least 30 days) for material changes and describe how notice will be delivered.

## Safety Boundaries

- Treat the output as informational drafting or issue spotting, not legal advice.
- Identify the governing jurisdiction and relevant effective date; verify changing requirements against current primary sources.
- Do not claim that language is compliant, enforceable, or complete. Flag uncertainty and recommend qualified counsel for material decisions.
- Do not file, publish, accept, sign, or send legal terms without the user reviewing and explicitly authorizing that action.

## Edge Cases

- **Users in the EU or UK** — Consumer protection directives may override certain ToS provisions. Mandatory arbitration is generally unenforceable for consumers in the EU. The right of withdrawal (14-day cooling-off period) applies to digital content purchases unless explicitly waived at the point of sale.
- **Open-source components in the platform** — If the platform includes or distributes open-source software, ToS should not conflict with applicable open-source licenses. Include an open-source notice section if required.
- **Government or educational users** — These entities often cannot agree to indemnification, arbitration, or governing law provisions. Consider a separate addendum or allow those clauses to be overridden by applicable government procurement terms.
- **Platform shutdowns or pivots** — ToS should address what happens to user data and prepaid subscriptions if the service is discontinued. Provide a data export period and prorated refund terms.
- **API and programmatic access** — If the platform offers an API, include rate limiting terms, acceptable automation use, and separate API terms that address machine-to-machine usage distinct from interactive use.
