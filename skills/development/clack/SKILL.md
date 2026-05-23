---
name: clack
description: Comprehensive guidance for building and debugging JavaScript and TypeScript CLIs with @clack/core and @clack/prompts, backed by bundled upstream source and examples. Use when implementing clack prompt flows, deciding between core primitives and styled prompts, adapting clack examples, or validating clack API usage.
---

# Clack CLI Skill

Use this skill to implement reliable interactive CLIs with `@clack/core` and `@clack/prompts`.

## Workflow

1. Decide whether to use `@clack/prompts` or `@clack/core`.
2. Read only the minimum reference files needed for the task.
3. Start from the closest example in `references/examples/`.
4. Implement cancellation handling after every prompt.
5. Add UX polish (`intro`, `outro`, `spinner`, `progress`, `tasks`, `log`, `taskLog`, `stream`) when useful.
6. Verify imports against export maps in `references/docs/prompts-exports.ts` and `references/docs/core-exports.ts`.

## Pick the Right Layer

Use `@clack/prompts` by default.
- Choose it for production-ready styling and quick delivery.
- Use it when the request maps to standard prompt types: text, confirm, select, multiselect, grouped prompts, logs, spinners, progress, tasks, or streaming logs.

Use `@clack/core` when lower-level control is required.
- Choose it for custom rendering, custom prompt behavior, or unstyled primitives.
- Use it when the request needs direct prompt classes (`TextPrompt`, `SelectPrompt`, `ConfirmPrompt`, `Prompt`) or deep customization.

## Mandatory Safety Patterns

Handle cancellation on every prompt result.

```ts
import * as p from '@clack/prompts';

const value = await p.text({ message: 'Your name?' });
if (p.isCancel(value)) {
  p.cancel('Operation cancelled.');
  process.exit(0);
}
```

Start and close sessions cleanly for user-facing CLIs.

```ts
p.intro('create-app');
// prompts
p.outro('Done');
```

## Prompt Design Guidance

Use these defaults unless the user asks otherwise.
- `text`: provide `validate` for required or constrained input.
- `confirm`: use for binary decisions; avoid coercing free-form text.
- `select`: use for mutually exclusive choices.
- `multiselect` or `groupMultiselect`: use for multi-choice and hierarchical multi-choice flows.
- `group`: gather structured answers while preserving dependencies between steps.
- `spinner` and `progress`: wrap long-running tasks and update status clearly.
- `tasks`: execute sequential task blocks with spinner status.
- `taskLog`: stream subprocess output and finish with success/failure.
- `stream`: render async or tokenized output (for LLM-style streaming).

## Implementation Sequence

1. Inspect user requirements and identify required prompt primitives.
2. Read the nearest example under `references/examples/`.
3. Confirm function/class availability from:
   - `references/docs/prompts-exports.ts`
   - `references/docs/core-exports.ts`
4. If behavior is unclear, inspect source under:
   - `references/source/prompts/`
   - `references/source/core/`
5. Implement with cancellation guards and clear terminal messaging.
6. Keep fallback behavior for non-interactive contexts when requested (see spinner and CI-oriented examples).

## Reference Loading Strategy

Start with these files.
- `references/docs/prompts-readme.md`
- `references/docs/core-readme.md`
- `references/INDEX.md`

Load specific source files only as needed.
- Prompts wrapper internals: `references/source/prompts/*.ts`
- Core prompt primitives: `references/source/core/prompts/*.ts`
- Core utility behavior: `references/source/core/utils/*.ts`

## Example-First Mapping

Use this quick mapping to avoid re-inventing flows.
- General prompt suite: `references/examples/basic/index.ts`
- Validation: `references/examples/basic/text-validation.ts`
- Autocomplete: `references/examples/basic/autocomplete.ts`
- Autocomplete multi-select: `references/examples/basic/autocomplete-multiselect.ts`
- Defaults: `references/examples/basic/default-value.ts`
- Filesystem path prompt: `references/examples/basic/path.ts`
- Spinner basics: `references/examples/basic/spinner.ts`
- Spinner cancellation: `references/examples/basic/spinner-cancel.ts`
- Advanced spinner cancellation: `references/examples/basic/spinner-cancel-advanced.ts`
- CI-oriented spinner behavior: `references/examples/basic/spinner-ci.ts`
- Timer-style spinner updates: `references/examples/basic/spinner-timer.ts`
- Progress bar: `references/examples/basic/progress.ts`
- Task log streaming: `references/examples/basic/task-log.ts`
- Stream utility: `references/examples/basic/stream.ts`
- Changesets integration flow: `references/examples/changesets/index.ts`

## Quality Bar

Before finalizing any clack implementation:
- Confirm every import exists in the current exports file.
- Ensure cancellation flow always exits safely.
- Ensure prompt wording is short and unambiguous.
- Ensure long-running operations provide visible status.
- Ensure selected layer (`core` vs `prompts`) matches customization needs.
