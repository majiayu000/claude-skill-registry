---
name: paper-finder
description: Discover recent arXiv papers matching a research profile and generate Obsidian-compatible Markdown notes. Use this skill when the user wants to find new papers, refresh their literature inbox, or search arXiv based on their interests.
---
# Paper Finder

Use this skill when you want to discover recent arXiv papers for a specific research profile and write the results as Obsidian-compatible Markdown notes.

## Run Retrieval

Run the CLI from the repository root:

```bash
python skills/paper-finder/find_papers.py \
  --profile path/to/research-interest.json \
  --output path/to/obsidian/inbox
```

Optional semantic ranking:

```bash
python skills/paper-finder/find_papers.py \
  --profile path/to/research-interest.json \
  --output path/to/obsidian/inbox \
  --semantic
```

Semantic settings can come from either source:

- `config/api_keys.json` with `semantic_model.api_base_url`, `semantic_model.api_key`, `semantic_model.model`
- Environment variables:
  - `STABLE_JARVIS_SEMANTIC_API_BASE_URL`
  - `STABLE_JARVIS_SEMANTIC_API_KEY`
  - `STABLE_JARVIS_SEMANTIC_MODEL`

You can still pass `--semantic-config path/to/semantic-config.json` for advanced overrides. The JSON file should match `stable_jarvis.paper_finder.semantic.SemanticConfig`.

## Build or Refresh a Profile

If the user does not already have a profile JSON, use Zotero MCP read tools to collect evidence first:

1. `zotero_list_collections`
2. `zotero_profile_evidence`

Then write a JSON profile matching the same structure used by `config/research-interest.example.json`:

- `profile_id`
- `profile_name`
- `zotero_basis`
- `retrieval_defaults`
- `interests[]`

Prefer short `method_keywords` and only a small number of `query_aliases` per interest.

Write it in `temp/paper-finder/research-interest.json`, if there is no such directory, create it.

## Enrich Candidate Notes

After the Python retrieval run finishes, read the generated Obsidian note and use Zotero MCP read tools to gather nearby library evidence. Then update the note's frontmatter and the `Why It Matters`, `Quick Takeaways`, and `Caveats` sections using the prompt in `skills/paper-finder/prompts/enrich-candidate.prompt.txt`.