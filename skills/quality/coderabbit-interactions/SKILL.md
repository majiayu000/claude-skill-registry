---
name: coderabbit-interactions
description: Systematic workflow for CodeRabbit reviews - local CLI, PR threads, and commit attribution
version: 1.1.0
compatibility: All repositories with CodeRabbit enabled

metadata:
  category: code-quality
  tags:
    - code-review
    - coderabbit
    - quality
  triggers:
    - before-push
    - on-demand
---

# CodeRabbit Interactions

Workflows for CodeRabbit code reviews: local CLI usage, PR thread processing, and commit attribution.

## Two Review Modes

| Mode | When | Reference |
|------|------|-----------|
| **Local CLI** | Before push, get early feedback | `references/cli-integration.md` |
| **PR Threads** | After CodeRabbit reviews your PR | `references/workflow-examples.md` |

## Skill Contents

### Available Resources

**references/** - Detailed documentation
- [cli integration](references/cli-integration.md)
- [commit formats](references/commit-formats.md)
- [setup](references/setup.md)
- [workflow examples](references/workflow-examples.md)

**scripts/** - Automation scripts
- [batch reply](scripts/batch-reply.ts)
- [export comments](scripts/export-comments.ts)
- [reply to threads](scripts/reply-to-threads.ts)
- [run local review](scripts/run-local-review.ts)

---

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

- `.claude/skills/pr-lifecycle` - PR lifecycle including CodeRabbit integration
- [CodeRabbit CLI Docs](https://docs.coderabbit.ai/cli/overview)
- [Cursor Integration](https://docs.coderabbit.ai/cli/cursor-integration)
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/coderabbit-interactions/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

