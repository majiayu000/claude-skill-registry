---
name: troubleshooting-assistant
description: Diagnoses and resolves MCP server registration failures, GPU detection, BigQuery authentication, index build failures, import errors, search quality issues, and performance problems.
---

# Troubleshooting Assistant Skill

Expert diagnostic system for identifying and resolving Claude Patent Creator issues.

## When to Use

System not working, error messages, slow performance, MCP server not loading, search returns no results/errors, GPU not detected, BigQuery auth fails, index build fails, tests failing, unexpected behavior.

## Troubleshooting Methodology

```
Problem Reported
  |
[1] Gather Information (errors, recent changes, system state)
  |
[2] Reproduce Issue (minimal test case, consistent?)
  |
[3] Isolate Component (which part failing? dependencies?)
  |
[4] Diagnose Root Cause (check logs, test components, verify config)
  |
[5] Apply Fix (targeted solution, verify works)
  |
[6] Prevent Recurrence (document, add monitoring, update checks)
```

## Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| MCP server not loading | `claude mcp list` -> Re-register if missing |
| GPU not detected | Reinstall PyTorch with CUDA |
| BigQuery auth fails | `gcloud auth application-default login` |
| Index not found | `patent-creator rebuild-index` |
| Import errors | Activate venv: `venv\Scripts\activate` |
| Slow searches | Check GPU usage, reduce top_k, disable HyDE |
| Irrelevant results | Rephrase query with MPEP terminology |

## Detailed Issue Guides

### MCP Server Issues

**Problems:** Server not loading, tools don't work/return errors

- 5-step diagnostic workflow
- Path verification and correction
- Dependency troubleshooting
- Server restart procedures

### GPU & BigQuery Issues

**Problems:** GPU not detected, slow performance, BigQuery auth fails, query timeouts

- CUDA detection and PyTorch reinstallation
- Performance diagnostics and optimization
- BigQuery authentication and permissions
- Timeout configuration

### Index, Dependencies & Configuration

**Problems:** Index not found, build fails, ModuleNotFoundError, import errors, env vars not loading, irrelevant search results

- Index rebuild procedures
- OOM (Out of Memory) solutions
- Virtual environment activation
- Pydantic validation errors
- Configuration troubleshooting
- Search quality tuning

## Diagnostic Tools

### Health Check Suite

```bash
# Full system health
patent-creator health

# Individual components
python scripts/test_gpu.py
python scripts/test_bigquery.py
python scripts/test_analyzers.py
python scripts/test_install.py
```

### Component Isolation

```python
# Test MPEP search
python -c "from mcp_server.mpep_search import MPEPIndex; \
           index = MPEPIndex(); \
           print('OK' if index.search('test', top_k=1) else 'FAILED')"

# Test BigQuery
python -c "from mcp_server.bigquery_search import BigQueryPatentSearch; \
           search = BigQueryPatentSearch(); \
           print('OK' if search.search_patents('neural network', limit=1) else 'FAILED')"

# Test analyzers
python -c "from mcp_server.claims_analyzer import ClaimsAnalyzer; \
           analyzer = ClaimsAnalyzer(); \
           print('OK' if analyzer.analyze('1. A test claim.') else 'FAILED')"
```

- Log analysis (debug mode)
- MCP communication debugging
- Performance profiling
- Memory profiling
- Issue escalation procedures

## Best Practices for Prevention

1. Regular health checks (weekly `patent-creator health`)
2. Monitor logs for warnings/errors
3. Keep dependencies updated (test before deploying)
4. Backup before changes (especially index rebuilds)
5. Document modifications
6. Test after changes (run test suite)
7. Version control (use git)
8. Environment consistency (same Python/CUDA versions)

## Quick Reference

### Most Common Errors

| Error | Category | Solution |
|-------|----------|----------|
| "Tool not found" | MCP | `claude mcp list` |
| "ModuleNotFoundError" | Dependencies | Activate venv, reinstall |
| "CUDA not available" | GPU | Reinstall PyTorch with CUDA |
| "Permission denied" (BigQuery) | Auth | `gcloud auth application-default login` |
| "Index not found" | Index | `patent-creator rebuild-index` |
| "Out of memory" | Index Build | Reduce batch size |
| "Validation error" | Input | Check Pydantic model parameters |

### Diagnostic Commands

```bash
# System health
patent-creator health

# Test components
python scripts/test_gpu.py
python scripts/test_bigquery.py
python scripts/test_install.py

# Check registration
claude mcp list

# Check paths
patent-creator verify-config

# Enable debug logging
export PATENT_LOG_LEVEL=DEBUG
```
