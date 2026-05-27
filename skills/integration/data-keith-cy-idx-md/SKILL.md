---
name: idx-md
description: AgentSkill for https://idx.md. Use the index to locate AI agent library topics and fetch HEAD/BODY markdown.
---

# idx.md

## Purpose
- Markdown registry for AI agent libraries and resources.
- Agents can browse to learn everything they could use, then fetch the exact markdown.

## Index locations
- https://idx.md/index.md
- https://idx.md/data/index.md

## Index entry format
- Each entry is a HEAD frontmatter block followed by a topic line.
- Topic line format: `|/data/{topic}|`

---
...frontmatter...
---
|/data/openclaw|

## How to fetch
- Read `https://idx.md/index.md`.
- Choose `{topic}` from the `|/data/{topic}|` line.
- HEAD metadata: `https://idx.md/{topic}` (or `/data/{topic}/HEAD.md`)
- BODY content: `https://idx.md/{topic}/BODY.md`
- After download, compute SHA-256 on the raw BODY bytes and compare to `content_sha256` in HEAD frontmatter.
- Use `retrieved_at` to decide whether a cached BODY needs refresh.

## URL map
- `/`, `/skill.md`, `/SKILL.md` -> this document
- `/index.md`, `/data/index.md` -> index listing
- `/{topic}` -> `/data/{topic}/HEAD.md`
- `/{topic}/HEAD.md` -> HEAD metadata
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
