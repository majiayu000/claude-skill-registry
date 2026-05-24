---
name: fastmod
description: Use fastmod to make mass code updates to avoid many repetitive changes.
---

# fastmod

## Instructions

You can occasionally use `fastmod` or `sed` to make mass updates to the codebase and avoid wasting tokens changing each case one at a time.

Before making many repetitive changes to the codebase, consider using `fastmod --accept-all`.

THINK HARD about how best to use `fastmod` as it can dramatically improve your productivity.

## Examples

Example of switching the `py_type` function to use `impl ResourceTracker` instead of `T: ResourceTracker`:

```bash
fastmod --accept-all 'fn py_type<T: ResourceTracker>(\(.+?)<T>' 'fn py_type$1<impl ResourceTracker>'
```
