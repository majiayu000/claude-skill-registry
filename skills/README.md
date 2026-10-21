# Legacy skill URL pointers

This frozen set of 312,160 SKILL.md pointers restores GitHub URLs from the last archive mirror on 2026-10-08. These files have no YAML frontmatter and are not installable skills. New skills receive no pointers.

Source data commit: `a21980a5b576646393ed574f158d7dd92fae4c3f`. Each pointer links to that immutable snapshot, registry search, and the removal request form. Pointer contents depend only on their legacy path and this fixed snapshot; do not rewrite them during publishes.

To regenerate in a separate output directory, run from the core checkout with the original frozen path list (one skills/.../SKILL.md per line):

```sh
.venv/bin/python scripts/write_legacy_skill_pointers.py --paths-file <legacy-paths.txt> --data-sha a21980a5b576646393ed574f158d7dd92fae4c3f --output-root <main-checkout>
```

Add `--check` to verify every pointer and this README byte-for-byte without writing. Matching files are left untouched; mismatched existing files cause an error.

For the one-time restoration, stage with `git add -f --sparse skills`, then run `git write-tree --prefix=skills/` in main. Pin that tree ID as `LEGACY_SKILL_POINTERS_TREE` in `.github/workflows/publish-from-core.yml`. Publishes exclude skills/ from checkout and preserve its index entries.
