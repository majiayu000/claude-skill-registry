---
name: kai-gtm-pack
description: Ship a complete go-to-market deliverable pack for a client as a cross-linked set of private HTML pages topped by a client hub (the ask, tool install, access grants, ordered signup checklist). Use when "GTM plan for [client]", "put together a GTM", "go to market plan", "build the client hub", "attach everything for the client", "package this for the client", or when an engagement's plan/audit/emails must be delivered as linked pages rather than loose files.
---

# Kai GTM Pack (v2)

## Objective

Turn GTM work for a client into a set of linked, privately-hosted web pages the client can act on — topped by a hub page that carries the arrangement, the ask, the tool install, the access grants, and the ordered signup checklist. Pages, not files: a local HTML file that was never deployed is not a deliverable.

## Done when

- Every keyword/volume/difficulty figure the plan leans on was re-pulled fresh this week (e.g. DataForSEO difficulty + volume), and any corrections to older figures are printed on the page with the pull date.
- The plan exists (via `/kai-growth-plan`: stage, do/don't, loops, metrics, 90 days, budget, skill routing) plus the attachments it implies (typically `/kai-audit`, `/kai-email-system`).
- Each deliverable renders as a self-contained single-file HTML page (inline style, zero JavaScript, `noindex,nofollow,noarchive`, print CSS), overflow-checked at mobile and desktop widths, deployed to the client's private URL convention, and every URL verified live (200 + robots meta).
- The hub page exists and carries, in order: the arrangement (what they get vs. what you're asking), the ask as the primary CTA with exact steps (and a phone-first path where one exists), tool install written for the client's actual setup, each access grant as a numbered click-path (screen, account, role, why, revocability), and the signup checklist grouped in the plan's order with verified URL + cost + one-line requirements per row — including the deliberate skips with their reasons.
- The set is cross-linked: hub links everything, internal footers link back, guest-facing pages link only to each other.
- The client's context file records the deliverables, the live links with safe-to-forward flags, the arrangement terms, and the access grants requested.

## Constraints

- The hub comes last — it links everything else, so it cannot be built first.
- If the client already has pages from you, copy the existing page's style block verbatim. A mismatched page breaks the set worse than a plain one.
- Guest-facing pages (brochure, public artifacts) never link to internal pages carrying budgets, margins, or the arrangement.
- Verify every signup URL the day you build the hub. If one won't load, flag it inline as unverified — never drop it silently and never let the checklist read smoother than reality (demo-gated pricing, foreign-language government portals, rep-led signups all get said).
- If data APIs fail or credentials are missing, ship with unverified figures marked explicitly — never present a stale number as fresh.
- The client keeps ownership of everything; access grants are stated as revocable.

## Context

- Planning is `/kai-growth-plan`'s job; this skill packages. Audit and email content come from `/kai-audit` and `/kai-email-system`.
- Origin engagement: a private dive operator. Re-verification caught a head term at difficulty 31 (claimed 0) and a keyword at 50/mo (claimed ~1,000). Six pages shipped as one set; the hub carried the trade (work in exchange for a product signup + services), a two-command plugin install for the client's Claude Code, two access-grant click-paths, and a 20-item week-grouped signup checklist with two flagged-unverified URLs.

## Escalate when

- The client has no private hosting convention yet — pick one (any static host with unguessable URLs + noindex) and confirm with the operator before deploying.
- The arrangement or the ask isn't settled — the hub states the deal plainly, so it cannot be written while the deal is ambiguous. Get the terms from the operator first.
- A checklist item requires access you don't have (client logins, government portals) — leave it as an explicit client action on the hub rather than guessing around it.
