---
name: prime-the-agent
description: "Fast 30-second session-starter. Loads the active site, identifies the page builder, loads inline schemas, and primes the agent on the do-not-write-raw-HTML rule before any work begins. Prevents the single most common failure mode in AI WordPress editing."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: workflow
---

# Prime the Agent

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** workflow
**Status:** stable
**Requires:** Respira for WordPress plugin + MCP server
**Telemetry endpoint:** https://www.respira.press/api/skills/track-usage

---

## Description

A fast, focused session-starter. Run this at the top of any conversation about a WordPress site to prime the agent on how to work with the site correctly. Prevents the single most common failure mode: the agent generating raw HTML instead of using the site's actual page builder.

This skill is not a full site audit. For that, use [Site Onboarding](https://respira.press/skills/site-onboarding) or [WordPress Site DNA](https://respira.press/skills/wordpress-site-dna). This is the 30-second preamble before any work.

---

## When to Use

Use Prime the Agent when:

- Starting a new conversation about an existing WordPress site
- The agent has just connected to a site via MCP and is about to start editing
- A previous session got confused and started writing raw HTML
- You're handing the conversation to a teammate or a different AI client and want the new context loaded clearly
- The site is one the agent has never worked on before

Skip this skill when:

- The agent is already mid-task on a site it has been working on for many turns
- The work is read-only and won't touch builder content
- You're asking a general WordPress question not tied to a specific site

---

## Trigger Phrases

This skill activates when the user says any of:

- "prime yourself"
- "prime the agent"
- "get ready to work on this site"
- "understand my site setup"
- "before we start"
- "prepare to work on wordpress"
- "warm up on this site"
- "load context for this site"
- "what builder does this site use"
- "give me a site briefing"

---

## Execution Workflow

Run these six steps **in order**, before any other action. Do not skip steps.

### Step 1 — Identify the active site

Call `respira_get_active_site`. If no active site is set or the call fails, stop and ask the user which connected site to work on. Then call `respira_list_sites` to show options.

### Step 2 — Load the site's context

Call `respira_get_site_context`. Capture: WordPress version, PHP version, active theme, plugin count, multisite y/n, site URL.

### Step 3 — Identify the active builder

Call `respira_get_builder_info`. This returns the active page builder (Elementor, Bricks, Divi, Gutenberg, Oxygen, Breakdance, Beaver, Brizy, WPBakery, Visual Composer, Thrive Architect, Flatsome, Spectra, Kadence Blocks, GenerateBlocks, or SeedProd), its version, and which modules are available.

**This is the most important call.** Every write to a page must go through this builder's native data structure. The agent's job is not to write WordPress pages — it's to write *this builder's* pages.

### Step 4 — Load the builder's inline schemas

Call `respira_get_builder_inline_schemas`. This returns the JSON schema for every module type the active builder supports. Keep these in working memory before any write.

### Step 5 — Quick content surface scan

Call `respira_list_pages` (limit 25) and `respira_list_custom_posts` (limit 10). The agent now knows what pages exist, what custom post types are defined, and roughly how big the site is.

### Step 6 — Acknowledge to the user

Output a short briefing in this exact shape:

```markdown
## Primed and ready

**Active site:** {site_url}
**WordPress:** {wp_version} · PHP {php_version} · Theme {theme_name}
**Active builder:** {builder_name} {builder_version}
**Content surface:** {page_count} pages · {custom_post_count} custom posts · {plugin_count} plugins
**Multisite:** {yes/no}

**Working rules I'll follow on this site:**
- Every page edit goes through {builder_name}'s native modules. No raw HTML.
- Before changing a live page, I'll call `respira_create_page_duplicate` first (SafeEdit).
- I'll use `respira_extract_builder_content` to read pages and `respira_inject_builder_content` to write them whole.
- For element-level changes I'll use `respira_find_element` → `respira_update_element`.
- For new pages from a brief I'll use `respira_build_page`, not `respira_update_page` with HTML.

Ready when you are.
```

---

## The hard rules (do not break)

These are the rules the agent must follow on every WordPress site that uses a page builder. Internalize these before any write operation.

### 1. The site is not a generic HTML page. It is a {builder} page.

If the active builder is Elementor, the page is a tree of Elementor widgets. If Bricks, it is a tree of Bricks elements. If Divi 5, it is a tree of Divi modules with the v5 catalog. If Gutenberg, it is a tree of blocks. Writing `<div>` or `<section>` HTML into the page bypasses the builder's data structure and **corrupts the page** — the builder won't recognize the content and the editor will show a blank canvas or an unparseable warning.

### 2. Use builder-native tools only

For the active builder, use this tool stack (in order of preference for each operation):

**To read a page:**
- `respira_extract_builder_content` (returns the builder's native structure)
- `respira_read_page` (returns metadata + content)
- `respira_get_page_outline` (returns headings + structure)

**To find something to edit:**
- `respira_find_element` (with text, class, widget type, or ID query)
- `respira_find_builder_targets` (returns builder-specific selectors)

**To change something:**
- `respira_update_element` (single element, the most common operation)
- `respira_update_module` (for module-level changes — Divi, Bricks)
- `respira_apply_builder_patch` (for builder-JSON patches)

**To write a whole page:**
- `respira_build_page` (for new pages from a brief — uses builder schemas)
- `respira_inject_builder_content` (for whole-page content drops in builder-native format)

**Never use:**
- `respira_update_page` with raw HTML for content changes. This replaces the entire page body and bypasses the builder — the result is a "code page" with no editable widgets. `respira_update_page` is only for page title, slug, status, or custom CSS.

### 3. Always duplicate-before-edit on live pages

Before changing any page that is published and indexed, call `respira_create_page_duplicate`. Edit the duplicate. Show the user the duplicate URL. Let them review before promoting the duplicate to the live page. This is SafeEdit, and it has saved more than one customer site from a regret.

### 4. Load inline schemas before any write

`respira_get_builder_inline_schemas` returns the exact attribute shape for every module the active builder supports. Read it before writing. If a module's schema says `padding` is a dimension object with `unit` and `value` keys, write a dimension object. If it says `font_size` is an integer, write an integer. Do not improvise.

### 5. Snapshot is automatic, but check it exists

Every write through Respira creates a TimeSnap automatically. If the user wants to roll back, call `respira_list_snapshots` then `respira_restore_snapshot`. You do not need to manually create snapshots — but if a customer is doing something risky (multi-page bulk update), you can take an explicit one with the snapshot helper.

---

## Examples

### Example 1 — New session, fresh site

User: *"prime yourself for this site"*

Agent: (runs Steps 1–6 in order, outputs the briefing)

Then: *"What would you like to work on?"*

### Example 2 — Mid-session correction

User: *"wait, you're writing HTML. I told you we use Bricks."*

Agent: (re-runs Step 3 — `respira_get_builder_info` — confirms Bricks)

Then: *"You're right. I'm re-priming. Active builder: Bricks 1.12. From here on every write goes through Bricks element schemas, not HTML. Continuing with [task]."*

### Example 3 — Builder is Gutenberg

User: *"prime the agent for my blog"*

Agent: (runs Steps 1–6)

Notes: For Gutenberg-only sites, "builder-native" means writing block markup (the `<!-- wp:paragraph -->` comments + serialized block JSON), not raw HTML. The same do-not-write-raw-HTML rule applies — block content is the native structure, not freeform HTML.

---

## Telemetry

This skill records a usage event when it runs. The event captures: active site URL hash, active builder, content-surface counts (pages, custom posts, plugins), success/failure, and total duration. No site content, no user prompts, no tool arguments are sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`

Telemetry can be disabled at the plugin level under **Respira → Settings → Privacy → Anonymous telemetry**.

---

## Why this skill exists

The single most common failure mode the Respira team sees in customer support is: an AI agent picks up a conversation about a WordPress site, doesn't check which builder is active, and starts writing raw HTML. The page goes into the database as a blob of HTML that the builder cannot parse. The editor opens to a broken canvas. The customer files a bug report.

This skill prevents that by making "before any work, find out what you're working on" a first-class, named, triggerable workflow. Run it. Then everything else works.
