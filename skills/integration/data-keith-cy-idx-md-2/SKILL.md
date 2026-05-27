---
name: idx-md
description: AgentSkill for https://idx.md. Use the index to locate AI agent library topics and fetch HEAD/BODY markdown.
---

# idx.md

## Purpose
- Markdown registry for AI agent libraries and resources.
- Agents can browse to learn everything they could use, then fetch the exact markdown.

## Index locations
- All topics (full listing, alphabetical): https://idx.md/data/index.md (canonical) or https://idx.md/index.md (alias)
- Capability navigation (browse by what the agent can do): https://idx.md/category/index.md
- Scenario navigation (browse by workflow / use-case): https://idx.md/scenario/index.md
- Industry navigation (browse by domain / vertical): https://idx.md/industry/index.md

## How to choose a navigation mode
- If you know what you want: start from `/data/index.md` and search by keywords in titles/tags.
- If you want tools by capability: start from `/category/index.md`.
- If you have a specific workflow/use-case: start from `/scenario/index.md`.
- If you're operating in a specific domain: start from `/industry/index.md`.

## Index entry format
- Each entry is a HEAD frontmatter block followed by a topic line.
- Topic line format: `|/data/{topic}|`
- The index may start with a short HTML comment preamble; entries begin at the first `---` frontmatter block.

---
...frontmatter...
---
|/data/openclaw|

## How to fetch
- Read `https://idx.md/data/index.md` (or `https://idx.md/index.md`).
- Choose `{topic}` from the `|/data/{topic}|` line.
- HEAD metadata: `https://idx.md/{topic}` (or `/data/{topic}/HEAD.md`)
- Vector shard (for embedding recall): `https://idx.md/{topic}/vectors.json`
- BODY content: `https://idx.md/{topic}/BODY.md`
- After download, compute SHA-256 on the raw BODY bytes and compare to `content_sha256` in HEAD frontmatter.
- Use `retrieved_at` to decide whether a cached BODY needs refresh.

## Vector-based retrieval (recommended)
- Use `/{topic}/vectors.json` as the retrieval layer, then fetch `/{topic}/BODY.md` only for top candidates.
- Each `vectors.json` currently contains one `head` record derived from HEAD metadata.
- Build/query embeddings on `records[].text`.
- Use `records[].metadata.content_sha256` as your embedding cache key; only re-embed when it changes.
- Suggested flow:
1. Collect topic candidates from `/data/index.md` or category/scenario/industry indexes.
2. Fetch each candidate's `/{topic}/vectors.json`.
3. Rank by vector similarity (optionally hybrid with lexical/tag score).
4. Fetch `/{topic}/BODY.md` for top-k and generate final answer from BODY.

## URL map
- `/`, `/skill.md`, `/SKILL.md` -> this document
- `/index.md`, `/data/index.md` -> index listing
- `/category/index.md` -> category index listing
- `/category/{category}/index.md` -> category topic listing
- `/scenario/index.md` -> scenario index listing
- `/scenario/{scenario}/index.md` -> scenario topic listing
- `/industry/index.md` -> industry index listing
- `/industry/{industry}/index.md` -> industry topic listing
- `/{topic}` -> `/data/{topic}/HEAD.md`
- `/{topic}/HEAD.md` -> HEAD metadata
- `/{topic}/vectors.json` -> vector shard for embedding recall
- `/{topic}/BODY.md` -> BODY content

## Constraints
- `.md` only; `.mdx` rejected by filename.

## Integrity / Hash
- `content_sha256` lives in the HEAD frontmatter.
- `content_sha256` is the SHA-256 of the exact BODY bytes (no normalization).
- Format: lowercase hex string.
- Verify by hashing the downloaded BODY.md bytes and comparing to `content_sha256`.
- If the hash differs, re-download BODY.md.

## Example flow
- Read `/index.md` -> pick `openclaw` -> fetch `/openclaw/HEAD.md` -> fetch `/openclaw/BODY.md`.

## Contribute
If you find a high-quality markdown resource that agents should know about, please open a PR to add it.
Repo: https://github.com/Keith-CY/idx.md

### What to add
- Add new sources to `sources/general.yml`.
- Use a direct markdown URL (`.md`) and prefer `raw.githubusercontent.com` for GitHub content.
- `.mdx` files are rejected.
- Choose a `type` and `slug` that match `^[a-z0-9][a-z0-9-]*$`.
- Avoid editing auto-generated registries (`sources/openclaw.yml`, `sources/openai.yml`, etc.) or `data/` outputs directly.

### Minimal entry example
```yaml
- type: skills
  slug: acme-awesome-skill
  source_url: https://raw.githubusercontent.com/acme/awesome-skill/main/SKILL.md
  title: Awesome Skill (optional)
  summary: One-line summary (optional)
  tags:
    - skills
  license: MIT (optional)
  upstream_ref: https://github.com/acme/awesome-skill/blob/main/SKILL.md (optional)
```

### How to submit
1. Fork the repo: https://github.com/Keith-CY/idx.md
2. Add your entry to `sources/general.yml`.
3. Open a PR with a short note on why the source is valuable for agents.
4. If you can run the build, include generated `data/` updates; otherwise the maintainer will handle it.

Thanks for helping keep idx.md useful and current.
