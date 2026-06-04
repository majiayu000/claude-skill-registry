---
name: art-director
description: Orchestrate iterative visual style searches with branch prompts, decision graphs, feedback loops, and final direction selection.
---

# Art Director

Use this skill when the work is an art-direction search for a media production workspace.

The skill coordinates this loop:

```text
brief -> references -> generation branches -> HTML preview -> feedback -> next branches -> selected direction
```

For single-image production, use the host repo's image-generation or media-run instructions. For comic pages, albums, storyboards, or platform-specific assets, use the host repo's format-specific playbook when one exists.

## Default Output Shape

For a project under `art-direction/<project>/`, each serious search pass should leave:

```text
art-direction/<project>/
  prompts/vNN/YYYY-MM-DD-vNN-<slug>-prompts.md
  process/vNN/YYYY-MM-DD-vNN-<slug>-log.md
  styles/YYYY-MM-DD-<style-system>.md
  assets/vNN-<slug>/
    <variant-id>.png
  vNN-<slug>.html
```

For a first run in an empty workspace, create the minimal folders before writing prompts:

```bash
mkdir -p art-direction/<project>/{prompts/v01,process/v01,styles,assets/v01-style-search}
cp skills/art-director/assets/style-search-map-template.html art-direction/<project>/v01-style-search.html
```

If the skill was installed without `assets/style-search-map-template.html`, create the same folders and write a simple local HTML preview from the cluster schema in this file.

If the run continues an existing direction, increment `vNN` and make every new node point back to its parent decision.

The visual map must be an iteration-cluster direction graph:

```text
idea
  -> iteration cluster
      -> option leaf nodes
      -> selected option node
      -> carry forward / drop
  -> next iteration cluster
      -> option leaf nodes
      -> selected option node
      -> output
```

Keep the important path explicit: iteration checkpoint -> option nodes -> selected option node -> next iteration checkpoint. Unselected options stay as leaf nodes with their status.

## Workflow

1. Read the current project files: `index.html`, latest `vNN-*.html`, `process/v*/`, `prompts/v*/`, `styles/`, and relevant `research/`.
2. Identify the active question: what style, artifact, audience, format, or campaign is being decided.
3. Build an iteration cluster before generation: incoming brief, 3-8 option leaves, difference axes, expected selection criteria, and what may carry forward.
4. Write prompts in `prompts/vNN/`. Each prompt needs iteration id, option id, role, difference axis, prompt, negative prompt, and reject criteria.
5. Generate or collect assets through the host repo's approved image-generation path.
6. Create or update the HTML direction map as the first section of `vNN-<slug>.html`.
7. Put preview cards under the map with anchors matching tree node ids.
8. Capture feedback as first-class nodes in the tree and in `process/vNN/...log.md`.
9. Create the next iteration from feedback: `feedback -> interpretation -> new branch -> asset -> decision`.
10. Mark selected, rejected, paused, and next branches explicitly.

## Iteration Cluster Contract

Every style-search HTML page starts with a direction graph that answers:

- Where did this visual direction come from?
- What was the brief for each iteration?
- Which option leaf nodes were shown for that iteration?
- Which option was selected?
- What changed in the next brief because of that selection?
- What was carried forward, dropped, or turned into output?

Use `skills/art-director/assets/style-search-map-template.html` as the starter preview when the host repo has no renderer yet. If a reusable host-repo renderer exists, record its path in the run log and use it as the local reference. A typical reusable setup is:

- proof page: `art-direction/<project>/vNN-dagre-full.html`;
- shared renderer/data shape: `art-direction/<project>/vNN-style-search-pages.js`;
- shared visual style: `art-direction/<project>/vNN-style-search-page.css`;
- graph runtime: a pinned dagre runtime, for example `@dagrejs/dagre@1.1.8`, when external network use is allowed by the host repo.

Serve preview pages through a local server:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/...`. If the preview depends on a CDN and the network is blocked, report the blocker and keep the run in `blocked` or `needs-local-runtime` status. Store third-party library source only when the host repo policy explicitly allows vendored dependencies.

## Dagre Rendering Contract

Recommended solution: dagre computes the graph layout; the page renders the graph as static HTML/SVG with a detail panel.

Responsibilities:

- dagre: node coordinates and edge routing for the directed decision graph;
- page JavaScript: graph schema normalization, DOM/SVG rendering, click handlers and validation;
- HTML/CSS: readable node cards, status colors, horizontal scroll and detail panel;
- detail panel: shows the selected node's body text and image asset when available.

Use manual SVG layout only as a fallback or baseline. Use Mermaid for docs and quick sketches only when dense style-search history is not required.

Required graph semantics:

- root idea node;
- iteration checkpoint nodes;
- option nodes for each iteration;
- selected option node connects to the next checkpoint;
- unselected options remain leaves;
- production output nodes attach to the producing checkpoint or selected option;
- visible labels use the iteration id, for example `V8-C`, so later readers can map preview cards back to the run log.

Cluster schema:

```json
{
  "id": "v8",
  "title": "V8 - Selected direction expansion",
  "brief": "Expand user-liked directions from V7.",
  "looked_at": "V8-A, V8-B, V8-C, V8-D",
  "selected": "v8-c",
  "parent": "v7",
  "carry_forward": "V8-C: sharp typography, high-contrast palette, warning label rhythm.",
  "drop": "Soft abstract metaphors as the main cover style.",
  "feedback": {
    "target": "v8-c",
    "safe_summary": "Reviewer wants the sharp typography direction pushed further.",
    "interpretation": "Intensify type scale and warning-label rhythm in V9."
  },
  "options": [
    {"id": "v8-a", "title": "V8-A - Soft sculpture system", "status": "shown"},
    {"id": "v8-c", "title": "V8-C - Brutal manifesto", "status": "selected"}
  ],
  "preview": "assets/v8-selected-directions/c-brutal-typography.png",
  "next": "v9",
  "terminal_status": "needs-feedback"
}
```

Required cluster fields:

- `id`
- `title`
- `brief`
- `looked_at`
- `options`
- `selected`
- `parent` when the cluster continues or forks a prior cluster
- `carry_forward`
- `drop`
- `feedback` when reviewer feedback exists
- `preview` when a representative image exists
- `next` unless the cluster is terminal

Required option statuses:

- `selected`
- `rejected`
- `shown`
- `output`

Terminal status values:

- `selected-final`
- `needs-feedback`
- `blocked`
- `needs-local-runtime`
- `reset`

## HTML Preview Rules

- The decision graph is the first visible section after the header.
- Every iteration cluster shows brief, looked-at variants, options, carry-forward, and dropped motifs.
- Option leaves render as visible nodes attached to their iteration checkpoint.
- Selected option nodes are highlighted and visually connect to the next iteration cluster.
- Production outputs attach to the cluster that produced them.
- The page includes a compact legend for status colors.
- The page includes a current selection block when a direction is selected.
- The page includes a next iteration block when feedback has created follow-up branches.
- The page is static HTML and is previewed through a local server.
- Every node with a representative image opens that image in a detail panel or links to a visible preview card.

Avoid duplicating the same graph nodes immediately below as cards or a second table. Add a legend, selected detail, or next-iteration block only when it answers a different question.

## Feedback Loop

When feedback arrives after a preview:

1. Record a redacted feedback summary in `process/vNN/...log.md`.
2. Quote raw feedback only when the source is safe for the repo visibility and the user has allowed it.
3. Add or update the iteration cluster's `feedback`, `carry_forward`, and `drop` fields.
4. Convert the feedback into 1-3 direct design operations: keep, drop, intensify, soften, merge, split, resize, reframe, change format, change reference.
5. Create the next iteration cluster with the changed brief and option leaves.
6. Generate the next branch set after the new cluster is visible in the HTML map.

Comment log format:

```md
## Feedback - YYYY-MM-DD HH:MM

Target node: `v12-03-operating-cards`

Safe summary:
> ...

Interpretation:
- Keep:
- Drop:
- Next branch:
```

## Branch Planning Rules

A good branch set varies real design architecture:

- layout system;
- palette role;
- typography behavior;
- image medium;
- narrative metaphor;
- artifact format;
- density;
- target platform;
- production layer: bitmap image, HTML/CSS overlay, carousel, comic, video storyboard, or another host-approved format.

Weak branch sets vary only color, mood words, or superficial adjectives.

Diversity gate:

- Use 3-8 option leaves.
- Cover at least three materially different axes across the set.
- Fail the branch plan if options differ only by palette, mood words, or adjectives.

## Selection Rules

Record selection as an operational decision:

- selected node id;
- why it won;
- what stays invariant;
- what must be removed;
- where the direction will be used next;
- required next asset or generation pass.

If the reviewer rejects the whole pass, make a new root child named `reset` and record the failure mode before generating again.

## Privacy And Source Rules

- Keep private chats, private screenshots, auth material, billing records, customer records, infrastructure details, and non-public repository links out of prompts, previews, READMEs, and public logs.
- Use repo-relative paths in run logs and examples.
- Replace internal project names with generic examples before publishing a reusable skill.
- Public references need source URL, author or owner, access date, and a usage boundary.
- Exact protected characters, brands, logos, or artist-style references need explicit rights, license, or editorial-risk notes in the host repo run log.

## Validation

Run the narrow checks that match the pass:

```bash
test -f art-direction/<project>/vNN-<slug>.html
rg -n "dagre|style-tree-data|cluster|graph|node-details" art-direction/<project>/vNN-<slug>.html
test -f art-direction/<project>/process/vNN/YYYY-MM-DD-vNN-<slug>-log.md
test -f art-direction/<project>/prompts/vNN/YYYY-MM-DD-vNN-<slug>-prompts.md
rg -n "feedback|carry_forward|drop|selected|terminal_status" art-direction/<project>/vNN-<slug>.html
git diff --check
```

If the preview uses an external CDN, also check the pinned runtime:

```bash
curl -I -L --max-time 10 https://cdn.jsdelivr.net/npm/@dagrejs/dagre@1.1.8/dist/dagre.min.js
```

For local visual review:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/...` and verify:

- the tree renders;
- every tree node with an asset links to a visible card;
- clicking a node opens its description and image in the detail panel;
- node count and edge count are greater than zero;
- the selected path exists;
- every referenced asset path resolves or is marked as pending;
- selected, rejected, and next states are visible;
- the current selection and next iteration are understandable from files.
