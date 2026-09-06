---
name: bazel
description: 'Use when writing Bazel BUILD files with cc_library or cc_binary rules, Bzlmod dependencies, toolchain registration, remote execution, sandbox debugging, or bazel query and cquery graphs.'
---

# Bazel

Bazel for C/C++ projects: BUILD files, Bzlmod dependencies, toolchain registration, remote execution, dependency graph queries, and sandbox debugging. Grounded against Bazel 9.2.0, where Bzlmod is always enabled, all WORKSPACE logic is removed, and every C++ rule loads from `@rules_cc`.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task writes or debugs Bazel BUILD files, `cc_library`/`cc_binary`/`cc_test` rules, Bzlmod dependencies, toolchain registration, remote execution, sandbox failures, or `bazel query`/`cquery`/`aquery` dependency graphs. |
| Authority | Reversible local: writes only BUILD files, `MODULE.bazel`, `.bzl` files, and Bazel output directories (`bazel-out`, `bazel-bin`); rollback is version control plus `bazel clean`. No remote mutation. |
| Side effect | Local builds write to the Bazel output base; remote execution and remote cache flags contact a user-supplied endpoint. |
| Done | The requested targets build or test with `bazel build`/`bazel test`, or the blocker is reported with the failing command and output. |

## Inputs

- Project layout (required): the source tree and where BUILD files should live.
- Bazel version (required if not inferrable): run `bazel version`. Bazel 9 removed WORKSPACE and the native C++ rules; instructions below assume Bazel 9.
- External dependencies (optional): library names; versions come from the Bazel Central Registry.
- Remote execution endpoint (optional): a user-supplied remote execution or cache service URL.

## Procedure

1. Lay out the workspace. Bazel 9 uses `MODULE.bazel` as the only dependency file; there is no WORKSPACE. Put a `BUILD` file in each package directory. Done when: `MODULE.bazel` exists at the root and each package has a `BUILD` file.

```text
my-project/
├── MODULE.bazel
├── BUILD
├── src/
│   ├── BUILD
│   └── main.cc
└── lib/
    ├── BUILD
    ├── mylib.cc
    └── mylib.h
```

2. Write BUILD rules. Load every C++ rule from `@rules_cc`; the native `cc_library`/`cc_binary`/`cc_test` rules were removed from Bazel 9. Done when: every target builds with `bazel build`.

```python
# lib/BUILD
load("@rules_cc//cc:defs.bzl", "cc_library", "cc_test")

cc_library(
    name = "mylib",
    srcs = ["mylib.cc"],
    hdrs = ["mylib.h"],
    copts = ["-Wall", "-Wextra", "-std=c++23"],
    visibility = ["//visibility:public"],
    deps = [
        "@abseil-cpp//absl/strings",
        "//util:helpers",
    ],
)

cc_test(
    name = "mylib_test",
    srcs = ["mylib_test.cc"],
    deps = [
        ":mylib",
        "@googletest//:gtest_main",
    ],
)
```

```python
# src/BUILD
load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
    name = "main",
    srcs = ["main.cc"],
    deps = ["//lib:mylib"],
    linkopts = ["-lpthread"],
)
```

```bash
bazel build //src:main
bazel build //...
bazel test //lib:mylib_test
bazel run //src:main -- arg1 arg2
# Binary lands at bazel-bin/src/main
```

3. Declare dependencies in `MODULE.bazel` with `bazel_dep`. Versions come from the Bazel Central Registry; the pins below are the versions Bazel 9.2.0 itself depends on. Done when: `bazel mod graph` resolves without errors.

```python
# MODULE.bazel
module(name = "my_project", version = "1.0")

bazel_dep(name = "rules_cc", version = "0.2.17")
bazel_dep(name = "platforms", version = "1.0.0")
bazel_dep(name = "abseil-cpp", version = "20250814.1")
bazel_dep(name = "googletest", version = "1.17.0.bcr.2")
```

```bash
bazel mod graph        # full resolved dependency graph
bazel mod deps         # direct and indirect module deps
bazel mod tidy         # fix up MODULE.bazel declarations
```

4. Query the dependency graph. Done when: the query answers the question asked.

```bash
bazel query "deps(//src:main)"                  # transitive deps
bazel query "rdeps(//..., //lib:mylib)"         # reverse deps
bazel query "somepath(//src:main, //lib:mylib)" # dependency path
bazel cquery "deps(//src:main)" --output=files  # configuration-aware
bazel cquery "//lib:mylib" --output=build       # effective rule
bazel aquery "//src:main"                       # action graph: flags, inputs, outputs
```

5. Register toolchains with platforms. Define a `platform` with constraint values, a `toolchain` binding a toolchain target to a toolchain type, then `register_toolchains` in `MODULE.bazel`. The C++ toolchain configuration API lives in rules_cc under `cc/toolchains`; see `references/bazel-cpp-toolchain.md`. Done when: `bazel build --platforms=//platforms:<name>` selects the registered toolchain.

```python
# platforms/BUILD
platform(
    name = "linux_x86_64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
)
```

```python
# MODULE.bazel
register_toolchains("//toolchains:my_cc_toolchain")
```

6. Configure remote execution or caching when the user supplies an endpoint. Done when: the build runs against the endpoint or the flag is rejected and reported.

```bash
bazel build //... \
  --remote_executor=grpc://build.example.com:50051 \
  --remote_instance_name=main

# Cache only, no remote execution
bazel build //... --remote_cache=grpc://cache.example.com:9092
```

7. Debug sandbox failures. Done when: the failing action is identified and its missing input or disallowed write is fixed.

```bash
bazel build //src:main --sandbox_debug        # show sandbox inputs/outputs
bazel build //src:main --verbose_failures --sandbox_debug
bazel build //src:main --spawn_strategy=local # bypass sandbox to isolate it
bazel build //src:main --subcommands          # print each command run
```

Common sandbox causes: "No such file or directory" means a missing `data` or `srcs` entry; "Permission denied" means a write outside the sandbox, fixed by routing outputs through declared rule outputs.

## Failure and recovery

- `bazel build` fails on a missing load: add `load("@rules_cc//cc:defs.bzl", ...)` for the rule used; Bazel 9 has no native C++ rules.
- `bazel_dep` version not found: run `bazel mod graph` to see the error, then pick a version listed in the Bazel Central Registry.
- Sandbox error persists after adding inputs: reproduce with `--spawn_strategy=local`; if the local run passes, the sandbox is missing a declared input.
- Remote execution unreachable: drop `--remote_executor` and rebuild locally; report the endpoint failure rather than retrying blindly.
- Query returns empty: check the target pattern with `bazel query "//..."` first; an empty pattern means the package path is wrong.
- Migration from WORKSPACE: run the Bzlmod migration path (`bazel mod tidy` after declaring deps); do not recreate WORKSPACE, Bazel 9 ignores it.

## Output

Working BUILD files and `MODULE.bazel` declarations, a verified `bazel build`/`bazel test` invocation, and for debugging tasks the identified failing action with its fix. For toolchain work, a registered `toolchain` plus `platform` pair verified by `--platforms`.
