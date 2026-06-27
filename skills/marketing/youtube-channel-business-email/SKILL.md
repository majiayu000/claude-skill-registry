---
name: youtube-channel-business-email
description: "YouTube channel business email and contact extractor: accepts a channel id (UCxxx), handle (@name), or URL; navigates the channel About view; extracts the business email from the description text plus full channel metadata (name, id, country, subscriber count, view count, video count, joined date, external links classified as social/aggregator/personal). When the description has no email, follows non-social outbound links (personal site, business site, link aggregator) and scans those pages for an email so creators who place their inquiry email on their own site are still covered. Use when user mentions youtube channel email, youtube business email, youtube creator email, youtube contact email, youtube channel contact, youtube channel scraper email, youtube email finder, youtube influencer email, youtube outreach, youtube sponsorship contact, youtube partnership email, scrape email from youtube, get email from youtube channel, find youtube creator contact, extract youtube channel emails in bulk, youtube channel inquiry email, business inquiries youtube, brand deal email youtube, lead generation youtube creators, youtube creator outreach list, youtube channel about email, ytInitialData about, youtube channel id to email, youtube handle to email, youtube channel url to email, youtube about page scraper, channel about page email, youtube channel metadata, youtube channel social links, youtube channel external links, youtube channel description email, follow channel website for email, scrape creator personal website from youtube. Also applies to building creator/KOL contact databases for influencer marketing, agency lead lists, sponsorship prospecting, brand-creator collaboration sourcing, and enriching existing YouTube channel lists with contact info."
---

# YouTube — Channel Business Email & Contact Extractor

> Input: a YouTube channel id (`UCxxx`), handle (`@name`), or channel URL. Output: structured channel metadata (id, name, counters, country, joined date, external links classified by kind) plus the channel's business email if it can be found on the About page description or on any linked personal/business website.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract a YouTube channel's business inquiry email together with the channel's About metadata and outbound link list, prioritising what is already publicly displayed on the channel's About page; if no email is visible there, walk the channel's own outbound links (personal site, business site, link aggregator) to recover an email that the creator publishes on a site they control.

## Prerequisites

- Target page is already open in the browser: `https://www.youtube.com/{@handle|channel/UCxxx}/about`
- No login is required for description and link extraction; running the browser while signed in to YouTube does not change what is returned by this Skill.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory; each `.py` script prints a self-contained JS snippet to stdout. To execute that snippet in the browser, hand it to browser-act's `eval` subcommand via bash command substitution: `browser-act --session <session-name> eval "$(python scripts/xxx.py {params})"`. The outer `$(...)` is bash syntax; use the bash tool to run it. Pure-Python scripts that already emit a JSON result on stdout (e.g. `normalize-channel-input.py`, `extract-emails-from-text.py`) are invoked directly: `python scripts/xxx.py {params}` — do NOT wrap them in `browser-act eval`.

### API: normalize a channel input into a canonical /about URL

`python scripts/normalize-channel-input.py '{channel-input}'`

Parameters:
- `{channel-input}`: a channel id (`UCxxxxxxxxxxxxxxxxxxxxxx`, 24 chars starting with `UC`), a handle (`@name`), a bare handle (`name`), or any channel URL (`https://www.youtube.com/@name`, `https://www.youtube.com/channel/UCxxx`, `https://www.youtube.com/c/legacy`, `https://www.youtube.com/user/legacy`). Trailing path segments and querystrings are stripped.

Output example:
```json
{
  "about_url": "https://www.youtube.com/@example/about",   // canonical URL to navigate to before extraction
  "input_type": "handle",                                  // one of: handle | channel_id | channel_url | legacy_custom_url | bare_handle | raw_url
  "value": "@example"                                      // normalised value (handle with @ prefix, or channel id, or raw url)
}
```

On unrecognised input the script returns `{"error": true, "message": "unrecognized input: ..."}`.

### DOM: extract channel About metadata + emails from description

Run from the channel's `/about` view (after `navigate` + `wait stable`). Reads `window.ytInitialData.aboutChannelViewModel` and pulls the description, full counter set, channel id, canonical URL, the resolved outbound links (with the YouTube redirect wrapper unwrapped), and any email addresses already present in the description text.

Extract: `browser-act --session <session-name> eval "$(python scripts/extract-channel-about.py)"`

Output example:
```json
{
  "channel_id": "UCxxxxxxxxxxxxxxxxxxxxxx",                // YouTube channel id (UCxxx)
  "channel_name": "Channel Display Name",                  // display name from channel metadata
  "canonical_channel_url": "http://www.youtube.com/@example", // canonical channel URL reported by YouTube
  "description": "Short bio line ...\n\nbusiness@example.com\n\nCity", // full About description text
  "country": "United States",                              // country shown on the About panel (localised text)
  "subscriber_count_text": "21M subscribers",              // raw display text (locale-formatted)
  "view_count_text": "5,455,901,172 views",                // raw display text (locale-formatted)
  "video_count_text": "1,831 videos",                      // raw display text (locale-formatted)
  "joined_date_text": "Joined Mar 21, 2008",               // raw display text (locale-formatted)
  "has_business_email_reveal_button": true,                // whether the "View email address" button is exposed on the page
  "bypass_business_email_captcha": false,                  // whether the current viewer can skip the email reveal captcha
  "emails_in_description": ["business@example.com"],       // emails matched in the description text; empty array when none
  "links": [                                               // outbound links with YouTube /redirect wrappers unwrapped
    {"title": "Twitter", "display": "twitter.com/example", "url": "http://twitter.com/example"}
  ]
}
```

On failure (page is not a channel `/about` view, `ytInitialData` missing, or `aboutChannelViewModel` not present), the script returns `{"error": true, "message": "..."}`.

### API: extract emails from arbitrary text + classify a URL by kind

`python scripts/extract-emails-from-text.py [--text '{text}' | --text-file {path}] [--classify-url '{url}']`

Parameters:
- `--text`: raw text to scan for email addresses (plain, markdown, or HTML)
- `--text-file`: path to a UTF-8 text file to scan for email addresses
- `--classify-url`: URL to classify into `social`, `link_aggregator`, or `personal_or_business` (used to decide which outbound links are worth fetching during email recovery)

Output example (with `--text` and `--classify-url`):
```json
{
  "classification": {
    "kind": "personal_or_business",          // social | link_aggregator | personal_or_business | invalid
    "domain": "example.com",
    "url": "https://example.com/"
  },
  "emails": ["info@example.com"]             // deduplicated, image/file extensions filtered out, obfuscated forms like name [at] brand [dot] io are recovered
}
```

Without any argument the script returns `{"error": true, "message": "provide --text, --text-file, or --classify-url"}`.

### Composite: end-to-end channel-to-business-email lookup

Cross-page composite: input normalisation → navigation → About extraction → optional follow of one or more non-social outbound links to recover an email when the description had none.

Before the loop, ensure a scratch directory exists for the markdown dumps used in step 6: `mkdir -p tmp` (run once per batch, not per channel).

1. Normalise the input:
   `python scripts/normalize-channel-input.py '{channel-input}'` — read `about_url` from stdout.
2. Navigate the browser session to that URL and wait for it to render:
   `browser-act --session <session-name> navigate {about_url}` → `browser-act --session <session-name> wait stable --timeout 12000` (a `Timed out waiting for page readiness` here is recoverable — proceed if the URL and title reflect the channel; check Known Limitations).
3. Pull the channel About payload:
   `browser-act --session <session-name> eval "$(python scripts/extract-channel-about.py)"`
4. If `emails_in_description` is non-empty, set `business_email = emails_in_description[0]` and `email_source = "description"`. Stop and emit the result.
5. Otherwise classify each link to decide which outbound URLs to walk; skip `social` links (Twitter/Instagram/TikTok/Facebook/etc. — they require login and are unreliable to scrape):
   For each `link.url` in `links`:
   `python scripts/extract-emails-from-text.py --classify-url '{link.url}'`
6. For every link classified as `personal_or_business` or `link_aggregator`, fetch its rendered text and look for an email; stop at the first match:
   - `browser-act stealth-extract '{link.url}' --content-type markdown > tmp/site.md`
   - `python scripts/extract-emails-from-text.py --text-file tmp/site.md`
   - If the result has non-empty `emails`, set `business_email = emails[0]`, `email_source = "linked_website:{classification.domain}"` and stop.
   - Order of attempts: `personal_or_business` first (most likely to host the creator's own contact page), then `link_aggregator` (linktr.ee / beacons.ai style pages that may surface a contact email).
7. If no email is recovered, emit `business_email = null`, `email_source = null`, `status = "no_email_found"`.

Final emitted record (one per channel input):
```json
{
  "input": "@example",                                       // original input as provided
  "channel_id": "UCxxxxxxxxxxxxxxxxxxxxxx",                  // resolved YouTube channel id (UCxxx)
  "channel_name": "Channel Display Name",                    // display name from channel metadata
  "channel_url": "https://www.youtube.com/@example",         // canonical channel URL
  "business_email": "business@example.com",                  // recovered email, or null when none was found
  "email_source": "description",                             // description | linked_website:{domain} | link_aggregator:{domain} | null
  "country": "United States",                                // localised country text
  "subscriber_count_text": "1.2M subscribers",               // raw display text
  "view_count_text": "123,456,789 views",                    // raw display text
  "video_count_text": "987 videos",                          // raw display text
  "joined_date_text": "Joined Jan 1, 2015",                  // raw display text
  "has_business_email_reveal_button": true,                  // whether the "View email address" gate is offered on the channel
  "links": [                                                 // outbound links with classification appended
    {"title": "Instagram", "display": "instagram.com/example", "url": "http://instagram.com/example", "kind": "social", "domain": "instagram.com"}
  ],
  "status": "ok"                                             // ok | no_email_found | error
}
```

On any unrecoverable error (input normalisation failed, navigation failed, extraction returned `error: true`), emit `status = "error"` together with the failing step name in `error_step` and the error message in `error_message`.

## Known Limitations

- The "View email address" button on `/about` is gated by reCAPTCHA and a YouTube server-side validation that rejects programmatically-solved captcha tokens (the call to `youtubei/v1/channel/reveal_business_email` returns HTTP 400 `INVALID_ARGUMENT` even when a captcha solver returns success). Emails that only exist behind that reveal button cannot be recovered by this Skill — only emails published in the description text or on a creator-controlled outbound site are returned.
- `wait stable` on YouTube `/about` pages frequently exceeds the default 30s due to long-lived media streams; the extraction is still valid as long as `ytInitialData.aboutChannelViewModel` is present (verified after the timeout). Treat a single `Timed out waiting for page readiness` as recoverable and run the extraction script anyway.
- `country`, `subscriber_count_text`, `view_count_text`, `video_count_text`, `joined_date_text` are returned verbatim in the locale that the underlying browser renders (e.g. an en locale yields `21M subscribers` while a zh-CN locale yields its own localised string with native digit grouping and the localised word for "subscribers"). Downstream consumers must do the parsing.
- Description-based email matching only finds emails that the creator typed into the About description. Many large creators (e.g. channels with `has_business_email_reveal_button = true` and an empty `emails_in_description`) keep their email behind the captcha-gated button and will therefore not be recovered.
- Outbound link walking is limited to one HTTP fetch per non-social link via `stealth-extract` (no JS interaction, no crawling deeper than the landing page). Sites that hide their email behind a contact form or a JS-rendered modal that does not appear in the initial markdown will yield no email.
- Image asset URLs whose path contains `@` (e.g. `image@2x.png`) and YouTube video URLs containing `@handle` are deliberately filtered out of the email match results; the trade-off is that very unusual emails ending in `.png`/`.jpg`/`.gif`/`.webp`/`.svg`/`.ico` would also be rejected (not encountered in practice).

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through channel inputs serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session.
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 channels to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly.
- **Reduce redundant pre-operations**: Keep one browser session open across the whole batch (one `browser open` then many `navigate`s); avoid reopening the browser between channels.
- **Error resumption**: Save results item by item during batch processing (append one JSON line per channel to an output file); on failure, resume from the breakpoint rather than starting over.
- **Skip social link walking when not needed**: The first match wins; once `emails_in_description` is non-empty, do not fetch any outbound link.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/youtube-channel-business-email-youtube-channel-business-email.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
