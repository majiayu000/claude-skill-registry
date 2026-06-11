---
name: did-event-study
description: Run a staggered difference-in-differences / event-study analysis to the Sant'Anna practitioner standard — drives the canonical packages (R `did`/`DRDID`/`didFF`/`contdid`; Stata `csdid`/`drdid`), enforces the doubly-robust default, a mandatory diagnostic + sensitivity suite, uniform-band inference, replicate-and-verify-against-source discipline, and ends in a graded credibility verdict. Use when user says "run a DiD", "event study", "staggered adoption", "Callaway Sant'Anna", "att_gt", "csdid", "did with multiple periods", or points at panel data with a treatment-timing variable. NEVER reimplements an estimator.
argument-hint: "[data path] [--outcome --unit --time --gvar] [--control nevertreated|notyettreated] [--continuous] [--stata]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
effort: high
---

# /did-event-study — DiD / event study, Sant'Anna practitioner standard

This is a **thin orchestrator over the canonical packages** — it never reimplements an estimator. It walks the practitioner workflow from *Difference-in-Differences with Multiple Time Periods* (Callaway & Sant'Anna 2021), the *Doubly Robust DiD* estimators (Sant'Anna & Zhao 2020), and the *"What's Trending in DiD?"* synthesis (Roth, Sant'Anna, Bilinski & Poe 2023), and it follows the **replicate-and-verify-against-source** discipline.

> **Actor → Critic.** The skill is the *Actor*: it runs your packages and the diagnostics. It then puts on the *Critic* hat for **Phase 8 — a graded credibility verdict**, never a binary "passes." A mismatch with a pre-test is *evidence on credibility*, not a gate. (This actor/critic + mandatory-diagnostic + graded-credibility shape mirrors `.claude/rules/orchestrator-protocol.md` and the verification posture of `audit-reproducibility`.)

> **Read first:** [`.claude/rules/did-conventions.md`](../../rules/did-conventions.md) — the HARD standards this skill enforces (data coding, DR default, control group, inference, aggregation, verification, and the pitfalls to avoid). Then the canonical resources in §Resources.

The methodological defaults below reflect **Pedro Sant'Anna's sign-off**: `notyettreated` control default, HonestDiD led by relative-magnitudes `Mbar` (also report `M`), `staggered` as an option with `att_gt` the workhorse, TWFE benchmark-only.

## When to use

- Staggered or 2×T adoption with panel or repeated cross-sections; a binary absorbing treatment, or a **continuous dose**.
- Any time someone reaches for a TWFE event study under staggered timing — route here instead.

## When NOT to use

- A single 2×2 with one pre / one post and no covariates is a one-liner — still use `DRDID::drdid()`, but you don't need the full pipeline.
- Reversible / switching treatments (units turning on **and** off): these packages assume absorbing treatment. Stop and reconsider the design.

## Workflow (fixed order)

### Phase 0 — Reproducibility setup (gate before any estimation)
- `set.seed(...)` is **REQUIRED** — all inference is bootstrap-based. (The JEL replication uses a fixed seed; pick one and pin it.)
- Pin software (`renv::restore(prompt = FALSE)`), use `here::here()` for paths (no hard-coded machine paths — the `git-guardrails` hook blocks them in `.R`/`.do`), one master script runs the pipeline end-to-end.
- Resolve namespace conflicts explicitly (`conflicted::conflict_prefer("select","dplyr")`, `…("filter","dplyr")`).

### Phase 1 — Design / estimand
- Reshape to **LONG**: one row per unit-period (`tidyr::pivot_longer`).
- Required columns: `yname` (outcome), `tname` (time), `idname` (**time-invariant, numeric** unit id), `gname` (group = **first period treated**; **never-treated coded EXACTLY `0`**).
- Tabulate the roll-out (share of units/population by cohort) to make the design explicit: **2×2 → 2×T → staggered G×T**.
- Pick the estimand up front. The recommended single summary is the **Overall ATT from `aggte(type = "group")`**; dynamics via `type = "dynamic"`.

### Phase 2 — Estimator selection
Follow the decision logic in §Estimator selection. Output: which estimator, `est_method`/`estMethod`, `control_group`, `panel` vs RC, covariates yes/no.

### Phase 3 — Estimation (drive the package; do not reimplement)
- **2×2 (one pre / one post):**
  ```r
  DRDID::drdid(yname, tname, idname, dname, xformla = ~covs, data, panel = TRUE, estMethod = "imp")
  ```
  IPW-only: `DRDID::ipwdid(..., normalized = TRUE)`; OR-only: `DRDID::ordid(...)`.
  - **Pre-flight (learned from validating Card–Krueger):** `panel = TRUE` requires `idname` **unique within each period** AND a **balanced** panel. Real datasets often aren't — check first:
    ```r
    stopifnot(nrow(dplyr::count(data, .data[[idname]], .data[[tname]]) |> dplyr::filter(n > 1)) == 0)  # idname unique by period
    balanced <- all(table(data[[idname]]) == length(unique(data[[tname]])))
    ```
  - **If unbalanced** (the common case): either (a) reproduce the **full-sample textbook 2×2** with `panel = FALSE` and a **row-unique id** (`data$rowid <- seq_len(nrow(data))`; this equals `feols(y ~ d*post)` to ~1e-10 — but RC SEs treat the waves as independent, so for a true panel report the clustered/panel SE separately); or (b) **balance** the panel (`keep ids present in all periods`) and use `panel = TRUE` — but this is a **different estimand** (the balanced subpopulation), so record it as a named alternative (`EXPLAINED`), e.g. "full-sample 2×2 = 2.914; balanced-panel DR = 2.972 (19 attriting stores dropped)."
  - DR with **no covariates reduces to the simple 2×2** — DRDID earns its keep once `xformla` adds covariates.
- **Staggered / multi-period (G×T or 2×T):**
  ```r
  out <- did::att_gt(
    yname, tname, idname, gname,
    xformla     = NULL,             # or ~ x1 + x2 (time-invariant / baseline covariates)
    data        = mydata,
    panel       = TRUE,             # FALSE for repeated cross-sections (idname ignored)
    control_group = "notyettreated",# staggered; "nevertreated" for a clean 2×T design
    est_method  = "dr",             # doubly robust DEFAULT (only used when xformla is set)
    base_period = "universal",      # REQUIRED for a readable event study + HonestDiD
    bstrap = TRUE, cband = TRUE, biters = 1000,   # publication: biters = 25000
    clustervars = NULL,             # ≤ 2, one must equal idname
    weightsname = NULL              # design-relevant weights if any
  )
  ```
  `att_gt` builds every `ATT(g,t)` from a clean `drdid` 2×2 — that is *why* it avoids the forbidden already-treated-as-control comparisons that bias TWFE.
- **TWFE event study — a benchmark/sanity-check, never the headline under heterogeneity:**
  `fixest::feols(y ~ i(time_to_treat, treat, ref = -1) | id + year, cluster = ~id)`. Confirm `att_gt(est_method = "reg")` matches it in simple cases (SEs differ only because of the bootstrap) so any divergence is attributable to *design*, not a coding bug.
- **Continuous dose [ALPHA — API may change]:**
  `contdid::cont_did(yname, dname, gname, tname, idname, data, target_parameter = "level"|"slope", aggregation = "dose"|"eventstudy")`. `dname` is the **time-invariant real dose** (its actual value pre-treatment, **not 0**); `gname = 0` for never-treated. `level → ATT(d)`, `slope → ACRT(d)`.
- **Stata twins** (`--stata`) — **R is the benchmark; Stata must match it.** `csdid y covs, ivar(id) time(t) gvar(g) method(dripw) notyet asinr` (the `asinr` option = "as in R") must reproduce `did::att_gt` to **1e-6**; `estat event` / `estat simple`; `drdid` for the 2×2. Any Python port is held to the same: **match R**.

### Phase 4 — Mandatory diagnostics (none skippable)
1. **Pre-trends (a PRE-TEST, not a test):** read pre-treatment `ATT(g,t)` for `t<g` and the **Wald p-value** from `summary(out)`; in event-study form all `e<0 ≈ 0`, with `e = -1 ≈ 0`. Passing is *evidence on credibility*, **not proof** PT holds where you need it. **Do NOT pre-test with a TWFE event study** — under selective timing it can reject PT even when it holds.
2. **Event study:** `aggte(out, type = "dynamic")` → `ggdid()` (red = pre pseudo-ATTs, blue = post; set `ylim` so panels compare). Pseudo-ATTs are valid only under no-anticipation.
3. **Negative-weights / forbidden-comparison check:** satisfied *by design* via `att_gt`/`csdid`; flag negative TWFE weights as the reason to prefer the ATT(g,t) building block.
4. **DR overlap:** inspect propensity-score overlap (the JEL Figure 1 idea). PS trimming default `trim.level = 0.995`; `ps.flag` reports IPT convergence.

### Phase 5 — Sensitivity (ROBUSTNESS, never a pass/fail pre-test)
- **HonestDiD (Rambachan & Roth)** — **lead with the relative-magnitudes `Mbar` breakdown** (headline), also report smoothness. Requires `base_period = "universal"`. **`honest_did()` is a NON-exported internal S3 method** in `HonestDiD` (bare `honest_did()` errors); use `HonestDiD:::honest_did(es, …)`, or the direct path below — **validated on `mpdta`**:
  ```r
  es    <- aggte(out, type = "dynamic")                 # universal base period
  IF    <- es$inf.function$dynamic.inf.func.e           # influence function
  sigma <- crossprod(IF) / n_units^2                    # IF-based covariance
  HonestDiD::createSensitivityResults_relativeMagnitudes(
    betahat = es$att.egt, sigma = sigma,
    numPrePeriods = sum(es$egt < 0), numPostPeriods = sum(es$egt >= 0),
    Mbarvec = c(0, 0.5, 1))                             # report the breakdown Mbar
  ```
- **didFF functional-form sensitivity (Roth & Sant'Anna 2023):** `didFF::didFF(...)`; where the implied counterfactual density of `Y(0)` dips below 0, parallel-trends-for-all-functional-forms is violated. Small p → reject insensitivity. (Parallel trends is **not** invariant to levels vs logs — the functional form is a substantive identification choice.)
- **He argues formal sensitivity should be standard practice.** Pair it with substantive reasoning about which time-varying confounders could break PT and how large a plausible violation is.

### Phase 6 — Inference
- Multiplier bootstrap, `bstrap = TRUE`, `cband = TRUE` → **uniform/simultaneous** bands robust to multiple testing. `biters = 25000` for publication. **Never** ship pointwise-only (`bstrap = FALSE, cband = FALSE`) as the headline.
- `clustervars` ≤ 2 (one = `idname`); cluster TWFE benchmarks at the unit level. Few-treated-cluster settings need care (e.g. a wild-cluster bootstrap via `fwildclusterboot`/`boottest`).
- Report design-relevant weights (`weightsname`) AND report weighted *and* unweighted.

### Phase 7 — Aggregation & reporting
- `aggte(out, type = "dynamic", min_e =, max_e =, balance_e =, bstrap = TRUE, biters = 25000, na.rm = TRUE)` for the event study; `type = "group"` for the headline **Overall ATT**; `type = "calendar"` per period. **Always pass `type` explicitly; avoid `type = "simple"`** (overweights early-treated).
- Report the `e ∈ {0,…,K}` average with `overall.att`/`overall.se`/CI, BOTH simultaneous and pointwise bands on the plot, and map **every coefficient/figure to its generating script + line**.

### Phase 8 — Credibility verdict (graded, honest — the Critic)
Synthesize the diagnostics into a **graded** verdict (Strong / Moderate / Weak / Not-credible) with explicit reasons — never a binary "passes":
- **Design** — `gname` coded right (`0` = never-treated)? absorbing treatment? clean control group exists?
- **Pre-trends** — Wald p + visual `e<0 ≈ 0` (state: evidence, not proof).
- **Sensitivity** — HonestDiD breakdown `Mbar`; `didFF` p-value.
- **Overlap** — DR/PS overlap acceptable; trimming not heavily binding.
- **Inference** — uniform bands; seed set; weights reported both ways.

## Estimator selection

```
Continuous dose?            → contdid::cont_did(...)            [ALPHA]
else 2 groups × 2 periods?  → DRDID::drdid(..., estMethod="imp")
else many periods/cohorts?  → did::att_gt(...)   (wraps drdid per ATT(g,t))
repeated cross-sections?    → att_gt(panel=FALSE) / drdid(panel=FALSE)
```
- **Doubly-robust is the default** (`est_method="dr"` / `estMethod="imp"`: IPT propensity score + WLS outcome regression — doubly robust for *inference*). `est_method` matters only with covariates.
- **Control group:** **`notyettreated` is the default for staggered G×T** (a larger, time-varying comparison; it imposes stronger cross-group PT — "no free lunch"); use `nevertreated` for a clean 2×T design or when a credible never-treated pool is the right comparison.
- **Under limited overlap**, prefer OR/regression-adjustment over DR.
- **Heterogeneity-robust estimators usually agree** (CS, Sun–Abraham, BJS, dCDH) — the first-order priority is a transparent target parameter + transparent comparison group, not agonizing over the package. Under **(quasi-)random rollout timing**, the efficient Roth–Sant'Anna `staggered` estimator is worth considering, but `att_gt` (Callaway–Sant'Anna) stays the workhorse default.

## Verification / replication standard (from `DiD_book`)
- Translate **from**, and verify **against**, the **original author code** — benchmark against the actual Stata `esttab`/`outreg` outputs, not printed paper numbers.
- **Match the source to `abs_diff < 1e-6`** on BOTH point estimate AND SE; loosen only deliberately and document the scope. "Replication first — match original numbers before extending."
- Mandatory infra: `renv.lock` + `renv::restore()`, `here::here()`, `set.seed`, one master script, machine-readable outputs (`.rds`, `.csv` coefficients, a per-analysis `verification_against_stata.csv`).
- **R is the benchmark; other languages match R.** His R packages (`did`/`DRDID`/`didFF`/`contdid`) are the canonical implementations — Stata (`csdid`/`drdid` via `asinr` = "as in R") and Python ports must **reproduce R** to **1e-6** (point + analytic SE; bootstrap-SE and cosmetic graphing differences excepted). *(This is distinct from replicating a published paper, where that paper's original author code — often Stata — is the truth for its numbers.)*

## Resources (canonical, public)
- **did-resources hub:** <https://psantanna.com/did-resources/> — the curated list (the JEL Practitioner's Guide, *What's Trending*, the 14-lecture course, the DiD checklist, all packages). **Lead here.**
- **Packages:** `did` <https://bcallaway11.github.io/did/> · `DRDID` <https://psantanna.com/DRDID/> · `didFF` · `contdid` · `staggered` · Stata `csdid`/`drdid` · Python `drdid`/`csdid`.
- **Papers:** Callaway & Sant'Anna (2021) <https://doi.org/10.1016/j.jeconom.2020.12.001> · Sant'Anna & Zhao (2020) <https://doi.org/10.1016/j.jeconom.2020.06.003> · Roth & Sant'Anna (2023, *Econometrica*) <https://doi.org/10.3982/ECTA19402> · Rambachan & Roth (2023, HonestDiD) · continuous treatment <https://arxiv.org/abs/2107.02637>.

## Output
Write to `scripts/R/_outputs/` (and `scripts/Stata/` if `--stata`): the master script, the `ATT(g,t)` + aggregations (`.rds`), the event-study figure (simultaneous + pointwise bands), the HonestDiD/`didFF` sensitivity, the `verification_against_stata.csv`, and a `did_credibility_verdict.md` (the Phase 8 graded verdict + every table→script:line map).

## Exit behavior
- Exit 0 with the graded verdict. A **Not-credible** verdict or a failed source-verification (`abs_diff ≥ 1e-6`) is surfaced prominently — never silently passed.
- Pairs with `/audit-reproducibility` (numeric claims ↔ outputs) and `/replication-package` (the deposit).

## What this skill does NOT do
- **Reimplement any estimator** — it drives your packages; if a number looks implausible, debug the wrapper / sample / weights / clustering / data construction / engine **before** interpreting it.
- **Handle reversible treatments**, or use TWFE as the headline under staggered timing.
- **Consult any private vault** — this skill is self-contained and public-resource-only.
- **Replace your judgment** — the credibility verdict is advisory; you are the auditor.

## Flags
- `--outcome` `--unit` `--time` `--gvar` — map columns to `yname`/`idname`/`tname`/`gname`.
- `--control` `<nevertreated|notyettreated>` — comparison group (default per §Estimator selection).
- `--continuous` — continuous-dose mode (`contdid`, ALPHA).
- `--stata` — also run the Stata twin (`csdid`/`drdid`) for the dual-software cross-check.

## Cross-references
- [`.claude/rules/did-conventions.md`](../../rules/did-conventions.md) — the enforceable standards.
- [`.claude/skills/audit-reproducibility/SKILL.md`](../audit-reproducibility/SKILL.md) · [`.claude/skills/replication-package/SKILL.md`](../replication-package/SKILL.md) · [`.claude/skills/power-analysis/SKILL.md`](../power-analysis/SKILL.md) · [`.claude/skills/simulation-study/SKILL.md`](../simulation-study/SKILL.md).
