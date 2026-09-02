---
name: readout
description: 'Use when a user wants a readable, shareable HTML document of findings. Produces a self-contained HTML readout under ~/.readouts, embedding cited source text and refreshing the local index. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Readout

Produce a readable, shareable HTML document of findings.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants a readable, shareable document of findings. |
| Authority | Reversible local write restricted to `~/.readouts/<output_name>.html` and `~/.readouts/index.html`. Rollback restores the prior index and removes the new readout. |
| Side effect | Writes self-contained HTML under `~/.readouts`. No remote mutation, VCS change, credential use, or external asset write. |
| Done | A self-contained HTML findings document exists at `~/.readouts/<output_name>.html` and the index at `~/.readouts/index.html` is transactionally updated. |

## Refusals

- Overwriting an existing readout: rejected. Stop; never overwrite `~/.readouts/<output_name>.html`.
- External resources in the HTML: rejected. A template override referring to an external stylesheet, script, image, font, or network resource is `non-self-contained-template`.
- Interpreting brief or source text as HTML: rejected. All inserted text is escaped.

## Inputs

- brief (required): a non-empty string or non-empty ordered list of findings. A string is rendered as paragraphs split on blank lines; a list is rendered as one section per item in input order.
- output_name (required): a filename stem without an extension or path separator.
- title (optional): the displayed document title; defaults to `output_name` with `-` and `_` replaced by spaces.
- sources (optional): an ordered list of readable source-file paths to embed. Preserve the supplied order; reject duplicate normalized paths.
- template_override (optional): a complete HTML document supplied by the user. It must contain at least one `{{TITLE}}`, `{{TIMESTAMP}}`, `{{BRIEF}}`, and `{{SOURCES}}` marker. Multiple occurrences of any marker are permitted and all are replaced. If absent, use the inline shell in Procedure step 3.

## Procedure

1. **Validate inputs.** Require a non-empty `brief`. Require `output_name` to match `^[A-Za-z0-9][A-Za-z0-9._-]*$`, reject `.` and `..`, and reject an existing `~/.readouts/<output_name>.html`. Normalize every source path without following it outside its containing filesystem root; require a regular readable file. Stop before any write on failure. Done when: all inputs pass validation or the procedure has stopped with a named failure.
2. **Escape all supplied text and source files to HTML entities.** Escape all inserted text in this order: `&` to `&amp;`, `<` to `&lt;`, `>` to `&gt;`, `"` to `&quot;`, and `'` to `&#39;`. Never interpret brief or source text as HTML. Render each non-empty brief paragraph as `<p>…</p>`; render list item `n` as `<section><h3>Finding n</h3><p>…</p></section>`. For each source, read exact UTF-8 text and emit `<details><summary>escaped-path</summary><pre><code>escaped-content</code></pre></details>`. An empty source list emits `<p>No source files supplied.</p>`. Invalid UTF-8 is `source-read-failed`; do not replace or discard bytes silently. Done when: all content is escaped and rendered.
3. **Assemble the HTML document via template replacement.** If `template_override` is absent, use this exact shell:

   ```html
   <!doctype html>
   <html lang="en">
   <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title>{{TITLE}}</title>
     <style>
       :root{color-scheme:light dark;font-family:ui-sans-serif,system-ui,sans-serif;line-height:1.55}body{max-width:72rem;margin:0 auto;padding:2rem}header{border-bottom:1px solid #8888;margin-bottom:2rem}main>section{margin-block:1.5rem}pre{overflow:auto;padding:1rem;border:1px solid #8888;border-radius:.5rem}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}details{margin-block:1rem}time{font-variant-numeric:tabular-nums;color:#666}a{color:inherit}
     </style>
   </head>
   <body>
     <header><h1>{{TITLE}}</h1><p>Generated <time datetime="{{TIMESTAMP}}">{{TIMESTAMP}}</time></p></header>
     <main><section id="findings"><h2>Findings</h2>{{BRIEF}}</section><section id="sources"><h2>Sources</h2>{{SOURCES}}</section></main>
   </body>
   </html>
   ```

   Escape the resolved title, obtain the current UTC timestamp in `YYYY-MM-DDTHH:MM:SSZ` form, and replace every occurrence of each marker (`{{TITLE}}`, `{{TIMESTAMP}}`, `{{BRIEF}}`, `{{SOURCES}}`). Multiple occurrences are permitted and all are replaced. Reject a shell with missing or remaining `{{…}}` markers after replacement. The result must contain no external stylesheet, script, image, font, or network reference. Done when: the document is assembled with no remaining markers and no external references.

4. **Atomically write the self-contained HTML document.** Ensure `~/.readouts/` exists. Retain prior `~/.readouts/index.html` bytes if present for rollback. Create `~/.readouts/<output_name>.html` only if absent, write the complete UTF-8 document, and close it successfully. A partial file is deleted on any write or close failure. Done when: the file is written and closed successfully.
5. **Refresh the self-contained index.html directory listing.** Enumerate regular `*.html` files directly under `~/.readouts/`, excluding `index.html` and temporary files. Sort basenames by ascending Unicode code-point order. Build an exact self-contained index with `<!doctype html>`, UTF-8 and viewport metadata, `<title>Readouts</title>`, `<h1>Readouts</h1>`, and one `<li><a href="URL_ENCODED_BASENAME">ESCAPED_STEM</a></li>` per file. Percent-encode every UTF-8 byte outside RFC 3986 unreserved characters in the `href`, and HTML-escape the displayed stem by step 2. Write the complete candidate to a temporary file in `~/.readouts/`, then atomically replace `index.html` only after the temporary write closes successfully. Done when: the index is atomically replaced.

## Failure and recovery

- `empty-brief`: stop before writing.
- `invalid-output-name`: stop before writing.
- `output-exists`: stop; never overwrite.
- `source-read-failed`: stop before writing.
- `invalid-template`: stop before writing.
- `non-self-contained-template`: stop before writing.
- `write-failed`: delete the partial target.
- `index-refresh-failed`: restore the prior index if replacement occurred; delete the new readout and temporary file.
- `done-predicate-failed`: re-read the new readout and index. Require the readout to be non-empty, contain the escaped title, brief rendering, UTC timestamp, and every supplied source path and exact escaped source text. Require the index to contain exactly one link to every current readout and no link to `index.html`. On any mismatch, restore the prior index bytes (or remove the new index if none existed), delete the new readout, and report `done-predicate-failed`.

No index failure is a successful partial result because the done predicate requires the index to be refreshed.

## Output

`~/.readouts/<output_name>.html` (self-contained HTML with brief, UTC timestamp, escaped source text) and `~/.readouts/index.html` (deterministically sorted self-contained index), ordered: readout, index.
