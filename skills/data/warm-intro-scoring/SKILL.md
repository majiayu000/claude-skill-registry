---
name: warm-intro-scoring
description: Use when ranking warm-introduction paths, evaluating connector matches, enriching warm connections and target contacts, or checking whether new matching factors improve recommendations.
---

# Warm intro scoring

Produce a ranked review artifact, a machine-readable scored-path CSV, and an honest evaluation summary. Reuse the existing scorers; do not invent a new weighted model for each run. No messages are sent by this skill.

## Engineering package

This copy is maintained outside the refreshable skills tree. Read `README.md` first and run `python3 check_all.py` from this folder. Use this folder as `SKILL_DIR` and its `vendor/` subfolder as `GTM_REPO`; bundled scripts default to the pinned vendor automatically. This copy has no dependency on the parent repository's `skills/` or `examples/` directories.

## Default input and workflow

Input: a list of warm connections and an optional list of target contacts. Accept CSV, database rows, or structured records with stable source IDs, names, profile URLs, company, role, and any relationship evidence. Reuse the current customer workspace and requester identity when known. Deduplicate contacts shared across both lists; retain their separate campaign memberships.

1. **Create customer DB tables.** Verify the active tenant and database dialect, inspect existing tables, and apply the additive [database schema](assets/customer-db.sql) through the supported customer DB interface. Reuse compatible existing tables; do not replace customer data. The supplied SQL targets PostgreSQL and must be adapted if the workspace uses another dialect. Record the workspace, migration result and table names.
2. **Resolve targets and enrich everyone.** If targets are absent, select ten actual customers or researched example targets in the customer's market using [the pipeline contract](references/pipeline.md). Pull full available profiles for every unique connector and target, including employment and education history. Cache raw receipts privately, build attributable features, and report incomplete profiles rather than dropping contacts.
3. **Enable incremental scoring.** Create the ingestion → profile enrichment → feature extraction → affected-pair scoring → artifact refresh pattern described in [the pipeline contract](references/pipeline.md). Default triggers are new connections, new targets, changed profiles, and relationship/willingness updates. Use durable event IDs, profile hashes, versioned features and a recoverable job queue. Verify replay, updates and failure recovery before calling the pattern enabled.
4. **Deliver the review artifact.** Show the three best paths per target, feature explanations, coverage, holds and freshness, plus machine-readable exports. Report whether the database and trigger are actually deployed, or only prepared.

This is the workflow to execute when the skill is invoked with contact data. Updating or installing the skill alone does not create live tables, incur enrichment spend, or enable a schedule. Use existing authorization for the chosen tenant and spend scope; ask only when these cannot be determined.

## Choose the scoring question

- **Find a connector to a named person:** requester → connector → target. Both relationships matter. Use the target-person office-hours scorer through `scripts/score.py`.
- **Find contacts by company/school criteria:** use the existing `lookup.py` discovery interface. Company proximity is not dated overlap. Do not present its score as target-person evidence.
- **Match people in a room:** use the event app's pair scorer (function 35%, previous roles 25%, school 15%, industry 15%, employers 10%). Keep missing dimensions unknown rather than redistributing their weight. Pair similarity is separate from warm-intro strength, product fit, and gifts. See [source adapters](references/sources.md).

Ask only for missing essentials: requester identity, customer market when neither targets nor customer context exists, intended reason for meeting, permitted data sources and budget. Missing targets alone do not require a question: use the ten-target fallback above. Reuse the user's existing approved scope. Default to private local artifacts and no live enrichment when cached evidence suffices.

## Gather and normalize evidence

When external data is requested, use [external evidence](references/external-data.md). Read current provider schemas. Resolve identities before joining facts. Keep company context separate from personal access.

Read [sources and input contract](references/sources.md). Reuse an owner-scoped LinkedIn Connections export or existing relationship database. Apify enriches supplied profile URLs; it does not magically retrieve all connections. Preserve connection-export provenance separately from profile enrichment. A profile URL, shared investor, event registration, or co-employment alone never proves a relationship.

Use stable IDs for requester, connector, target, employer and evidence. Hold ambiguous names and conflicting identities. Preserve source locator, evidence kind, subjects, observed date, actual interaction/employment dates, and a short supported detail. Only use information available as of the scoring date. Never invent jobs/dates to explain a known successful introduction.

For paid enrichment, validate the selected tool schema and do a one-row pilot (`--rows 0:1`) before a reviewed bounded batch. See the executable Deepline example in [sources](references/sources.md). Keep tokens, raw profiles, messages, connection lists and real-person artifacts outside Git. Credentials do not imply consent to send messages or publish people.

## Score and review

The wrapper requires a GTM Eng Skills checkout; it imports the maintained example scorer rather than shipping another copy. Set `GTM_REPO` to that checkout and `SKILL_DIR` to this skill directory. Install requires Python 3.10+; scoring/rendering use only the standard library.

```bash
python3 "$SKILL_DIR/scripts/score.py" reviewed-evidence.json \
  --repo "$GTM_REPO" --output scored-paths.csv
python3 "$SKILL_DIR/scripts/render.py" scored-paths.csv --output intro-review.html
```

Outputs refuse overwrite and are created with private permissions. Select a new output filename per run. The reference fixture is `assets/example.json`; use it only for demonstration.

The pinned baseline uses direct-introduction evidence 160, dated work overlap 80, owner relationship 0/5/10/15, school/city/community 40, role/industry 20, investor context capped at 3. These are ordinal evidence points, not percentages or success probabilities. Keep `model_version` and baseline segment in exports. The campaign example and event app use different scales; never mix their numeric scores.

**Separate score from permission and confidence.** The wrapper holds a nominally strong path for review unless both relationships have at least medium cited confidence and the connector has documented willingness for this particular introduction. A decline blocks the path while retaining the factual score. Even a ready-for-human-review path is not approved or sent. Unknown willingness stays unknown. A historic introduction is not current willingness. Recheck stale/conflicting evidence before proposing an ask.

Read [factor research](references/factors.md) when extending the model. New signals are hypotheses until evaluated. Keep weak affinities as context or tie-break candidates; do not let many weak facts overwhelm stronger evidence. Exclude sensitive-trait inference and hidden/private social data. Same city, college, sports team, professional club or public social exchange can suggest a conversation, not familiarity.

## Tune attributes and expand company networks

When a user supplies their employer, apply [company-network expansion](references/company-network.md): issuer investors → public portfolio pages → canonical employer matches, with source coverage reported. Use named, dated board roles separately from investor affiliation. Work and school matches must retain actual tenure/cohort intersection and date precision. For work overlap, supply company size and function/location from the same dated roles under the v4 tuning contract. Large-company overlap alone earns less than matching function and location.

For adjustable preferences, produce normalized feature paths under [the tuning contract](references/tuning.md) and run `python3 scripts/tuning.py normalized-features.json --output tuning.html`. The artifact exposes adjustable weights, reranks locally, preserves fixed review holds and exports weights. `assets/portfolio-focus.weights.json` raises portfolio priority to 120 points. These are explicit preferences in a separate heuristic model, not calibrated success probabilities or a silent change to the legacy baseline. Score sourced direct investor roles highly under the v3 contract; professional-community membership has a low default weight. Restore sourced city, industry and professional-community fallback matches with the v2 tuning contract. Do not infer missing facts. Missing/undated features remain zero/unknown; do not fabricate overlap dates to enable a slider.

## Deliver the artifact

Apply [clear output rules](references/readable-output.md) to all new reports and explanations. Use target contact → possible intro paths → score breakdown. Keep source details and weight controls separate from the main path review.

Open the generated HTML locally when possible. It must show target and connector identities, requester path, top three alternatives, component scores, evidence IDs, both-edge confidence, willingness and reasons to hold. Include search/status filters, an empty state and responsive keyboard-accessible controls. `scripts/render.py` supplies this without a server or dependencies. The HTML contains the selected people; do not publicly host it without authorization.

For a full target list, reconcile every source contact by stable identity. Report matched, missing, ambiguous, and excluded self-pairs. Do not select one contact per account unless requested. Keep all scored candidates available to the weight tuner; page the display instead of truncating the candidate universe. `scripts/tuning.py` supports account filters and local path ratings with notes. Download feedback before closing or reloading the tab. Ratings capture ranking opinions; they do not record an introduction, reply, meeting, or connector permission. See [competitive feature review](references/competitive-review.md) for evidence-backed gaps and the limits of current product research.

The ask preview is illustrative only. Export CSV matches the existing ask-thread loader; keep `reviewed_override=false`. If draft generation is requested, use the existing ask drafter with its segment/row gates and retain `approved=false`. Sending is a separate authorized action. Do not copy raw private evidence into an outbound ask.

## Evaluate before claiming improvement

Use the [evaluator contract](references/evaluator.md) for baseline-versus-candidate comparisons. It defines ranking eligibility, mature outcome denominators, research-driven adversarial cases and release gates. Run `python3 "$SKILL_DIR/scripts/evaluate.py" --help` for the executable input/output contract and start with `assets/evaluation-example.json`. Invalid inputs fail closed without a scorecard. Valid JSON and HTML scorecards distinguish insufficient evidence from exploratory comparisons; no result automatically approves deployment.


Run `python3 "$SKILL_DIR/scripts/check.py" --repo "$GTM_REPO"`. Check real ask compatibility without generating or sending asks. [Evaluation](references/evaluation.md) explains the historical audit and regression cases.

For predictive evaluation, require a private dated outcome set: candidate paths available at ask time, connector confirmation/decline, intro sent, target reply, meeting completed, and censored/unknown outcomes. Hold out time and target/account groups. Compare on the same candidate universe; report recall@3/MRR only with relevant-route labels, and reply/meeting rates only with comparable observed sends. Unsent drafts are not failures. Do not fit new weights to hand-selected anecdotes or quote a success rate from structural tests.

Finish with the artifact and CSV paths, scoring version, checks run, real-data coverage and any missing evidence. If the requested reference artifact is inaccessible, say so; do not claim visual parity.
