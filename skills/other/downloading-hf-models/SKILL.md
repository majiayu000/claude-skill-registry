---
name: downloading-hf-models
description: Get the correct command syntax for downloading models from HuggingFace. Use when downloading models, running "hf download", or pulling models from HuggingFace repos.
---

# HuggingFace Model Download

## Command Pattern

Always use `uv run` with the HuggingFace Hub package as an inline dependency:

```bash
uv run --with huggingface_hub hf download <repo> <file> --local-dir <path>
```

## Common Mistakes to Avoid

- **Wrong**: `pip install huggingface_hub && huggingface-cli download ...`
- **Wrong**: `uv run hf download ...` (missing `--with`)
- **Wrong**: `uv run --with "huggingface_hub[cli]" ...` (the `[cli]` extra doesn't exist, the CLI is included in the base package)

## Syntax Reference

### Download a specific file

```bash
uv run --with huggingface_hub hf download <org>/<repo> <filename> --local-dir <destination>
```

### Download multiple files

```bash
uv run --with huggingface_hub hf download <org>/<repo> <file1> <file2> --local-dir <destination>
```

### Download with glob pattern

```bash
uv run --with huggingface_hub hf download <org>/<repo> --include "*.gguf" --local-dir <destination>
```

**Warning**: Large GGUF models are often split into parts (e.g., `model.gguf.part-000`, `.part-001`, etc.). Use `--include "*.gguf*"` (note the trailing `*`) to match both single GGUFs and split parts. Use `--dry-run` first to check what files will be downloaded.

### Download entire repo

```bash
uv run --with huggingface_hub hf download <org>/<repo> --local-dir <destination>
```

## Notes

- `HF_TOKEN` environment variable is used automatically for gated models
- `--local-dir` places files directly in the target directory (no nested `.cache` structure)
- Downloads are resumable — re-running the same command skips already-downloaded files
- For GGUF models, download only the quant you need rather than the whole repo
