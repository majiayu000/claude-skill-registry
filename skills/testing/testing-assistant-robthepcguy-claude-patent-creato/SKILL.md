---
name: testing-assistant
description: Manages testing lifecycle including unit tests, integration tests, validation, and quality assurance.
---

# Testing Assistant Skill

Expert system for testing and validating the Claude Patent Creator.

**FOR CLAUDE:** Test scripts in scripts/ directory.
- Go directly to running appropriate test
- Run from project root
- Tests require active venv
- Only run diagnostics if tests fail

## When to Use

Running test suites, validating new features, testing after changes, debugging failures, creating tests, setting up CI/CD, performance testing, E2E validation, regression testing.

## Testing Pyramid

```
         /\
        /  \       E2E (Manual + Automated)
       /----\
      / API  \     Integration Tests
     /--------\
    /  Unit   \    Unit Tests
   /----------\
```

**Strategy:** More unit tests (fast, isolated), fewer integration (moderate), minimal E2E (slow).

## Test Suite Overview

```bash
scripts/
+-- test_install.py          # Complete installation validation
+-- test_gpu.py              # GPU detection and CUDA
+-- test_bigquery.py         # BigQuery connection
+-- test_analyzers.py        # Claims, spec, formalities
+-- test_embedding_speed.py  # Performance benchmarks
+-- test_checkpoint.py       # Index checkpoint system
```

**Quick Test:**
```bash
python scripts/test_install.py
```


## Manual Testing via Claude

Test MCP tools through Claude Code interface.

### Quick Test Examples

```
1. MPEP Search: "Search MPEP for claim definiteness requirements"
2. Patent Search: "Search for patents about neural networks filed in 2024"
3. Claims Review: "Review these claims: [paste test claims]"
4. Full Review: "/full-review" (with test application)
5. Diagrams: "Create a flowchart for this process: [describe]"
```

### Validation Checklist

```bash
[OK] MPEP search returns relevant results
[OK] BigQuery search finds patents
[OK] Claims analyzer identifies issues
[OK] Specification analyzer checks support
[OK] Formalities checker validates format
[OK] Diagrams generate successfully
[OK] Full review workflow completes
[OK] All MCP tools accessible
[OK] Error messages clear and helpful
[OK] Performance acceptable (<2s most ops)
```


## Creating New Tests

### Quick Start

```python
# Unit test template
def test_basic_functionality():
    from mcp_server.your_module import YourClass
    instance = YourClass()
    result = instance.method("test input")
    assert result is not None
    print("[OK] test_basic_functionality passed")
```

**Test Categories:**
1. Basic functionality
2. Edge cases
3. Performance
4. Error handling


## Performance Testing

### Quick Benchmark

```python
from mcp_server.mpep_search import MPEPIndex
import time

index = MPEPIndex()
index.search("test", top_k=5)  # Warm up

start = time.time()
result = index.search("claim definiteness", top_k=5)
duration = time.time() - start
print(f"Search took: {duration:.3f}s")
```

### Performance Thresholds

| Operation | Threshold | Notes |
|-----------|-----------|-------|
| MPEP search (first) | <3s | Model loading |
| MPEP search (subsequent) | <500ms | Cached models |
| BigQuery search | <2s | Network dependent |
| Claims analysis | <3s | 20 claims |
| Spec analysis | <10s | 10 pages |
| Diagram generation | <1s | SVG output |


## Troubleshooting Test Failures

| Problem | Solution |
|---------|----------|
| Import errors | Activate venv, `pip install -r requirements.txt` |
| GPU tests fail | Check `nvidia-smi`, reinstall PyTorch, or skip |
| BigQuery fails | Re-auth: `gcloud auth application-default login` |
| Index not found | Rebuild: `patent-creator rebuild-index` |
| Too slow | Check GPU usage, first run slower, check system load |


## Best Practices

1. Test after every change
2. Automated testing
3. Test pyramid (more unit, fewer E2E)
4. Fast tests (<5 min suite)
5. Isolated tests (no dependencies)
6. Clear assertions
7. Document tests
8. Version control tests
9. Regular execution (weekly)
10. Monitor performance

## Quick Reference

### Run All Tests
```bash
python scripts/test_install.py
python scripts/test_gpu.py
python scripts/test_bigquery.py
python scripts/test_analyzers.py
python scripts/test_embedding_speed.py
```

### Regression Test
```bash
python scripts/test_install.py || exit 1
python scripts/test_bigquery.py || exit 1
python scripts/test_analyzers.py || exit 1
echo "[OK] All regression tests passed!"
```

### Manual Checklist
```
□ Ask Claude to search MPEP
□ Ask Claude to search patents
□ Ask Claude to review claims
□ Run /full-review command
□ Generate a diagram
□ Verify all tools work
□ Check performance (<2s)
```
