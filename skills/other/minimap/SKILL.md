---
name: minimap
description: 'Use when a compact current-work view is needed from Git state, recorded repository test evidence, and optional graph.yaml. Return one read-only view that classifies every claim as conquered, disputed, or fog. Don''t use for tasks that require source or remote-system changes.'
---

# Minimap

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Use on an explicit model or human request for a compact view of current work state, including at an SDD phase boundary. |
| Authority | Read-only: inspect local Git state, recorded test evidence, and root graph.yaml only; never mutate files, VCS, credentials, paid services, publications, deployments, or remote state. Never run tests. |
| Side effect | Emit one compact view and write nothing. |
| Done | Every reported claim has exactly one class (conquered, disputed, or fog) and a concise justification from the evidence join, with absent graph knowledge represented as fog. |

## Inputs

- A repository or worktree root, inferred from the current directory when unambiguous.
- Its readable current Git commit, tree identity, tracked changes, conflicts, and relevant branch or upstream state.
- The latest repository test result already recorded by the repository or supplied by the caller. A usable result identifies its checks and outcomes and binds them to a commit identifier or tree digest. Its absence is allowed and produces fog; this skill never creates or refreshes it.
- Optional project-root `graph.yaml`. Its absence is allowed and produces fog for graph knowledge while Git-and-test claims are still rendered.

## Procedure

1. Resolve one repository root and snapshot its read-only Git evidence: current commit and tree identity, tracked dirty paths, conflicts, and branch or upstream facts relevant to the requested view. Do not inspect or report unrelated repositories. Done when: the root is identified and the Git snapshot contains commit SHA, tree identity, dirty path list, conflict list, and branch/upstream state, each read without mutation.
2. Locate the latest already-recorded repository test result using its explicit completion time or repository-defined ordering. If no unique latest result can be established, treat applicable test knowledge as missing and record that reason; never run a test or invent an ordering. Done when: one test result is selected as the latest, or no unique latest exists and the reason is recorded so that test knowledge will be fog.
3. Accept a recorded test result only when it names its checks and outcomes and carries a commit identifier or tree digest. Compare that binding with the current commit or tree. A matching binding is current; a well-formed nonmatching binding is stale and remains contradiction evidence, not current proof. Done when: the selected result is classified as current or stale against the current commit or tree, or it is rejected as malformed and the rejection reason is recorded.
4. Read `references/graph-schema.md`. If root `graph.yaml` exists, read it without modification. Require schema `odin.graph/v1`, a non-empty revision, unique non-empty node IDs, non-empty labels, and edges whose endpoints exist. Accept only node types `Invariant`, `Surface`, `Store`, `Hazard`, and `Decision`, and edge types `constrains`, `reads`, `writes`, and `fails-when`. Reject an unknown schema version, node type, edge type, duplicate node ID, or dangling edge. Ignore unknown top-level and per-record fields. Treat nodes and edges as immutable assertions within their declared revision; do not infer, replan, or alter topology. Done when: `graph.yaml` is parsed and every node and edge passes the schema checks, or it is rejected with the specific violation named, or it is absent and graph knowledge is marked fog.
5. Form the smallest complete claim set from current Git facts, each recorded check outcome, and each valid graph node or edge relevant to the requested work. Preserve source identity for every fact. When `graph.yaml` is absent, add a graph-knowledge claim rather than omitting that source. Do not invent claims or applicability links unsupported by the inputs. Done when: every claim in the set traces to a named source (Git fact, test outcome, or graph node/edge), and no claim exists that lacks a source.
6. For each claim, join all applicable evidence without granting any source global precedence. Classify it `disputed` when applicable sources contradict, proof is stale, or dirty state affects the paths or tree covered by the claim. Otherwise classify it `fog` when applicable evidence is missing. Otherwise classify it `conquered` only when all applicable evidence is current and agrees. Done when: every claim has exactly one classification, and the classification is justified by the specific evidence sources that were joined.
7. Render one compact view with exactly the three class headings `conquered`, `disputed`, and `fog`, including empty headings when a class has no claims. Place every claim under exactly one heading with its supporting source identities and one concise join justification. This single view is the complete SDD-minimap result; emit no second campaign or status map. Done when: the view contains all three headings, every claim appears under exactly one, and each claim line carries its source identities and join justification.

## Failure and recovery

- `blocked: git-unavailable` — return no partial minimap when the repository root or required Git evidence cannot be read. Retry only after the root or read access is corrected.
- `blocked: invalid-recorded-test-result` — return no partial minimap when a present selected artifact cannot be parsed into named checks, outcomes, and a commit or tree binding. Correct or replace the artifact; do not run tests. A genuinely absent or non-uniquely ordered artifact is not this failure and yields fog as defined above.
- `blocked: invalid-graph` — return no partial minimap when a present `graph.yaml` violates the accepted schema. Correct the graph outside this read-only run, then retry. Absence is not invalid and yields fog.
- `blocked: evidence-read-failure` — return no partial minimap when an input changes during the snapshot or cannot be read completely. Retry from a fresh read-only snapshot.

No rollback applies because the procedure performs no mutation. Never suppress a failure or return the done predicate unless every emitted claim has exactly one justified class.

## Output

Return either the complete compact view or one exact `blocked: <failure-class>` result with the failing input and reason. The complete view contains only the `conquered`, `disputed`, and `fog` classes; each entry contains a claim, source identities, and the evidence-join justification.
