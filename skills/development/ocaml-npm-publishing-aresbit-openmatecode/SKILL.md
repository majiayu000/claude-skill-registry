---
name: ocaml-npm-publishing
description: Publishing OCaml to npm via js_of_ocaml and wasm_of_ocaml. Use when discussing browser targets, JavaScript compilation, WASM output, npm packages, or the two-branch workflow.
license: ISC
---

# OCaml to NPM Publishing

## When to Use This Skill

Invoke this skill when:
- Setting up npm publishing for OCaml projects
- Configuring js_of_ocaml or wasm_of_ocaml
- Discussing browser targets for OCaml
- Creating the npm branch workflow

## Branch Structure

```
main branch     - OCaml source code, dune build files, opam packages
npm branch      - Built JavaScript/WASM assets, package.json, README for npm
```

The `npm` branch is an orphan branch with no shared history.

## Dune Build Rules

### Library with Browser Bindings

In `lib/js/dune`:

```dune
; Library compiled to bytecode (required for js_of_ocaml)
(library
 (name mylib_js)
 (public_name mylib-js)
 (libraries mylib brr)
 (modes byte)
 (modules mylib_js))

; Executable compiled to both JS and WASM
(executable
 (name mylib_js_main)
 (libraries mylib_js)
 (js_of_ocaml)
 (modes js wasm)
 (modules mylib_js_main))

; Friendly filename for JS
(rule
 (targets mylib.js)
 (deps mylib_js_main.bc.js)
 (action (copy %{deps} %{targets})))

; Friendly filename for WASM
(rule
 (targets mylib.wasm.js)
 (deps mylib_js_main.bc.wasm.js)
 (action (copy %{deps} %{targets})))

; Install web assets
(install
 (package mylib-js)
 (section share)
 (files
  mylib.js
  mylib.wasm.js
  (glob_files_rec (mylib_js_main.bc.wasm.assets/* with_prefix mylib_js_main.bc.wasm.assets))))
```

### dune-project Package

```dune
(package
 (name mylib-js)
 (synopsis "Browser library via js_of_ocaml/wasm_of_ocaml")
 (depends
  (ocaml (>= 5.1.0))
  (mylib (= :version))
  (js_of_ocaml (>= 5.0))
  (js_of_ocaml-ppx (>= 5.0))
  (wasm_of_ocaml-compiler (>= 5.0))
  (brr (>= 0.0.6))))
```

## Creating the NPM Branch

```bash
# Create orphan branch
git switch --orphan npm

# Add npm-specific files
git add package.json README.md LICENSE release.sh .gitignore
git commit -m "Initial npm package setup"

# Switch back
git checkout main
```

## NPM Branch Files

See `templates/` for:
- `package.json.template`
- `release.sh.template`

### package.json

```json
{
  "name": "mylib-jsoo",
  "version": "1.0.0",
  "description": "Description here",
  "browser": "mylib.js",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/user/repo.git#npm"
  },
  "files": [
    "mylib.js",
    "mylib.wasm.js",
    "mylib_js_main.bc.wasm.assets/",
    "README.md",
    "LICENSE"
  ]
}
```

Key points:
- Use `"browser"` not `"main"` (js_of_ocaml is browser-only)
- Point repository URL to `#npm` branch
- Include WASM assets directory

### release.sh

Script to copy built assets from main branch to npm branch.

## Workflow Summary

1. Develop on `main` branch (OCaml source)
2. Build: `dune build @install`
3. Switch to `npm` branch
4. Run `./release.sh` to copy built assets
5. Update version in `package.json`
6. Commit and `npm publish`

## README for npm

Focus on browser usage:
1. Clear browser-only notice
2. Installation via npm
3. Browser usage with `<script>` tags
4. Both JS and WASM examples
5. Browser compatibility requirements
