---
name: ocaml-testing
description: "Testing strategies for OCaml libraries. Use when discussing tests, alcotest, eio mocks, test structure, test-driven development, or cram tests in OCaml projects."
license: ISC
---

# OCaml Testing

## Core Philosophy

1. **Unit Tests First**: Prioritize unit tests for individual modules.
2. **1:1 Test Coverage**: Every `lib/*.ml` should have `test/test_*.ml`.
3. **Isolated Tests**: Each test independent, no external state.
4. **Clear Names**: Describe what is tested, not how.

## Test Organization

```
project/
├── lib/
│   ├── user.ml
│   └── auth.ml
├── test/
│   ├── dune
│   ├── test.ml           # Main runner
│   ├── test_user.ml      # Tests for user.ml
│   └── test_auth.ml      # Tests for auth.ml
└── third_party/          # Fetched sources for reference
```

**Rules**:
- Test file `test_foo.ml` tests library module `foo.ml`
- Every test module exports `suite : string * unit Alcotest.test_case list`
- Main `test.ml` aggregates all suites

## Basic Test Structure

```ocaml
(* test/test_user.ml *)
let test_create () =
  let user = User.create ~name:"Alice" in
  Alcotest.(check string) "name" "Alice" (User.name user)

let test_validate_empty () =
  let result = User.create ~name:"" in
  Alcotest.(check bool) "fails" true (Result.is_error result)

let suite = ("user", [
  "create", `Quick, test_create;
  "validate_empty", `Quick, test_validate_empty;
])
```

```ocaml
(* test/test.ml *)
let () = Alcotest.run "MyProject" [
  Test_user.suite;
  Test_auth.suite;
]
```

## Test Naming

- **Suite names**: lowercase, single word (`"user"`, `"auth"`)
- **Case names**: lowercase with underscores (`"create"`, `"parse_error"`)

## Dune Configuration

```lisp
(test
 (name test)
 (libraries mylib alcotest))
```

For Eio-based libraries:
```lisp
(test
 (name test)
 (libraries mylib alcotest eio_main eio.mock))
```

## Testing with Eio Mocks

Prefer mocks for deterministic, fast tests.

```ocaml
let test_with_mock_clock () =
  Eio_mock.Backend.run @@ fun () ->
  let clock = Eio_mock.Clock.make () in
  Eio_mock.Clock.advance clock 1.0;
  Alcotest.(check bool) "advanced" true true

let test_with_mock_flow () =
  Eio_mock.Backend.run @@ fun () ->
  let flow = Eio_mock.Flow.make "test" in
  Eio_mock.Flow.on_read flow [
    `Return "data";
    `Raise End_of_file;
  ];
  (* test with flow *)
```

**Mock modules**: `Eio_mock.Backend`, `Eio_mock.Clock`, `Eio_mock.Flow`, `Eio_mock.Net`, `Eio_mock.Fs`

## Cram Tests (End-to-End)

For CLI/executable testing. Use directories ending in `.t/`.

```
test/
└── my_feature.t/
    ├── run.t           # Test script
    └── input.txt       # Real test files (not cat << EOF)
```

**Rules**:
- Create actual files in directory, don't embed with `cat > file << EOF`
- Test the compiled executable behaviour
- Use for integration/CLI tests, not unit tests

## Coverage Checklist

For each module:
- [ ] Test all public functions from `.mli`
- [ ] Test success cases
- [ ] Test error cases
- [ ] Test edge cases (empty, max values, invalid input)

## Running Tests

```bash
dune runtest              # Run all tests
dune runtest --verbose    # Verbose output
dune exec test/test.exe   # Run specific test
dune test --instrument-with bisect_ppx  # With coverage
```

## Best Practices

1. **Prefer mocks over real I/O** - Fast, deterministic
2. **Test edge cases** - Empty, max, invalid
3. **One assertion per test** when practical
4. **Clean up resources** - Even in tests
5. **Keep integration tests minimal** - Most should be unit tests
