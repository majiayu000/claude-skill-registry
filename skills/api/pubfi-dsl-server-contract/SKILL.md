---
name: pubfi-dsl-server-contract
description: Use when defining or validating the server-side contract for PubFi DSL requests, including schema validation, aggregation mapping, limits, and response envelopes.
---

# PubFi DSL Server Contract

## Overview

This skill defines the server-side contract for executing PubFi DSL requests. The server only accepts structured DSL and maps requests to a fixed, audited OpenSearch query shape. The server does not accept SQL, OpenSearch DSL, or natural language compilation.

## When To Use

- You are implementing the DSL validation layer.
- You are defining or auditing the allowed query templates.
- You are designing the response envelope and error model.

## Core Rules

- Reject any request that includes SQL, OpenSearch DSL, or unknown fields.
- Validate against the schema before execution.
- Enforce hard limits for time window, top-k, fields, and aggregation sizes.
- Only execute allowed aggregation primitives (terms, date_histogram, cooccurrence).
- Do not compute business metrics server-side. Return documents and aggregation results only.

## Required Server Behaviors

- Provide a `schema` endpoint that lists allowed fields, aggregation kinds, and hard limits.
- Provide a `query` endpoint that accepts DSL and returns a deterministic response envelope.
- Log request metadata for audit and billing reconciliation.

## Error Model

The server returns errors using `ApiEnvelope` codes and English messages.

- `ERR_INVALID_PAYLOAD`: The request violates schema or limits.
- `ERR_INTERNAL`: The service failed unexpectedly.

Rate limiting and quota enforcement are out of scope for this contract draft and should be implemented at the gateway layer.

## References

- See `references/contract.md` for endpoint definitions, response envelopes, and template mappings.
