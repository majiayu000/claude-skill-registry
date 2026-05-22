---
name: svelte-template-directives
# prettier-ignore
description: Svelte template directives ({@attach}, {@html}, {@render}, {@const}, {@debug}). Use for DOM manipulation, third-party libs, tooltips, canvas, dynamic HTML. @attach replaces use: actions.
---

# Svelte Template Directives

## @attach (Svelte 5.29+)

**The reactive alternative to `use:` actions.** Re-runs when dependencies
change, passes through components via spread, supports cleanup functions.

```svelte
<script>
	import ImageZoom from 'js-image-zoom';

	function useZoom(options) {
		return (element) => {
			new ImageZoom(element, options);
			return () => console.log('cleanup');
		};
	}
</script>

<!-- Re-runs if options changes (use: wouldn't!) -->
<figure {@attach useZoom({ width: 400 })}>
	<img src="photo.jpg" alt="zoomable" />
</figure>
```

## Quick Reference

| Directive   | Purpose                        | Reactive? |
| ----------- | ------------------------------ | --------- |
| `{@attach}` | DOM manipulation, 3rd-party    | Yes       |
| `{@html}`   | Render raw HTML strings        | Yes       |
| `{@render}` | Render snippets                | Yes       |
| `{@const}`  | Local constants in blocks      | N/A       |
| `{@debug}`  | Pause debugger on value change | N/A       |

## @attach vs use: Actions

| Feature               | `use:`  | `@attach`           |
| --------------------- | ------- | ------------------- |
| Re-runs on arg change | No      | **Yes**             |
| Composable            | Limited | **Fully**           |
| Pass through props    | Manual  | **Auto via spread** |
| Convert legacy        | N/A     | `fromAction()`      |

## Reference Files

- [attach-patterns.md](references/attach-patterns.md) - Real-world @attach
  examples
- [other-directives.md](references/other-directives.md) - @html, @render,
  @const, @debug

## Notes

- `@attach` requires Svelte 5.29+
- Use `fromAction` from `svelte/attachments` to convert legacy actions
- Attachments pass through wrapper components when you spread props
- **Last verified:** 2025-01-13

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual
-->
