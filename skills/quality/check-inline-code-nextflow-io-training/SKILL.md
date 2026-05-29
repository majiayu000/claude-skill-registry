---
name: Check Inline Code Formatting
description: Review inline code in markdown files for proper formatting and syntax highlighting. Check for missing backticks on CLI flags, filenames, and code elements. Verify that inline syntax highlighting (#!groovy) is used appropriately. Use when reviewing documentation or quiz questions.
---

# Check Inline Code Formatting

Review inline code in markdown files for proper formatting and appropriate use of syntax highlighting.

## What to Check

### 1. Missing Backticks

The following should always be wrapped in backticks:

**CLI flags and options:**

- `-resume`, `-profile`, `-params-file`, `--input`, etc.

**Filenames and paths:**

- `nextflow.config`, `.command.sh`, `work/`, `modules/`, etc.

**Commands:**

- `nextflow run`, `nextflow log`, `docker run`, etc.

**Code elements:**

- Variable names: `params.input`, `outputDir`
- Process names: `SAYHELLO`
- Operators and methods: `collect()`, `map()`, `view()`
- Directives: `container`, `publishDir`, `memory`

### 2. Inline Syntax Highlighting

Use `` `#!groovy code` `` for Groovy/Nextflow code that benefits from syntax colouring.

**DO use `#!groovy` for:**

- Variable interpolation: `` `#!groovy ${variable}` ``
- Closures: `` `#!groovy { meta.id }` `` or `` `#!groovy .map { it * 2 }` ``
- Method chains with closures: `` `#!groovy channel.of(1,2,3).map { it * 2 }` ``
- String interpolation: `` `#!groovy "${greeting}-output.txt"` ``
- Type declarations: `` `#!groovy param: String = 'value'` ``

**DO NOT use `#!groovy` for:**

- Single words or identifiers: use `` `outputDir` `` not `` `#!groovy outputDir` ``
- Simple directives: use `` `container 'uri'` `` not `` `#!groovy container 'uri'` ``
- Plain dot notation: use `` `processName.out` `` not `` `#!groovy processName.out` ``
- Keywords alone: use `` `include` `` not `` `#!groovy include` ``

**The rule:** Only use `#!groovy` when there's meaningful syntax structure (braces, interpolation, operators) that highlighting will visually enhance. A single word or simple expression gains nothing from syntax highlighting.

### 3. Consistency

- Similar code references should be formatted the same way throughout a document
- Quiz answer options should have consistent formatting

## Examples

### Good inline code formatting

```markdown
Run the workflow with `nextflow run main.nf -resume`.

The `#!groovy ${greeting}` variable is interpolated into the string.

Set memory with `#!groovy process { withName: 'FOO' { memory = '4.GB' } }`.

The `container` directive specifies the Docker image.

Access outputs with `processName.out.outputName`.
```

### Bad inline code formatting

```markdown
<!-- Missing backticks -->

Run the workflow with nextflow run main.nf -resume.

<!-- Unnecessary #!groovy on single word -->

The `#!groovy container` directive specifies the image.

<!-- Missing #!groovy on closure -->

Transform with `.map { it.toUpperCase() }`.
```
