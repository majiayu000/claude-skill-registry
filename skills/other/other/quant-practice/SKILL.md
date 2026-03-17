---
name: quant-practice
description: Generate quant practice notebooks from example questions.
allowed-tools: Read, Grep, Glob, Write, Bash, AskUserQuestion
---

# Quant Practice Skill

Generate a Jupyter notebook of quant practice questions using example questions as templates. The user specifies the number of questions and topics. You generate novel questions (different tickers/values/date ranges) and provide solutions, then append them to the notebook.

## Inputs to Collect
- `count`: number of questions
- `topics`: comma-separated list (e.g. `returns,portfolio,signals`). Empty means mixed.

## Workflow
1. **Create a blank notebook** with a header cell:
   - Run:
     - `python .claude/skills/quant-practice/scripts/generate_notebook.py --topics "<topics>" --count <count>`
   - The script prints the notebook path. Capture it.
2. **Select example questions** from the index:
   - Run:
     - `python .claude/skills/quant-practice/scripts/select_questions.py --topics "<topics>" --count <count>`
   - This prints a JSON array of example question file paths.
3. **Generate novel questions**:
   - For each example question:
     - Read the markdown file.
     - Write a *new* question inspired by the example. Change tickers, numbers, or date ranges so it is materially different.
     - Write a complete solution in Python.
4. **Append each question** to the notebook:
   - Run:
     - `python .claude/skills/quant-practice/scripts/add_question_to_notebook.py --notebook <path> --question-text "<question>" --solution-text "<solution>"`
   - This appends:
     - A markdown question cell
     - An empty code cell for the user’s solution
     - A hidden solution cell

## Utility
- List available topics:
  - `python .claude/skills/quant-practice/scripts/get_topics.py`
  - Add `--only-active` to show only topics from active questions.

## Notes
- `questions/index.json` controls topic labels and which examples are active.
- If there aren’t enough active questions for a topic, either switch to mixed topics or ask the user to add more examples.
- Use simple, self-contained Python solutions (numpy/pandas/yfinance as appropriate).
