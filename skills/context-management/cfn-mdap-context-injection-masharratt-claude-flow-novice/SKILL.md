---
name: cfn-mdap-context-injection
description: Inject MDAP codebase files for troubleshooting (coordinator, implementers, validators, Docker, orchestration)
version: 1.0.0
tags: context-injection, debugging, mdap
status: production

# What it does
Outputs portions of CFN MDAP codebase grouped by functional area for debugging. Provides immediate context without reading entire codebase.

# When to use
1. Docker mode failures → --docker flag
2. CLI mode issues → --cli flag  
3. Orchestration deadlocks → --cfn-loop flag
4. Full MDAP workflow → --all flag

# When NOT to use
1. Need few files → Use Read directly
2. Runtime logs → Use docker logs
3. Documentation → Check docs/ first
4. Token budget critical → Start with --coordinator

# How to use
Basic: bash inject.sh --docker
Advanced: bash inject.sh --docker --cfn-loop (combined contexts)
Full: bash inject.sh --all --codesearch --tests (~260K tokens)

# Parameters
--all, --coordinator, --mdap, --cli, --docker, --cfn-loop, --config, --decomposers, --validators, --index, --codesearch, --tests, --file <path>

# Expected output
Concatenated file contents with === FILE: path === delimiters

# Real-world example
Docker specialist debugging "infinite wait in Wave 2" runs --docker --cfn-loop to get configs + orchestration in one injection.