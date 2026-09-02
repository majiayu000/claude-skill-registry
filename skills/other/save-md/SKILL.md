---
name: save-md
description: 'Use when asked to save a named source as a .md file with frontmatter. Captures a URL, file, or pasted text as one Markdown artifact with provenance and without summarization. Don''t use for remote, credential, publish, deploy, or irreversible changes.'
---

# Save source as Markdown

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User says save this, save this article, convert this, keep this source, or get the markdown for a named URL, file, or pasted text. |
| Authority | Reversible-local: write only the named .md file. Rollback is deleting the file. |
| Side effect | Writes one .md file to the working directory from a named source; no other artifact mutated. |
| Done | A .md file exists with YAML frontmatter and the source body preserved, not summarized. |

## Inputs

- Source (required): the URL, file path, or content to save. Must be supplied by the user. The skill does not guess which source the user means.
- Filename (optional): the desired .md filename. If omitted, infer from the source title or URL basename. If omitted and the source is ambiguous, stop and ask.
- Title (optional): override for the frontmatter `title` field. If omitted, infer from the source.
- Extract body only (optional): if true and the source is a web page, strip navigation, ads, footers, and unrelated page structure while preserving substantive content. Defaults to false. When false, preserve the source verbatim regardless of source type.

## Procedure

1. Confirm the source and filename if ambiguous. Stop if the user does not provide or confirm them. Done when: the source and filename are confirmed.
2. Fetch or read the source content. For a URL: retrieve via HTTP GET. For a file: read the file. For pasted content: use as-is. Done when: the content is retrieved or the fetch failure is reported.
3. Extract the body. When `extract_body_only` is false, preserve the source verbatim regardless of source type. When true and the source is a web page, strip navigation, ads, footers, scripts, and unrelated page structure while preserving all substantive text, headings, lists, code blocks, tables, and images with their original src attributes. When true and the source is a file or pasted content, use it verbatim. Done when: the body is extracted according to the flag.
4. Generate YAML frontmatter containing at minimum: `source` (the original URL, file path, or label the user provided), `title` (the inferred or user-supplied title), `saved_at` (ISO 8601 datetime of extraction), `source_type` (one of `url`, `file`, or `text`). Done when: frontmatter is generated.
5. Write the .md file to the working directory: frontmatter first, then a blank line, then the extracted body. Do not add summaries, introductions, or commentary. Preserve whitespace and structure from the source. Verify the file exists, is non-empty, and contains frontmatter and body. Done when: the file is written and verified.

## Failure and recovery

- Source unreachable: HTTP error, file not found, or permission denied. Stop. Do not create a file.
- Filename conflict: the target .md file already exists. Stop. Do not overwrite. Report the conflict.
- Empty source: the source resolves but has no extractable body content. Stop. Do not write a file.
- Write failure: disk full, permission error, or I/O error. Stop. Report the error.
- Verification failure: the file does not exist, is empty, or is missing frontmatter or body after write. Delete the file (reversible-local authority) and report the failure. Do not claim done. If the user explicitly requests leaving the file, honor that choice but report the verification failure.

## Output

One `.md` file in the working directory. The file contains YAML frontmatter followed by a blank line, then the source body preserved according to the `extract_body_only` flag. The body is not summarized, condensed, or rewritten.
