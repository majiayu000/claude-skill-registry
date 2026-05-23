---
name: training-metrics-csv-exporter
description: Extracts specific training metrics from experiment logs at regular intervals and saves them to a CSV file for analysis. Processes time-series training data (like entropy_loss, clip_ratio, response_length_mean) at specified step intervals, formats data into a structured table, and creates a CSV file.
---
# Instructions

## Primary Use Case
When a user requests to extract and save specific training metrics from experiment logs at regular step intervals (e.g., "every 100 steps") into a CSV file.

## Core Workflow

### 1. Identify Target Experiment
- **Input**: User provides a target project/experiment (often via URL like `wandb.ai/entity/project`).
- **Action**: Query the project to list available runs/experiments.
- **Decision Point**: Determine which experiment to analyze based on user criteria (e.g., "shortest answers" → lowest `response_length/mean`).

### 2. Extract Metrics History
- **Input**: Selected experiment run identifier.
- **Action**: Query the run's history for the specific metrics requested by the user (e.g., `actor/entropy_loss`, `response_length/clip_ratio`, `response_length/mean`).
- **Note**: Use sampling queries to efficiently retrieve data at all steps.

### 3. Sample at Specified Intervals
- **Input**: Full history data and user-specified interval (e.g., "from step 0, at intervals of every 100 steps").
- **Action**: Filter the history to extract data points only at the requested steps (e.g., 0, 100, 200, ... up to the final step).
- **Output**: A structured list/dictionary of values for each target step.

### 4. Create CSV File
- **Input**: Sampled data with columns: step, metric1, metric2, ...
- **Action**: Format data as CSV with appropriate headers.
- **Output**: Write CSV file to the workspace with a descriptive filename (e.g., `shortest_length_experiment.csv`).

### 5. Provide Summary
- **Action**: Present a concise analysis summary to the user, highlighting:
  - Which experiment was selected and why.
  - Key observations from the extracted data (trends, min/max values).
  - Location and contents of the generated CSV file.

## Key Tools & Patterns
- **W&B Queries**: Use `wandb-query_wandb_tool` for:
  - Project/run listing (`ProjectInfo`, `GetRuns`).
  - History keys inspection (`RunHistoryKeys`).
  - Sampled history data (`RunHistorySampled` with appropriate `specs`).
- **File Operations**: Use `filesystem-write_file` to create the CSV, and optionally `filesystem-read_file` to verify.
- **Large Output Handling**: When tool outputs are truncated, use `local-view_overlong_tooloutput` and related navigation/search tools to extract needed data.

## Common User Phrases That Trigger This Skill
- "Record [metrics] into [filename].csv"
- "Save experiment data to a CSV file"
- "Extract data at intervals of every X steps"
- "Get the metrics from step 0, every 100 steps"
- "Analyze which experiment has the shortest/longest [metric]"

## Error Handling & Edge Cases
- **Missing Metrics**: If a requested metric key doesn't exist in the run's history, inform the user and adjust the CSV columns accordingly.
- **Insufficient Steps**: If the run has fewer steps than the requested interval, sample all available steps and note the limitation.
- **Large Datasets**: For runs with many steps, use sampled history queries with appropriate `max_items` to avoid timeouts.
