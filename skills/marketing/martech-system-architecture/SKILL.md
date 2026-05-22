---
name: martech-system-architecture
description: Design and implement a scalable marketing technology stack that balances first-party data collection with third-party tools. Use this skill when moving beyond basic conversion tracking, consolidating redundant SaaS tools, or preparing for multi-touch attribution (MTA).
---

# MarTech System Architecture

Marketing Technology (MarTech) is the bridge between product, growth, and engineering. This skill focuses on building a "future-proof" system that preserves data integrity and attribution power as a company scales from 30 to 500+ employees.

## Core Principles

- **Tools solve problems:** Never buy a tool to "have" a capability; buy it because a specific problem (e.g., "we can't identify which ads drive opportunities") is too expensive to ignore.
- **Build AND Buy:** Do not view this as a binary choice. Buy a tool to solve 90% of the baseline problem (e.g., email delivery) and build the final 10% internally to create a competitive advantage.
- **Think Gray:** Avoid making snap decisions on tools or architecture. Delay the decision as long as possible until the pain point is clearly defined to avoid technical debt.

## The PPS Framework for System Design
Before implementing any new MarTech tool or process, walk through these three steps:

1. **Problem:** Define the discrete issue (e.g., "Onboarding is manual and slow for the sales team").
2. **People:** Identify stakeholders (e.g., "Does the CRO need to approve this? Do the sellers need training?").
3. **System:** Only after defining the above, design the technical solution (e.g., "Automate permissions via a Command K interface").

## Implementation: Future-Proof Attribution
To avoid the common pitfall of having "zero data" for multi-touch attribution (MTA) later, implement this ingestion strategy today:

### 1. Data Collection Taxonomy
Ensure your website or app collects the following parameters on every session:
- **Referrer:** The origin URL.
- **Ad Network IDs:** Specific parameters like `fbclid` (Facebook), `gclid` (Google), and `ttclid` (TikTok).
- **Standard UTMs:** Source, Medium, Campaign, Content, Term.

### 2. State Management (First/Last Touch)
Instead of just sending the current UTM to your database, store the "First" and "Last" state locally (e.g., in first-party cookies or local storage):
- **UTM_First_Medium:** Stays constant once set.
- **UTM_Last_Medium:** Overwritten every time the user arrives via a new marketing channel.

### 3. Data Flow
- **Ingestion:** Use a CDP (e.g., Amplitude, Segment) or a collector (e.g., Snowplow) to fire a page-view event containing both the "First" and "Last" attributes.
- **Storage:** Route all events to a data warehouse (e.g., Snowflake).
- **Activation:** Use a Reverse ETL tool (e.g., Hightouch, Census) to sync "Opportunity Created" or "LTV" data back to ad networks to optimize bidding based on downstream value rather than just clicks.

## The "Golden Stack" Recommendations

| Category | B2C Recommendation | B2B Recommendation |
| :--- | :--- | :--- |
| **CDP / Analytics** | Amplitude | Amplitude |
| **Warehouse** | Snowflake | Snowflake |
| **Email/Lifecycle** | Customer.io (early) → Braze | Braze or HubSpot |
| **Reverse ETL** | Hightouch | Hightouch |
| **Attribution** | AppsFlyer (Mobile) or Branch | Branch (Web focus) |

## Examples

**Example 1: Setting up Attribution for a New Launch**
- **Context:** A growth PM wants to track which LinkedIn ads lead to high-value signups.
- **Application:** Instead of just looking at the LinkedIn dashboard, the MarTech lead ensures the `li_fat_id` and UTMs are captured in a first-party cookie. They fire an event to Snowflake.
- **Output:** A SQL query can now join the user's initial LinkedIn click with their purchase event six months later, even if the browser cleared the original referral data.

**Example 2: Managing Tool Redundancy**
- **Context:** A company has both HubSpot and Salesforce, leading to data silos.
- **Application:** Apply the "Build and Buy" framework. Use HubSpot for top-of-funnel lead capture (Buy) and Salesforce as the source of truth for deals (Buy), but build a custom integration via a Reverse ETL (Build) to ensure user events from the product are visible to sales reps in Salesforce.
- **Output:** Sales reps see "Feature X used 5 times" directly on the Lead record without logging into a separate analytics tool.

## Common Pitfalls
- **The "Village" Approach:** Assuming everyone can manage the CDP. Around 100-150 employees, you must hire a dedicated MarTech person to prevent schema rot and contract bloat.
- **Tool Bias:** Hiring a PM who says, "We must use Segment because I used it at my last job." Always prioritize the Problem/People before the specific tool name.
- **Ignoring Browsers:** Relying solely on third-party cookies. Browsers (Safari/Chrome) now truncate URL parameters. You must move to server-side tracking or first-party cookie storage to maintain data accuracy.
- **Admin Neglect:** Giving "Edit" access to everyone. One untrained user can send a "Test" email to a million-person production list. Automate permissions based on role and tenure.