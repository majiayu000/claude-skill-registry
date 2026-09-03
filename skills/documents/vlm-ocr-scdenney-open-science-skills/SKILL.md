---
name: vlm-ocr
description: OCR a scanned or image-only corpus with vision-language models, in three phases — evaluate compares candidate OCR systems against stratified human ground truth and picks one on measured CER/WER; run builds the production pipeline (model selection, image handling, prompts, architecture, batching, accuracy evaluation, reproducibility); clean corrects the raw OCR text with LLM and rule-based passes, quality diagnostics, multilingual handling, and span-level provenance. Use when the question is which OCR or VLM to run on a corpus or how accurate one is on your own pages, when scanned documents have to be transcribed at scale, or when raw OCR output needs correction, QA, or a provenance log. Not for born-digital documents with a text layer — those go to doc-to-markdown.
argument-hint: "[evaluate|run|clean] [describe your corpus, languages, candidate or chosen models, and compute environment]"
---

# VLM-OCR: Scanned Corpora from Page Images to Research-Usable Text

## Instructions

This skill covers the whole path from a corpus of page images to text an analysis can consume: choosing an OCR system by measurement (`evaluate`), running the chosen model across the corpus (`run`), and correcting and documenting its output (`clean`).

**Use this skill only for scanned or image-only documents.** Born-digital PDFs, Word files, and anything carrying an embedded text layer belong to `doc-to-markdown`, which extracts the text directly and needs no model at all. A PDF yielding under ~300 extractable characters per page is a scan; that is the trigger for this skill.

### Phase selection

Infer the phase from what the user brings:

| What you are given | Phase |
|---|---|
| A corpus with no model chosen yet, or the question of which OCR system to use or how accurate one is on these pages | `evaluate` |
| A chosen model and a corpus to transcribe at scale | `run` |
| Raw OCR output needing correction, quality diagnostics, or a provenance record | `clean` |

The argument `evaluate`, `run`, or `clean` forces a phase. Otherwise infer it, and state which phase you are working in before you start.

### Phase order and handoff

`evaluate` → `run` → `clean`. Each phase produces exactly what the next one consumes:

- `evaluate` emits a model registry, a declared normalization recipe, per-stratum CER/WER, and a documented model choice — possibly one model per script or era. `run` takes the chosen model and the registry.
- `run` emits per-page structured records: transcription, uncertain spans, layout markers, page-type flags, and the full pipeline provenance block. `clean` uses these to route pages to a correction strategy and to anchor its own edit log.
- `clean` emits corrected text plus a span-level provenance log anchored to the raw OCR revision, with the raw text preserved alongside every corrected variant.

Moving backwards is legitimate and expected: a `run` whose diagnostics fail returns to `evaluate` for a different model, and a `clean` pass that finds systematic transcription failure returns to `run` at higher DPI or without quantization.

### Provenance rules that hold in every phase

- **Pin and date every model.** Exact identifier plus revision or commit hash for open-weight models; the dated identifier for hosted APIs. Family-name reporting ("we used Qwen and Gemma") is not reproducible, and neither is an undated proprietary model name.
- **Record every parameter in machine-readable form** alongside the output, not in prose notes: quantization, DPI, prompt text or prompt id, generation parameters (temperature, max tokens, sampling strategy, seed), software versions, and hardware.
- **Never overwrite the previous stage's text.** Raw OCR survives every correction pass; each stage writes a new artifact and leaves its input intact, so a downstream researcher can choose a different normalization.
- **Declare normalization once and reuse it.** The recipe declared in `evaluate` §4 is the same one `run` §6 reports against and `clean` §4 scores with. Two different recipes across phases make the numbers incomparable.
- **Prefer locally-hosted open-weight models pinned to a revision** when publication-grade reproducibility is required; hosted APIs change underneath you (Barrie, Palmer & Spirling 2025).
- For the methods-section disclosure of any phase, compose with `methods-reporting`. For the hardest pages, where no single model is reliable, the multi-model voting logic in `model-council-voting` applies to OCR transcriptions as well.

---

## Phase `evaluate`: Comparing OCR Systems Before You Commit

Before running any OCR model across a whole corpus, run a controlled comparison on a small, human-transcribed sample and let the measured error rates pick the model. This is the **selection gate**: choose a model and document why, then move to `run`.

### 1. Run a Comparison Before You Commit

- Treat model choice as an empirical question, not a default — test, do not guess. A model that tops a general vision-language leaderboard, or that read one language well, can still fail on your script, era, or page layout. The only trustworthy signal is its error rate on pages like yours.
- The comparison is cheap insurance. Evaluating a 50–100 page sample once prevents discovering, after a 50,000-page bulk run, that the chosen model silently dropped every table or collapsed on degraded scans.
- Scope the comparison to the decision. The concrete figures throughout this phase come from one 9-system, 64-page comparison across two languages and seven decades, run by the author before committing to a bulk pipeline — enough to rank candidates on the strata that matter, not a full corpus. Treat them as one comparison on one corpus, not as general findings.
- The output is a go/no-go gate: keep the model whose accuracy clears your threshold on the strata you care about, or conclude that no single model does and split the corpus by script or era (§6).

### 2. Assemble the Candidate Set

- Include three kinds of system: several **open-weight VLMs**, one or two **proprietary APIs**, and a **traditional OCR baseline** (Tesseract). The reference comparison held six open-weight VLMs spanning two size tiers and three families, plus Tesseract, plus two proprietary APIs run through their own scripts — nine systems total. Choose current models by the criteria in the `run` phase §1 rather than copying a fixed list; what transfers is the shape of the candidate set, not its membership.
- Pick the VLM candidates from **OCR benchmarks (e.g., OCRBench)**, not general multimodal leaderboards. General vision-language ability does not predict transcription fidelity on dense historical print; the `run` phase §1 covers benchmark-grounded model selection in detail.
- Always keep a **traditional baseline**. Even when it loses, Tesseract anchors what "hard" means for your corpus and shows where a VLM actually earns its extra cost and latency.
- Record an exact registry entry per system — `name` / `hf_id` (or dated API identifier) / `type` / `quantization` / `loader`, one row per model — so the run is reconstructible from the registry alone.

### 3. Build a Stratified Ground-Truth Set

- Human-transcribe a **stratified** sample, not a convenience sample. Stratify on the dimensions that actually drive OCR difficulty: language/script, era (a decade bracket), and content type — running body text, multi-column tables, illustrated or captioned pages, degraded or water-damaged print, and front matter / title pages. Build a page manifest tagging each page with `language`, `year`, `decade`, `subject`, and `content_type`, and sample across all of them.
- Size: roughly **50–100 pages** is a workable default for a handful of candidate systems (a house default that balances transcription effort against per-stratum cell sizes, not a cited figure). More strata require more pages so that each cell holds enough pages to mean something.
- Store ground truth as **one UTF-8 `.txt` per page**, keyed by a stable page id (`ground_truth/<page_id>.txt`), so scoring joins on the id rather than on file order. Transcribe faithfully — preserve the characters actually on the page (hanja alongside hangul, diacritics) — and decide up front how to render non-text regions (tables, figures) so the reference and the OCR output are scored on the same basis.
- Transcribe **before** looking at any model output, so the reference is not anchored to a model's guesses. Two independent transcribers on a subset, with disagreements reconciled, guard against a single transcriber's systematic errors (the inter-coder logic in the `text-classification` skill applies here too).

### 4. Character and Word Error Rate

- CER and WER are **edit-distance** metrics. CER = Levenshtein(reference, hypothesis) ÷ length(reference); WER is the same at the word level (a word-level dynamic-programming edit distance ÷ reference word count). Implement both directly — a character Levenshtein distance for CER and a word-level DP for WER (Levenshtein 1966) — rather than trusting an unaudited helper, and report which implementation was used.
- **Declare normalization before scoring; it changes the numbers.** A workable default: apply Unicode **NFC**, strip markdown artifacts (headers, bold/italic, links — VLMs routinely emit markdown), collapse whitespace, and stay deliberately **case-sensitive** (no lowercasing) to preserve OCR fidelity. State each choice (NFC vs NFKC, case sensitivity, punctuation and markdown handling) and apply it identically to every system. Comparing a markdown-emitting VLM against a plain-text baseline without stripping markup unfairly penalizes the VLM.
- **Report both CER and WER, and report the distribution, not a single mean.** Give mean *and* median with the page count (`n`) per cell. The median resists the blank-page and repetition-loop outliers that wreck a mean, while the mean exposes how bad the tail gets.
- **Interpretation bands** (house defaults, consistent with the `run` phase §6): CER below ~5% is excellent, below ~10% is usable with cleanup, and above that the text needs heavy correction or a different model. These are planning guides, not cited cutoffs — set the operative threshold from what your downstream analysis tolerates.
- **Score every stratum, not just the overall mean.** Aggregate CER/WER by model, by language × model, by decade bracket × model, and by content type × model — because a model can win overall and still fail on tables, on one script, or on the oldest decade.

### 5. Run the Comparison Efficiently

- **Load and unload models sequentially to fit one GPU.** Import torch lazily and release each model (a `gc` pass) before loading the next, so several large VLMs are scored on a single card without holding them all in memory at once. State the exact quantization per model (GPTQ-Int4, NF4, BF16) — it affects both fit and accuracy.
- **Serve via vLLM or Ollama** for batched throughput where the model supports it — a vLLM OpenAI-compatible server in front of the largest open-weight candidate is the usual arrangement; run proprietary APIs through their own rate-limited scripts.
- **Measure speed (seconds per page) alongside accuracy, but do not compare a traditional baseline's speed to a VLM's as if equal.** Tesseract is fast because it does far less, and it fails on non-Latin script. Report speed as context for cost, never as a quality signal.
- **Make the run resumable and idempotent:** write one output file per page per model and skip pages already done, so a crash partway through the comparison does not restart everything.

### 6. Interpret: There Is No Single Best Model

- **Expect no universal winner.** The lesson of the reference comparison is fit-to-script-and-corpus: on the Latin-script language most models clustered within a couple of percent CER, while on the Korean pages the field split by roughly 25% even among the best. One comparison on one corpus, but the pattern is the reason to run your own. When that happens, pick per script or per era rather than forcing one model.
- **Skill does not transfer across scripts.** A model that reads Polish beautifully can collapse on Korean hanja–hangul. Never generalize a single-language result to a script the model was not measured on.
- **The "OCR specialist" is not guaranteed to win.** In that same comparison a document-only OCR model produced the most blank pages and repetition loops, and general-purpose VLMs beat it. Judge on measured CER for *your* pages, not on a system's category label.
- **Open can rival proprietary and also reproduce.** The best open-weight models matched the proprietary APIs while remaining pinnable and re-runnable; the proprietary APIs are fast and capable but change underneath you between versions (the reproducibility argument the `run` phase §7 and the `model-council-voting` skill also make). Weigh accuracy against reproducibility, not accuracy alone.
- **Decide and document:** the chosen model(s), the threshold they cleared, the strata where they win and lose, and any split (e.g., model A for Polish, model B for Korean).

### 7. Reproducibility and Reporting

- **Publish the model registry** — exact ids, quantization, loaders or dated API identifiers, decoding settings, and seeds — and the ground-truth set (or a precise description of how it was built and transcribed).
- **Report the full results table:** CER and WER, mean and median, `n`, broken down by model and by stratum (language, era, content type), with the normalization recipe stated alongside.
- **Report speed per system** for cost context, carrying the traditional-baseline caveat.
- **Report per-model failure modes** — blank pages, repetition loops, garbled or hallucinated script. These are decision-relevant and invisible in an averaged CER.
- Carry the chosen model, the registry, and the normalization recipe forward into the `run` phase; for the methods-section disclosure of the comparison, compose with `methods-reporting`.

---

## Phase `run`: The Production VLM-OCR Pipeline

For a worked language-specific transcription prompt (pre-reform Cyrillic) and a per-page JSON output schema with `uncertain_spans`, `layout_markers`, and `flags`, see `reference/prompt-and-schema.md`.

### 1. Model Selection

- **Run your own comparison before selecting — this is a gate, not a preference.** Benchmarks and published studies narrow the candidate set; they do not decide it. Score the shortlist on a human-transcribed sample of your own pages and let the measured error rates pick the model. The `evaluate` phase holds the comparison protocol, the stratified ground-truth design, and the go/no-go gate. Everything below narrows the shortlist that comparison scores.
- **Start from OCR benchmarks, not general VLM leaderboards.** OCRBench (Liu et al. 2024) tests across 29 document OCR dimensions; OCRBench v2 (Fu et al. 2025) extends to multilingual scripts and multi-page documents. General vision-language benchmarks (MMMU, VQAv2) do not predict OCR accuracy.
- **Verify language support explicitly.** Confirm the target language appears in the model's training set with per-language accuracy data. Qwen3-VL (Bai et al. 2025) enumerates 39 languages with OCR benchmarks; models that claim "multilingual support" without language-specific evidence may fail on non-Latin scripts.
- **Compare across models for your script family.** E-ARMOR (2025) compares five VLMs and two traditional OCR systems across 54 languages on a hand-annotated dataset. Use this or similar comparative studies rather than relying on a single model's self-reported scores.
- **Assess quantization tradeoffs before committing.** Low-bit quantization (e.g., W3A16, W4A8) enables single-GPU deployment but can degrade VLM accuracy non-uniformly across modalities. Li et al. (2025) show that **language tokens are an order of magnitude more sensitive to quantization than vision tokens**; treating them equally during calibration over-weights the insensitive modality and hurts performance. Always compare quantized output against a full-precision baseline on a pilot sample before committing to a bulk run.
- **Test the instruct variant against reasoning variants.** For OCR tasks, instruction-following models typically outperform chain-of-thought variants, which may add latency and fabricate content rather than improving transcription fidelity.

### 2. Image Handling and Preprocessing

- **Separate OCR input resolution from archival preservation.** For archival capture, FADGI (2016) prescribes 300-400 ppi across books, journals, and manuscripts (with 400+ ppi for 4-star compliance), and Metamorfoze (van Dormolen 2012) applies similar European standards. For VLM OCR input, resolution requirements are lower but not well-pinned by the KB: calibrate on a pilot, do not drop below ~150-200 ppi, and raise DPI for small type, faded ink, or pre-industrial typography.
- **Prefer native image extraction over rasterization.** Scanned PDFs store each page as an embedded image at the original scan resolution. Extract these byte-for-byte using PDF library methods rather than re-rasterizing, which downsamples and re-encodes (Pitt OCR Best Practices). Reserve rasterization for VLM input when a specific DPI is needed.
- **Test preprocessing on a sample before applying corpus-wide.** Learned image restoration combined with neural post-correction can yield large CER reductions on degraded historical documents — Guan et al. (2025) report 63.9-70.3% CER reduction for the full PreP-OCR pipeline (ResShift image restoration + ByT5 post-correction), not for classical deskew/binarization/contrast alone. Classical preprocessing alone may not help and can actively hurt: Machidon & Machidon (2025) find that grayscale conversion, binarization, and dilation did not improve OCR on degraded folkloristic scans and in some cases introduced artifacts that worsened recognition. Always run with and without preprocessing on a diverse sample and compare.
- **Store archival images separately from OCR derivatives.** Save native-resolution images for preservation and generate OCR-resolution images in memory for the VLM. Do not save OCR-resolution rasterizations as the archival copy.

### 3. Prompt Engineering

- **Build language-specific prompts that enumerate expected characters.** For diacritics-heavy languages (Polish, Czech, Vietnamese, Turkish), list every expected diacritical character explicitly in the prompt. For CJK scripts, instruct the model to handle mixed-script content (e.g., Korean hangul with classical Chinese hanja).
- **Specify structured output format.** Instruct the model to output markdown preserving headings, paragraphs, footnotes, and tables. Structured prompts with explicit output format significantly outperform generic "extract text" instructions.
- **Include negative instructions.** "Do not translate," "do not interpret," "do not add content not present in the image." VLMs will summarize, translate, or describe images unless explicitly constrained.
- **Handle page-type edge cases in the prompt.** Instruct the model on what to return for blank pages, illustration-only pages, and pages with only page numbers. Without this guidance, models may hallucinate content for non-text pages (Gbelidji 2026).
- **Guard against over-historicization on period documents.** VLMs trained with broad historical exposure may project archaic orthography anachronistically. Levchenko (2025) documents GPT-4o inserting historical characters in 59% of 18th-century Russian files regardless of prompt. Validate on the target period and stratify ground-truth sampling by decade (see §6) to detect this failure mode; no prompt will fully suppress it.

### 4. Pipeline Architecture

- **Separate GPU-intensive OCR from CPU-only post-processing.** The minimum viable pipeline has three stages: (1) VLM OCR producing per-page raw text, (2) quality diagnostics classifying problem pages, (3) assembly into combined document-level output. olmOCR (Poznanski et al. 2025) demonstrates this extract-describe-assemble pattern at scale.
- **Integrate diagnostics as automated gates.** Diagnostics should classify each page into action categories (OK, rule-fixable, LLM-fixable, manual review) using language-aware detection: diacritic-to-Latin ratios for European scripts, CJK character ratios for East Asian scripts, repetition density, symbol density, and page length anomalies. These categories are exactly the routing input the `clean` phase consumes.
- **Store all results as structured JSON with full metadata.** Every pipeline stage should output structured data (model name, quantization, DPI, timestamps, per-page results) rather than flat text files. This enables automated aggregation and corpus-level quality dashboards.
- **Design for resumability.** The pipeline should detect already-processed documents and skip them on re-run. Store a completion marker (e.g., `results_raw.json`) per document so partial runs can resume without re-processing.

### 5. Batch Strategy and Resource Planning

- **Calibrate GPU-hour estimates from a measured run.** Process 10-20 pages, measure per-page time, multiply by corpus page count, and add 30% buffer for variance and failed retries. Do not rely on model documentation or theoretical throughput.
- **Structure batch processing as one job per document.** This minimizes job scheduling overhead, simplifies failure recovery (re-run one document, not one page), and produces self-contained output directories.
- **Use the tranche/gate pattern.** Split the corpus into a small test tranche (3-5 documents per language) and bulk tranches. Complete accuracy evaluation on the test tranche before committing GPU-hours to bulk runs. This is the single most important resource management decision.
- **Handle large documents explicitly.** Books exceeding the job wall-clock limit should be split into page-range chunks submitted as separate jobs writing to the same output directory. The assembly stage must merge chunks.
- **Track all jobs in a manifest.** Maintain a CSV or database mapping each document to its tranche, job ID, status, GPU-hours consumed, and quality metrics. This supports both operational monitoring and post-hoc reporting.

### 6. Accuracy Evaluation

- **Combine ground-truth sampling with automated proxies.** Human-transcribed ground truth with CER/WER computation gives a rigorous accuracy number; dictionary-based hit rates give a scalable quality signal across every page. Neither alone is sufficient.
- **Stratify the ground-truth sample.** Select pages spanning languages, decades (older print is harder), print quality (faded vs. clean), and content type (body text, tables, captions). A sample of 20-30 pages per language is a practical minimum for a reliable CER estimate (Levchenko 2025) — that figure is the **ongoing-monitoring** minimum for a pipeline already in production, not the size of the up-front selection comparison, which the `evaluate` phase §3 sizes separately. The stratification scheme, the normalization declaration, and the CER/WER implementation are specified once in the `evaluate` phase; reuse them here rather than defining a second set.
- **Document the evaluation tool.** CER/WER scores differ across evaluation tools due to normalization differences (whitespace handling, Unicode normalization, punctuation treatment). Neudecker et al. (2021) demonstrate that tool choice changes reported accuracy. Specify which tool you used, which normalization was applied, and whether the comparison was case-sensitive.
- **Acknowledge CER/WER limitations.** Character-level edit distance does not capture layout errors, semantic correctness, or structural fidelity. A model can scramble column order while achieving low CER (Beyene & Dancy 2026). Supplement with dictionary hit rates, manual inspection of representative pages, and downstream task performance.
- **Set go/no-go thresholds relative to downstream needs.** A mean CER below 5% is excellent; below 10% is acceptable for most computational text analysis. Calibrate against what your analysis pipeline can tolerate rather than pursuing absolute accuracy — van Strien et al. (2020) show that the impact of OCR quality on downstream NLP tasks is task-specific (topic modeling, NER, dependency parsing, and retrieval degrade at different thresholds), so the right threshold depends on which downstream task consumes the text.

### 7. Reproducibility and Documentation

- **Record every pipeline parameter in machine-readable format.** Model name and exact version, quantization method, DPI, prompt text, generation parameters (temperature, max tokens, sampling strategy), software versions, and hardware specifications. Store as JSON alongside the output.
- **Produce per-document processing reports.** Each document should have a JSON report recording pipeline stages completed, timestamps, page counts (processed, failed), quality summary, and output file manifest.
- **Aggregate into a corpus-level batch summary.** A single CSV mapping all documents to their quality metrics, processing metadata, and tranche membership supports both quality monitoring and methods reporting.
- **Archive the complete pipeline code and prompts.** The OCR can only be reproduced if the exact code, prompts, and model weights are available. Pin model versions and software dependencies. If using a model from a hub (HuggingFace, etc.), record the commit hash.
- **Treat hosted-API non-determinism as a reproducibility hazard.** Levchenko (2025) measured coefficient-of-variation (CV) of daily word-accuracy over seven days and found roughly a 10x spread across models (e.g., CV=0.307 vs. 0.037). Commercial hosted APIs can silently change underneath you. Barrie, Palmer & Spirling (2025) generalize the point for political-science LM work: temperature=0 does not fix it, many LM-based pipelines fail the re-runnable and repeatable sub-standards of replication, and the disciplinary recommendation is locally-hosted, versioned open-weight models. Prefer local open-weight models pinned to a specific revision when publication-grade reproducibility is required; otherwise, report the evaluation window and replicate the pilot run before and after any bulk campaign.
- **Hand off.** Pass raw per-page output to the `clean` phase (LLM-based correction, constrained decoding, Unicode normalization, provenance). Before publication, audit the pipeline documentation with the `methods-reporting` skill (APSA/JARS/DA-RT standards for methods sections).

---

## Phase `clean`: Post-OCR Text Cleanup for Research Corpora

### 1. Cleanup Strategy Selection

- **Characterize the error-generating DGP before selecting a method.** Document source language(s), era, typeface family (Fraktur, Antiqua, typewritten, handwritten), scan DPI, OCR engine, and domain jargon. Each parameter constrains which corrections are plausible and which risk introducing semantic drift. When the text came from the `run` phase, most of this is already in the per-page `pipeline` record.
- **Choose between LLM correction, rule-based fixes, or a hybrid pipeline based on error type.** LLM correction excels at context-dependent errors (wrong but plausible characters, broken words, missing diacritics). Rule-based fixes handle deterministic patterns (control characters, Unicode normalization, repetition artifacts, whitespace) with zero risk of content alteration. Use rule-based fixes unconditionally for these categories.
- **Default to the hybrid approach for research corpora.** Run LLM correction first on all pages, then apply deterministic rule fixes on top. This order matters: LLM correction may introduce formatting artifacts that rule fixes clean up, while the reverse order wastes rule-fix effort on text the LLM will rewrite (Machidon & Machidon 2025).
- **Pilot-test LLM correction per language before corpus-wide deployment.** LLM post-correction effectiveness is highly language-dependent: English achieves 7-58% CER reduction across open models, while Finnish shows negative or near-zero improvement across the same model set (Kanerva et al. 2025). Never assume cross-language transferability.
- **Consider whether correction is needed at all.** Define the quality threshold before choosing a strategy. The Hill & Hengchen 70-80% quality band (reported in van Strien et al. 2020) marks the critical threshold below which most downstream NLP tasks perform poorly; above 80% quality many tasks (e.g., topic modeling) tolerate residual noise. If the downstream analysis sits comfortably above this band, the risk of correction-introduced errors may outweigh the benefit.

### 2. LLM-Based Correction

- **For most pages, use a small text-only model.** The correction input is already text; image understanding is not needed for well-OCR'd pages. A 7-13B parameter model with 4-bit quantization fits in ~4-20GB VRAM and runs on a single GPU. Larger fp16 models (e.g., Llama-3.1-70B at fp16 yielding ~42% CER reduction vs ~39% at 4-bit) gain 2.5-4.7pp but require roughly 3x the memory (132GB vs 43GB) and often a second GPU (Kanerva et al. 2025).
- **For severely degraded pages, use multimodal correction.** Feeding both the original page image and the OCR text to a correction model can achieve below 1% CER on degraded documents, but doubles GPU cost (Greif et al. 2025). Reserve this for flagged pages, not routine processing.
- **Write tight correction prompts.** Instruct the model to "fix clear OCR mistakes only: wrong characters, broken words, garbled punctuation, repetition artifacts. Do not translate, modernize, or add anything. Output the corrected text only." Loose prompts invite hallucination.
- **Supply socio-cultural context in the prompt.** Including document era, publication type, language register, and genre (e.g., "The text is from an English newspaper in the 1800s") meaningfully reduces CER beyond generic correction prompts — the top-performing CLOCR-C configuration achieved over 60% CER reduction on the NCSE dataset using a modular prompt that combines expert framing, recovery instructions, publication context, text-type context, and anti-overgeneration instructions (Bourne 2024). Misleading or mismatched context degrades performance, so use the real document metadata.
- **Add language-specific instructions.** For Polish, explicitly mention diacritics restoration (ą, ć, ę, ł, ń, ó, ś, ź, ż). For Korean, mention hangul integrity and hanja preservation. The correction model needs to know which character set to favor.
- **Mitigate hallucination with constrained decoding.** Constrained decoding techniques — beam search with CER-based re-ranking, sequence-level similarity re-ranking, and token-level Constrained Beam Search that interpolates the model's distribution with a character-similarity distribution — enforce fidelity between input and output and prevent plausible-but-fabricated substitutions (Sastre et al. 2025). Prefer token-level CBS with dynamic α if model logits are accessible; otherwise fall back to beam search with CER re-selection. This matters because WER can worsen even when CER improves: fine-tuning alone in Sastre et al. left CER roughly flat (0.314→0.321) while WER jumped from 0.633 to 0.821, a failure mode constrained decoding directly addresses.
- **Use worked prompt templates and a provenance schema.** See `reference/prompt-templates-and-schema.md` for a minimal constrained-decoding-friendly baseline prompt, a Bourne-style socio-cultural-context prompt, and a span-level JSONL provenance schema (per Guo & Wei 2026 §3.2/§3.3).
- **Strip LLM overgeneration with alignment-based post-processing.** Llama-family models routinely prepend "Here is the corrected text:" or append error-by-error explanations. Without post-hoc trimming (character-level local alignment of output against input, keeping only the aligned region), Llama-3-8B scored -74.1% CER; with trimming, +7.3% (Kanerva et al. 2025). Gemma and GPT-4o are largely unaffected but the step is cheap and should be applied universally.
- **Disable chain-of-thought for correction tasks.** Reasoning modes add latency without improving transcription fidelity. Use low-temperature sampling or greedy decoding for deterministic output.
- **Tune segment length for corpus-scale processing.** Short segments (50-100 words) score notably worse CER% across models; 200-300 words appears optimal for page-level correction (Kanerva et al. 2025). When splitting long documents, use a stride that preserves left context (left-uncorrected-concatenate parallelizes cleanly; left-corrected-concatenate is sequential but slightly better at segment boundaries).
- **Track all changes with edit-distance metrics.** Compute Levenshtein distance and change ratio (edit distance / original length) per page. Flag pages where the correction model altered more than 10% of characters for manual review — high change ratios may indicate hallucination rather than correction. This 10% threshold is an operational heuristic; calibrate against your pilot evaluation.

### 3. Rule-Based Fixes

- **Apply deterministic fixes in a fixed order.** (1) Control character removal, (2) zero-width and invisible Unicode character removal, (3) NFKC Unicode normalization, (4) consecutive character repetition collapse, (5) standalone symbol line removal, (6) whitespace normalization. This ordering prevents interactions between fixes.
- **Tune repetition collapse thresholds to the corpus.** The default of collapsing runs of 4+ identical characters to 3 works for most scripts but may need adjustment for languages with legitimate long character sequences or for documents with intentional formatting patterns.
- **Rule-based diacritics restoration is viable for some languages.** For Polish, rule-based approaches (removing word breaks, rejecting case-changing corrections, restoring diacritical characters replaced with visually similar ASCII) are competitive with LLM-based correction and more predictable (Ogrodniczuk 2022).
- **Generate synthetic OCR errors for training when ground truth is scarce.** Glyph-similarity-based synthetic corruption (feature-matched character confusions) produces more realistic training data than random-injection baselines, and outperforms in low-resource languages (Guan & Greene 2024).
- **Preserve the raw text alongside every cleaned version.** Rule-based fixes are deterministic and reversible, but downstream researchers may prefer different normalization choices. Store both raw and cleaned text at every stage.

### 4. Quality Diagnostics and Metrics

- **Move beyond CER/WER as the sole quality measure.** Character-level edit distance is sensitive to normalization choices (ligature handling, Unicode compatibility, PUA character treatment), does not capture semantic correctness, and can return substantially different numbers across evaluation tools on the same data (Beyene & Dancy 2026; Neudecker et al. 2021). A model can scramble column order while achieving perfect CER.
- **Use precision as a primary metric for historical and archival corpora.** CER and WER emerged from speech recognition, where insertions and deletions are symmetric. Historical and archival research is asymmetric: false positives (hallucinated tokens, invented entities) are more costly than false negatives (missed content), because historians already expect absence. Precision on downstream tasks (e.g., NER precision, entity similarity) often aligns better with analytic needs than CER/WER and can show improvement even when CER/WER indicate regression (Backer & Hyman 2025).
- **Build a multi-signal diagnostic profile per page.** Character composition ratios (diacritics-to-Latin for European scripts, CJK character ratios for East Asian), repetition artifact density, symbol density, and page length anomalies (empty, suspiciously short, suspiciously long) each capture different failure modes.
- **Use dictionary hit rates as an automated quality proxy.** Tokenize OCR output and check against morphological dictionaries or analyzers. Compute per-page and per-document valid-token rates. This scales to every page in the corpus without human effort.
- **Calibrate thresholds against downstream task requirements.** OCR quality directly impacts NER, classification, topic modeling, and other downstream NLP tasks. Below the Hill & Hengchen 70-80% quality band (reported in van Strien et al. 2020), most NLP tasks perform poorly; above 80% many tasks converge. Define acceptable error rates based on what your analysis pipeline can tolerate, not abstract accuracy targets.
- **Classify pages by recommended action.** Map diagnostic signals to action categories: OK (no intervention), rule-fixable (deterministic cleanup sufficient), LLM-fixable (context-dependent errors), manual review (critical failures). This prioritizes human attention on the pages that need it most, and it matches the routing categories the `run` phase §4 already assigns.

### 5. Multilingual Considerations

- **Check diacritic ratios for Latin-script languages.** For Polish, a page of body text with zero diacritical characters almost certainly has OCR errors. Flag pages where the diacritic-to-alphabetic ratio drops below a language-calibrated threshold (Ogrodniczuk 2022).
- **Treat Korean spacing as a distinct post-OCR task.** Korean uses space-delimited eojeol units, and OCR frequently merges or splits them incorrectly. Dedicated syllable-and-morpheme spacing models (Choi & Kim 2021) address this error type specifically and may outperform general-purpose LLM correction, though direct LLM benchmarks on this task are not well-established.
- **Use morphological analyzers as correction validators.** Morfeusz for Polish, Mecab-ko for Korean — tokens that parse successfully are likely correct; tokens that fail to parse are OCR error candidates. This provides both a diagnostic signal and a correction filter.
- **Protect dialectal and archaic text from normalization.** Correction models trained on standard modern language may silently replace historical or dialectal tokens with modern near-neighbors, introducing semantic drift (e.g., Machidon & Machidon 2025 document *žlahnega* → *glavnega* in Slovene folkloristic text; Kanerva et al. 2025 document historical long-s and v/w substitutions). Test on a sample of the oldest and most linguistically distinctive documents before corpus-wide deployment, and disable normalization flags that modernize orthography.

### 6. Corpus-Level Quality Assurance

- **Implement a three-tier review workflow.** (1) Automated pass/fail based on diagnostic thresholds applied to all documents, (2) spot-check review of flagged documents (10-15% of corpus), (3) deep review of a random sample of passing documents (2-5% of corpus) to catch false negatives.
- **Define specific flagging thresholds.** Mean quality score below 0.80, LLM correction change ratio above 10%, dictionary hit rate below 80%, or more than 5% empty pages. These are operational defaults, not empirically derived cutoffs — calibrate against your pilot evaluation and pre-register the final values.
- **Route flagged documents to specific remediation actions.** Re-run LLM cleanup with a different prompt, re-OCR at higher DPI or without quantization (back to the `run` phase), or escalate to manual transcription. Each action has different cost and quality implications.
- **Produce a corpus-level quality dashboard.** Aggregate per-document metrics into a summary CSV or report: document ID, language, page count, mean quality score, dictionary hit rate, correction change ratio, flag status, review outcome. This supports both operational monitoring and methods reporting.

### 7. Provenance and Documentation

- **Maintain a complete audit trail of all corrections.** Each correction should be attributed to its source (LLM model version, rule name) with before/after text preserved at the page level (Guo & Wei 2026). Correction pathways can substantially alter extracted entities and downstream interpretations.
- **Log model details for the LLM correction stage.** Model name, quantization method, prompt text, generation parameters (temperature, max tokens, sampling), and per-page edit-distance metrics. This is the minimum required to reproduce or audit the correction.
- **Log rule-fix details.** Which rules fired and how many characters each rule changed per page. This enables downstream researchers to assess whether rule fixes were aggressive or conservative for a given document.
- **Produce a cleanup comparison artifact.** A CSV or JSON with page-level before/after text pairs and metrics (edit distance, change ratio, flagged status) enables downstream researchers to assess correction quality and choose their preferred text version.
- **Record all thresholds and human review outcomes.** Sampling decisions, flagging thresholds, remediation actions, and human review results should be documented in a methods section alongside the corpus, not just in internal notes.
- **Pre-register the correction strategy when downstream inference depends on cleaned text.** Correction pathways can substantially alter extracted entities — Guo & Wei 2026 show that raw, fully-corrected, and provenance-filtered variants of the same corpus yield materially different NER inventories (176 volatile entities in their pilot). Correction-stack flexibility (prompt wording, trust-policy threshold, model version) is a researcher-degrees-of-freedom problem in the Simmons et al. 2011 sense: each un-documented choice is a forking path that can shift downstream inferences. Pre-registration is the standard remedy (Nosek et al. 2018). When cleaned text feeds named-entity-based, topic-based, or embedding-based inferential analyses, pre-register the correction model, prompt, decoding configuration, and provenance-filter trust policy alongside the analysis plan (cross-reference the `pre-registration-writing` skill).

---

## Quality Checks

### `evaluate`

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
- [ ] Model registry, ground-truth set, normalization recipe, and seeds archived for reproducibility (compose with `methods-reporting`)

### `run`

- [ ] **Model benchmarked for task:** VLM selected based on document-OCR benchmarks (OCRBench or equivalent), not general VLM leaderboards (Liu et al. 2024; Fu et al. 2025)
- [ ] **Language support verified:** Target language confirmed in the model's explicit training set with per-language accuracy data (Bai et al. 2025)
- [ ] **Quantization tradeoff assessed:** If using 4-bit or 8-bit quantization, accuracy impact measured on a pilot sample against full-precision baseline (Li et al. 2025)
- [ ] **DPI justified:** OCR input DPI calibrated on a pilot (not dropped below ~150-200 ppi without evidence), with archival images stored separately at FADGI/Metamorfoze targets (FADGI 2016; van Dormolen 2012)
- [ ] **Native extraction preferred:** Embedded images extracted byte-for-byte from scanned PDFs rather than re-rasterized, when available
- [ ] **Preprocessing tested on sample:** Any image preprocessing (classical or learned restoration) validated on a diverse sample before corpus-wide application; headline CER reductions from PreP-OCR-style pipelines reflect combined restoration + post-correction, not classical preprocessing alone (Guan et al. 2025; Machidon & Machidon 2025)
- [ ] **Prompts are language-specific:** OCR prompts explicitly name the script system, enumerate expected diacritics or character sets, and include negative instructions
- [ ] **Pipeline stages separated:** GPU-intensive OCR decoupled from CPU-only diagnostics and assembly, with structured JSON output at each stage
- [ ] **Diagnostics integrated:** Automated quality diagnostics classify every page by action category with language-aware character detection
- [ ] **Resource estimate calibrated:** GPU-hours estimated from a measured calibration run, not assumed from model documentation
- [ ] **Test tranche gated:** Accuracy evaluation completed on a test tranche before committing to bulk GPU-hours
- [ ] **Ground truth sampled:** Human-transcribed ground truth created for a stratified sample of pages, with CER/WER computed and reported (Levchenko 2025)
- [ ] **Evaluation tool documented:** CER/WER tool identified and normalization choices recorded, given known tool discrepancies (Neudecker et al. 2021)
- [ ] **Pipeline fully documented:** Model version, quantization, DPI, prompts, generation parameters, and software versions recorded in machine-readable format
- [ ] **Model stability acknowledged:** If using a hosted API, evaluation window recorded and pilot re-run before and after the bulk campaign; publication-grade corpora use pinned open-weight models (Levchenko 2025; Barrie, Palmer & Spirling 2025)
- [ ] **Processing reports generated:** Per-document JSON reports and corpus-level batch summary CSV produced and archived

### `clean`

- [ ] **DGP characterized:** Source language(s), era, typeface, scan DPI, OCR engine, and domain documented before method selection
- [ ] **Strategy justified:** Cleanup approach (LLM, rule-based, or hybrid) chosen based on error types, corpus size, and resource constraints
- [ ] **LLM correction pilot-tested per language:** Cleanup validated on a sample from each language before corpus-wide application (Kanerva et al. 2025)
- [ ] **Socio-cultural context supplied in prompts:** Document era, publication type, and genre included; misleading context avoided (Bourne 2024)
- [ ] **Segment length tuned:** Input segments of 200-300 words used; boundary concatenation strategy chosen (Kanerva et al. 2025)
- [ ] **Overgeneration stripped:** Alignment-based trimming applied to LLM outputs to remove "Here is the corrected text:" preambles and trailing commentary (Kanerva et al. 2025)
- [ ] **Hallucination risk mitigated:** Constrained decoding (token-level CBS preferred; beam + CER re-rank as fallback) applied to prevent fabricated content (Sastre et al. 2025)
- [ ] **Change ratio tracked:** Per-page edit distance and change ratio computed and stored; pages exceeding the flagging threshold (default 10%) reviewed
- [ ] **Rule-based fixes ordered correctly:** Deterministic fixes applied in the prescribed sequence (control chars, zero-width, NFKC, repetitions, symbols, whitespace)
- [ ] **Metrics go beyond CER/WER:** Quality assessed using multiple signals (precision for historical corpora, character composition, dictionary hit rates, diagnostic flags), not CER/WER alone (Backer & Hyman 2025; Beyene & Dancy 2026; Neudecker et al. 2021)
- [ ] **Downstream impact considered:** Quality thresholds set relative to the intended analysis and the 70-80% critical quality band (van Strien et al. 2020), not abstract accuracy targets
- [ ] **Language-specific patterns addressed:** Diacritics ratios, morphological parsing, and spacing rules checked for each language in the corpus
- [ ] **Dialectal and archaic text protected:** Correction models tested for damage to non-standard language varieties; modernization flags disabled where relevant (Machidon & Machidon 2025)
- [ ] **Flagging thresholds defined and calibrated:** Numeric thresholds (quality score, change ratio, dictionary hit rate, empty page rate) set and calibrated against pilot evaluation
- [ ] **Stratified human review conducted:** Review sample stratified by language, document age, print quality, and flag category; sampling fraction justified
- [ ] **Both raw and cleaned text preserved:** Original OCR output retained alongside every cleanup stage for auditability
- [ ] **Correction provenance logged:** Each correction attributed to its source (LLM model, rule name) with before/after text, edit type, confidence, and review status (Guo & Wei 2026)
- [ ] **Correction strategy pre-registered:** When cleaned text feeds inferential analyses, the correction model, prompt, decoding configuration, and trust policy are pre-registered alongside the analysis plan
- [ ] **Cleanup comparison artifact produced:** Page-level CSV or JSON with raw text, cleaned text, and per-page metrics archived
- [ ] **Methods documented:** All thresholds, sampling decisions, model versions, prompts, and human review outcomes recorded
