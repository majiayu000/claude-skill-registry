---
name: coderabbit-workflow
description: Systematic workflow for CodeRabbit reviews - local CLI, PR threads, and commit attribution
compatibility: All repositories with CodeRabbit enabled

metadata:
  version: "2.0.0"
  category: code-quality
  tags:
    - code-review
    - coderabbit
    - quality
  triggers:
    - before-push
    - on-demand
---

# CodeRabbit Workflow

Address CodeRabbit review comments systematically. Workflows for local CLI usage, PR thread processing, and commit attribution.

## When to use this skill

- When addressing CodeRabbit review comments on a PR
- Before push, to get early feedback with local CLI
- When asked to "fix coderabbit issues" or "address coderabbit comments"

## Skill Contents

### Available Resources

**📚 references/** - Detailed documentation
- [cli integration](references/cli-integration.md)
- [commit formats](references/commit-formats.md)
- [setup](references/setup.md)
- [workflow examples](references/workflow-examples.md)

**🔧 scripts/** - Automation scripts
- [batch reply](scripts/batch-reply.ts)
- [export comments](scripts/export-comments.ts)
- [reply to threads](scripts/reply-to-threads.ts)
- [run local review](scripts/run-local-review.ts)

---

## Two Review Modes

| Mode | When | Reference |
|------|------|-----------|
| **Local CLI** | Before push, get early feedback | `references/cli-integration.md` |
| **PR Threads** | After CodeRabbit reviews your PR | `references/workflow-examples.md` |

## Quick Start

1. Export comments: `node .claude/skills/coderabbit-workflow/scripts/export-comments.ts --pr <number>`
2. Review by severity: critical, major, minor
3. Apply fixes following patterns in `references/workflow-examples.md`
4. Commit with CodeRabbit co-author attribution (see below)
5. Update exported JSON to mark comments as fixed (set `status: 'fixed'`)
6. Push and reply to threads: `node .claude/skills/coderabbit-workflow/scripts/reply-to-threads.ts --file .tmp/coderabbit-*.json`

**Note:** The reply script only processes comments with `status !== 'pending'`. After applying fixes, update the JSON file to change status from `'pending'` to `'fixed'` before running the reply script.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/run-local-review.ts` | Run CodeRabbit CLI and save findings |
| `scripts/export-comments.ts` | Export PR comments to local JSON |
| `scripts/reply-to-threads.ts` | Batch reply to threads after fixes |

## References

| Reference | Content |
|-----------|---------|
| `references/setup.md` | Installation, authentication, troubleshooting |
| `references/cli-integration.md` | CLI commands and async workflow |
| `references/commit-formats.md` | All commit message templates |
| `references/workflow-examples.md` | Complete workflow examples |

## Key Requirement: Co-Author

All CodeRabbit fix commits must include:

```text
Co-authored-by: coderabbitai[bot] <136622811+coderabbitai[bot]@users.noreply.github.com>
```

See `references/commit-formats.md` for all templates.

## Related

- [pr-workflow](.claude/skills/pr-workflow/SKILL.md) - PR lifecycle including CodeRabbit integration
- [CodeRabbit CLI Docs](https://docs.coderabbit.ai/cli/overview)
- [Cursor Integration](https://docs.coderabbit.ai/cli/cursor-integration)
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/coderabbit-workflow/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

