---
name: mandela
description: 'Audit an evaluation, benchmark, or scoring harness for leakage, answering whether outside ground truth actually enters or the system is grading itself. Use when building or reviewing an eval or benchmark, or when the user says "is this eval leaking" or "check this benchmark for contamination". It reports where ground truth enters and where it does not, and it edits nothing.'
---
# Mandela

Audit a validation for leakage: does outside ground truth actually enter, or is everyone confirming a result no one produced?

## Method

1. **Name the validation** and its components: what plays model, scorer, designer, dataset.
2. **Ask the core question:** does external ground truth enter independently?
3. **Test against all 8 patterns** and report only the ones that fire:

   1. Recall, not reason - a memorized answer recited instead of one derived.
   2. Wrong null hypothesis - a control that removes the label but not the signal.
   3. Shared hallucination - two components verifying each other.
   4. Tautology - a scorer grading buckets it drew.
   5. Verifier equals designer - a private, unreproducible recipe in holdout clothes.
   6. Shared-pool bias - train and holdout drawn from one labeler pool.
   7. Frame injection - a question that hands the subject the hypothesis.
   8. Demand characteristics - subjects who know they are being measured.

4. **Give the independence fix** for each hit. Read-only; name the leak and the fix, do not rewrite the experiment. See `../clean-and-true/references/idioms.md` for the clean-room procedure.

## Completion

Every applicable pattern was tested, only the firing ones are reported, and each carries an independence fix. A pass that finds no leak reports that.

