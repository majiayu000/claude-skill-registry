---
name: ocaml-project-setup
description: "Standards for OCaml project metadata files. Use when initializing a new OCaml library/module, preparing for opam release, setting up CI, discussing project structure, or ensuring proper .mli/.ocamlformat files exist."
license: ISC
---

# OCaml Project Setup

## Required Files

Every OCaml project needs:

| File | Purpose |
|------|---------|
| `dune-project` | Build configuration, opam generation |
| `dune` (root) | Top-level build rules |
| `.ocamlformat` | Code formatting (required) |
| `.gitignore` | VCS ignores |
| `LICENSE.md` | License file |
| `README.md` | Project documentation |
| CI config | GitHub Actions / GitLab CI / Tangled |

## Interface Files (.mli)

**Every library module must have an `.mli` file** for:
- Clear API boundaries
- Proper encapsulation
- Documentation surface

```ocaml
(* lib/user.mli *)

(** User management.

    This module provides types and functions for user operations. *)

type t
(** A user. *)

val create : name:string -> email:string -> t
(** [create ~name ~email] creates a new user. *)

val name : t -> string
(** [name u] is the user's name. *)

val pp : t Fmt.t
(** [pp] is a pretty-printer for users. *)
```

**Documentation style**:
- Functions: `[name args] is/does ...`
- Values: `[name] is ...`
- End with period

## Standard Module Interface

For modules with a central type `t`:

```ocaml
type t
val v : ... -> t                           (* pure constructor *)
val create : ... -> (t, Error.t) result    (* constructor with I/O *)
val pp : t Fmt.t                           (* pretty-printer - required *)
val equal : t -> t -> bool                 (* equality *)
val compare : t -> t -> int                (* comparison *)
val of_json : Yojson.Safe.t -> (t, string) result
val to_json : t -> Yojson.Safe.t
```

## OCamlFormat Configuration

**Required**: `.ocamlformat` in project root.

```
version = 0.28.1
```

Run `dune fmt` before every commit.

## Logging Setup

Each module using logging should declare a source:

```ocaml
let log_src = Logs.Src.create "project.module"
module Log = (val Logs.src_log log_src : Logs.LOG)
```

Log levels:
- `Log.app` - Always shown (startup)
- `Log.err` - Critical errors
- `Log.warn` - Potential issues
- `Log.info` - Informational
- `Log.debug` - Verbose debugging

## User Configuration

Read from `~/.claude/ocaml-config.json`:

```json
{
  "author": { "name": "Name", "email": "email@example.com" },
  "license": "ISC",
  "ci_platform": "github",
  "git_hosting": { "type": "github", "org": "username" },
  "ocaml_version": "5.2.0"
}
```

## License Headers

Every source file starts with license header:

```ocaml
(*---------------------------------------------------------------------------
  Copyright (c) {{YEAR}} {{AUTHOR}}. All rights reserved.
  SPDX-License-Identifier: ISC
 ---------------------------------------------------------------------------*)
```

## Project Structure

```
project/
├── dune-project
├── dune
├── .ocamlformat
├── .gitignore
├── LICENSE.md
├── README.md
├── lib/
│   ├── dune
│   ├── foo.ml
│   └── foo.mli         # Required for every .ml
├── bin/
│   ├── dune
│   └── main.ml
├── test/
│   ├── dune
│   ├── test.ml
│   └── test_foo.ml
├── .github/workflows/  # GitHub Actions
├── .gitlab-ci.yml      # GitLab CI
└── .tangled/workflows/ # Tangled CI
```

## dune-project

```lisp
(lang dune 3.21)
(name project_name)
(generate_opam_files true)

(license ISC)
(authors "Name <email@example.com>")
(maintainers "Name <email@example.com>")
(source (tangled user.domain/project_name))

(package
 (name project_name)
 (synopsis "Short description")
 (description "Longer description")
 (depends
  (ocaml (>= 5.2))
  (alcotest (and :with-test (>= 1.7.0)))))
```

**Note**: Don't add `(version ...)` - added at release time.

### Tangled Source Syntax

For projects hosted on tangled.org, use the succinct source stanza:

```lisp
(source (tangled user.domain/project-name))
```

Examples:
- `(source (tangled anil.recoil.org/ocaml-brotli))`
- `(source (tangled user.example.org/my-library))`

## Tangled CI Configuration

For projects hosted on tangled.org, create `.tangled/workflows/build.yml`:

```yaml
when:
  - event: ["push", "pull_request"]
    branch: ["main"]

engine: nixery

dependencies:
  nixpkgs:
    - shell
    - stdenv
    - findutils
    - binutils
    - libunwind
    - ncurses
    - opam
    - git
    - gawk
    - gnupatch
    - gnum4
    - gnumake
    - gnutar
    - gnused
    - gnugrep
    - diffutils
    - gzip
    - bzip2
    - gcc
    - ocaml
    - pkg-config

steps:
  - name: opam
    command: |
      opam init --disable-sandboxing -a -y

  - name: repo
    command: |
      opam repo add aoah https://tangled.org/anil.recoil.org/aoah-opam-repo.git

  - name: deps
    command: |
      opam install . --confirm-level=unsafe-yes --deps-only

  - name: build
    command: |
      opam exec -- dune build

  - name: test
    command: |
      opam install . --confirm-level=unsafe-yes --deps-only --with-test
      opam exec -- dune runtest --verbose
```

### Tangled Workflow Syntax

| Field | Description |
|-------|-------------|
| `when` | Trigger conditions: `event` (push/pull_request) and `branch` |
| `engine` | Build engine, use `nixery` for Nix-based builds |
| `dependencies.nixpkgs` | List of Nix packages to include |
| `environment` | Global or per-step environment variables |
| `steps` | Build steps with `name` and `command` |

Per-step environment variables:

```yaml
steps:
  - name: test
    environment:
      MY_VAR: value
    command: |
      echo $MY_VAR
```

## Templates

See `templates/` directory for:
- `dune-project.template`
- `dune-root.template`
- `ci-github.yml`
- `ci-gitlab.yml`
- `ci-tangled.yml`
- `gitignore`
- `ocamlformat`
- `LICENSE-ISC.md`
- `LICENSE-MIT.md`
- `README.template.md`
