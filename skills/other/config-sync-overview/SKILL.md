---
name: config-sync-overview
description: Provide structured config-sync system and directory overview. Use when config-sync architecture guidance is required.
---
## Purpose

Provide a single, governed entry point for config-sync system knowledge, including phase pipeline, backup strategy, target tool mapping, and .claude directory semantics derived from documentation.

## IO Semantics

Input: Questions or tasks that require understanding of config-sync phases, backup layout, target tool directories, or .claude directory structure.
Output: Normalized descriptions of phases, directories, and configuration precedence with pointers to relevant documentation sections.
Side Effects: None. Read-only access to documentation files.

## Deterministic Steps

1. Documentation Loading
   - Load docs/config-sync-guide.md for config-sync architecture, phases, and target tool mapping.
   - Load docs/directory-structure.md for .claude directory semantics and configuration priority.

2. Phase Pipeline Extraction
   - Confirm the eight config-sync phases: collect, analyze, plan, prepare, adapt, execute, verify, report.
   - Record which phases handle backups, verification, and reporting.
   - Expose this pipeline to agents as a stable sequence for planning and reasoning.

3. Target Tool Mapping
   - Extract target tools and their configuration directories from the guide.
   - For each tool, record config directory, key files, and configuration format.
   - Provide this mapping to agents when selecting targets or resolving directory questions.

4. Directory Semantics Extraction
   - Extract meanings of core .claude directories relevant to config-sync: rules/, commands/, docs/, backup/, projects/.
   - Record configuration priority and migration guidance where applicable.
   - Provide concise explanations instead of full documentation dumps.

5. Answer Generation
   - When invoked by agent:config-sync or related agents, answer using extracted pipeline, mappings, and directory semantics.
   - Avoid inventing new paths or phases; answer strictly within the documented model.
   - When information is missing, instruct agents to consult the underlying documentation rather than guessing.

## Validation Criteria

- Phase pipeline in this skill matches docs/config-sync-guide.md.
- Target tool directory mapping matches docs/config-sync-guide.md.
- .claude directory semantics match docs/directory-structure.md.
- Responses remain consistent with documentation and do not introduce undocumented behaviors.
