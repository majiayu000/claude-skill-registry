# Writing Extracted Implementations

Phase 3 produces `extracted/*.py` modules. This file governs **how much
of each module you implement** and how to prove what you wrote is
right. The bar depends on what evidence you have.

## The two regimes

### Regime 1 — No ground truth (default)

No `probe-context/` directory exists in your work dir, and you have no
web research tools. Emit **contract-documented stubs**: the function
signature, a docstring stating the input/output contract as precisely
as the skill text allows, and a `raise NotImplementedError(...)` body.
Do NOT write vendor API calls from memory — SDK and endpoint shapes
drift faster than any model's training data, and a plausible-but-wrong
implementation is worse than an honest stub because it fails at
runtime instead of at review.

### Regime 2 — Ground truth available (implement for real)

`probe-context/` exists (observed MCP traffic + inferred schemas from
an instrumented run of this exact skill), and/or you have WebSearch /
WebFetch. Now you are expected to write **working implementations**:

1. **Contract from observation.** The observed input payload keys are
   your function parameters; the observed result shape is your return
   contract. If the skill prose disagrees with the observed traffic,
   trust the traffic and note the discrepancy in the compilation report.
2. **Endpoint from current docs, never memory.** Before writing a
   vendor call, use WebSearch/WebFetch to confirm the current endpoint,
   auth scheme, request/response shape, and official SDK name. Cite the
   doc URL in the module docstring. If you cannot verify a shape, fall
   back to Regime 1 for that function and say why in the report.
3. **Credentials via environment variables only.** One variable per
   vendor, named `<VENDOR>_API_KEY` (or the vendor's own documented
   convention, e.g. `GOOGLE_APPLICATION_CREDENTIALS`). Read it at call
   time, and raise a clear `RuntimeError` naming the variable when it
   is missing. NEVER hardcode a credential, NEVER invent a
   plausible-looking value, NEVER default to a dummy that would send a
   request with fake auth.
4. **Minimal dependencies.** Prefer the vendor's official Python SDK
   when one exists and is current; otherwise plain `httpx`. Every
   third-party dependency you introduce must be listed in the module
   docstring so the adapter's requirements emission can pick it up.
5. **Honest error surfaces.** No silent fallbacks, no bare excepts, no
   returning empty results on failure. A 4xx/5xx should raise with the
   response body attached — errors are how the durable runtime knows
   to retry or park.

## Tests are part of the deliverable

When you implement for real (Regime 2), also write
`tests/test_extracted.py` in your work dir:

- **Golden-fixture tests from observed payloads.** Every parse /
  transform / filter function gets called with a real observed payload
  (copy it from `probe-context/observed-tools.json` into the test as a
  fixture literal) and asserted against the real result. These are the
  highest-value tests you can write: they prove the implementation
  handles what production actually sends.
- **Network functions get a transport-stubbed test.** Monkeypatch the
  HTTP layer (or inject a fake client) and assert the function builds
  the documented request and parses the documented response — using
  the observed payloads as the canned response body. **No test may
  touch the network**, require credentials, or be nondeterministic:
  they must pass with plain `pytest` in an offline environment.
- **Constants get pinned.** Every constant lifted in Phase 3 (batch
  sizes, thresholds, day windows) gets one assertion, so a silent edit
  fails a test instead of shipping.

Structure the file so `pytest tests/` passes from the work dir root —
imports as `from extracted.<module> import <fn>` with a conftest or
sys.path line if needed. If a test would need something you can't
provide deterministically, don't write a flaky approximation; note the
gap in the compilation report instead.

## What NOT to do, in any regime

- Do not write to `signatures/` from this file's rules — judge modules
  are governed by `llm-judge-extraction.md`.
- Do not call MCP at runtime from extracted code. The `mcp:` binding on
  the node (see `ir-schema.md`) is how the MCP backend wires itself;
  your `extracted/` implementation is the *direct-API* backend the
  user selects with `--backend api`. Keep both true to the same
  contract.
- Do not invent data the observation doesn't show. An inferred schema
  from one sample marks fields it saw; absence of a field is not
  license to add speculative ones.
- Do not soften a failing contract to make a test pass. The observed
  payload is the spec; if your implementation can't reproduce it,
  the implementation is wrong.

## BDR worked example

`enrich_contact_batch` under Regime 2, with an observed
`zoominfo_enrich_contacts` call in probe-context:

- Function takes `contacts: list[dict]` (the observed input key),
  chunks by the lifted `BATCH_SIZE = 10`, calls the documented
  ZoomInfo enrich endpoint with `ZOOMINFO_API_KEY` from the env, and
  returns the observed response shape (`{"contacts": [...]}`)
  normalized per the inferred schema.
- `tests/test_extracted.py` asserts: chunking math at the boundary
  (10, 11, 20 contacts), request shape against a stubbed transport
  using the observed input, response parsing against the observed
  result payload verbatim, and `BATCH_SIZE == 10`.
- Module docstring cites the ZoomInfo enrich doc URL fetched during
  implementation and lists `httpx` as the dependency.
