---
name: vlm-ocr-evaluation
description: "Compare OCR systems before a bulk run: candidate set, stratified ground truth, CER/WER, normalization, per-language and per-stratum accuracy."
argument-hint: "[describe your corpus, the candidate OCR systems, and the languages/scripts to evaluate]"
---

# VLM-OCR Evaluation: Comparing OCR Systems Before You Commit

## Instructions

Before running any OCR model across a whole corpus, run a controlled comparison on a small, human-transcribed sample and let the measured error rates pick the model. This skill is the **selection gate** that precedes the `vlm-ocr-pipeline` skill: use this to choose a model and document why, then use `vlm-ocr-pipeline` to run the chosen model at scale and `post-ocr-cleanup` to clean its output. For the hardest pages, where no single model is reliable, the multi-model voting logic in `model-council-voting` can be applied to OCR transcriptions as well.

### 1. Run a Comparison Before You Commit

- Treat model choice as an empirical question, not a default — test, do not guess. A model that tops a general vision-language leaderboard, or that read one language well, can still fail on your script, era, or page layout. The only trustworthy signal is its error rate on pages like yours.
- The comparison is cheap insurance. Evaluating a 50–100 page sample once prevents discovering, after a 50,000-page bulk run, that the chosen model silently dropped every table or collapsed on degraded scans.
- Scope the comparison to the decision. The user's `ocr_pipeline/comparison/` setup runs nine systems on 64 pages spanning two languages and seven decades before committing to a bulk pipeline — enough to rank the candidates on the strata that matter, not a full corpus.
- The output is a go/no-go gate: keep the model whose accuracy clears your threshold on the strata you care about, or conclude that no single model does and split the corpus by script or era (§6).

### 2. Assemble the Candidate Set

- Include three kinds of system: several **open-weight VLMs**, one or two **proprietary APIs**, and a **traditional OCR baseline** (Tesseract). The gei comparison's `MODELS` registry in `run_comparison.py` holds six open-weight VLMs (Qwen3.5-35B, Qwen3-VL-32B, Qwen3.5-9B, Gemma, MiniCPM-V, DeepSeek-OCR) plus Tesseract, with two proprietary APIs (GPT-4.1, Claude) run by separate scripts — nine systems total.
- Pick the VLM candidates from **OCR benchmarks (e.g., OCRBench)**, not general multimodal leaderboards. General vision-language ability does not predict transcription fidelity on dense historical print; the `vlm-ocr-pipeline` skill covers benchmark-grounded model selection in detail.
- Always keep a **traditional baseline**. Even when it loses, Tesseract anchors what "hard" means for your corpus and shows where a VLM actually earns its extra cost and latency.
- Record an exact registry entry per system — name, HuggingFace id or dated API identifier, quantization, and loader — as the gei registry does (`name`/`hf_id`/`type`/`loader` per model). Family-name-only reporting ("we used Qwen and Gemma") is not reproducible.

### 3. Build a Stratified Ground-Truth Set

- Human-transcribe a **stratified** sample, not a convenience sample. Stratify on the dimensions that actually drive OCR difficulty: language/script, era (a decade bracket), and content type — running body text, multi-column tables, illustrated or captioned pages, degraded or water-damaged print, and front matter / title pages. The gei manifest tags each page with `language`, `year`, `decade`, `subject`, and `content_type` and samples across all of them.
- Size: roughly **50–100 pages** is a workable default for a handful of candidate systems (a house default that balances transcription effort against per-stratum cell sizes, not a cited figure). More strata require more pages so that each cell holds enough pages to mean something.
- Store ground truth as **one UTF-8 `.txt` per page**, keyed by a stable page id (`ground_truth/<page_id>.txt` in `compute_accuracy.py`). Transcribe faithfully — preserve the characters actually on the page (hanja alongside hangul, diacritics) — and decide up front how to render non-text regions (tables, figures) so the reference and the OCR output are scored on the same basis.
- Transcribe **before** looking at any model output, so the reference is not anchored to a model's guesses. Two independent transcribers on a subset, with disagreements reconciled, guard against a single transcriber's systematic errors (the inter-coder logic in the `text-classification` skill applies here too).

### 4. Character and Word Error Rate

- CER and WER are **edit-distance** metrics. CER = Levenshtein(reference, hypothesis) ÷ length(reference); WER is the same at the word level (a word-level dynamic-programming edit distance ÷ reference word count). `compute_accuracy.py` implements both — a character Levenshtein distance for CER and a word-level DP for WER (Levenshtein 1966).
- **Declare normalization before scoring; it changes the numbers.** The gei `normalize_text` applies Unicode **NFC**, strips markdown artifacts (headers, bold/italic, links — VLMs routinely emit markdown), and collapses whitespace, but is deliberately **case-sensitive** (no lowercasing) to preserve OCR fidelity. State each choice (NFC vs NFKC, case sensitivity, punctuation and markdown handling) and apply it identically to every system. Comparing a markdown-emitting VLM against a plain-text baseline without stripping markup unfairly penalizes the VLM.
- **Report both CER and WER, and report the distribution, not a single mean.** Give mean *and* median with the page count (`n`) per cell. The median resists the blank-page and repetition-loop outliers that wreck a mean, while the mean exposes how bad the tail gets.
- **Interpretation bands** (house defaults, consistent with the `vlm-ocr-pipeline` skill): CER below ~5% is excellent, below ~10% is usable with cleanup, and above that the text needs heavy correction or a different model. These are planning guides, not cited cutoffs — set the operative threshold from what your downstream analysis tolerates.
- **Score every stratum, not just the overall mean.** The gei evaluation aggregates CER/WER by model, by language × model, by decade bracket × model, and by content type × model — because a model can win overall and still fail on tables, on one script, or on the oldest decade.

### 5. Run the Comparison Efficiently

- **Load and unload models sequentially to fit one GPU.** The gei runner imports torch lazily and releases each model (a `gc` pass) before loading the next, so several large VLMs are scored on a single card without holding them all in memory at once. State the exact quantization per model (GPTQ-Int4, NF4, BF16) — it affects both fit and accuracy.
- **Serve via vLLM or Ollama** for batched throughput where the model supports it (`run_qwen35_vllm.py` runs Qwen3.5 through a vLLM OpenAI-compatible server); run proprietary APIs through their own rate-limited scripts.
- **Measure speed (seconds per page) alongside accuracy, but do not compare a traditional baseline's speed to a VLM's as if equal.** Tesseract is fast because it does far less, and it fails on non-Latin script. Report speed as context for cost, never as a quality signal.
- **Make the run resumable and idempotent:** write one output file per page per model and skip pages already done, so a crash partway through the comparison does not restart everything.

### 6. Interpret: There Is No Single Best Model

- **Expect no universal winner.** The lesson of the gei comparison is fit-to-script-and-corpus: on Latin-script Polish most models cluster within a couple of percent CER, while on Korean the field splits by roughly 25% even among the best. When that happens, pick per script or per era rather than forcing one model.
- **Skill does not transfer across scripts.** A model that reads Polish beautifully can collapse on Korean hanja–hangul. Never generalize a single-language result to a script the model was not measured on.
- **The "OCR specialist" is not guaranteed to win.** In the gei run a document-only OCR model produced the most blank pages and repetition loops, and general-purpose VLMs beat it. Judge on measured CER for *your* pages, not on a system's category label.
- **Open can rival proprietary and also reproduce.** The best open-weight models matched the proprietary APIs while remaining pinnable and re-runnable; the proprietary APIs are fast and capable but change underneath you between versions (the reproducibility argument the `vlm-ocr-pipeline` and `model-council-voting` skills also make). Weigh accuracy against reproducibility, not accuracy alone.
- **Decide and document:** the chosen model(s), the threshold they cleared, the strata where they win and lose, and any split (e.g., model A for Polish, model B for Korean).

### 7. Reproducibility and Reporting

- **Publish the model registry** — exact ids, quantization, loaders or dated API identifiers, decoding settings, and seeds — and the ground-truth set (or a precise description of how it was built and transcribed).
- **Report the full results table:** CER and WER, mean and median, `n`, broken down by model and by stratum (language, era, content type), with the normalization recipe stated alongside.
- **Report speed per system** for cost context, carrying the traditional-baseline caveat.
- **Report per-model failure modes** — blank pages, repetition loops, garbled or hallucinated script. These are decision-relevant and invisible in an averaged CER.
- For the bulk run that follows, compose with `vlm-ocr-pipeline` (production OCR with the chosen model) and `post-ocr-cleanup` (cleaning its output); for the methods-section disclosure of the comparison, compose with `methods-reporting`.

## Quality Checks

- [ ] Comparison run on a human-transcribed sample **before** any bulk OCR; model choice treated as empirical, not as a default
- [ ] Candidate set spans open-weight VLMs + at least one proprietary API + a traditional baseline (Tesseract); VLM candidates chosen from OCR benchmarks, not general leaderboards
- [ ] Ground truth **stratified** on script/language, era, and content type (body, tables, illustrations, degraded, front matter)
- [ ] ~50–100 pages (house default) with enough pages per stratum cell to be informative; one UTF-8 `.txt` per page id
- [ ] Ground truth transcribed faithfully (scripts and diacritics preserved) and **before** viewing any model output
- [ ] Normalization recipe declared before scoring (NFC, case sensitivity, markdown/whitespace handling) and applied identically to every system
- [ ] CER **and** WER computed as edit-distance ratios (Levenshtein 1966); mean **and** median reported with `n`
- [ ] Accuracy reported **per stratum** (model × language, × era, × content type), not just an overall mean
- [ ] Interpretation thresholds stated as house defaults tied to downstream tolerance, not as cited cutoffs
- [ ] Models loaded/unloaded sequentially (or served) to fit hardware, with quantization recorded; run resumable, one file per page per model
- [ ] Speed reported as cost context with the traditional-baseline caveat (fast because it does less)
- [ ] Per-model failure modes (blank pages, repetition loops, garbled script) reported alongside CER
- [ ] No single-best model assumed: fit-to-script documented and any per-script/era model split stated
- [ ] Model registry, ground-truth set, normalization recipe, and seeds archived for reproducibility (compose with `vlm-ocr-pipeline`, `post-ocr-cleanup`, `methods-reporting`)
