---
name: ase-code-dissect
argument-hint: "[--help|-h] [--max-parts|-m <count>] [--staged|-s] [--dry|-d] [--force|-f] [<dissect-hint>]"
description: >
    Dissect the current Git change set, treated as an epic, domain-wise
    and logically into cohesive parts and materialize each part in its
    own dedicated Git WorkTree. Use when the user calls to "dissect",
    "split", "break up", or "decompose" a large change set into atomic,
    separately committable parts.
user-invocable: true
disable-model-invocation: false
effort: xhigh
allowed-tools:
    - "Bash(git *)"
    - "Bash(rm -f *)"
    - "Write"
    - "Read"
    - "Edit"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-code-dissect">
Dissect a Change Set
</purpose>

<expand name="getopt"
    arg1="ase-code-dissect"
    arg2="--max-parts|-m=8 --staged|-s --dry|-d --force|-f">
    $ARGUMENTS
</expand>

<objective>
*Dissect* the current Git change set, treated as an *epic*, domain-wise
and logically into *cohesive parts*, and materialize every part in its
own dedicated *Git WorkTree*, so each part can be reviewed and
committed *atomically* and *independently*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-common-dissect.md

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Change Set and Hint">

    1.  Determine the *dissection hint*: set
        <dissect-hint><getopt-arguments/></dissect-hint>, with any
        leading and trailing whitespace stripped. Additionally, inherit
        the always existing <ase-project-id/> from the current context,
        as it names the worktrees and branches of all derived parts.

        <if condition="<dissect-hint/> is not empty">
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ⇌ hint: **<dissect-hint/>**
        </template>
        </if>
        <else>
        No dissection hint was given, so the parts are derived from the
        change set alone. Do not output anything.
        </else>

    2.  Determine the *repository root* by running the corresponding
        command (taken exactly as given) and capturing its output into
        <repo-root/>:

        `git rev-parse --show-toplevel`

    3.  Determine the *diff details* and the *diff statistics* by
        running the corresponding commands (taken exactly as given) and
        capturing their full outputs into <diff/> and <stat/>:

        <if condition="<getopt-option-staged/> is equal `true`">
        `git diff --cached HEAD`

        `git diff --cached --numstat HEAD`
        </if>
        <else>
        `git diff`

        `git diff --numstat`
        </else>

    4.  <if condition="<getopt-option-staged/> is not equal `true`">
        Additionally, *fold in the untracked files* -- they are part of
        the working copy change set, but carry no diff of their own.
        Determine them *read-only* by running the corresponding command
        (taken exactly as given):

        `git -C "<repo-root/>" ls-files --others --exclude-standard`

        *Skip* every listed entry below the `.ase/` directory -- it
        carries *ASE*'s own state and the worktrees created by this very
        skill, and hence is never part of the user's change set.

        Then, for *every* remaining listed file, capture its creation
        diff by running the corresponding command (taken exactly as
        given) and *append* its output to <diff/>:

        `git -C "<repo-root/>" diff --no-index --binary /dev/null "<file/>"`

        This command intentionally exits with a non-zero status,
        because the two compared paths differ; treat this exit status
        as *success*, not as an error. Judge the *outcome* by the
        *output* instead: a run which emits *no* diff on standard output
        but an `error:` or `fatal:` message (e.g. the entry is a *nested*
        Git repository, which `git ls-files` reports as a directory) is a
        *real* failure -- append nothing for that entry and only output
        the following <template/>, then continue with the next file:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ⊘ untracked: `<file/>`, ▶ status: **not foldable into the change set**
        </template>
        </if>
        <else>
        Untracked files are *not* folded in under `--staged`/`-s`,
        because they are by definition *not* part of the Git index. Do
        not output anything.
        </else>

    5.  <if condition="<diff/> is empty">
        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ▶ status: **no changes to dissect**
        </template>
        </if>

    </step>

2.  <step id="STEP 2: Dissect Change Set">

    1.  *Derive the parts* of the epic:

        <expand
            name="dissect-derive"
            arg1="ase-code-dissect"
            arg2="<dissect-hint/>"
            arg3="<ase-project-id/>"
        >
        the individual hunks of the captured <diff/>, weighted by the
        line counts of <stat/> and -- for the folded-in untracked files,
        which carry no <stat/> entry -- by their own diff line counts
        </expand>

        Additionally, try to keep *all* hunks of *one* file in the
        *same* part, and split a file's hunks across parts *only* when
        they are genuinely unrelated -- this keeps the per-part patches
        applicable.

        A *single* hunk is *atomic* here, so rule 3's splitting
        permission does *not* apply to it: you *MUST NOT* break a hunk
        into sub-hunks, because this would require re-computing its `@@`
        header and hence destroy the byte-exactness the per-part
        <patch/> depends on.

    2.  *Report the parts*:

        <expand name="dissect-report" arg1="<ase-project-id/>"></expand>

    </step>

3.  <step id="STEP 3: Detect Target Collisions"
        condition="<getopt-option-dry/> is not equal `true`">

    1.  Determine the *existing worktrees* and *existing branches* by
        running the corresponding commands (taken exactly as given) and
        capturing their outputs:

        `git worktree list --porcelain`

        `git branch --list`

    2.  Set <collisions/> to all <part-id/> of <parts/> for which either
        a worktree directory `<repo-root/>/.ase/worktree/<part-id/>` or
        a branch `<part-id/>` already exists.

    3.  <if condition="<collisions/> is not empty AND <getopt-option-force/> is not equal `true`">
        Only output the following <template/> -- with <collisions/>
        rendered as a comma-separated list of code spans -- and then
        immediately *STOP* processing the entire current skill, leaving
        *all* existing worktrees and branches untouched:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ⊘ collisions: <collisions/>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ✪ dissection: **<n/>** parts, ▶ status: **targets exist**
        </template>

        Directly *after* this <template/>, and *before* stopping, give
        the corrective hint by expanding the following (which, depending
        on the configured <ase-guidance-level/>, may expand into nothing
        and hence emit no output at all):

        <ase-tpl-hint level="minimal">
        Re-run `/ase-code-dissect --force` to remove and re-create the colliding worktrees and branches.
        </ase-tpl-hint>
        </if>

    4.  <if condition="<collisions/> is not empty AND <getopt-option-force/> is equal `true`">
        *Remove* every colliding target by running the corresponding
        commands (taken exactly as given) per colliding <part-id/>, and
        silently ignore the failure of an individual command when the
        corresponding worktree or branch does not exist:

        `git worktree remove --force "<repo-root/>/.ase/worktree/<part-id/>"`

        `git worktree prune`

        `git branch -D <part-id/>`
        </if>

    </step>

4.  <step id="STEP 4: Materialize WorkTrees"
        condition="<getopt-option-dry/> is not equal `true`">

    You *MUST* *NEVER* mutate the *original* working copy in this step:
    do *not* modify, stage, stash, revert, or commit anything outside of
    the freshly created worktrees.

    1.  Set <tmp-dir/> to the value of the `TMPDIR` environment variable
        if it is known in the current session context, and to `/tmp`
        otherwise. Do not output anything.

    2.  For *every* part in <parts/>, in their derived order:

        1.  Assemble <patch/> from the *verbatim* subset of <diff/>
            assigned to this part: keep the complete `diff --git` file
            headers and the complete `@@` hunk headers of the assigned
            hunks, and change *nothing* inside them.

            The captured <diff/> is *byte-exact* input and <patch/> stays
            *byte-exact*, too, because `git apply` rejects even the
            smallest deviation. You *MUST* therefore *NEVER* re-wrap a
            line, re-indent a line, normalize or strip trailing
            whitespace, drop the leading context/`+`/`-` marker column,
            re-encode a character, or omit the trailing newline -- and
            you *MUST* *NEVER* re-render any part of the diff as
            Markdown, so no bullet marker and no inline code span is ever
            introduced into <patch/>.

        2.  Use the `Write` tool to write <patch/> to the patch file
            `<tmp-dir/>/ase-dissect-<part-id/>.patch`.

        3.  Create the worktree by running the corresponding command
            (taken exactly as given), which creates the directory
            *and* -- named after its last path component -- the branch
            <part-id/> from `HEAD`. The `.ase` directory is usually
            git-ignored, so the worktree itself never shows up as a
            change:

            `git worktree add "<repo-root/>/.ase/worktree/<part-id/>"`

            <if condition="this command fails">
            Only output the following <template/>, then *continue* with
            the *next* part -- a single failing part *never* aborts the
            remaining ones:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ◉ part: **<part-id/>**, ▶ status: **worktree failed to create**
            </template>
            </if>

        4.  Apply the patch *inside* the freshly created worktree by
            running the corresponding command (taken exactly as given):

            `git -C "<repo-root/>/.ase/worktree/<part-id/>" apply --whitespace=nowarn "<tmp-dir/>/ase-dissect-<part-id/>.patch"`

            <if condition="this command fails">
            Only output the following <template/>, then *continue* with
            the *next* part -- a single failing part *never* aborts the
            remaining ones:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ◉ part: **<part-id/>**, ▶ status: **patch failed to apply**
            </template>
            </if>

        5.  <if condition="a `CHANGELOG.md` file exists in the created worktree">
            Add *one* new entry to the *first* (most recent) section of
            that `CHANGELOG.md` *inside the worktree*, summarizing
            *this part's* change set only, and strictly aligned with the
            established style and conventions of the project (usually
            `- <change-type/> [<artifact-kind/>]: <summary/>`).

            The *existing* `CHANGELOG.md` is *changed*, never replaced:
            you *MUST* use the `Read` tool to read it and the `Edit` tool
            to insert the single new entry *in place*, and you *MUST*
            *NEVER* use the `Write` tool on it, as this would drop the
            entire remaining change history.

            <if condition="the patch of this part already added an entry to that `CHANGELOG.md`">
            The part's own change set already carries its `CHANGELOG.md`
            entry, so you *MUST* *NOT* add a second one. Keep the entry
            which came with the patch and, if it mentions changes which
            landed in *other* parts, reduce it to *this* part's change
            set only.
            </if>
            </if>
            <else>
            The project keeps no `CHANGELOG.md`, so nothing is added and
            no `CHANGELOG.md` is created. Do not output anything.
            </else>

        6.  Leave the worktree *uncommitted*: do *not* run `git add` and
            do *not* run `git commit`, so the user keeps full control
            over the final commit of every part.

        7.  Only output the following <template/>:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ◉ part: **<part-id/>**, ▶ status: **worktree created**
            </template>

    3.  *Clean up* the temporary patch files by running the
        corresponding command (taken exactly as given) once per
        <part-id/> of the *successfully* materialized <parts/>, and
        silently ignore the failure of an individual command when the
        corresponding patch file does not exist:

        `rm -f "<tmp-dir/>/ase-dissect-<part-id/>.patch"`

        The patch file of a *successful* part is a pure *intermediate*:
        it was already consumed by `git apply` and its content is fully
        preserved in the worktree, so it is removed. The patch file of a
        part whose worktree or patch *failed* is *kept* instead, because
        it is that part's only materialization and would otherwise be
        lost. Do not output anything.

    </step>

5.  <step id="STEP 5: Report Result">

    1.  <if condition="<getopt-option-dry/> is equal `true`">
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ✪ dissection: **<n/>** parts, ▶ status: **dry-run -- no worktrees created**
        </template>
        </if>
        <else>
        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-code-dissect**, ✪ dissection: **<n/>** parts, ▶ status: **change set dissected**
        </template>
        </else>

    2.  Finally, give the closing hints by expanding the following
        (which, depending on the configured <ase-guidance-level/>, may
        each expand into nothing and hence emit no output at all):

        <if condition="<getopt-option-dry/> is not equal `true`">
        <ase-tpl-hint level="minimal">
        The parts are uncommitted in `.ase/worktree/<id>` -- review and commit each of them separately, then remove them via `git worktree remove`.
        </ase-tpl-hint>
        </if>
        <else>
        <ase-tpl-hint level="minimal">
        Re-run `/ase-code-dissect` without `--dry` to actually create the reported worktrees, optionally with a `<dissect-hint>` argument if the reported split is not the intended one.
        </ase-tpl-hint>
        </else>

        <ase-tpl-hint level="normal">
        Use `/ase-meta-diff` and `/ase-meta-review` inside a part's worktree to summarize and review it before committing.
        </ase-tpl-hint>

        <ase-tpl-hint level="verbose">
        Use `/ase-code-dissect --staged` to dissect the staged changes only, `--max-parts <count>` to bound the number of parts, `--force` to re-create already existing worktrees, and a `<dissect-hint>` argument to steer the split.
        </ase-tpl-hint>

    </step>

</flow>
