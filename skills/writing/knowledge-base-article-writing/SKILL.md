---
name: knowledge-base-article-writing
description: Write clear, searchable help center articles and FAQ entries based on support data, product documentation, and common customer questions. Use when the user requests knowledge base article writing or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Knowledge Base Article Writing

Produce polished help center articles and FAQ entries that deflect support tickets by giving customers clear, self-serve answers. This skill turns support ticket patterns, product changes, and common questions into structured articles optimized for readability, search, and scannability, following documentation best practices for step-by-step guides, troubleshooting flows, and reference material.

## Workflow

1. **Identify topic from support data** — Mine support ticket trends, search analytics (what customers search for but don't find), and CSM feedback to find the highest-impact topics. Prioritize by ticket volume (articles addressing the top 10 question clusters deflect the most tickets), topic complexity (complex topics benefit most from written guides), and recency (new features or recent changes need documentation immediately).

2. **Research the solution** — Gather the authoritative answer from engineering docs, internal wikis, product specs, and subject matter experts. Test the workflow yourself end-to-end in the product to verify accuracy. Document the exact UI text, button labels, and navigation paths as they appear in the current product version. Note any prerequisites, required permissions, or plan-tier restrictions.

3. **Structure the article** — Follow a consistent template: **Title** (action-oriented, matches how customers search), **Summary** (1-2 sentence answer for scanning), **Prerequisites** (what the reader needs before starting), **Steps** (numbered, one action per step, with expected outcome), **Troubleshooting** (common errors and their fixes), and **Related Articles** (links to adjacent topics). Keep the hierarchy flat — use H2 for major sections and H3 sparingly.

4. **Add visual aids and code examples** — Include screenshots for UI-heavy workflows (annotated with numbered callouts matching the steps), code snippets for API or CLI workflows (with language tags, copy buttons, and expected output), and diagrams for architecture or flow explanations. Every image should have alt text. Every code block should be tested and runnable.

5. **Optimize for search** — Write the title using the exact phrasing customers use (check search analytics). Front-load keywords in the first sentence. Add metadata tags for category, product area, and plan tier. Include common alternate phrasings as a "Also known as" line or in the article metadata. Keep URLs clean and human-readable.

6. **Review for accuracy and clarity** — Have a subject matter expert verify technical accuracy. Run a readability check targeting grade 8 reading level. Ensure every step is testable by someone with no prior context. Check that screenshots match the current UI. Validate all links. Set a review-by date (typically 90 days or on next product release affecting the topic).

## Usage

Describe the article topic, target audience, and any specific details to include. The agent writes a complete, publish-ready article.

```
Write a help center article for "How to set up SSO with SAML." Target audience
is IT admins. Our product supports Okta, Azure AD, and OneLogin. Include
troubleshooting for common SAML errors.
```

## Examples

### Example 1: How-to article — SSO with SAML setup

**Input:** SSO/SAML setup guide for IT administrators.

**Output:**

---

**How to Set Up Single Sign-On (SSO) with SAML**

Enable SAML-based SSO so your team can sign in using your company's identity provider. Supported providers: Okta, Azure AD, and OneLogin.

**Prerequisites**
- Admin role in your account (Settings → Team → Roles shows "Admin" next to your name)
- Access to your identity provider's admin console
- Your account must be on the Enterprise plan

**Steps**

1. Go to **Settings → Security → Single Sign-On** and click **Configure SSO**.

   *[Screenshot: Settings page with Security tab highlighted and SSO section visible]*

2. Select your identity provider from the dropdown: **Okta**, **Azure AD**, or **OneLogin**.

3. Copy the values shown on screen — you will need these in your identity provider:
   - **ACS URL:** `https://app.example.com/auth/saml/callback`
   - **Entity ID:** `https://app.example.com/saml/metadata`
   - **RelayState:** leave blank unless using a custom landing page

4. In your identity provider's admin console, create a new SAML application using the values from step 3.

   **Okta:** Applications → Create App Integration → SAML 2.0 → paste ACS URL and Entity ID.

   **Azure AD:** Enterprise Applications → New Application → Create your own → SAML → Basic SAML Configuration → paste values.

   **OneLogin:** Applications → Add App → SAML Custom Connector → Configuration → paste values.

5. Download the **Federation Metadata XML** file from your identity provider and upload it on the SSO configuration page.

6. Set the required attribute mappings:
   ```
   email    → user.email       (Required)
   firstName → user.firstName  (Required)
   lastName  → user.lastName   (Required)
   role      → user.role       (Optional — maps to app roles)
   ```

7. Click **Test Connection**. A new browser tab opens. Sign in with your identity provider credentials. If successful, you'll see "SSO connection verified."

8. Toggle **Enforce SSO** to require all team members to sign in via your identity provider. Non-SSO login will be disabled after a 24-hour grace period.

**Troubleshooting**

| Error | Cause | Fix |
|-------|-------|-----|
| "SAML response signature invalid" | Metadata XML is outdated or from the wrong app | Re-download the metadata XML from your IdP and re-upload it |
| "User not found" | Email in SAML assertion doesn't match any account email | Verify the email attribute mapping in your IdP sends the user's primary email |
| "Clock skew detected" | Server time difference between IdP and our service exceeds 5 minutes | Ensure your IdP server's NTP is synced. We allow a 5-minute skew tolerance |
| "Audience mismatch" | Entity ID in your IdP doesn't match the value from step 3 | Copy the exact Entity ID from Settings → SSO — trailing slashes matter |
| Test passes but users can't log in | Enforce SSO is off, or users are hitting the wrong login URL | Share the SSO login URL from Settings → SSO with your team, and enable Enforce SSO |

**Related Articles**
- Managing Team Roles and Permissions
- Setting Up SCIM User Provisioning
- Configuring Multi-Factor Authentication

---

### Example 2: FAQ entry — billing questions

**Input:** Common billing FAQ covering plan changes, invoices, and refunds.

**Output:**

---

**Billing FAQ**

Answers to the most common questions about plans, invoices, payments, and refunds.

**How do I upgrade or downgrade my plan?**

Go to **Settings → Billing → Plan** and click **Change Plan**. Select your new plan and confirm. Upgrades take effect immediately and you'll be charged a prorated amount for the remainder of your billing cycle. Downgrades take effect at the start of your next billing cycle — you keep access to your current plan's features until then.

**Where can I find my invoices?**

All invoices are available at **Settings → Billing → Invoice History**. Click any invoice to view or download a PDF. Invoices are also emailed to the billing contact on file within 24 hours of each charge.

**How do I update my payment method?**

Go to **Settings → Billing → Payment Method** and click **Update**. We accept Visa, Mastercard, American Express, and ACH bank transfer (annual plans only). Your new payment method will be used for all future charges.

**Can I get a refund?**

We offer a full refund within 14 days of any charge if you're not satisfied. After 14 days, we issue prorated credit toward future billing. To request a refund, email billing@example.com with your account email and the invoice number. Refunds are processed within 5-7 business days.

**What happens if my payment fails?**

We retry failed payments on days 1, 3, and 7. You'll receive an email notification after each failed attempt. If payment isn't resolved within 14 days, your account is downgraded to the free tier. Your data is preserved for 90 days — upgrade anytime to restore full access.

**Do you offer annual billing discounts?**

Yes. Annual billing saves 20% compared to monthly billing on all paid plans. Switch to annual billing anytime from **Settings → Billing → Plan** — select "Annual" and your savings are applied immediately with a prorated credit for any remaining monthly balance.

**Related Articles**
- Understanding Your Invoice Line Items
- Setting Up ACH Bank Transfer Payments
- Managing Multiple Billing Accounts

---

## Best Practices

- Write titles as questions or action phrases that match how customers search — "How to set up SSO" beats "SSO Configuration Guide" because customers search in natural language.
- One article, one topic. If an article covers two distinct workflows, split it. Customers who search for "export data" should not land on a page that also covers "import data" — even if they seem related to you.
- Start every article with a one-sentence summary that directly answers the question. Customers scan, not read — if the answer is in the first line, they get value even if they don't read further.
- Use consistent terminology that matches the UI labels exactly. If the button says "Configure," don't write "Set Up" in the article. Mismatches between documentation and UI cause confusion and erode trust.
- Include a "last verified" date on every article and build an automated alert when the product area it covers receives an update in the changelog.
- Track article effectiveness with two metrics: search-to-view rate (are customers finding it?) and deflection rate (did the customer open a ticket within 30 minutes of viewing?).

## Edge Cases

- **Product UI changes between writing and publishing** — Always take screenshots last, after the article text is finalized. Include the product version number in image alt text so stale screenshots are easier to identify during audits.
- **Feature available only on certain plans** — Add a callout banner at the top: "This feature is available on Pro and Enterprise plans." Do not bury plan restrictions in step 4 after the reader has already invested time.
- **Multi-language knowledge base** — Write the canonical article in English first, then localize. Do not machine-translate and publish without human review — technical terms and UI labels must match the localized product interface.
- **Deprecated features** — Don't delete articles for deprecated features. Add a deprecation banner with the sunset date and link to the replacement article. Customers on legacy plans may still need the old documentation.
- **Conflicting information from multiple sources** — When internal docs disagree with the product's actual behavior, the product behavior is the source of truth. Test in the product, document what actually happens, and file a bug if the behavior is wrong.
