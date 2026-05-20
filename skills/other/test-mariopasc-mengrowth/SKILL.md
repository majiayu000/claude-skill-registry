---
name: test
description: Run pytest tests for the MenGrowth project
disable-model-invocation: true
---

Run the following tests and report results:

`~/.conda/envs/mengrowth/bin/python -m pytest $ARGUMENTS -v --tb=short`

If `$ARGUMENTS` is empty, run all tests in `tests/`.
