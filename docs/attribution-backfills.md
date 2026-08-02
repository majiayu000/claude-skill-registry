# Attribution Backfills

This ledger records contributor credit restored after a generated change had
already been published without its source `Co-authored-by` trailer. The normal
publish workflow now derives validated trailers from the pinned core and data
commit ranges; entries here are only for pre-automation history and must link
the original contribution, authoritative port, and published artifact.

## Lee — DynamoDB on-demand pricing correction

- Contributor: [Lee (`LeeroyHannigan`)](https://github.com/LeeroyHannigan)
- Original report: [main issue #54](https://github.com/majiayu000/claude-skill-registry/issues/54)
- Original patch: [main PR #53](https://github.com/majiayu000/claude-skill-registry/pull/53)
- Authoritative port: [data PR #103](https://github.com/majiayu000/claude-skill-registry-data/pull/103)
- Attributed data commit: `1884f5ff62faefcbbcd656105660254edf23fa61`
- First published main commit: `2d82af0b54ec083b2c593042a33b4255aaf1601e`

The data commit preserved `Co-authored-by: Lee <leeroyhannigan@yahoo.ie>`, but
the old subject-only main publisher dropped the trailer. The main commit that
introduces this ledger is the non-history-rewriting attribution backfill.
