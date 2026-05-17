# Hex.pm trusted-publishers — upstream tracking and plugin stance

Hex.pm has an open issue tracking server-side provenance attestation
for package releases — analogous to npm's "provenance" or PyPI's
trusted-publishers feature.

- Upstream issue: <https://github.com/hexpm/hexpm/issues/1193>
- EEF Ægis roadmap: <https://security.erlef.org/aegis/roadmap/hex-vulnerability-handling.html>

When this lands, the plugin can defer registry-level provenance checks
to Hex.pm itself rather than reproducing them client-side.

## Plugin stance

Phase 1+2+3 work assumes **no registry-side attestation**. Every audit
runs locally against tarball contents because that's the only signal
available today. As soon as Hex.pm publishes a trusted-publishers API,
the plugin adopts a hybrid model:

1. **Prefer registry signal.** A package with a verified trusted
   publisher (e.g., release built and signed by a GitHub Actions
   workflow on `main`) gets a positive trust signal — comparable to
   `:safe_to_run` in the `hex_vet.exs` ledger.
2. **Keep tarball rules as the floor.** Tarball-level audit stays
   primary for packages without trusted-publisher attestation, and
   for defense-in-depth even on attested packages — registry-side
   verification doesn't catch a malicious build pipeline.
3. **Surface attestation gap as a finding.** Once a meaningful share
   of the ecosystem adopts trusted publishers, packages WITHOUT
   attestation become the outliers worth flagging.

## Placeholder rule

When the API ships, register a new rule slot:

```text
Rule 9 — Missing trusted-publisher attestation (INFO → WARN over time)
  Method: Hex API `/api/packages/:name/releases/:version` reads the
          `provenance` field (or equivalent).
  Severity: INFO until adoption > 20% of top-500; WARN after.
  False positives: dropped before adoption threshold; the absence
          isn't useful signal until most packages do attest.
```

The placeholder lives here, not in `heuristics.md`, until the upstream
API contract stabilizes. Adding it prematurely would lock the plugin
into a guessed schema.

## Decision log

The Phase 2 corpus review (2026-05-12) noted: **zero verified
maintainer-account compromises** in the Hex ecosystem. Trusted
publishers reduce the attack surface for the class of compromise the
plugin protects against — when registry-side attestation exists, the
client-side maintainer-change rule (rule 6) becomes a sanity check
rather than a primary defense.

This is good news for everyone except the plugin's value proposition.
We track upstream because: (a) if attestation ships before an
incident, Phase 3's hook value-prop narrows; (b) when it ships, the
plugin should adopt — not compete — to stay aligned with where the
ecosystem is heading.

## Action items (gated on upstream)

- [ ] Watch hexpm#1193 for API design merge
- [ ] When API merges, implement Rule 9 placeholder against staging
- [ ] When >20% of top-500 attest, promote Rule 9 to WARN default
- [ ] When >80% of top-500 attest, reconsider whether tarball rules
  are still worth the wall-time cost on attested packages

No action is required from plugin users today. This doc exists so
contributors and downstream-aware users know the plugin's roadmap
intersects upstream registry work.
