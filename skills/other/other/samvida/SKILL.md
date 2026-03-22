---
name: samvida
description: Generate an agentic contract (llms.txt) for any business website. Crawls the site, fills gaps conversationally, and produces a structured agent-optimized llms.txt. Trigger when a user asks to "generate llms.txt", "create an agentic contract for [url]", "make my site agent-readable", or "update my llms.txt".
---

# Samvida — Agentic Contracts for Your Business

## Overview

This skill crawls a business website, extracts structured information, and generates a properly formatted `llms.txt` file — the standard that makes any business readable and transactable by AI agents.

It follows the [llmstxt.org](https://llmstxt.org) specification with business-specific extensions:
- `## Team` — builds agent trust in the people behind the business
- `## Clients & Testimonials` — social proof for agent decision-making
- `## For Agents` — how agents can interact (or a clear "coming soon" notice)

Read `references/llms_txt_spec.md` before generating any output.

---

## Workflow

### Step 1 — Get the URL

If the user didn't provide a URL, ask:
> "What's the website URL?"

Normalize it (add `https://` if missing).

---

### Step 2 — Crawl

Run the crawler:
```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/crawl.py \
  {url} > /tmp/llms_business_info.json
```

Read `/tmp/llms_business_info.json`. Note:
- What pages were crawled
- What was found vs missing (team, pricing, testimonials, API)
- Whether an existing `llms.txt` was found

Tell the user briefly:
> "Crawled {domain} ({N} pages). Found: {what was found}. I'll ask about a few things I couldn't determine."

If the crawl found an existing `llms.txt`, note it:
> "I noticed you already have a llms.txt at {domain}/llms.txt. I'll generate a fresh one — you can compare and decide which to keep."

---

### Step 3 — Ask for additional sources (always ask this first)

> "Are there any other pages I should read? (docs, API reference, existing llms.txt, press page — anything useful)"

If they provide URLs, re-run the crawl with those extras:
```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/crawl.py \
  {url} {extra_url1} {extra_url2} > /tmp/llms_business_info.json
```

If they say no/skip, continue.

---

### Step 4 — Generate Pass 1 draft + gap report

Generate a draft llms.txt now using what you have from the crawl. Use all heuristic signals (`team_found`, `testimonials_found`, `pricing_found`, etc.) and the `raw_text_summary`.

Write the draft. For any section you couldn't populate confidently, use a clear `[NOT FOUND]` placeholder.

Then show it to the user with a gap report:

> "Here's a first draft of your llms.txt:
> ```
> {draft}
> ```
>
> **Found automatically:** {brief list — e.g. emails, pricing page, testimonials from Wybrid + Cital}
> **Couldn't determine:** {brief list — e.g. team, pricing figures, API}
>
> Two questions to start:
>
> 1. {Most important gap — e.g. "Who's on the founding team? Names, roles, and an email if you're comfortable."}
> 2. {Second most important — e.g. "What's your pricing model? Even a rough description — per-candidate, subscription, etc."}
>
> _(I have a few more after these. Also — say **'dig deeper'** if you'd rather I try to find it myself.)"

---

### Step 4b — Handle "dig deeper" (Pass 2)

If the user says "dig deeper" (or similar — "try again", "re-crawl", "look harder"):

Re-run the crawl in deep mode:
```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/crawl.py \
  {url} {extra_urls} --deep > /tmp/llms_business_info.json
```

This returns `pages_raw` — the full raw text of every crawled page. Use it to extract structure with the LLM. In your generation prompt (Step 5), add:

```
In addition to the heuristic signals, here is the full raw text from each crawled page.
Extract team members, testimonials, pricing details, and any API information directly from this text.

Homepage raw text:
{pages_raw[homepage_url]}

Team page raw text (if available):
{pages_raw[team_url]}

Pricing page raw text (if available):
{pages_raw[pricing_url]}
```

Tell the user:
> "Doing a deeper crawl — this takes a bit longer but I'll extract everything I can from the raw page content."

After Pass 2, show the updated draft with the same gap report format. Whatever still can't be found, ask the user directly.

---

### Step 5 — Conversational gap-filling (for anything still missing)

Ask questions **one at a time** — only for things still `[NOT FOUND]` after Pass 1/2. Wait for each answer. Stop as soon as you have enough to finalize.

Use your judgment — if the user has already filled most gaps conversationally, skip remaining questions and generate.

**Q1 — Core value for agents (always ask):**
> "In one or two sentences: what should an AI agent understand about what it can *do* or *get* by working with {domain}?"

**Q2 — Team (ask if team not found in crawl):**
> "I didn't find team info publicly. Want to add a Team section? It helps agents trust who's behind the business. Just names, roles, and emails if you're comfortable."

**Q3 — Clients / testimonials (ask if not found):**
> "Any existing clients or testimonials I can include? Even a couple of company names or a one-line quote builds agent trust. Totally optional."

**Q4 — API / integration (ask if api_found=false):**
> "Is there a public API or docs page agents can reference? (skip if not applicable)"

**Q5 — Pricing (ask if pricing_found=false):**
> "What's the pricing model? Even a rough description helps — like 'per assessment' or 'monthly subscription'."

**Q6 — ICP / agent-buyers (ask if not obvious from context):**
> "Who are the kinds of agents or automated systems most likely to want to work with you? (e.g. HR bots, recruiting pipelines)"

**Q7 — Anything else (optional, ask last):**
> "Anything else agents should know before working with you? (geographic limits, onboarding steps, etc.)"

---

### Step 6 — Generate final llms.txt

Read `references/llms_txt_spec.md` now if you haven't already.

Generate the complete `llms.txt` using ALL information gathered:
- The crawled `business_info` JSON (and `pages_raw` if deep mode ran)
- The user's answers from the conversation
- The spec from `references/llms_txt_spec.md`

**Generation rules:**
1. Follow the spec format exactly: H1 title → blockquote summary → H2 sections → named links
2. Every bullet = `- [Title](url): description` — no plain text bullets
3. Section order: Services → Team → Clients & Testimonials → Compliance → Reviews → For Agents → Pricing → API → Links → Optional
4. **`## Team`**: Always include. Use crawled/user-provided data. If none available, omit silently.
5. **`## Clients & Testimonials`**: Always try to include. Structure:
   - ICP bullets first (who the business serves)
   - Then a `###` subsection per named client where you have a real quote or case study detail
   - Each subsection: blockquote with verbatim/lightly-cleaned quote, optional Problem: and Outcome: lines
   - If you only have a name + one-liner with no detail, a single bullet is fine
   - Never invent quotes or outcomes
6. **`## Compliance`**: Include if any certifications or standards (SOC 2, ISO 27001, GDPR, HIPAA, etc.) are mentioned anywhere on the site or by the user. Omit if none found.
7. **`## Reviews`**: Include if any third-party ratings, scores, awards, or recognitions (G2, ProductHunt, Trustpilot, Gartner, Capterra, Forbes, YC, etc.) are mentioned. Omit if none found.
8. **`## For Agents`**: ALWAYS include. If no API info: add the "coming soon" notice + contact email. Never skip.
7. **`## Pricing`**: If unknown, link to pricing page with no summary. If no pricing page, omit.
8. **`## API`**: Document URL only — no auth details, no secrets.
9. **`## Optional`**: FAQs, blog, case studies, anything supplementary.
10. Do NOT invent facts. If something is unknown and user didn't provide it, either omit it or note it clearly.
11. Keep it tight — this is for agents, not humans. No marketing fluff.

Write the final llms.txt to `/tmp/samvida_llms.txt`.

---

### Step 7 — Show and confirm

Show the full llms.txt to the user in a code block, then ask:

> "Here's your llms.txt 👆
>
> Does this look right? You can:
> - Tell me what to change
> - Say **'save'** to download it
> - Say **'deploy'** when you're ready to push it live (Phase 2)"

---

### Step 8 — Handle revisions

If the user asks for changes, make them and show the updated version. Repeat until satisfied.

If they say **'save'**: tell them the file is at `/tmp/samvida_llms.txt` and they can copy it to their project.

If they say **'deploy'**: proceed to Step 9.

---

### Step 9 — Deploy

**If an existing llms.txt was found during crawl**, warn first:
> "⚠️ I found an existing llms.txt at **{domain}/llms.txt**. Deploying will replace it. Want to see a diff first, or go ahead?"

Show a simple diff if requested (old vs new, first 20 lines each).

**First, detect the platform** — check the crawl data for CMS detection, or ask:
> "Which platform is **{domain}** hosted on? (Webflow / Framer / Cloudflare / other)"

Then follow the relevant path below.

---

#### 9a — Cloudflare Workers (any site with Cloudflare DNS)

Best for: any site whose DNS goes through Cloudflare (the orange cloud ☁️ is enabled).

> "To deploy to **{domain}/llms.txt** via Cloudflare Workers, I need 3 things:
>
> 1. **API Token** — Cloudflare dashboard → My Profile → API Tokens → Create Token → **'Edit Cloudflare Workers'** template
> 2. **Account ID** — top-right of your Cloudflare dashboard
> 3. **Zone ID** — Cloudflare dashboard → click your domain → right sidebar under 'API'
>
> These are only used for this deployment and never stored."

```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/deploy.py \
  --provider cloudflare \
  --llms-txt /tmp/samvida_llms.txt \
  --cf-token "{token}" \
  --account-id "{account_id}" \
  --zone-id "{zone_id}" \
  --domain "{domain}"
```

---

#### 9b — Webflow (fully automated)

Best for: sites hosted on Webflow (webflow.io or custom domain via Webflow hosting).

> "To deploy to Webflow, I need your **Webflow Site API Token**:
>
> Webflow dashboard → your site → **Site Settings → Integrations → API Access → Generate API Token**
>
> Scopes to enable: Assets (Read/Write), Sites (Read), Redirects (Read/Write), Publishing (Publish)
>
> Optionally: your **Site ID** (visible in the Webflow dashboard URL — auto-detected if omitted)."

```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/deploy.py \
  --provider webflow \
  --llms-txt /tmp/samvida_llms.txt \
  --webflow-token "{token}" \
  --domain "{domain}"
  # --site-id "{site_id}"  # optional
```

**How it works:** Uploads llms.txt to Webflow's CDN → adds a 301 redirect `/llms.txt` → CDN URL → publishes. Agents follow the redirect transparently.

**Note:** Redirect API requires Webflow Basic plan or above. If the user is on Starter, Samvida will output manual redirect steps.

---

#### 9c — Framer (instructions-only)

Framer has no public REST API for file hosting or redirect management. No credentials needed — just run the script and relay the output.

```bash
~/.virtualenvs/samvida/bin/python3 \
  ~/.openclaw/workspace/samvida/scripts/deploy.py \
  --provider framer \
  --llms-txt /tmp/samvida_llms.txt \
  --domain "{domain}"
```

The script outputs three options (A/B/C) with step-by-step instructions and prints the full llms.txt content for the user to save. Relay all of it clearly to the user.

---

#### 9d — CMS detected (Cloudflare Worker deployed but CMS takes priority)

**On CMS detected** (output contains `SAMVIDA_CMS:{name}`):

> "The Worker deployed successfully, but **{CMS}** is serving `/llms.txt` directly from their servers — so it takes priority over the Worker.
>
> Run the right deploy command for your platform:
> {paste the CMS-specific instructions from the script output}

---

**On any error:** relay the script's human-readable error message directly with a suggested fix.

---

## Notes

- **Existing llms.txt**: If the crawl found one, mention it early: "I noticed you already have a llms.txt. I'll generate a fresh one — you can compare and decide which to keep."
- **Anchor-only links** (e.g. `/#section`): Skip for Level 2 crawling — they don't load new content.
- **The For Agents section is mandatory** — even if empty of details, it signals intent to support agents and provides a contact path.
- **Never ask all questions at once** — it's a conversation, not a form.
