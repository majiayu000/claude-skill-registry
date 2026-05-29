---
name: ce-payload-governance
description: >
  Validate explanation payload schemas, metadata and provenance fields, and ADR-005
  and ADR-028 governance invariants.
---

# CE Payload and Governance

You are managing the persistent payload schema for calibrated explanations. All
serialization logic must follow ADR-005 (Payload Schema v1) and provide
sufficient observability for governance (ADR-028).

## Schema v1 Payload Contract (Mandatory)

All serialized explanations exported as JSON must follow the v1.0.0 schema.

| Key | Type | Description |
|---|---|---|
| `schema_version` | `str` | Must be `"1.0.0"` for the v1.x series. |
| `task` | `str` | `"classification"` or `"regression"`. |
| `index` | `int` | The index of the instance in the input set. |
| `explanation_type` | `str` | `"factual"`, `"alternative"`, or `"fast"`. |
| `prediction` | `dict` | Prediction dict with keys `predict`, `low`, `high`. |
| `rules` | `list` | List of rule dicts with `feature`, `rule`, `rule_weight`, etc. |
| `provenance` | `dict` | (Optional) Information about the library/generator. |
| `metadata` | `dict` | (Optional) Technical/audit metadata (tenant_id, etc.). |

```json
{
  "schema_version": "1.0.0",
  "task": "classification",
  "prediction": {"predict": 0.8, "low": 0.7, "high": 0.9},
  "provenance": {"library_version": "1.0.0"},
  ...
}
```

## Generation (Serialization)

To generate the payload from a domain object, use the `to_json()` method or
stream it for large datasets.

```python
# 1. Export a full collection (CalibratedExplanations)
# Returns a dict containing all explanations and collection-level metadata
payload = explanations.to_json()

# 2. Export a single instance (FactualExplanation / AlternativeExplanation)
# Returns a dict following the schema v1 payload contract
instance_payload = explanations[0].to_json()

# 3. Stream large datasets (JSONL)
# For environments where memory matters, uses a generator
for chunk in explanations.to_json_stream(format="jsonl"):
    print(chunk)
```

## Governance Metadata (ADR-005/028)

To support auditability, use `provenance` and `metadata` as the official
extension surface. Never add top-level keys outside the schema.

### Recommended Fields
- `provenance.library_version`: The runtime version used to produce the payload.
- `provenance.calibration_version`: A deterministic identifier for the calibration
  state (e.g., checkpoint_id).
- `metadata.audit`: Audit metadata (correlation/request ID).
- `metadata.tenant_id`: Multi-tenant identifier.

## Reading (Deserialization)

To read a payload back into a domain-model object, use the `from_json` class
method or the serialization helper.

```python
import json
from calibrated_explanations import CalibratedExplanations
from calibrated_explanations.serialization import from_json

# 1. Load a full collection from a JSON string/file
with open("explanations.json", "r") as f:
    data = json.load(f)
    collection = CalibratedExplanations.from_json(data)

# 2. Load a single explanation instance from a dict
explanation = from_json(data["explanations"][0])
```

## Prediction Invariant (ADR-021 §4)

Internal code must enforce that predictive intervals are mathematically
coherent before serialization:

```python
# Invariant: low <= predict <= high
def _validate_invariants(payload: dict[str, Any]) -> None:
    pred = payload["prediction"]
    assert pred["low"] <= pred["predict"] <= pred["high"]
```

---

## Contributor Checklist

1. [ ] **JSON-safe** — only `dict`, `list`, `str`, `int`, `float`, `bool`, `None`.
   Convert all `numpy` types (`list()` or `.item()`).
2. [ ] **Stable versioning** — do not increment `schema_version` unless
   introducing a breaking structural change (ADR-005).
3. [ ] **Validation** — always run `validate_payload(payload)` if the library
   provides it.
4. [ ] **No data leakage** — do not include sensitive training data in
   non-rule fields. Rule conditions are the only public feature representation.
5. [ ] **Metadata propagation** — ensure `tenant_id` and `request_id` are
   propagated transitionally from the logging context into the payload
   `metadata` block.

## Validation Example

Use the internal validator to verify exported payloads in tests:

```python
from calibrated_explanations.serialization import to_json
from calibrated_explanations.schema import validate_payload

def test_should_export_valid_v1_payload(explanation):
    json_data = to_json(explanation)
    # Raises ValidationError on failure
    validate_payload(json_data)
    assert json_data["schema_version"] == "1.0.0"
```
