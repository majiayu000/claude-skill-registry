---
name: ce-serializer-impl
description: >
  Implement ADR-031 serializer and persistence APIs with versioned primitives and
  compatible load behavior.
---

# CE Serializer Implementation

You are implementing calibrator serialization or explainer state persistence
per ADR-031. The contract is: versioned JSON-safe primitives + fail-fast on
schema incompatibility.

Load `references/serialization_templates.md` for full code templates.

---

## Key contracts

### Calibrator `to_primitive` / `from_primitive`

All built-in calibrators must implement this pair:
- `to_primitive()` returns a dict with `schema_version` as the first key
  and only JSON-safe values. The built-in calibrators (`VennAbers`,
  `IntervalRegressor`) use pickle + base64 encoding with sha256 checksum
  for complex internal state.
- `from_primitive(payload)` validates `schema_version`, `calibrator_type`,
  and payload checksum integrity. Raises `ConfigurationError` on any
  mismatch with a guidance message.

### Explainer `save_state` / `load_state`

- On-disk format: directory artifact with `manifest.json` plus referenced files.
- Manifest fields include `schema_version`, `created_at_utc`, `artifact_type`,
  and `files` (mapping `filename -> sha256`).
- `save_state` accepts a filesystem path, writes an artifact directory, returns `Path`.
- `load_state` validates manifest schema version and per-file sha256 checksums;
  raises `IncompatibleStateError` if unsupported or integrity check fails.

### Round-trip invariant (ADR-031 §4)

After a save/load round-trip, the restored calibrator must produce **identical**
outputs (`np.allclose(ref, restored, atol=1e-9)`).

---

## Additional compatibility expectations

- Wrapper object round-trips via `pickle.dump/load` and `joblib.dump/load`
  should remain functional.
- Explanation collection objects should remain pickleable.

## Out of Scope

- Third-party calibrator schema management - external packages own their schema versions.

## Evaluation Checklist

- [ ] `to_primitive()` returns a dict with `schema_version` as the first key.
- [ ] All values are JSON-safe (no numpy arrays, no non-serialisable objects).
- [ ] `from_primitive()` validates `schema_version`, `calibrator_type`, and checksum.
- [ ] `from_primitive()` raises `ConfigurationError` on any validation failure.
- [ ] Round-trip test verifies identical predictions (not just no-exception).
- [ ] `json.dumps(primitive)` test verifies JSON-safety.
- [ ] Checksum tamper test verifies `from_primitive()` rejects corrupted payloads.
- [ ] `save_state` / `load_state` manifest includes `schema_version`, `created_at_utc`, `artifact_type`, and `files`.
- [ ] `load_state` validates per-file sha256 checksums before deserialising.
- [ ] Unsupported state schema version raises `IncompatibleStateError`.
- [ ] Wrapper pickle and joblib round-trips are covered in integration tests.
