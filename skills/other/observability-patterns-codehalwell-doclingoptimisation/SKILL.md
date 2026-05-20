---
name: observability-patterns
description: >
  Use this skill when implementing logging, monitoring, timing, or diagnostics. Triggers on:
  logging setup, performance profiling, timing, stderr output, or mentions of "logging",
  "monitoring", "timing", "profiling", "observability", or "diagnostics".
---

# Observability Patterns — DoclingOptimisation

## Current Logging
- Python `logging` module with custom format (`%(message)s`)
- All logs go to stderr (stdout reserved for markdown output)
- Timing helper `_step()` logs elapsed time since process start
- Pipeline profiling enabled: `settings.debug.profile_pipeline_timings = True`

## Logging Standards
- Use `logging.getLogger("docling-processor")` for the main logger
- Include elapsed time in all step messages
- Log CPU detection results, accelerator config, batch sizes
- Log input file metadata (name, size)
- Log conversion timing (convert duration, export duration, total)

## For Azure Deployment
- Container App Job logs go to Azure Log Analytics
- Consider structured JSON logging for machine-parseable output
- Track: conversion time, file size, thread count, model used
- Set up alerts for: job failures, timeouts, excessive memory usage

## Health Monitoring
- Container App Jobs don't need health check endpoints
- Monitor job execution status via Azure Container Apps API
- Track job duration trends to detect performance regressions
