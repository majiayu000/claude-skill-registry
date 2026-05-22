---
name: model-checkpoint-evaluator
description: When the user needs to evaluate multiple model checkpoints across various benchmarks to identify the best performing model based on evaluation metrics like accuracy, F1-score, or custom scoring functions. This skill scans directories containing model checkpoints, runs benchmark evaluations using predefined scoring algorithms, calculates overall performance scores, and identifies the checkpoint with the highest evaluation metric. It handles complex evaluation workflows involving multiple benchmark categories and mathematical scoring formulas.
---
# Instructions

## Overview
This skill evaluates model checkpoints across multiple benchmark categories using predefined scoring algorithms, identifies the best-performing checkpoint based on overall evaluation accuracy, and prepares it for deployment (e.g., uploading to Hugging Face Hub with updated documentation).

## Workflow

### 1. Scan Workspace and Identify Checkpoints
- List directories in the workspace to locate checkpoint folders.
- Checkpoint folders are typically named with step numbers (e.g., `step_100`, `step_200`).
- Extract step numbers from folder names for evaluation.

### 2. Run Benchmark Evaluations
- Use the bundled `benchmark_calculator.py` script to compute scores for each checkpoint.
- The script implements 15 benchmark scoring functions derived from the original Cython module:
  - **Core Reasoning Tasks**: Math Reasoning, Logical Reasoning, Common Sense
  - **Language Understanding**: Reading Comprehension, Question Answering, Text Classification, Sentiment Analysis
  - **Generation Tasks**: Code Generation, Creative Writing, Dialogue Generation, Summarization
  - **Specialized Capabilities**: Translation, Knowledge Retrieval, Instruction Following, Safety Evaluation
- Each scoring function uses mathematical formulas (sigmoid, rational, exponential) based on step value.

### 3. Calculate Overall Performance
- For each checkpoint, compute the average of all benchmark scores as the `eval_accuracy`.
- Identify the checkpoint with the highest `eval_accuracy`.

### 4. Prepare Best Model for Deployment
- Update the model's `README.md` with benchmark scores (keep three decimal places).
- Ensure all necessary files are present: `config.json`, `pytorch_model.bin`, figures.
- If required, push the model to Hugging Face Hub:
  - Use the Hugging Face token from `hf_token.txt`.
  - Create/update repository with the model name specified by the user.
  - Upload the entire checkpoint folder.

## Key Decisions
- **Benchmark Scoring**: Use the formulas in `benchmark_calculator.py`; do not modify them.
- **README Update**: Only replace `{RESULT}` placeholders with scores; preserve all other content.
- **File Handling**: Copy necessary assets (e.g., figures) to the checkpoint folder before upload.
- **Error Handling**: If a checkpoint folder is missing required files, skip it and log a warning.

## Notes
- The skill assumes checkpoints are in a structured directory (e.g., `workspace/checkpoints/`).
- For Hugging Face upload, ensure `huggingface_hub` is installed and the token is valid.
- All benchmark scores are rounded to three decimal places in the final README.
