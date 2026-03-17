---
name: form-patterns
# prettier-ignore
description: DaisyUI v5 form patterns. Use for inputs, selects, textareas, validation, and form structure with fieldset/legend.
---

# Form Patterns

## Quick Start

```svelte
<form {...my_form} class="space-y-4">
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Name</legend>
		<label class="validator input w-full">
			<input
				type="text"
				name="name"
				placeholder="Your name"
				class="grow"
				required
			/>
		</label>
	</fieldset>

	{#if my_form.error}
		<div class="alert alert-error">{my_form.error}</div>
	{/if}

	<button class="btn btn-block btn-primary" type="submit"
		>Submit</button
	>
</form>
```

## Core Principles

- **v5 structure**: Use `fieldset`/`fieldset-legend` (NOT old
  `form-control`/`label-text`)
- **Input wrapper**: `<label class="input w-full">` contains
  `<input class="grow">`
- **Validation**: Add `validator` class to label for automatic
  validation UI
- **Selects/textareas**: Apply classes directly (e.g.,
  `select w-full`) - no wrapper
- **Error handling**: Remote functions provide `.error` property
  automatically
- **Spacing**: Use `space-y-4` on forms for consistent spacing

## Reference Files

- [forms-guide.md](references/forms-guide.md) - Complete DaisyUI v5
  form patterns and examples
