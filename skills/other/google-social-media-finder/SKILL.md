---
name: google-social-media-finder
description: "Searches Google to discover social media profiles associated with a person, brand, or username; returns platform name, profile URL, username, bio snippet, and follower count across X, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Snapchat, Threads, and more. Use when user wants to find someone's social media accounts, look up social profiles, discover where a person is active online, find brand social media pages, search social accounts by name, track digital footprint, find influencer profiles, check a company's social presence, locate a public figure's profiles, social media lookup, social media finder, find accounts across platforms, social profile search, online presence discovery, who is this person on social media, what social media does X use, find username across platforms."
---

# Google — Social Media Finder

> Name or brand → all social media profiles found on Google (platform, URL, username, bio, followers)

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Given a person's name, brand name, or username, search Google and return all matching social media profile results from known platforms.

## Prerequisites

- No login required — Google search is publicly accessible

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### DOM: social media profile results (data extraction type)

Navigate to the Google search page for the target name, then extract all social media profile results.

**Step 1 — Navigate:**

```
navigate https://www.google.com/search?q={name}+social+media
```

Replace `{name}` with the person's or brand's name, using `+` in place of spaces (e.g., `Taylor+Swift`, `Elon+Musk`, `Nike`).

**Step 2 — Wait for page:**

```
wait stable
```

**Step 3 — Extract:**

```bash
eval "$(python scripts/extract-social-profiles.py)"
```

Output example:
```json
{
  "error": false,
  "count": 5,
  "results": [
    {
      "platform": "Instagram",      // social media platform name
      "username": "taylorswift",    // handle or page name shown alongside platform
      "url": "https://www.instagram.com/taylorswift/",  // direct profile URL
      "title": "Taylor Swift (@taylorswift) • Instagram photos and videos",  // page title
      "snippet": "274M followers · 0 following · 706 posts ...",  // bio/description snippet from search result
      "followers": "超过 2.7亿位关注者"  // follower count as displayed (language depends on browser locale)
    }
  ]
}
```

On error: `{"error": true, "message": "..."}` — check that the browser navigated to a Google search page and `.tF2Cxc` result containers are present.

## Pagination

**URL Pagination**: URL pattern `https://www.google.com/search?q={name}+social+media&start={offset}`, where `offset = (page - 1) * 10` (page 1 → `start=0` or omit, page 2 → `start=10`, page 3 → `start=20`). Next page link: `a#pnnext`. Termination: `a#pnnext` is absent (last page reached) or no social media results returned.

## Success Criteria

`result count >= 1` and `platform` and `url` fields are non-null for every item

## Known Limitations

- Results depend on Google's index — newly created or low-traffic profiles may not appear
- Follower count text is localized to the browser's display language (e.g., Chinese characters for a Chinese-locale stealth browser)
- Google may show sub-pages of the same profile as separate results (e.g., both `/elonmusk` and `/elonmusk/with_replies` from X); deduplicate by base URL if needed
- Google SERP layout changes occasionally; if `.tF2Cxc` stops matching, inspect page HTML for updated container class names

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/social-media-finder-google-social-media-finder.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
