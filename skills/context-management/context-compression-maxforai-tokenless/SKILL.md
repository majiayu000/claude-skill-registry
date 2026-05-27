---
name: context-compression
description: Use Tokenless for large files and noisy tool outputs before they enter context. Must be used when commands, Read output, diffs, logs, or search results are large.
---

# Tokenless Context Compression

When working in this project, do not feed noisy raw outputs or large files directly into context.

Tokenless is mandatory for large or noisy context:
- If a file is large, first use `tokenless read --agent --data-dir <dir> <file>`.
- If a Bash command is noisy, first use `tokenless run --agent --data-dir <dir> -- <command>`.
- If a Tokenless hook blocks or caps a tool call, do not bypass it with another full-output command.
- If you need exact evidence after a packet, expand the artifact before editing.
- If Tokenless reports a pending large-file gate, the next action must be the exact `NEXT REQUIRED COMMAND`.

The hook automatically caps high-noise Bash commands and large low-risk Read outputs through Tokenless.

Keep tool inputs small:
- Tokenless saves context by replacing large tool outputs with compact packets. Do not recreate the same token cost by sending huge generated tool inputs.
- Prefer `tokenless read`, `tokenless expand`, and small bounded `Edit`/`MultiEdit` calls over large patch scripts.
- Do not create large heredocs, `cat > file <<EOF`, giant `node -e` / `python -` commands, or temporary apply/fix/rewrite scripts unless the user explicitly asks.
- If you feel tempted to write a big script to patch a large file, stop and use Tokenless to expand the exact lines, then edit only that small region.

For manual local development in this repository, use `./plugins/claude-code/bin/tokenless` or the packaged `tokenless` alias:

```bash
./plugins/claude-code/bin/tokenless run --agent --data-dir /tmp/tokenless-dev -- npm test
```

High-noise commands include:
- npm test, pnpm test, yarn test
- pytest
- npm/pnpm/yarn build, lint, typecheck, install
- go test, cargo test, mvn test/verify/package, gradle build/test
- git diff, git log
- rg, grep -R
- find, tree, ls -R
- docker logs/build, kubectl logs/describe, Vercel/Netlify CLI logs

When you see a `TOKENLESS-PACKET` block:
1. Treat it as a compressed evidence packet.
2. Use the key failures, relevant files, line numbers, and raw artifact pointer.
3. Do not ask for the full raw output unless needed.
4. If needed, use the full raw artifact command shown in the `Raw artifact:` line.

When you see a `TOKENLESS-READ-PACKET` block:
1. Treat it as a compact local summary of a large file.
2. Read `Action boundary` before running any other command. It defines what tool commands are valid for this artifact.
3. If it contains `Action brief` and `Editable snippets`, treat those snippets as the first-pass edit surface, not as a table of contents to explore.
4. For broad visual/style tasks, do one minimal native `Read` to register editor state if you plan to edit, then make 6-10 bounded `Edit` calls from the snippets before doing more exploration.
5. Use only the artifact lookup commands shown in `Action boundary` when a needed `old_string` is not present in the snippets.
6. Do not expand every listed region by default.
7. Do not use repeated `grep`, `rg`, `sed`, or small `Read` calls to re-map the same file after a packet has already identified the edit targets.
8. Do not add unrelated files, scripts, or JS/HTML interactions for a CSS-only request unless the user explicitly asks.

Tool boundaries:
- `tokenless read` creates a whole-file packet only.
- `tokenless read` is not a range, selector, or line lookup tool.
- Do not invent `tokenless read --range`, `tokenless read --selector`, `tokenless read --lines`, or similar flags.
- `tokenless expand` is the artifact lookup tool for a specific selector/text or line range.
- `tokenless show` / raw artifact access is not for normal editing.

Large CSS visual-edit protocol:
1. After a `TOKENLESS-READ-PACKET`, do not perform a second full-file read.
2. Identify the smallest useful edit set from `Editable snippets`: tokens/variables, background layer, shared cards, buttons, one optional hero/visual area, one optional timeline/footer area.
3. After the registration `Read`, make 6-10 bounded `Edit` calls when the snippets are sufficient.
4. If exact `old_string` is missing, use at most two `tokenless expand` lookups before the first edit.
5. Do not wait for `File must be read first`; proactively do one minimal native `Read` only to register editor state, then immediately edit. If the error still appears, do not remap the file.
6. After the first successful edit, continue editing only if the user request still clearly needs it; otherwise stop with a concise summary.
7. Do not open the page or run visual validation unless the user explicitly asks for validation.
8. Do not make “extra premium” changes outside the asked surface, such as mouse-tracking JS, custom scrollbars in HTML, or new runtime scripts, unless requested.
9. Final answer should be 3-5 concise bullets only; do not write a long change diary.

Large source edit protocol:
1. After a `TOKENLESS-READ-PACKET` for `.js`, `.jsx`, `.ts`, `.tsx`, `.py`, `.vue`, or `.svelte`, do not perform a second full-file read.
2. Do one minimal native `Read` only to register editor state if you plan to edit.
3. Use `Source map`, `SFC sections`, `Project file hints`, and `Editable snippets` as the first-pass edit surface.
4. Make 4-8 bounded `Edit` calls from the snippets; do not remap the file with `grep`, `rg`, `sed`, or repeated `Read` calls.
5. If exact `old_string` is missing, use at most two `tokenless expand` lookups before editing.
6. Do not run tests, build, typecheck, browser validation, or package commands unless the user explicitly asks for validation.
7. Final answer should be 3-5 concise bullets only; do not write a long change diary.

For multi-file JS/TS/Python/Vue/Svelte tasks:
1. Use `Project file hints` before running `ls`, `find`, or broad `rg`.
2. If a hinted adjacent file must be edited, read that exact file; do not map the whole project first.
3. Keep the first pass to the requested file plus clearly referenced adjacent files only.

Trajectory budget:
- Goal: one packet read, one minimal registration `Read` when editing, zero artifact expands unless required, one bounded serial `Edit` phase, concise final answer.
- If you are about to run a fourth exploration command after a packet, stop and edit from the evidence already available.
- If Tokenless blocks with stale state, run the required refresh once, then resume bounded editing. Do not probe around the stale gate with alternate raw reads.
- Extra `tokenless expand` calls are a soft budget, not a hard denial. The 3rd lookup may include a warning; later lookups may be compacted. Treat either as a signal to edit from existing evidence unless the user requested exact review/security/legal/syntax validation.

Large-file edit discipline:
1. Prefer normal editing behavior after the compact summary has identified the relevant area.
2. Use bounded serial `Edit` calls because this Claude Code environment may not expose `MultiEdit`.
3. For broad visual/style requests, pick a few high-impact regions and stop after meaningful improvements.
4. A successful small `Edit` or bounded `MultiEdit` keeps a Tokenless edit lease for the same file.
5. Run `tokenless read` again after `Write`, large edits, external file changes, lease exhaustion, or when Tokenless explicitly blocks with `TOKENLESS-STALE`.
6. If a stale-packet hook blocks an edit, the blocked tool call did not execute.
7. Do not use a large generated patch script as a workaround for the stale gate.

When a large `Read` is capped:
1. Run the exact `tokenless read` command shown by the hook.
2. Use the packet to identify relevant selectors, symbols, sections, or line ranges.
3. If the packet includes exact snippets, attempt the next bounded edit from them before expanding.
4. Expand only with the exact artifact lookup commands shown in the packet if the compact summary is not enough to make the next bounded edit.
5. Do not replace this flow with `cat`, unbounded `grep`, or a full-file `Read`.

When Tokenless prints `NEXT REQUIRED COMMAND`:
1. Run that command exactly.
2. Do not run `cat`, a full-file `Read`, or broad file dumps against the gated file first.
3. After the command succeeds, continue from the compact summary and expand only if needed.

Bounded commands are allowed after Tokenless has created the packet:
- `sed -n '100,160p' file`
- `rg -n "target" file`
- `tokenless expand <artifact_id> --around "target"`

Bounded commands are fallback tools after the packet, not the default path. If the packet provides snippets for the intended edit, edit first.
Bounded commands are not a replacement for the initial large-file Tokenless packet when the file is known to be large.
Large generated commands are not bounded, even if they write locally. Avoid large heredocs, large inline scripts, and temporary patch helpers unless the user explicitly asks for them.

Never assume omitted sections are irrelevant if the task requires exact full-text review. For legal, financial, security-critical, or exact patch review tasks, inspect raw artifacts when necessary.
