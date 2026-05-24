---
name: ocaml-docs
description: "Fixing odoc documentation warnings and errors. Use when running dune build @doc, resolving reference syntax issues, cross-package references, ambiguous references, hidden fields, or @raise tags in OCaml documentation."
license: ISC
---

# OCaml Documentation (odoc) Skill

## When to Use

Use this skill when fixing odoc documentation warnings, typically from `dune build @doc`.

**Prerequisites:** This skill covers odoc v3 syntax which is not yet in released versions of dune or odoc. You need:
- dune pinned to https://github.com/jonludlam/dune/tree/odoc-v3-rules-3.21
- odoc pinned to https://github.com/jonludlam/odoc/tree/staging

## Reference Syntax

Use path-based disambiguation `{!Path.To.kind-Name}` rather than `{!kind:Path.To.Name}`:

```ocaml
(* Correct *)
{!Jsont.exception-Error}
{!Proto.Incoming.t.constructor-Message}
{!module-Foo.module-type-Bar.exception-Baz}

(* Incorrect *)
{!exception:Jsont.Error}
{!constructor:Proto.Incoming.t.Message}
```

This allows disambiguation at any position in the path.

## Reference Kinds

- `module-` for modules
- `type-` for types
- `val-` for values
- `exception-` for exceptions
- `constructor-` for variant constructors
- `field-` for record fields
- `module-type-` for module types

## Cross-Package References

When odoc cannot resolve a reference to another package, add a documentation dependency in `dune-project`:

```lisp
(package
 (name mypackage)
 ...
 (documentation (depends other-package)))
```

Do NOT convert doc references `{!Foo}` to code markup `[Foo]` - this loses the hyperlink.

## Cross-Library References (Same Package)

When referencing modules from another library in the same package, use the full path through re-exported modules.

Example: If `claude.mli` has `module Proto = Proto`, reference proto modules as `{!Proto.Incoming}` not `{!Incoming}`.

## Missing Module Exports

If odoc reports "Couldn't find X" where X is the last path component:

1. Check if the module is re-exported in the parent module's `.mli`
2. Add `module X = X` to the parent's `.mli` if missing

## Ambiguous References

When odoc warns about ambiguity (e.g., both an exception and module named `Error`):

```ocaml
{!Jsont.exception-Error}  (* for the exception *)
{!Jsont.module-Error}     (* for the module *)
```

## @raise Tags

For `@raise` documentation tags, use the exception path with disambiguation:

```ocaml
@raise Jsont.exception-Error
@raise Tomlt.Toml.Error.exception-Error
```

## Escaping @ Symbols

The `@` character is interpreted as a tag marker in odoc. When you need a literal `@` in documentation text (e.g., describing @-mentions), escape it with a backslash:

```ocaml
(* Correct - escaped @ *)
(** User was \@-mentioned *)
(** Mentioned via \@all/\@everyone *)

(* Incorrect - will produce "Stray '@'" or "Unknown tag" warnings *)
(** User was @-mentioned *)
(** Mentioned via @all *)
```

## Hidden Fields Warning

When odoc warns about "Hidden fields in type 'Foo.Bar.t': field_name", it means a record field uses a type that odoc can't resolve in the documentation.

**Diagnosis:**
1. Find the field definition in the `.mli` file
2. Identify what type the field uses (e.g., `uri : Uri.t`)
3. Check if that type's module is re-exported in the wrapper `.mli`

**Fix Option 1:** Re-export the module in the wrapper `.mli`:
```ocaml
(** RFC 3986 URI parsing *)
module Uri = Uri
```

**Fix Option 2:** If you only want to expose the type (not the whole module), use `@canonical`:

1. Add a type alias in the wrapper `.mli`:
   ```ocaml
   type uri = Uri.t
   ```

2. Add `@canonical` to the original type's documentation:
   ```ocaml
   (* In uri.mli *)
   type t
   (** A URI. @canonical Requests.uri *)
   ```

This tells odoc to link `Uri.t` to `Requests.uri` in the generated documentation.

## Interpreting Error Messages

| Error Pattern | Meaning | Fix |
|--------------|---------|-----|
| `unresolvedroot(X)` | X not found as root module | Check library dependencies, add documentation depends |
| `Couldn't find "Y"` after valid path | Y doesn't exist at that location | Verify module structure, check exports |
| `Reference to 'X' is ambiguous` | Multiple items named X | Add kind qualifier (e.g., `exception-X`) |
| `Hidden fields in type ... : field` | Field's type not resolvable | Re-export the type's module in wrapper `.mli` |

## Debugging

1. Run `dune clean` before `dune build @doc` to ensure fresh builds
2. Check the library's `.mli` file to see what modules are exported
3. For cross-library refs, trace the module path through re-exports
