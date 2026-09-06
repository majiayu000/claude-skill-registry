---
name: no-hide
description: 'Use when the user asks to detect clever-concealment patterns that obscure real code structure. Not for refactoring the concealment away: use unleak-abstraction.'
---

# No hide

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User wants to find clever concealment that obscures real structure. |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | A report identifying concealment that obscures real structure. |
| Done | Every applicable concealment form has been applied to every file in scope, every confirmed instance is reported with file, line, form, and severity, or an explicit none-found statement is emitted. |

## Inputs

- Target scope (required): file path, directory path, module name, or diff range to inspect.
- Concealment form (optional): if the user names a specific form, restrict detection to that form. If omitted, detect all forms.

## Procedure

1. Resolve the target. Locate the supplied scope. If the target does not exist or cannot be read, stop and return `target-missing`. Done when: the target is located and readable.
2. Parse each target file. Read the full text of every reachable source file within the scope. Done when: every reachable source file in scope is read.
3. Detect concealment patterns. Apply every applicable form to every file in scope. Do not stop scanning a file after the first high-severity pattern; continue through all forms across all lines so that additional high-impact findings are not suppressed.

   | Form | What to flag |
   |---|---|
   | Abstraction layering | Classes of indirection that add no behavior and require the reader to mentally reconstruct what a direct implementation would look like. One forwarding or delegation layer is allowed; two or more on the same call chain is concealment. |
   | Obscured naming | Names that describe implementation technique instead of domain concept, or names that invert the polarity of the operation (e.g., `disableSecurity()` that enables it, `close()` that opens a resource). |
   | Implicit control flow | Conditional logic encoded in naming conventions, comment conventions, or ordering rather than explicit if/else/switch. Loops whose termination depends on a mutable global or a side effect not visible at the call site. |
   | Indirection masking dependencies | Static calls, eager imports, or compile-time instantiation that make the runtime dependency graph invisible. Singleton accessors that bypass injection. Global mutable state accessed without an explicit reference. |
   | Structure serving author taste | File and module organization chosen for the author's sense of elegance rather than the reader's navigation. Depth-first directory trees where breadth-first would match the mental model. |

   Done when: every applicable form has been applied to every file in scope.

4. Classify severity.

   - High: actively misleads or inverts meaning. The reader will reach a wrong conclusion.
   - Medium: requires extra effort to decode; no active falsehood.
   - Low: friction without meaningful misdirection.

   Done when: every confirmed instance has a severity assignment.

5. Return the report. If no pattern is found, state that explicitly. If patterns are found, include every confirmed instance with file, line or range, pattern form, and severity. Done when: the report covers every confirmed instance or states explicitly that no pattern was found.

## Failure and recovery

- target-missing: the supplied scope does not exist or cannot be read. Do not proceed. Return `{status: "target-missing", scope: <supplied>}`.
- context-insufficient: the scope is too large to inspect within available context budget. Return partial results for confirmed findings; mark unscanned remainder as `incomplete`.
- out-of-scope form: the user named a concealment form this skill does not detect. Return `{status: "form-unknown", forms: <list of supported forms>}`.
- stop rather than widen: if the target scope contains items that are not source code, ignore them. Do not scan configuration, documentation, or generated artifacts unless the user explicitly names them.

## Output

One structured report: status, findings, summary, done flag, in that order.
