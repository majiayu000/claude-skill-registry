---
name: kai-gtm-pack
description: Ship a complete go-to-market deliverable pack for a client as a cross-linked set of private HTML pages topped by a client hub (the ask, tool install, access grants, ordered signup checklist). Use when "GTM plan for [client]", "put together a GTM", "go to market plan", "build the client hub", "attach everything for the client", "package this for the client", or when an engagement's plan/audit/emails must be delivered as linked pages rather than loose files.
---

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

Turn GTM work into something a client can actually act on: a set of linked web pages, not a folder of markdown. The hub is the deliverable; everything else hangs off it.

## When to use

- "GTM plan for [client]" / "go to market" / "put together a GTM" for a real client business
- "Build the client hub" / "attach everything" / "package this for the client"
- An engagement where the client must *do* things afterward (sign up for platforms, grant access, install tooling) and you want one link that walks them through it
- Any deliverable that will be forwarded to a non-technical operator — pages, not files

## When NOT to use

- Planning itself — that's `/kai-growth-plan` (this skill *packages* the plan; it doesn't write it)
- A single strategy page or customer-facing brochure with no hub and no follow-up actions — build just the page
- Your own product's marketing — this is for client engagements with a handoff
- Loose internal analysis nobody outside the team will read

## Workflow

Order matters. The hub comes last because it links everything else.

1. **Verify the numbers before reusing them.** Read the client's existing context and prior strategy work. Any keyword volume/difficulty, CPC, or market figure the plan will lean on gets re-pulled fresh (e.g. DataForSEO bulk keyword difficulty + search volume — one call, pennies). Older figures are wrong surprisingly often; put the corrections *on the page* with the fresh pull date. Never ship a plan citing numbers you didn't check this week.
2. **Write the plan with `/kai-growth-plan`.** Stage diagnosis → prioritized do/don't → growth loops → metrics → 90-day roadmap → budget → skill routing. Save the markdown to the client's outputs folder first — it is the source of truth the pages render from.
3. **Produce the attachments the plan implies.** Typically `/kai-audit` (full audit of the current site) and `/kai-email-system` (lifecycle emails the plan's review/referral engine needs). Keep each as markdown in the client's outputs folder.
4. **Render each deliverable as a single-file HTML page.** One self-contained file per deliverable: inline `<style>`, zero JavaScript, `noindex,nofollow,noarchive` robots meta, print CSS. If the client already has pages from you, copy the existing page's style block verbatim so the set reads as one artifact. Check for horizontal overflow at mobile and desktop widths (render and probe `scrollWidth > clientWidth` — tables and code blocks are the usual offenders).
5. **Deploy the set.** Push every page to your private hosting convention (unguessable per-client slug, noindex, robots disallow) and verify each URL returns 200 and carries the robots meta. A local HTML file is not a deliverable — these exist to be sent as links.
6. **Build the hub.** The page the client keeps. In order:
   - **The arrangement** — what they get vs. what you're asking in return, stated in one card each (a signup, a trade, an invoice — whatever the deal is).
   - **The ask, with the working link** — the single most important action, as the page's primary CTA, with the exact steps it takes (and the phone-first path if one exists — non-technical clients often prefer calling).
   - **Tool install** — how they install your tooling into *their* setup (name the actual client: e.g. the two `/plugin` commands for Claude Code, not a generic README link).
   - **Access grants you need** — each as a numbered click-path: which screen, which email/account to add, which role, and the one line on why. State that they keep ownership and can revoke.
   - **The signup checklist** — every platform the plan requires (business profiles, review surfaces, booking/payments, insurance/permits, directories, analytics), grouped in the *plan's* order ("Week 1", "Week 2"…), each with the verified signup URL, cost, and one line of requirements. Verify every URL the day you build; flag any that won't load as unverified rather than dropping it silently. Include the deliberate skips (platforms the plan says to refuse) with the reason — clients find them on their own and wonder.
7. **Cross-link the set.** The hub links every page. Every internal page's footer links back to the hub and its siblings. Guest-facing pages (brochure, public-facing artifacts) link only to each other — never to internal pages with budgets, margins, or the arrangement.
8. **Update the client's context file.** Deliverables table with dates, live-link table with a safe-to-forward flag per page, the arrangement terms, and the access grants requested. The next session (or the next agent) starts from that file.

## Examples

A private dive-operator engagement (the origin of this skill):

- Re-verified 15 keywords before planning: confirmed the difficulty-0 cluster, but caught a head term at difficulty 31 (claimed 0) and a certification keyword at 50/mo (claimed ~1,000) — corrections printed on the GTM page with the re-pull date.
- Shipped six pages as one set: guest brochure + reef log (guest-facing, link only each other), and GTM plan / audit / emails / hub (internal, cross-linked footers).
- The hub carried the arrangement (the work in exchange for a product signup + services trade), the signup CTA with both the web and phone paths, two `/plugin` install commands for the client's Claude Code, two access grants as click-paths (analytics service account as Viewer; site-admin invite), and a 20-item signup checklist grouped by week with costs and two flagged-unverified URLs.

## Failure mode

- **Keyword/data API fails or has no credentials:** ship the plan but mark every unverified figure explicitly ("unverified — re-pull before acting"). Never present a stale number as fresh.
- **No private hosting exists for the client yet:** any static host works (a private Netlify/Vercel deploy, an S3 bucket with a long path). The convention that matters: unguessable URL + noindex + a single link the client keeps.
- **The set already has a visual style and yours doesn't match:** stop and copy the existing page's style block. A mismatched page breaks the "one artifact" read worse than a plain one.
- **The client can't act on a checklist item (no login, government portal in another language, demo-gated pricing):** say so inline at that row — never let the checklist read smoother than reality.
