---
name: lcp-protocol-spec
description: Edit LCP protocol docs under docs/protocol/ in BOLT-style (TLVs, message formats, state flow).
metadata:
  short-description: Work on the LCP wire protocol spec
---

You are editing the Lightning Compute Protocol (LCP) specification and related protocol docs.

## Scope

- Primary spec: `docs/protocol/protocol.md` (and `docs/protocol/protocol-ja.md` when applicable)
- Related implementation: `go-lcpd/`

## Non-negotiables

- No modification to BOLTs: do not propose or require changes to upstream Lightning BOLT behavior. LCP is an application-layer protocol.
- Leverage, do not reinvent: reuse Lightning primitives for authentication, encryption, routing, and payment binding when possible.
- BOLT-quality documentation: aim for BOLT-level rigor, formatting, and readability.
- TLV streams only: define new message fields as TLVs for extensibility; avoid fixed-position fields unless the existing spec already does so.

## Leveraging BOLT features

### Transport

- Onion messages: for non-payment data transport, prefer onion messages over a custom TCP transport.
- Custom messages: for direct peer-to-peer communication, use high-range custom message types (>= 32768) and follow BOLT #1 parity rules.

### Data structure

- Extension areas: if attaching to existing messages (`init`, HTLC-related messages, etc.), use spec-defined extension TLVs.

### Privacy

- Blinded paths: if the protocol carries identifiers or route information, use route blinding / blinded paths to protect endpoint privacy.

## Specification strictness

Keep message and TLV definitions parseable and consistent. Use a BOLT-style definition shape like:

```text
1. type: <TypeNumber> (`<message_name>`)
2. data:
   * [`<type>`:`<field_name>`]
   * [`<length>`*`<type>`:`<array_name>`]
```

## Workflow

1. Identify the exact section you are changing (message definition, TLV table, state machine, examples).
3. Update the English spec first (`docs/protocol/protocol.md`). If the Japanese page is meant to mirror it, update `docs/protocol/protocol-ja.md` accordingly (it may be a summary).
4. Keep terminology consistent with identifiers used in `go-lcpd/` (when they exist).
5. If you introduce new fields:
   - Define them as TLVs with explicit type numbers and clear semantics.
   - Specify validation rules (required/optional, size limits, encoding, error handling).
6. Add/adjust examples to match the new behavior.

## Validation

- For prose/spec changes: re-read for consistency and BOLT-style formatting.
- If the change implies implementation changes, ensure `go-lcpd/` is updated in the same PR and validated with:
  - `cd go-lcpd && make test`
  - `cd go-lcpd && make lint`
