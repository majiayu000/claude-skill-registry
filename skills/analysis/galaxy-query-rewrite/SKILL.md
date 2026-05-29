# Galaxy Query Rewrite + Review (Repo Skill)

Use this skill when you want an agent to **review all benchmark queries** and **rewrite** any that are:
- tool-leaking (e.g., “perform `tool_x`”)
- templated / repetitive (especially repeated under the **same ground-truth tool**)
- dataset-leaking (filenames/accessions/URLs)
- inconsistent with the gold tool’s real purpose

This skill assumes the benchmark source of truth is:

- `data/benchmark/v1_items.jsonl`

## What to produce

1. A clean, updated `data/benchmark/v1_items.jsonl` (in-place).
2. A refreshed `data/benchmark/v1_items_readable.md` for human review.

## Hard rules (rewrite must satisfy)

1. **English only** for the query string.
2. Must ask for a **Galaxy tool recommendation**.
3. Must **not** mention tutorial/GTN.
4. Must **not** include dataset identifiers (SRR/ENA IDs, file extensions, URLs, etc.).
5. Must **not** mention tool IDs, tool names, or backticked “function/tool” strings.
6. Must be **close to real user queries**:
   - Write from a **Galaxy user** perspective (what you have + what you want), not a tool developer/maintainer perspective.
   - Include a short, plausible context (data type + goal + expected output).
   - Avoid “benchmarky” language (e.g., “perform X”, “for this task”) with no detail.
   - Avoid sounding like the tool help page; write as a user describing what they need.
7. For the **same tool (base id)**, queries must not be repeated or near-duplicates.

## Science-first vs tool-first queries (rewrite guidance)

When rewriting, preserve the *starting point* style unless the item is too vague:

- **Science-first (principle/goal first):** user starts from a scientific question (“identify cell types”, “find differentially expressed genes”, “infer variants”). Rewrite by adding the minimal missing “data type + expected output” while keeping it question-driven.
- **Tool-first (operation/workflow first):** user starts from a concrete step (“QC paired-end FASTQ”, “trim adapters”, “map reads”). Rewrite by making the step goal and output explicit (report/metrics/output files) without drifting into parameter/config instructions.

### Balance target (soft)

Across a batch, it’s good to keep **science-first** and **tool-first** reasonably mixed, but do **not** force an exact split (no “make it 75/75 just to match a quota”). Prefer to **preserve** each item’s existing `metadata.query_type`, and only change the label when a rewrite would otherwise make the wording inconsistent with the label.

## Review workflow (agent checklist)

1. Run the checker:
   - `ruby -EUTF-8 skills/galaxy-query-generation/scripts/check_v1_items.rb data/benchmark/v1_items.jsonl`
2. Read the batch **line-by-line** (no skipping):
   - Even if a query passes the checker, rewrite it if it’s still “benchmarky”, too generic, or near-duplicate.
   - Use scripts only to *surface* candidates; do not rely on scripts as the only filter.
3. Scan for anti-patterns in v1:
   - Tool leakage: backticks, “perform `...`”, “run `...`”.
   - Copy/paste templates (identical/similar sentences).
   - Dataset leakage (file extensions, accessions, URLs).
4. Enforce **within-tool diversity**:
   - Group items by `tools[0]` base id (strip toolshed version).
   - If any group contains duplicated or near-duplicated query text, rewrite them to be clearly different.
5. Ground-truth integrity + expansion checks:
   - If `tools[]` has multiple entries, ensure it is intentional:
     - `metadata.ground_truth_alternatives` should be `true`, and a short `metadata.ground_truth_alternatives_note` should explain why multiple tools are acceptable.
   - Ensure `metadata.tool_focus` matches one of the `tools[]` entries (and reflects the main intended ground truth).
   - If `tools[0]` is a placeholder/non-stable ID or not runnable on the target server snapshot, consider a **manual ground-truth expansion**:
     - Add an acceptable Toolshed GUID alternative to `tools[]` and set `metadata.ground_truth_alternatives=true`.
     - Do not expand unless you can justify that the alternative is genuinely equivalent for the user intent.
5. Rewrite strategy:
   - Keep the **user intent** the same, but change perspective/constraints.
   - Add a small realistic constraint when helpful (runtime, reproducibility, “probabilities not labels”, “avoid data leakage”, “save metrics”, etc.).
   - Avoid parameter/config questions.
6. Regenerate readable markdown:
   - `python3 -m scripts.benchmark.export_readable --input data/benchmark/v1_items.jsonl --output data/benchmark/v1_items_readable.md`

## 10 example rewrites (patterns to imitate)

These are examples of **good** queries (no tool leakage, specific intent, and not templated).

1)
- Query: I'm working with a labeled image dataset (handwritten digits) for multi-class classification. My labels are a single column of class IDs, but the model expects one-hot targets. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/sklearn_to_categorical/sklearn_to_categorical/1.0.11.0`

2)
- Query: I'm working with a labeled image dataset (handwritten digits) for multi-class classification. I want to specify the neural network architecture (layers/activations/input shape) in a config file. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/keras_model_config/keras_model_config/1.0.11.0`

3)
- Query: I'm working with a labeled image dataset (handwritten digits) for multi-class classification. I already have a saved architecture/config and want to instantiate the actual model object. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/keras_model_builder/keras_model_builder/1.0.11.0`

4)
- Query: I'm working with a labeled image dataset (handwritten digits) for multi-class classification. I want to train a neural network and evaluate it (e.g., accuracy/loss on validation data). Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/keras_train_and_eval/keras_train_and_eval/1.0.11.0`

5)
- Query: I'm working with a labeled image dataset (handwritten digits) for multi-class classification. I’ve trained a model and now want predictions for a new dataset (labels or probabilities). Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/model_prediction/model_prediction/1.0.11.0`

6)
- Query: I'm working with a high-dimensional biomarker feature table (e.g., RNA-seq or DNA methylation) to predict chronological age (regression). I want to do cross-validated hyperparameter tuning (grid/random search) and pick the best settings. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/sklearn_searchcv/sklearn_searchcv/1.0.11.0`

7)
- Query: I'm working with a high-dimensional biomarker feature table (e.g., RNA-seq or DNA methylation) to predict chronological age (regression). I want to train a tree-based ensemble (random forest / boosting) and evaluate it. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/sklearn_ensemble/sklearn_ensemble/1.0.11.0`

8)
- Query: I have a chemical dataset where you want to classify samples from molecular descriptors (QSAR-style). I need to compare hyperparameter combinations with CV and select the best-performing model. Also, I care about picking a scoring metric that matches my goal. What Galaxy tool should I run for this step?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/sklearn_searchcv/sklearn_searchcv/1.0.11.0`

9)
- Query: I'm working with a numeric feature matrix where you want to discover groups (unsupervised clustering). I want to cluster samples based on numeric features and get cluster assignments. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/bgruening/sklearn_numeric_clustering/sklearn_numeric_clustering/1.0.11.0`

10)
- Query: I'm working with a multi-omics dataset to predict breast cancer subtypes and interpret learned features. I want to try multiple models automatically on tabular data and see which performs best. Which tool in Galaxy can do this?
- Tool: `toolshed.g2.bx.psu.edu/repos/goeckslab/tabular_learner/tabular_learner/0.1.4`
