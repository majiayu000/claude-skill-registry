---
name: rspress-api-docs
description: Generate API documentation from TypeScript source code for RSPress. Use when documenting package APIs, extracting types from source code, or creating function/class reference pages.
allowed-tools: Read, Write, Edit, Glob, Grep
context: fork
agent: rspress-doc-agent
---

# RSPress API Documentation

You are a specialized skill for generating API documentation from TypeScript
source code in the Savvy Web Workflow documentation site.

## Documentation Approaches

**Manual Documentation** (Recommended): Read source files, extract type
signatures, and write structured markdown. This approach gives you full control
over content organization and clarity.

**Automated Documentation** (Limited): Tools like TypeDoc can generate docs,
but require integration setup and often produce verbose output that needs
editing.

This skill focuses on the manual approach for better results.

## API Documentation Directory

API reference documentation lives under package directories:

```text
docs/src/en/{package}/api/
├── index.mdx             # API overview (frontmatter only, user can add content)
├── functions/            # Function reference pages
│   ├── index.mdx
│   └── function-name.mdx
├── types/                # Type and interface reference
│   ├── index.mdx
│   └── type-name.mdx
└── classes/              # Class reference pages
    ├── index.mdx
    └── class-name.mdx
```

**Note:** All API documentation files are generated as `.mdx` files. The main
`index.mdx` overview file is only generated if it doesn't exist - if you've
added custom content to it, it will be preserved across regenerations.

## Manual Documentation Workflow

1. **Find the source code** - Use Glob to locate package source files
1. **Identify exports** - Use Grep to find exported functions, types, classes
1. **Read source files** - Extract type signatures, JSDoc comments
1. **Create markdown pages** - Write structured documentation for each export
1. **Link from index** - Add entries to `api/index.mdx` for navigation

## Function Documentation

Create function reference pages at `api/functions/{function-name}.mdx`:

```markdown
# functionName

Brief description of what the function does.

## Signature

```typescript
function functionName<T>(param1: string, param2: T): Promise<Result>
```

## Parameters

| Name   | Type     | Description              |
|--------|----------|--------------------------|
| param1 | string   | Description of parameter |
| param2 | T        | Generic parameter        |

## Returns

`Promise<Result>` - Description of return value

## Examples

```typescript
const result = await functionName('value', { data: true });
console.log(result);
```

## Throws

* `Error` - When validation fails
* `TypeError` - When parameters are invalid

## Related

* [RelatedType](../types/related-type.md)
* [Package Overview](../index.mdx)

```text

<!-- markdownlint-disable MD024 -->

## Type/Interface Documentation

Create type reference pages at `api/types/{type-name}.mdx`:

```markdown
# TypeName

Brief description of what this type represents.

## Definition

```typescript
interface TypeName {
  property1: string;
  property2?: number;
  method(): void;
}
```

## Properties

| Property  | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| property1 | string | Yes      | Description of property  |
| property2 | number | No       | Optional property        |

## Methods

### method()

Description of the method.

**Returns**: `void`

## Usage

```typescript
const example: TypeName = {
  property1: 'value',
  method() {
    console.log('called');
  }
};
```

## Related

* [relatedFunction](../functions/related-function.md)

```text

## Class Documentation

Create class reference pages at `api/classes/{class-name}.mdx`:

```markdown
# ClassName

Brief description of the class purpose.

## Constructor

```typescript
constructor(param1: string, options?: Options)
```

### Parameters

| Name    | Type    | Description       |
|---------|---------|-------------------|
| param1  | string  | Required parameter|
| options | Options | Optional config   |

## Properties

| Property | Type   | Description            |
|----------|--------|------------------------|
| name     | string | Read-only property     |

## Methods

### methodName(param: Type): ReturnType

Description of what the method does.

**Example**:

```typescript
const instance = new ClassName('value');
const result = instance.methodName(param);
```

## Related

* [Options](../types/options.md)

```text

<!-- markdownlint-enable MD024 -->

## Extracting Exports from Source

Use these patterns to find exports in TypeScript files:

**Find all exports**:

```bash
grep -r "^export " src/
```

**Find exported functions**:

```bash
grep -r "^export function " src/
```

**Find exported types**:

```bash
grep -r "^export (type|interface) " src/
```

**Find exported classes**:

```bash
grep -r "^export class " src/
```

## API Index Page

The overview file at `api/index.mdx` is auto-generated with frontmatter only.
If the file doesn't exist, it will be created with:

```markdown
---
title: API Reference
description: Auto-generated API documentation for package-name
overview: true
---

```

You can add custom content below the frontmatter. The plugin preserves existing
`index.mdx` files, so your custom content won't be overwritten.

## Tips

* Extract JSDoc comments from source code for descriptions
* Include practical examples that users can copy
* Link related types and functions together
* Keep parameter tables concise but complete
* Test code examples before documenting them
* Use proper TypeScript syntax highlighting
* Follow existing documentation patterns in the project
