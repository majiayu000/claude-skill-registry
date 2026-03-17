---
name: ocaml-rfc-integration
description: Working with IETF RFCs in OCaml projects. Use when mentioning RFC numbers, implementing internet standards, adding specification documentation, or discussing protocol compliance.
license: ISC
---

# RFC Integration for OCaml Projects

## When to Use This Skill

Invoke this skill when:
- User mentions implementing an RFC
- Adding RFC citations to documentation
- Fetching RFC specifications
- Validating code against RFC requirements
- Discussing internet protocol standards

## RFC Fetching and Storage

### Fetching RFCs

Always fetch RFCs in **plain text format** from:
```
https://datatracker.ietf.org/doc/html/rfcXXXX.txt
```

**Important**: Use `.txt` extension, not `.html`.

### Storage Location

Save RFC files to `spec/` directory in project root:
```
spec/rfc6265.txt
spec/rfc3492.txt
```

Create `spec/` directory if it doesn't exist.

## OCamldoc RFC Citation Format

### Basic RFC Link

```ocaml
{{:https://datatracker.ietf.org/doc/html/rfcXXXX}RFC XXXX}
```

### Section-Specific Links

```ocaml
{{:https://datatracker.ietf.org/doc/html/rfcXXXX#section-N.M}RFC XXXX Section N.M}
```

### Common Section References

- `#section-N` - Main numbered section
- `#section-N.M` - Subsection
- `#appendix-X` - Appendix (A, B, C, etc.)

## Documentation Patterns

### Module-Level Documentation

```ocaml
(** RFC 3492 Punycode: A Bootstring encoding of Unicode for IDNA.

    This module implements the Punycode algorithm as specified in
    {{:https://datatracker.ietf.org/doc/html/rfc3492}RFC 3492}.

    {2 References}
    {ul
    {- {{:https://datatracker.ietf.org/doc/html/rfc3492}RFC 3492} - Punycode}
    {- {{:https://datatracker.ietf.org/doc/html/rfc5891}RFC 5891} - IDNA}} *)
```

### Function-Level Documentation

```ocaml
val adapt : delta:int -> numpoints:int -> firsttime:bool -> int
(** [adapt ~delta ~numpoints ~firsttime] computes the new bias value.

    Implements the bias adaptation algorithm from
    {{:https://datatracker.ietf.org/doc/html/rfc3492#section-6.1}RFC 3492 Section 6.1}. *)
```

### Type-Level Documentation

```ocaml
type error =
  | Overflow of position
      (** Arithmetic overflow. See
          {{:https://datatracker.ietf.org/doc/html/rfc3492#section-6.4}
          RFC 3492 Section 6.4}. *)
  | Invalid_digit of position * char
      (** Invalid Punycode digit. See
          {{:https://datatracker.ietf.org/doc/html/rfc3492#section-5}
          RFC 3492 Section 5}. *)
```

### Constants and Parameters

```ocaml
val base : int
(** The base value (36) for Punycode encoding.
    See {{:https://datatracker.ietf.org/doc/html/rfc3492#section-5}
    RFC 3492 Section 5}. *)
```

## Reading and Parsing RFCs

### RFC Structure

1. **Header**: RFC number, title, authors, date
2. **Table of Contents**: Section numbers and titles
3. **Abstract**: Brief summary
4. **Main Body**: Numbered sections
5. **Appendices**: Lettered sections
6. **References**: Citations to other documents

### Key Sections to Extract

- **Introduction** - Background and motivation
- **Terminology** - Key terms (MUST, SHOULD, MAY)
- **Algorithm** - Core specification
- **Security Considerations** - Security implications

## Validation Workflow

1. Read the RFC from `spec/` directory
2. Extract key requirements (MUST, SHOULD, MAY)
3. Read implementation code
4. Check each requirement is implemented
5. Verify error handling matches RFC
6. Report gaps or inconsistencies

## Best Practices

### DO

- Always fetch and save RFC text files to `spec/`
- Use section-specific links when possible
- Link error types to their RFC requirements
- Document RFC parameters and constants
- Keep citations consistent across related functions

### DON'T

- Link to HTML versions of RFCs
- Assume RFC sections without checking
- Omit section numbers in citations
- Duplicate RFC text verbatim (summarize instead)

## Handling RFC Updates

When an RFC obsoletes another:
```ocaml
(** Implements {{:https://datatracker.ietf.org/doc/html/rfc6265}RFC 6265}
    which obsoletes {{:https://datatracker.ietf.org/doc/html/rfc2965}RFC 2965}. *)
```

## Multiple RFC References

```ocaml
(** IDNA-compatible encoding combining
    {{:https://datatracker.ietf.org/doc/html/rfc5891}RFC 5891} (IDNA Protocol)
    with {{:https://datatracker.ietf.org/doc/html/rfc3492}RFC 3492} (Punycode). *)
```
