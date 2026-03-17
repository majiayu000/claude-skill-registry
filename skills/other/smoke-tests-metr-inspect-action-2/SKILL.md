---
name: smoke-tests
description: Run smoke tests on a deployed environment to ensure basic functionality.
---

E.g. to test staging:

```bash
unset HAWK_MODEL_ACCESS_TOKEN_ISSUER
AWS_PROFILE=staging scripts/dev/create-smoke-test-env.py env/smoke-staging --terraform-dir ../mp4-deploy/terraform_inspect
set -a && source env/smoke-staging && set +a && AWS_PROFILE=staging uv run pytest tests/smoke -m smoke --smoke -vv -n 10
```

Must run `hawk login` first if not logged in
