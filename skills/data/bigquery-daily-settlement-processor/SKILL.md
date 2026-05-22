---
name: bigquery-daily-settlement-processor
description: When the user needs to perform end-of-day data settlement processing for gaming or analytics platforms using Google BigQuery, this skill handles the complete workflow. It processes daily score data from streaming tables to 1) Generate ranked leaderboards by aggregating player scores and creating date-stamped tables with player rankings, and 2) Update historical player statistics by inserting daily aggregated metrics into master tracking tables. Key triggers include 'end-of-day settlement', 'daily leaderboard generation', 'player statistics update', 'BigQuery data processing', 'daily score aggregation', and 'historical stats maintenance'.
---
# Instructions

## Goal
Process end-of-day settlement for a gaming platform by:
1.  **Generating a Daily Leaderboard:** Create a new table named `leaderboard_YYYYMMDD` containing the top 100 players ranked by their total daily score.
2.  **Updating Historical Statistics:** Insert aggregated daily metrics for all players into the master `player_historical_stats` table.

## Prerequisites
- **Access:** Ensure the AI agent has the necessary permissions to run queries and create/update tables in the target Google BigQuery project and dataset.
- **Context:** The user request must specify the target date for processing (e.g., "today", "2025-11-26"). If not specified, you must determine the current date.

## Execution Steps

### 1. Initialization & Context Gathering
- **Identify Dataset:** First, list available datasets to confirm the target dataset (e.g., `game_analytics`) exists.
- **Inspect Source Table:** Run a sample query on the source streaming table (e.g., `daily_scores_stream`) to understand its schema. **Crucially, always qualify the table name with the dataset (e.g., `dataset.table`)**.
- **Determine Target Date:** Query the source table to find the latest data date or use the provided date. Confirm this is the date you intend to process.

### 2. Schema Verification
- **Check Historical Stats Table:** Inspect the `player_historical_stats` table to understand its full column structure. This ensures your INSERT query matches the expected schema.

### 3. Core Processing (Execute Both Queries)
Run the following two BigQuery operations. Use the confirmed dataset name and target date (formatted as `YYYY-MM-DD`).

**Task 1: Create Daily Leaderboard**
