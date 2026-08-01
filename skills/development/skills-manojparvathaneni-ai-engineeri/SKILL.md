---
name: skills-manojparvathaneni-ai-engineeri
description: '├── pyproject.toml    # Dependencies managed by uv'
---

# Project Development Skill

## Structure
```
project-XX-name/
├── README.md
├── pyproject.toml    # Dependencies managed by uv
├── .venv/            # Created by uv (gitignored)
├── src/
├── tests/
├── config/
└── data/
```

## Package Management (uv)

### Scripts with Inline Dependencies
```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "requests"]
# ///

# Your code here
```
Run: `uv run script.py`

### Projects with pyproject.toml
```toml
[project]
name = "project-name"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.109.0",
    "anthropic>=0.18.0",
]

[project.optional-dependencies]
dev = ["pytest", "black"]
```

Commands:
```bash
uv init                    # Create new project
uv add fastapi anthropic   # Add dependencies
uv add --dev pytest        # Add dev dependency
uv sync                    # Install all deps
uv run python main.py      # Run with deps
uv run pytest              # Run tests
```

## Cross-Platform
- Use pathlib for paths
- Use python-dotenv for secrets
- Test on WSL/Linux/Mac

## Common Patterns
- FastAPI for backends
- React for frontends
- anthropic/openai for LLM clients
