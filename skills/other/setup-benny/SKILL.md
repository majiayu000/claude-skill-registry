---
name: setup-benny
description: 'Use when installing a third-party automation pack or template repository safely and deterministically. Fetches the source archive, verifies every file against an expected manifest of hashes, applies required transformations using strict unique anchors, checks for destination conflicts, and atomically moves files to the target with a saved rollback manifest. Not for unattended runs; requires explicit human invocation.'
disable-model-invocation: true
---

# Install automation pack

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User needs to install a third-party automation pack or template repository safely and deterministically |
| Authority | Reversible local write (hash-guarded rollback). Explicit human invocation starts the install; preview every target and consequence before writing |
| Side effect | Fetches the source archive to a scratch location, verifies all files against expected hashes, applies placeholder transformations, and atomically moves files to the target directory |
| Done | The pack is installed in the target directory and passes safety checks |

## Inputs

- Source archive URL (required): the URL to fetch the pack or template repository from.
- Target directory (required): the local path where the pack will be installed.
- Expected file manifest with hashes (required): a mapping of file paths to expected SHA-256 hashes, used to verify every extracted file.
- Required file transformations (required): placeholder replacements keyed by strict unique anchors, applied to specified files after extraction.

## Procedure

1. Fetch the source archive to a scratch location. Download the archive from the source URL to a temporary directory. Done when: the archive is downloaded and extracted to the scratch location.
2. Verify all extracted files against the expected manifest and blob IDs. For every file in the extracted tree, compute its SHA-256 hash and compare against the expected manifest. Fail with hash mismatch if any file's hash does not match. Done when: every extracted file's hash matches the expected manifest.
3. Apply required transformations using strict unique anchors. For each transformation: locate the unique anchor string in the target file, replace it with the specified value, and confirm the anchor was found exactly once. Fail if an anchor is not found or appears more than once. Done when: all transformations are applied and every anchor was found exactly once.
4. Check the target directory for conflicts. If the target directory exists and contains files, compare each existing file's hash against the managed-state manifest from a prior install. Block if existing files differ from managed state, indicating manual modifications. Done when: the target directory is confirmed empty or matches prior managed state.
5. Atomically move files to the target and save the applied manifest for rollback. Move all files from the scratch location to the target directory in one operation. Write the applied manifest (file paths, post-transformation hashes, and the original source URL) to a managed-state file beside the target for rollback on future runs. Done when: all files are moved to the target and the applied manifest is saved.

## Failure and recovery

- Hash mismatch: a file's computed hash does not match the expected manifest. Stop before moving any file to the target. Report the mismatched file, expected hash, and actual hash. The scratch directory is cleaned up.
- Transformation anchor not found: a required anchor string is absent from the target file or appears more than once. Stop before moving any file to the target. Report the anchor and the file. The scratch directory is cleaned up.
- Destination conflict: the target directory contains files whose hashes differ from the prior managed-state manifest, indicating manual modifications. Stop before overwriting. Report the conflicting files and their expected versus actual hashes. Do not overwrite user modifications.
- Rollback: if any step fails after files have been moved to the target, use the saved applied manifest to restore the target to its pre-install state: remove installed files and restore any prior managed-state files from the manifest.

## Output

The pack installed in the target directory with all files passing hash verification and transformations applied, plus a saved applied manifest enabling rollback on future runs.
