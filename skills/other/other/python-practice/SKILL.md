---
name: python-practice
description: Generate Jupyter notebook practice challenges for Python. Use when the user wants practice problems, coding exercises, study notebooks, or drill questions for pandas or algorithms.
allowed-tools: Read, Grep, Glob, Write, Bash, AskUserQuestion
---

# Python Tutor

Generate a Jupyter notebook filled with practice challenges and questions. Challenges cover **pandas** (data manipulation, cleaning, exploration, time series) and **algorithms** (vanilla Python data structures, sorting, searching, recursion).

Follow the rules in [RULES.md](RULES.md).

## Workflow

1. **Gather parameters** using AskUserQuestion. Ask the user:
   - **Category**: Which category to focus on, or generate a random mix from all categories. Present the subcategories listed below.
   - **Difficulty**: easy, medium, or hard.
   - **Number of questions**: How many challenges to include (default 10).
   - **Output directory**: Where to save the notebook. Default is `notebooks/practice`.
   - **Previous exercises folder** (optional): Path to a folder containing previous practice notebooks. If provided, scan these notebooks to avoid repeating exact questions. You may generate the same *type* of question but must vary the data, parameters, or scenario to ensure uniqueness.

2. **Check for previous exercises** (if folder provided):
   - Scan notebooks in the previous exercises folder for question prompts.
   - Extract the core challenge type from each (e.g., "filter DataFrame by condition", "implement binary search").
   - When generating new questions, avoid repeating the exact same prompt. You may reuse the same question *type* but must change the data, column names, values, or scenario to make it fresh.

3. **Generate varied question data** using the helper scripts (see [Scripts](#scripts) below). For every notebook:
   - Run `random_tickers.py` to pick a fresh set of tickers for the session.
   - Run `fetch_price_data.py` to get real market data for those tickers. Use the `--format code` or `--format returns` flag to get a Python snippet you can embed in the notebook setup cell.
   - Run `random_data.py` to generate random numbers, date ranges, or messy DataFrames as needed by the questions.
   - Vary the data in each question so notebooks are never identical.

4. **Build the notebook** using `generate_notebook.py`:
   - **Option A — from the question bank**: Use `--bank` to pull pre-written questions and randomize:
     ```bash
     python scripts/generate_notebook.py \
       --bank questions/bank.json \
       --category pandas --difficulty easy --count 5 \
       --output notebooks/practice
     ```
   - **Option B — custom questions**: Generate a JSON array of question objects and pipe to the script:
     ```bash
     python scripts/generate_notebook.py \
       --category pandas --difficulty medium \
       --output notebooks/practice < /tmp/questions.json
     ```
   - Each question object must have `prompt` (str) and `solution` (str). Optional fields:
     - `hint` (str, will be rendered in a collapsed `<details>` tag). Hints must be hidden by default.
     - `setup` (str, per-question code cell), `subcategory` (str).

5. **Customize the setup cell** — replace the template's sample data with the real market data fetched in step 3. Use the output of `fetch_price_data.py --format code` or `--format returns` as the setup cell content.

6. **Confirm** the notebook path to the user when finished.

## Notebook Structure

Each generated notebook must follow this structure:

1. **Title cell** (markdown): includes category, difficulty, date, and number of questions.
2. **Setup cell** (code): import statements and sample datasets. For pandas notebooks, embed real market data fetched with `fetch_price_data.py`.
3. **For each question**:
   - A **markdown cell** with the challenge prompt, numbered (e.g. "### Challenge 1"). Include:
     - A clear problem statement
     - Any sample data or expected output
     - When appropriate include a **hidden hint** wrapped in a `<details><summary>💡 Hint</summary>...</details>` tag (initially collapsed).
   - An **empty code cell** for the user to write their solution.
   - A **hidden solution cell** wrapped in a markdown `<details><summary>✅ Solution</summary>...</details>` tag so the user can reveal it.

## Scripts

All scripts live in [scripts/](scripts/) and are run from that directory.

### `generate_notebook.py`
Builds a `.ipynb` file from a category template + question data. Uses `nbformat`.

```bash
# From question bank:
python scripts/generate_notebook.py --bank questions/bank.json \
  --category pandas --subcategory series --difficulty easy --count 5 --output notebooks/practice

# From a JSON file of custom questions:
python scripts/generate_notebook.py --questions /tmp/my_questions.json \
  --category algorithms --difficulty hard --output notebooks/practice

# From stdin:
cat questions.json | python scripts/generate_notebook.py --category pandas --output notebooks/practice
```

### `random_tickers.py`
Pick random ticker symbols to use in questions. Avoids repeating the same tickers.

```bash
python scripts/random_tickers.py --count 4                  # 4 random tickers
python scripts/random_tickers.py --count 3 --sector tech    # from tech sector
python scripts/random_tickers.py --count 5 --diverse        # one per sector
python scripts/random_tickers.py --list-sectors              # show all sectors
```

**Use this every time** you generate a notebook to ensure fresh ticker sets.

### `fetch_price_data.py`
Fetch real stock price data from Yahoo Finance via `yfinance`. Embed the output in notebook setup cells so students work with real market data.

```bash
# Get a code snippet to embed in the notebook
python scripts/fetch_price_data.py --tickers AAPL MSFT TSLA --period 6mo --format code

# Get daily returns as a code snippet
python scripts/fetch_price_data.py --tickers AAPL MSFT --period 3mo --format returns

# Random tickers + real data
python scripts/fetch_price_data.py --random 4 --period 1y --format code

# Save as CSV
python scripts/fetch_price_data.py --tickers SPY QQQ --start 2023-01-01 --end 2024-01-01 --output prices.csv
```

### `random_data.py`
Generate random numbers, date ranges, names, and messy DataFrames for question variety.

```bash
python scripts/random_data.py --type integers --count 10 --min 1 --max 100
python scripts/random_data.py --type floats --count 5 --min -0.05 --max 0.05
python scripts/random_data.py --type date_range --start 2020-01-01 --periods 30 --freq B
python scripts/random_data.py --type names --count 8
python scripts/random_data.py --type messy_dataframe --rows 20
```

Use `--type messy_dataframe` to generate data-cleaning exercises with realistic problems (missing values, inconsistent casing, whitespace, bad types, duplicates).

## Templates

Category-specific notebook templates live in [templates/](templates/). Each template provides:
- A title cell with `{{difficulty}}`, `{{date}}`, `{{count}}`, `{{subcategories}}` placeholders
- A setup cell with appropriate imports and sample datasets

| Template | File | Description |
|----------|------|-------------|
| Pandas | `templates/pandas_template.ipynb` | Imports pandas, numpy, matplotlib, seaborn. Pre-built sample datasets (stock_returns, messy_data, sectors). |
| Algorithms | `templates/algorithms_template.ipynb` | Imports collections, heapq, math, typing. Includes a `check()` helper for testing solutions. |

## Question Bank

Pre-written questions are stored in [questions/bank.json](questions/bank.json). The bank is organized as:

```
{ category: { subcategory: { difficulty: [question, ...] } } }
```

Each question has: `prompt`, `solution`, and optionally `hint` and `setup`.

## Categories and Subcategories

### Pandas

Refer to [references/PANDAS_NOTE.md](references/PANDAS_NOTE.md) for the topic tree and [references/PANDAS_FOR_DATA_SCIENCE.md](references/PANDAS_FOR_DATA_SCIENCE.md) for functions and techniques. Use [examples/PANDAS_EXAMPLES.md](examples/PANDAS_EXAMPLES.md) for sample data patterns.

Subcategories:
- **Series**: creation, retrieval, modification, alignment, built-in methods
- **DataFrames**: retrieval (loc/iloc, slicing, boolean masks), modification, column operations
- **Data exploration**: apply/applymap, correlations, covariance, DataFrame-Series arithmetic
- **Missing data**: detection, dropping, filling, interpolation
- **Reindexing and sorting**: reindex, drop, sort_index, sort_values
- **Categorical data**: unique values, value_counts, isin, dummy variables
- **File I/O**: reading/writing CSV, Excel, pickle
- **Multi-indexing**: multi-index DataFrames and Series, stack/unstack, swaplevel
- **Time series**: timestamps, offsets, date ranges, resampling, shifting
- **GroupBy, pivot, merge**: groupby, pivot_table, merge/join, concat
- **Rolling and quantiles**: rolling windows, qcut, shift for returns
- **Plotting**: line, bar, scatter, histograms, heatmaps with seaborn

### Algorithms

Focused on vanilla Python (no external libraries).

Subcategories:
- **Data structures**: lists, dicts, sets, tuples, deques, heaps
- **Sorting**: bubble, merge, quick, insertion sort implementations
- **Searching**: linear search, binary search
- **Recursion**: factorial, fibonacci, tree traversal, divide and conquer
- **String manipulation**: reversal, palindromes, anagrams, pattern matching
- **Math and logic**: primes, GCD, modular arithmetic, bit manipulation

## Difficulty Levels

- **Easy**: Single-concept problems. Provide hints and sample data. Expect 1-5 lines of code per solution.
- **Medium**: Combine 2-3 concepts. Provide sample data but no hints. Expect 5-15 lines of code.
- **Hard**: Multi-step problems requiring chaining operations or designing algorithms. No hints. Expect 10-30+ lines of code.

## Additional Resources

- For pandas topic details, see [references/PANDAS_NOTE.md](references/PANDAS_NOTE.md)
- For pandas functions reference, see [references/PANDAS_FOR_DATA_SCIENCE.md](references/PANDAS_FOR_DATA_SCIENCE.md)
- For numpy context, see [references/NUMPY.md](references/NUMPY.md)
- For code examples and sample data, see [examples/PANDAS_EXAMPLES.md](examples/PANDAS_EXAMPLES.md)
