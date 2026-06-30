---
name: ase-meta-changelog
argument-hint: "[--help|-h]"
description: >
    Update changes entries in CHANGELOG.md files
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git log *)"
    - "Bash(git diff *)"
    - "Bash(git show *)"
    - "Write"
    - "Edit"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-changelog">
Update ChangeLog Entries
</skill>

<expand name="getopt" arg1="ase-meta-changelog">
    $ARGUMENTS
</expand>

<objective>
Help to complete, consolidate and sort *ChangeLog* entries of the most
recent *ChangeLog* section, based on underlying *Git* commits and staged
changes.
</objective>

Format
------

The *ChangeLog* file is a Markdown formatted file named `CHANGELOG.md`,
and contains sections with headers in the style `N.M.K (YYYY-MM-DD)`.

Each *ChangeLog* entry is always formatted as `<prefix/>: <summary/>`
where the <prefix/> is one of the following tags and their usual related
changes:

    -   `FEATURE`:     new        functionality or configuration
    -   `IMPROVEMENT`: improved   functionality or configuration
    -   `BUGFIX`:      corrected  functionality or configuration
    -   `UPDATE`:      updated    functionality or configuration
    -   `CLEANUP`:     cleaned up functionality or configuration
    -   `REFACTOR`:    refactored functionality or configuration

The <summary/> is not longer than about 60-80 characters. The
*ChangeLog* entries for a single product release version are also always
grouped and sorted according to the above <prefix/> list.

Processing
----------

<flow>

1.  <step id="STEP 1: Locate and read ChangeLog entries">

    The *ChangeLog* file `CHANGELOG.md` is located in the *current*
    directory or one of the *parent* directories of the current project.
    Locate and read this file. Store its relative path in <filename/>.

    You *MUST* *NOT* output anything, except the result with the
    following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **CHANGELOG FILE:** `<filename/>`
    </template>

    </step>

2.  <step id="STEP 2: Determine artifact changes">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **DETERMINE ARTIFACT CHANGES:**
    </template>

    To update to entries of the most recent *ChangeLog* section, consult
    the Git *commits* plus the currently already staged changes in the Git
    *index*, but *ignore* the Git *stash* and still unstaged changes.

    For finding the corresponding Git *commits*, first determine the
    correct baseline Git tag. Take the `N.M.K` from the *first* (most
    recent) level-2 header in the *ChangeLog* file and check whether a
    corresponding Git tag already exists with the command `git tag --list
    N.M.K`. If this command produces *no* output, the first section is
    still in-progress/untagged, so use the `N.M.K` from the *second*
    level-2 header as the baseline tag instead. If this command *does*
    produce output, the first section is already released/tagged, so use
    the `N.M.K` from the *first* level-2 header as the baseline tag. Then
    check all Git commits between `HEAD` and this baseline tag with the
    command `git log N.M.K..HEAD --numstat --pretty=format:'%h: %s'`.

    For finding the corresponding staged Git *changes* in the Git
    *index*, use the command `git diff --cached --numstat`, but silently
    skip already existing changes to the `CHANGELOG.md` file itself. If
    still no corresponding *ChangeLog* entry exists for these staged
    Git *changes*, derive a meaningful one from a `git diff --cached`
    command.

    </step>

3.  <step id="STEP 3: Complete ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **COMPLETE ENTRIES:**
    </template>

    Without immediately modifying the `CHANGELOG.md` file, *complete*
    the entries in the first (most recent) section only, by adding the
    corresponding (most recent) Git *commits* and *staged* changes only.

    For each Git commit, reduce the Git commit messages to a single
    short <summary/> sentence, not longer than 60-80 characters.

    If a <summary/> is too short or especially is not comprehensible
    enough because of too little context information, add some essential
    context, especially references to the class/module/package, etc.
    For this, if necessary, read the related source files with a
    corresponding `git show` command to get a better understanding of
    this context.

    </step>

4.  <step id="STEP 4: Consolidate and sort ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **CONSOLIDATE ENTRIES:**
    </template>

    Without immediately modifying the `CHANGELOG.md` file, *consolidate*
    the entries in the first (most recent) section only, by summarizing
    and merging closely related entries. Perform the entry consolidation
    per <prefix/> group only.

    Without immediately modifying the `CHANGELOG.md` file, *sort* the
    entries in the first (most recent) section only. Instead of the
    chronological commit order, group the entries by the <prefix/>es.

    </step>

5.  <step id="STEP 5: Write modified ChangeLog entries">

    You *MUST* *NOT* output anything, except introduce the current
    operation with an output based on the following <template/>:

    <template>
    <ase-tpl-bullet-signal/> **UPDATING CHANGELOG:**
    </template>

    Finally, *update* the `CHANGELOG.md` file with the completed,
    consolidated and sorted *ChangeLog* entries. Also, update the date
    `YYYY-MM-DD` in the `N.M.K (YYYY-MM-DD)` header of the *first* (most
    recent) section.

    You *MUST* *NOT* output any further summary or give any further
    explanations.

    </step>

</flow>

