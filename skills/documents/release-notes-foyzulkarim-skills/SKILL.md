---
name: release-notes
description: "Draft a changelog for the next release by summarizing git commits since the last tag. Use only when the user asks to draft release notes, write a changelog entry, or prepare the next version's notes — never trigger automatically."
model: inherit
color: plum
---

# Release Notes

Draft a release changelog by summarizing the commits since the last release, then suggest the
next semver version and prepend the entry to `CHANGELOG.md` at the project root.

## Steps

1. **Find the commit range and version baseline.** Determine the last released tag:

   ```bash
   git describe --tags --abbrev=0 2>/dev/null
   ```

   - If a tag exists, the range is `<tag>..HEAD`, and the tag itself is the version baseline.
   - If no tag exists (fresh repo), use the full history and **ask the developer** for the
     current version — do not infer it from any manifest, lockfile, or config file belonging to
     the project. This skill only reads git; it never inspects a project's toolchain.

2. **Collect the commits** in the range:

   ```bash
   # with a tag:
   git log <tag>..HEAD --oneline --no-merges
   # without a tag:
   git log --oneline --no-merges
   ```

3. **Group the commits** by type, inferring the type from the message
   (Conventional Commits prefix if present, otherwise from the wording):
   - **Features** — new functionality (`feat`, "Add", "Support")
   - **Fixes** — bug fixes (`fix`, "Fix", "Correct")
   - **Chores / Maintenance** — `chore`, `refactor`, `docs`, deps, tooling
   - Drop noise (pure formatting/typo commits) or fold them into a related entry.

4. **Suggest the next version** from the baseline established in Step 1 (the tag, or the
   version the developer gave you), using semver:
   - Breaking changes → **major**
   - Any new feature → **minor**
   - Only fixes/chores → **patch**

   State the bump explicitly (e.g. `1.1.0 → 1.2.0`) and the one reason for it.

5. **Draft the release entry** in this shape (omit empty sections):

   ```markdown
   ## v<next-version> — <YYYY-MM-DD>

   ### Features
   - <user-facing summary> (<short-sha>)

   ### Fixes
   - <user-facing summary> (<short-sha>)

   ### Maintenance
   - <user-facing summary> (<short-sha>)
   ```

6. **Write the entry to `CHANGELOG.md`** at the project root:

   - If `CHANGELOG.md` does not exist, create it with a top-level heading:
     ```markdown
     # Changelog
     ```
   - Read the current contents of `CHANGELOG.md`.
   - Prepend the new entry (insert it immediately after the `# Changelog`
     heading line, before any existing entries) so the file stays newest-first.
   - Write the updated file.

   Use the Read and Write (or Edit) tools to do this — do **not** shell out to
   `sed` or `awk`.

7. **Report to the user** what was written: show the new entry inline and
   confirm the file was updated.

## Notes

- Write entries from the **user's** perspective (what changed for them), not a
  verbatim commit-message dump.
- Include today's date (from the `currentDate` context, or `date +%Y-%m-%d`)
  in the entry heading.

## You Must NOT

- Create, move, or push a git tag — the tag is the developer's release action, not yours.
- Bump the version in any manifest, lockfile, or config file. This skill records what
  changed; it does not perform the release.
- Push anything, or open a PR. The `CHANGELOG.md` edit stays in the working tree.
- Infer the current version from a project manifest when no tag exists — ask the developer
  instead. The version baseline is git's, never the toolchain's.
- Rewrite, reorder, or delete existing `CHANGELOG.md` entries — only prepend the new one.
