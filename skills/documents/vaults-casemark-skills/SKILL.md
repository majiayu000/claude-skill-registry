---
name: vaults
description: Manages case.dev encrypted document vaults for legal workflows. Creates vaults, uploads files and directories, lists and downloads objects, and runs semantic search across vault contents. Use when the user mentions "vault", "upload documents", "document storage", "download files", "vault search", or needs to manage case files and discovery documents.
---

# case.dev Vaults

Encrypted document storage with automatic OCR, chunking, and semantic search. Each vault is an isolated container for a case, project, or document collection.

Requires the `casedev` CLI. See `setup` skill for installation and auth.

## Create a Vault

```bash
casedev vault create --name "Smith v Jones Discovery" --description "Phase 1 documents" --json
```

Flags: `--name` (required), `--description`, `--disable-graph`, `--disable-indexing`.

## List Vaults

```bash
casedev vault list --json
casedev vault list --wide --json   # includes description column
```

## Upload Files

### Single file

```bash
casedev vault object upload ./contract.pdf --vault VAULT_ID --json
```

Flags: `--name` (override filename), `--content-type`, `--no-ingest` (skip indexing).

### Directory (recursive)

```bash
casedev vault upload ./discovery-docs/ --vault VAULT_ID --json
```

## List Objects

```bash
casedev vault object list --vault VAULT_ID --json
```

## Download Files

```bash
casedev vault download --vault VAULT_ID --object OBJECT_ID --out ./output/ --json
casedev vault download --vault VAULT_ID --out ./all-docs/ --json
casedev vault download --vault VAULT_ID --path "exhibits/" --out ./exhibits/ --json
```

## Semantic Search

```bash
casedev search vault "force majeure clause" --vault VAULT_ID --json
```

Search methods:
- `--method hybrid` (default) — combines vector + keyword search
- `--method fast` — keyword-only, faster
- `--limit` / `-l` — max results (default 10)
- `--object OBJECT_ID` — restrict to specific object(s), repeatable

If hybrid mode returns a server error, retry with `--method fast`.

## Common Workflow

```bash
# 1. Create vault
casedev vault create --name "Acme v Beta" --json

# 2. Upload documents
casedev vault upload ./case-files/ --vault VAULT_ID --json

# 3. Wait for ingestion
casedev vault object list --vault VAULT_ID --json

# 4. Search
casedev search vault "indemnification obligations" --vault VAULT_ID --json
```

## Focus Workflow

```bash
casedev focus set --vault VAULT_ID
casedev vault object list --json          # no --vault needed
casedev search vault "damages" --json
```

## Troubleshooting

**"Missing vault ID"**: Provide `--vault VAULT_ID` or set focus with `casedev focus set --vault`.

**Upload fails with HTTP 4xx**: Check file size (max 500MB per object), verify vault ID, confirm auth.

**Search returns no results**: Ensure objects have completed ingestion. Try `--method fast` if hybrid fails.
