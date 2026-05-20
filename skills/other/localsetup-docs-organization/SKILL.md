---
name: localsetup-docs-organization
description: "Repo-level docs router: classify documentation requests, propose paths and filenames, and keep indexes in sync."
metadata:
  version: "0.1.0"
---

# docs-organization

Docs-organization is the repo-level router for documentation work. It decides where docs live, how they are named, and how the indexes stay current.

Use this skill whenever an agent is:

- Creating a new doc
- Moving or renaming a doc
- Making a significant update to an existing doc

The goal is to keep docs discoverable, avoid duplicate trees, and keep both machine and human indexes in sync without blocking non standard work.

## Inputs

Inputs are passed as a structured object. All fields are repo local and must be treated as untrusted text.

Required:

- intent: short description of what the doc is for
- title: proposed human title

Optional:

- summary: one to three sentence description
- doc_type_hint: coarse type such as `runbook`, `adr`, `spec`, `how_to`, `notes`, `reference`
- tags: list of short strings, usually component names, domains, or features
- allow_nonstandard_docs: boolean, default false, true only when the caller intentionally wants a path that disagrees with the recommended placement

Example input payload:

```yaml
intent: "Document how to rotate API keys for payments service"
title: "Payments API key rotation runbook"
summary: "Step by step runbook for rotating API keys in production for the payments service."
doc_type_hint: "runbook"
tags:
  - "payments"
  - "api-keys"
  - "runbook"
allow_nonstandard_docs: false
```

## Outputs

Outputs describe the recommended category, location, and metadata for the doc, along with any warnings.

Fields:

- category_label: human label for doc category such as `architecture`, `runbook`, `decision_log`, `spec`, `how_to`, `notes`, `reference`
- category_slug: folder safe slug derived from the label, lowercase ASCII, hyphen separated
- component_slug: optional slug for the primary system, feature, or component
- proposed_path: repo relative folder path for the doc, usually under the docs root, for example `docs/incident-runbooks/payments`
- filename: slugified filename with `.md` suffix, for example `payments-architecture-overview.md`
- index_entry: structured record suitable for `docs/index.yaml`
- warnings: list of human readable warning strings, including `nonstandard_location` when overrides happen

Example output payload:

```yaml
category_label: "runbook"
category_slug: "incident-runbooks"
component_slug: "payments"
proposed_path: "docs/incident-runbooks/payments"
filename: "payments-api-key-rotation.md"
index_entry:
  id: "docs-incident-runbooks-payments-api-key-rotation"
  path: "docs/incident-runbooks/payments/payments-api-key-rotation.md"
  title: "Payments API key rotation runbook"
  category_label: "runbook"
  category_slug: "incident-runbooks"
  component_slug: "payments"
  status: "ACTIVE"
  last_updated: "2026-03-09"
  doc_type: "runbook"
  tags:
    - "payments"
    - "api-keys"
    - "runbook"
  nonstandard_location: false
warnings: []
```

## Behavior overview

At a high level this skill:

1. Classifies the request into a category and optional component.
2. Suggests a folder and filename under the docs root.
3. Checks the existing index to see if an update to an existing doc is better than creating a new one.
4. Proposes index changes and the human facing index layout.
5. Enforces strict advisory rules while still allowing deliberate non standard placements.

Later sections describe these steps in more detail.

## Classification and folder slugs

### Classification inputs

When classifying a request, use:

- intent
- title
- summary
- doc_type_hint
- tags

Rules:

- Prefer doc_type_hint when present to choose an initial category_label.
- When doc_type_hint is missing, infer the type from intent, title, and tags. For example, titles containing "runbook" or "playbook" likely map to a runbook category.

### Category labels

Keep the category vocabulary small and repo specific.

Examples of category_label values:

- architecture
- runbook
- decision_log
- spec
- how_to
- notes
- reference

Rules:

- Always prefer reusing category labels already used in this repo.
- Only introduce a new label when the intent clearly does not fit any existing one.

### Category manifest

This skill uses a repo local manifest file to record known categories.

- Path: `docs/.docs-classifications.yaml`
- Structure: list of entries, each with:
  - label: human label
  - slug: folder safe slug
  - description: short explanation of how this category is used in this repo

Behavior:

- On classification:
  - Load the manifest if present.
  - If a label exists that fits the request, reuse it and its slug.
  - If none fit, create a new label and slug, and append it to the manifest.
- The manifest is repo local configuration, not part of the framework. Framework upgrades must not overwrite it.

### Slug generation

Slug rules for category_slug and component_slug:

- Lowercase all letters.
- Replace spaces and separator characters with `-`.
- Drop characters that are not safe across common filesystems.

Examples:

- `Incident runbooks` becomes `incident-runbooks`
- `API reference` becomes `api-reference`
- `User settings panel` becomes `user-settings-panel`

## Proposed path

Docs root:

- Default docs root is `docs/`.
- A repo can override the root using `docs.config.yaml`, but the skill must still work when the config file is absent.

Path rules:

- Base pattern: `docs/<category_slug>/`
- When a clear component_slug exists: `docs/<category_slug>/<component_slug>/`

Guidance:

- Only add more depth when there is a clear structural reason, such as a well known subsystem boundary.
- Avoid deeply nested trees by default.

## Document placement and reuse logic

### Reuse before create

The standard flow for a new request:

1. Run classification to produce category_label, category_slug, component_slug, and proposed_path.
2. Search for existing docs that might be the right place to update.
   - Primary search surface is `docs/index.yaml` if it exists.
   - Use:
     - Title similarity.
     - Shared tags.
     - Same category_label and component_slug.
3. Decide if there is a strong candidate for update.
   - Examples of a strong match:
     - Same component_slug and very similar title.
     - Same category_label and overlapping tags where the topic clearly sounds the same.
4. If there is a strong match:
   - Suggest updating that existing doc.
   - Return both:
     - The proposed new location.
     - The recommended existing path.
5. If the caller chooses update:
   - Keep path and filename from the existing doc.
   - Only change content and metadata.
6. If the caller still wants a new doc:
   - Proceed to new file creation.

### New file creation

Filename behavior:

- Base rule:
  - Slugify the title and append `.md`.
- Conflict handling:
  - If a file already exists at the proposed path:
    - If the topic is clearly the same, suggest merging into the existing doc.
    - If it is genuinely distinct, append a small semantic suffix to the filename, for example:
      - `payments-architecture-overview-v2.md`
      - `payments-architecture-deep-dive.md`

Folder behavior:

- If proposed_path does not exist, it should be created under the docs root when the doc is written.

### Doc metadata header

Managed docs should use minimal front matter to support index operations.

Required metadata:

- status: value from `DOCUMENT_LIFECYCLE_MANAGEMENT.md` such as ACTIVE, PROPOSAL, DEPRECATED
- last_updated: ISO date string
- doc_type: same language as doc_type_hint when appropriate
- tags: list of strings

Update rules:

- On each significant update:
  - Refresh last_updated.
  - Optionally adjust status if the doc has stabilized or changed phase.

## Index design and ownership

This skill maintains two related indexes.

### Machine index: docs/index.yaml

- Path: `docs/index.yaml`

Schema for each entry:

- id: stable identifier
  - Either a deterministic slug derived from the path.
  - Or a generated UUID stored in both the doc header and index.
- path: repo relative path to the doc
- title
- category_label
- category_slug
- component_slug: optional
- status
- last_updated
- doc_type
- tags: list of strings
- nonstandard_location: optional boolean, true when the chosen path disagrees with the skill recommendation

Rules:

- The combination of id and path is the identity for an entry.
- The path may change when docs move, but the id must stay stable.
- When this skill creates, moves, or significantly edits a doc:
  - Update or insert the associated entry in `docs/index.yaml`.

### Human index: docs/INDEX.md

- Path: `docs/INDEX.md`

Content expectations:

- Sections grouped by category_label.
- Within each category:
  - List entries with:
    - Title.
    - Link to path.
    - Optional short description or tags.

Ordering:

- Choose a single rule and keep it consistent in this repo:
  - Alphabetical by title.
  - Or descending by last_updated.

Update rules:

- Treat `docs/index.yaml` as the source of truth.
- Regenerate or patch `docs/INDEX.md` from `docs/index.yaml`, not the other way around.
- Ensure:
  - No stale entries.
  - No missing entries for managed docs.

### Query patterns for other tools

Other agents and tools should use `docs/index.yaml` as their entry point.

Examples:

- To find docs for a category:
  - Filter entries by category_label.
- To find docs for a component:
  - Filter by component_slug.
- To find the primary doc for a topic:
  - Use tags and doc_type to choose the top candidate, for example the main architecture overview for a given service.

## Enforcement rules (strict advisory)

### Normal behavior

Default expectation:

- Docs creation or movement should go through this skill.
- The skill returns:
  - Recommended path and filename.
  - Warnings as needed.

### Handling non standard operations

When a caller wants to use a different path than the recommended one:

- If allow_nonstandard_docs is false:
  - Emit a clear warning that this is non standard.
  - Return both:
    - The recommended location.
    - The requested non standard path.
- If allow_nonstandard_docs is true:
  - Treat this as a deliberate override.

In both cases:

- The index should still be updated.
- The index entry should set nonstandard_location to true when the chosen path does not match the recommended placement.

### Framework docs guardrail

This skill must respect the framework docs boundary.

Rules:

- `_localsetup/docs/` remains the home of framework docs.
- This skill must not redefine where framework docs live.
- It may:
  - Use the same metadata pattern.
  - Help with subfolder organization inside framework docs when requested.
  - But it must not conflict with `DOCUMENT_LIFECYCLE_MANAGEMENT.md` and related framework docs.

## Integration with other Localsetup skills

### Script and docs quality

Reference skill: `localsetup-script-and-docs-quality`.

Rules:

- All markdown and file handling behaviors follow that skill.
- This includes:
  - Encoding and formatting rules.
  - File creation discipline.
  - Handling external input as hostile.

### Humanizer

Reference skill: `localsetup-humanizer`.

Rules:

- For substantial new docs or large rewrites:
  - Recommend or require a pass through the humanizer before finalization.
- Provide a hook in the behavior:
  - Callers can:
    - Generate content.
    - Run it through the humanizer.
    - Then save it via the docs organization index update path.

## Configuration and extensibility

### Optional config file: docs.config.yaml

Path:

- `docs.config.yaml` at the repo root.

Fields:

- root: docs root path, default `docs/`.
- categories: map from category_label to:
  - slug
  - short description
- aliases: map from alternate labels to canonical labels.
- required_front_matter_fields: list of extra metadata fields that this repo expects in doc headers.

Behavior:

- The skill must work without this config file.
- When config exists:
  - It takes precedence over heuristics and the category manifest.
  - New labels can still be added and recorded.

### Future extensions

Examples you can mention but do not need to implement immediately in this repo:

- Rules for when to split large docs.
- Automatic cross linking between related docs using tags and component_slug.
- Audits to:
  - Find nonstandard_location entries.
  - Suggest reorganizations.

## Testing and validation

To validate implementations that follow this skill description, use these scenarios.

### New repo scenario

- Start in a repo with no `docs/` directory.
- Actions:
  - Create:
    - One architecture doc.
    - One runbook.
    - One how to.
- Verify:
  - `docs/` appears with reasonable subfolders.
  - `docs/index.yaml` and `docs/INDEX.md` exist.
  - Entries match expectations for category, component, and tags.

### Messy existing repo scenario

- In a repo with ad hoc docs:
  - Add a new doc for a topic that already has partial coverage.
- Verify:
  - This skill proposes updating an existing doc where it makes sense.
  - New folders are not created that mirror existing ones.

### Move and rename scenario

- Move a doc from one folder to another through this behavior.
- Verify:
  - File path changes.
  - id stays the same.
  - Index entries are updated.

### Override scenario

- Intentionally create a doc in a non recommended location with allow_nonstandard_docs true.
- Verify:
  - Warning is present.
  - Index marks nonstandard_location true.

---
name: localsetup-docs-organization
description: >
  Classify documentation, choose folder slugs, keep an index up to date,
  and encourage updates to existing docs instead of bloat.
metadata:
  version: "0.1.0"
---

# Docs organization skill

## Purpose

This skill is the repo level docs router. It decides where docs live, how they are named, and how the documentation index stays current. It is used for new doc creation, moving docs, and significant doc updates. The goal is to prevent documentation bloat by encouraging updates to existing docs, classifying content into reusable categories, and maintaining both human and machine readable indexes.

## Inputs

Required:

- intent: short natural language description of what the doc is for.
- title: proposed human title.

Optional:

- summary: one to three sentence description of what the doc will cover.
- doc_type_hint: runbook, adr, spec, how_to, notes, reference, or similar.
- tags: list of domain, component, or feature tags, for example ["payments", "batch-jobs"].
- allow_nonstandard_docs: boolean override flag to explicitly allow operations outside the recommended structure. Default is false.

## Outputs

- category_label: generic human label for the doc category, for example "architecture", "runbook", "decision_log", "spec", "how_to", "notes", "reference".
- category_slug: folder safe slug derived from the label, lowercase ASCII and hyphen separated, for example "architecture", "incident-runbooks", "feature-specs".
- component_slug (optional): slug for the primary system or feature, for example "payments" or "auth-service".
- proposed_path: repo relative folder path, for example "docs/incident-runbooks/payments".
- filename: slugified filename for the doc, for example "payments-architecture-overview.md".
- index_entry: structured metadata row suitable for insertion into "docs/index.yaml".
- warnings: list of warning strings, including "nonstandard_location" when overrides are used or when the operation falls outside the normal structure.

## Classification and folder slug behavior

### Classification inputs

The skill uses these inputs to classify a documentation request:

- intent
- title
- summary
- doc_type_hint
- tags

When doc_type_hint is present, it is the primary signal for choosing the category label. When it is missing, the skill infers type from intent, title, and tags.

### Category labels

The skill assigns a category_label such as:

- architecture
- runbook
- decision_log
- spec
- how_to
- notes
- reference

These are examples, not a fixed global list. The rule is:

- Prefer reusing category labels that already exist in this repo.
- Only create a new label when the intent clearly does not fit any existing label.

### Category manifest

The skill maintains a repo local manifest file:

- Path: "docs/.docs-classifications.yaml"

Each entry in this manifest holds:

- label
- slug
- description

On each classification:

- Load the manifest if it exists.
- If a label is available that fits the new intent, reuse that label and its slug.
- If none fit, create a new label and slug, append it to the manifest, and use it for this request.

The manifest is repo specific and is not part of the framework itself.

### Slug generation

Slugs are generated with these rules:

- Lowercase all characters.
- Replace spaces and separators with "-".
- Remove characters that are unsafe on common filesystems.

Examples:

- "Incident runbooks" becomes "incident-runbooks".
- "API reference" becomes "api-reference".

### Proposed path

Docs root:

- Default docs root is "docs/". This can be overridden by an optional "docs.config.yaml" file, but the skill must work without that file.

Path rules:

- Base pattern is "docs/<category_slug>/".
- When a clear component_slug exists, use "docs/<category_slug>/<component_slug>/".

Additional depth is only added when there is a clear structural reason. Deeply nested trees are discouraged by default.

## Document placement and reuse

### Reuse before create

Standard flow for handling a new documentation request:

1. Run classification to produce category_label, category_slug, component_slug, and proposed_path.
2. Search for existing docs that might be the right place to update. The primary search surface is "docs/index.yaml" if it exists. The search considers:
   - Title similarity.
   - Shared tags.
   - Same category_label and component_slug.
3. Decide if there is a strong candidate for update. Examples of a strong match include:
   - Same component_slug and very similar title.
   - Same category_label and overlapping tags where the topic appears to be the same.
4. If a strong match exists:
   - Suggest updating that existing doc.
   - Return both the proposed new location and the recommended existing path.
5. If the caller selects update:
   - Keep path and filename from the existing doc.
   - Change only content and metadata.
6. If the caller still wants a new doc:
   - Proceed to new file creation using the proposed_path.

### New file creation

Filename behavior:

- Slugify the title and append ".md" to create the filename.

Conflict handling:

- If the filename already exists in proposed_path:
  - If the topic is clearly the same, suggest merging instead of creating a second file.
  - If the topic is truly distinct, append a small semantic suffix such as "-v2" or "-deep-dive". For example:
    - "payments-architecture-overview-v2.md"
    - "payments-architecture-deep-dive.md"

Folder behavior:

- If proposed_path does not exist, create it under the docs root.

### Doc metadata header

Each managed doc should include front matter or a compact metadata header with at least:

- status: using lifecycle values from "DOCUMENT_LIFECYCLE_MANAGEMENT.md" (for example ACTIVE, PROPOSAL, DRAFT, DEPRECATED, ARCHIVED).
- last_updated: ISO date string.
- doc_type: for example "runbook", "adr", "spec", "how_to", "reference".
- tags: list of strings.

On each significant update, the skill should refresh last_updated and may adjust status when the change stabilizes the doc and the caller indicates that it is now current.

## Index design and ownership

The skill owns two index files under the docs root.

### Machine index

- Path: "docs/index.yaml"

Schema for each entry:

- id: stable identifier for the doc. It can be a deterministic slug derived from the path or a generated UUID that is stored both in the doc header and the index.
- path: repo relative path to the doc.
- title: human readable title.
- category_label.
- category_slug.
- component_slug (optional).
- status.
- last_updated.
- doc_type.
- tags.
- nonstandard_location (optional boolean).

The combination of id and path identifies a document. Path may change when files move, but id should remain stable.

### Human index

- Path: "docs/INDEX.md"

Content:

- Sections grouped by category_label.
- Within each category, list entries with:
  - Title.
  - Markdown link to the path.
  - Optional short description or tags.

Ordering:

- Use a single rule and keep it consistent. For example:
  - Sort entries alphabetically by title within each category.
  - Or sort entries by last_updated descending within each category.

### Index update rules

Whenever the skill creates, moves, or significantly edits a doc, it must:

- Update or insert the associated entry in "docs/index.yaml".
- Regenerate or patch "docs/INDEX.md" from "docs/index.yaml", not the other way around.

This avoids stale or missing entries. Managed docs should always have a matching index entry.

### Query patterns for other tools

Other agents or tools should treat "docs/index.yaml" as the source of truth for locating docs:

- To find docs for a category, filter entries by category_label.
- To find docs for a component, filter entries by component_slug.
- To find the primary doc for a topic, use tags and doc_type to select the best candidate, such as the main architecture overview for a service.

## Enforcement rules (strict advisory)

### Normal behavior

Default expectation:

- Documentation creation or movement goes through this skill.
- The skill returns the recommended path and filename along with any warnings.

### Handling non standard operations

When a caller wants to use a different path:

- If allow_nonstandard_docs is false:
  - Emit a clear warning that the operation is non standard.
  - Return both the recommended location and the requested non standard path.
- If allow_nonstandard_docs is true:
  - Treat this as a deliberate override.

In both cases:

- Update the index to reflect the actual chosen path.
- Set nonstandard_location true when the chosen path does not match the recommended placement.

### Framework docs guardrail

Framework docs live under "_localsetup/docs/". This skill must not redefine where framework docs live. It may use the same metadata pattern and help with subfolder organization for framework docs where appropriate, but it must not conflict with "DOCUMENT_LIFECYCLE_MANAGEMENT.md" and related framework documentation.

## Integration with other Localsetup skills

### Script and docs quality

This skill composes with "localsetup-script-and-docs-quality". All markdown and file handling behaviors must follow that skill, including:

- Encoding and formatting rules.
- File creation discipline.
- Handling external input and partial failures.

### Humanizer

This skill also composes with "localsetup-humanizer". For substantial new docs or large rewrites:

- Recommend or require a pass through the humanizer before finalization.

Callers can:

- Generate content.
- Run it through the humanizer for style and clarity.
- Then save it and update indexes via this docs organization skill.

## Rules and context wiring

### Cursor rules

For Cursor, add or update rules under ".cursor/rules" to state that:

- When user instructions involve creating or updating documentation, such as:
  - "create documentation for X"
  - "write a runbook"
  - "document this feature"
  - "update the docs for Y"
- Agents should:
  - Invoke "localsetup-docs-organization" first to obtain:
    - proposed_path
    - filename
    - updated index entry

Rules should also state that:

- Nonstandard placements are allowed only with explicit override, and such docs must be marked in the index with nonstandard_location.

### Other platform contexts

For each supported agent host, add a short rule or pointer that:

- Identifies this skill as the default docs router.
- Mirrors the same triggers used for Cursor.

### Framework docs index

If a framework level docs index references skills, add a short entry describing this skill:

- What it does.
- Where its SKILL.md lives.
- Where its rules are documented.

## Configuration and extensibility

### Optional config file

Define an optional repo level configuration file:

- Path: "docs.config.yaml" at repo root.

Fields:

- root: docs root path, default "docs/".
- categories: map from category_label to:
  - slug.
  - short description.
- aliases: map from alternate labels to canonical labels.
- required_front_matter_fields: repo specific extra metadata fields.

Behavior:

- The skill must function without this config file, using heuristics and "docs/.docs-classifications.yaml" instead.
- When "docs.config.yaml" exists, it takes precedence over heuristics where applicable, but the skill can still add new labels to the manifest.

### Future extensions

Potential extensions that do not need to be implemented immediately:

- Rules for when to split large docs into multiple files.
- Automatic cross linking between related docs using tags and component_slug.
- Audit and cleanup helpers that:
  - Find entries with nonstandard_location true.
  - Suggest reorganizations to bring them into the standard structure.

## Testing and validation

To validate this skill, test at least these scenarios in a real repo:

### New repo scenario

- Start with no "docs/" directory.
- Create:
  - One architecture doc.
  - One runbook.
  - One how to doc.
- Verify:
  - "docs/" appears with reasonable subfolders.
  - "docs/index.yaml" and "docs/INDEX.md" exist.
  - Entries match expectations for category, component, and tags.

### Messy existing repo scenario

- In a repo with ad hoc docs, add a new doc for a topic that already has partial coverage.
- Verify:
  - The skill proposes updating an existing doc where it makes sense.
  - New folders are not created that mirror existing ones.

### Move and rename scenario

- Move a doc from one folder to another through this behavior.
- Verify:
  - File path changes.
  - id stays the same.
  - Index entries are updated.

### Override scenario

- Intentionally create a doc in a non recommended location with allow_nonstandard_docs set to true.
- Verify:
  - A warning is present.
  - Index marks nonstandard_location true for that entry.

