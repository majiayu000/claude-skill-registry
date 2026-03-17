---
name: coding-typescript
cluster: coding
description: "TypeScript 5.x: strict mode, generics, decorators, mapped/conditional types, utility types, tsconfig"
tags: ["typescript","ts","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "typescript types generics strict tsconfig decorators mapped conditional"
---

# coding-typescript

## Purpose
This skill equips the AI to assist with TypeScript 5.x development, focusing on advanced features like strict mode, generics, decorators, mapped and conditional types, utility types, and tsconfig configuration. Use it to generate, debug, and optimize TypeScript code in real-time.

## When to Use
Apply this skill when working on projects requiring type safety, such as web apps with React or Node.js backends. Use it for code reviews, refactoring legacy JavaScript to TypeScript, or implementing complex type logic in strict mode environments. Avoid it for plain JavaScript unless migration is planned.

## Key Capabilities
- Enforce strict mode via tsconfig: Set `"strict": true` in tsconfig.json to catch errors like implicit any.
- Handle generics: Define reusable functions like `function identity<T>(arg: T): T { return arg; }`.
- Use decorators: Apply class decorators such as `@Component` from frameworks like Angular.
- Work with mapped types: Create types like `type Partial<T> = { [P in keyof T]?: T[P]; }`.
- Implement conditional types: Use constructs like `type IsString<T> = T extends string ? true : false;`.
- Leverage utility types: Apply `Omit<T, K>` or `Pick<T, K>` for type manipulation.
- Configure tsconfig: Specify options like `"target": "es2022"` and `"module": "esnext"` for builds.

## Usage Patterns
To accomplish tasks, invoke this skill by prefixing queries with the skill ID, e.g., "Use coding-typescript to write a generic array filter function." Always include specific TypeScript version details (5.x) in requests. For code generation, provide context like "Generate a TypeScript class with decorators in strict mode." When debugging, supply error messages and code snippets for targeted fixes. Integrate with IDEs by referencing tsconfig paths, e.g., run `tsc --project ./tsconfig.json` before AI-assisted edits.

## Common Commands/API
Use the following TypeScript CLI commands for tasks:
- Compile with strict mode: `tsc --strict index.ts` to enforce all strict options.
- Watch for changes: `tsc -w --noEmitOnError` to monitor files and block emits on errors.
- Generate declaration files: `tsc --declaration` to output .d.ts files for types.
For API patterns, reference TypeScript's compiler API in code: Import from 'typescript' and use `ts.createProgram()` for programmatic compilation. If external tools like ESLint are involved, set env vars like `$TSCONFIG_PATH` for custom configs. Code snippet for a generic function:
```typescript
function reverse<T>(array: T[]): T[] {
  return array.reverse();
}
```
For decorators, apply like this:
```typescript
function logged(target: any) { console.log(target); }
@logged
class Example {}
```

## Integration Notes
Integrate this skill with Node.js projects by ensuring TypeScript is installed via `npm install typescript@5.x`. For auth in related services (e.g., if fetching types from a remote API), use env vars like `$TYPESCRIPT_API_KEY` in scripts. In tsconfig.json, add paths for modules: `"paths": { "@app/*": ["src/*"] }`. When combining with other skills, chain outputs, e.g., use "coding-javascript" first for JS parts, then pipe to this for TypeScript conversion. Ensure compatibility by targeting ES modules: Set `"module": "esnext"` and use bundlers like Webpack.

## Error Handling
To handle TypeScript errors, always enable strict mode and use `tsc --pretty` for readable output. For type errors, check for specifics like "Type 'string' is not assignable to type 'number'" and suggest fixes via code snippets. Implement try-catch in runtime code, e.g.:
```typescript
try {
  const result = someFunction(); // Assume it might throw
} catch (error) {
  console.error(`Error: ${(error as Error).message}`);
}
```
For build errors, rerun `tsc` with `--diagnostics` to get detailed reports. If AI-generated code fails, re-query with the exact error message, e.g., "Fix this TypeScript error: 'TS2322: Type X is not assignable to type Y' in the following code: [snippet]".

## Concrete Usage Examples
1. **Example 1: Generating a generic utility type**  
   Query: "Use coding-typescript to create a mapped type that makes all properties of an interface optional."  
   Response: Generate code like `type Optional<T> = { [K in keyof T]?: T[K]; }`. Then, apply it: `interface User { name: string; age: number; } type PartialUser = Optional<User>;`.

2. **Example 2: Configuring tsconfig for strict mode**  
   Query: "Set up a tsconfig.json for a project with strict mode and decorators."  
   Provide: Create a file with `{ "compilerOptions": { "strict": true, "experimentalDecorators": true, "target": "es2022" } }`. Then, compile with `tsc --project tsconfig.json` to verify.

## Graph Relationships
- Related to cluster: "coding" (e.g., links to "coding-javascript" for shared patterns).
- Tagged with: "typescript", "ts", "coding" (connects to skills like "coding-react" for TypeScript-based frameworks).
- Dependencies: Requires "general-coding" for basic syntax, and integrates with "tooling-npm" for package management.
