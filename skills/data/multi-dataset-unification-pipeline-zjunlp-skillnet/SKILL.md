---
name: multi-dataset-unification-pipeline
description: When the user requests to find, analyze, and merge multiple datasets from Hugging Face or similar repositories into a unified format. This skill handles the complete pipeline searching for datasets, examining their structure, parsing format specifications, converting diverse dataset formats (ToolACE, Glaive, XLAM, etc.) into a standardized schema, and merging them into a single output file. Key triggers include requests involving 'dataset unification', 'format conversion', 'merge datasets', 'Hugging Face datasets', 'tool-calling datasets', 'JSONL output', or when users provide a format specification document like 'unified_format.md'.
---
# Instructions

## 1. Understand the Request
- Identify the target datasets (names, IDs, or search queries).
- Locate and read any provided format specification (e.g., `unified_format.md`).
- Clarify the scope: number of entries per dataset, output file name/location.

## 2. Search and Validate Datasets
- Use `huggingface-dataset_search` to find each dataset.
- Use `huggingface-hub_repo_details` to get metadata and confirm availability.
- Note the dataset size and structure.

## 3. Analyze Dataset Structures
- Load a sample from each dataset using `datasets.load_dataset`.
- Examine the column names and a few sample entries.
- Identify the native format (e.g., ToolACE uses `system`/`conversations`, Glaive uses `conversations`/`tools`, XLAM uses `query`/`answers`/`tools`).

## 4. Convert to Unified Format
- **Always** refer to the provided `unified_format.md` (or equivalent) for the target schema.
- **Key Rules**:
    - `conversation_id`: Format as `{source_short_name}_{index}` (e.g., `toolace_0`).
    - `messages`: List of messages with `role` (`user`/`assistant`/`tool`), `content`, and optionally `tool_calls` or `tool_call_id`.
    - `tool_calls`: For assistant messages, include `id` (format `tool_call_{n}`), `name`, `arguments`.
    - `tools`: List of normalized tool definitions.
    - Remove system messages if they only contain tool instructions.
    - If assistant only made tool calls, set `content` to `null`.
    - Do not add tool return results or assistant replies not in the original data.
- Use the bundled `scripts/convert_and_merge.py` for reliable, deterministic conversion of ToolACE, Glaive, and XLAM formats.
- For new dataset formats, write a custom converter following the patterns in the script.

## 5. Merge and Output
- Limit entries per dataset as requested (default: first 500).
- Merge all converted entries into a single list.
- Write to a JSONL file in the workspace (default: `unified_tool_call.jsonl`).
- Verify the output: count entries, check file size, validate format against the specification.

## 6. Finalize
- Provide a summary: datasets found, entries converted, output location.
- Optionally, show a sample entry from each source for validation.
- Confirm the task is complete.
