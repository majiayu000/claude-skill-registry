---
name: ase-arch-discover
argument-hint: "[--help|-h] [--limit|-l=12] <functionality>"
description: >
    Discover additional, third-party components (libraries/frameworks) for
    the technology stack to provide needed functionality.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(npm search --json *)"
    - "Bash(curl -s https://search.maven.org/*)"
    - "Skill"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-arch-discover">
Discover Components
</skill>

<expand name="getopt"
    arg1="ase-arch-discover"
    arg2="--limit|-l=12">
    $ARGUMENTS
</expand>

<objective>
*Discover* additional, *third-party components* (libraries/frameworks)
for the technology stack to *provide* the *needed functionality*
<request><getopt-arguments/></request>.
</objective>

<flow>
1.  <step id="STEP 1: Determine Functionality">
    1.  Derive the needed <functionality/> from the <request/>, but keep
        the functionality description very *brief* but still *precise*.

    2.  If <functionality/> is not clear, not precise, or not specific
        enough, let the *user interactively choose* the intended
        functionality.

        In the following, you *MUST* *NOT* use your built-in
        <user-dialog-tool/> tool! Instead, you *MUST* just show a
        custom dialog according to the expanded `custom-dialog`
        definition. You *MUST* closely follow this definition:

        <expand name="custom-dialog" arg1="--no-other">
            Functionality: Which functionality should the components provide?
            <answer-1/>: (grounded candidate functionality 1)
            <answer-2/>: (grounded candidate functionality 2)
            <answer-3/>: (grounded candidate functionality 3)
            <answer-4/>: (grounded candidate functionality 4)
        </expand>

        Then use the <result/> and its corresponding grounded candidate
        functionality to adjust <functionality/> accordingly.

    3.  Display the determined final functionality with just the following
        <template/>:

        <template>
        <ase-tpl-bullet-normal/> **FUNCTIONALITY**: <functionality/>
        </template>
    </step>

2.  <step id="STEP 2: Determine Technology Stack">
    1.  Determine the used technology stack:

        1.  If a file `package.json` is found in the top-level directory
            of the project and contains an entry `typescript` under `dependencies`
            or `devDependencies`, then <stack>TypeScript</stack>.

        2.  Else, if a file `package.json` is found in the top-level directory
            of the project, then <stack>JavaScript</stack>.

        3.  Else, if a file `build.gradle.kts` or `settings.gradle.kts`
            is found in the top-level directory, then <stack>Kotlin</stack>.

        4.  Else, if a file `build.gradle` is found in the top-level directory and
            is applying `kotlin`, `org.jetbrains.kotlin.jvm`, `kotlin-android`,
            or `kotlin-multiplatform` plugins, then <stack>Kotlin</stack>.

        5.  Else, if a file `pom.xml` is found in the top-level directory and
            contains `kotlin-maven-plugin` or `kotlin-stdlib` dependencies, then
            <stack>Kotlin</stack>.

        6.  Else, if a file `pom.xml` or `build.gradle` is found in the top-level directory
            of the project, then <stack>Java</stack>.

        7.  Else, use <stack>Unknown</stack>.

    2.  Display the determined final technology stack with just the
        following <template/>:

        <template>
        <ase-tpl-bullet-normal/> **TECHNOLOGY STACK**: <stack/>
        </template>
    </step>

3.  <step id="STEP 3: Discover Components">
    1.  If <stack/> is "Unknown", the technology stack could not be
        determined and no component discovery backend is available.
        Inform the user with just the following <template/> and then
        *STOP* the entire flow (do not perform any further steps):

        <template>
        <ase-tpl-bullet-normal/> **RESULT**: technology stack could not be determined -- component discovery is only supported for JavaScript, TypeScript, Java, and Kotlin projects.
        </template>

    2.  From <stack/> and <functionality/>, derive essential keywords
        <keyword-L/> (L=1-M), which allow you to search for suitable
        components.

    3.  Determine the *candidate pool size* <pool/> as twice the
        <getopt-option-limit/> (i.e. <pool/> = 2 &times;
        <getopt-option-limit/>). Each discovery source below may fetch up
        to <pool/> candidates so that the later ranking and trimming
        (which alone is governed by <getopt-option-limit/>) has a
        meaningful set to choose from.

        In the to be discovered candidate set of components <component-K/>
        (K=1-C, where C is the merged and deduplicated candidate count),
        remember the component name as <name-K/>, the
        official package name as <package-K/>, the latest version as
        <version-K/>, the stars as <stars-K/>, the created date as
        <created-K/>, the last updated date as <updated-K/>, the total
        number of downloads in the last month as <downloads-K/>.

    4.  If <stack/> is "JavaScript" or "TypeScript":

        1.  Based on the essential keywords <keyword-L/> (L=1-M),
            use the `ase-meta-search` skill in a subagent to *generally*
            discover an initial set of a maximum of <pool/> *NPM packages*
            <component-K/> and at least their real name <name-K/> and
            their unique package names <package-K/>.

        2.  Use the shell command `npm search --json --searchlimit <pool/>
            "<keyword-1/>" [...] "<keyword-M/>"` to *specifically*
            discover an additional set of a maximum of <pool/> *NPM packages*
            <component-K/> and at least their unique package names
            <package-K/>, based on the essential keywords <keyword-L/>
            (L=1-M). Merge the results into the already existing result
            set, but deduplicate entries.

    5.  If <stack/> is "Java" or "Kotlin":

        1.  Based on the essential keywords <keyword-L/> (L=1-M),
            use the `ase-meta-search` skill in a subagent to *generally*
            discover an initial set of a maximum of <pool/> *Maven packages*
            <component-K/> and at least their real name <name-K/> and
            their unique Maven coordinates <package-K/> of the form
            `groupId:artifactId`.

        2.  Use the shell command `curl -s 'https://search.maven.org/solrsearch/select?q=<keyword-1/>+[...]+<keyword-M/>&rows=<pool/>&wt=json'`
            to *specifically* discover an additional set of a maximum
            of <pool/> *Maven packages* <component-K/> and at least their
            unique Maven coordinates <package-K/> (i.e. `<g/>:<a/>` from
            each result document's `g` and `a` fields), based on the
            essential keywords <keyword-L/> (L=1-M). Merge the results
            into the already existing result set, but deduplicate
            entries by Maven coordinate.

    6.  Call the `ase_component_info(stack: "<stack/>", components:
        [ "<package-1/>", ..., "<package-C/>" ])` tool of the `ase` MCP
        server *once* for the entire candidate set of discovered packages.
        The tool dispatches internally on <stack/> and fetches all
        metadata in maximum parallel and returns an array of objects `{
        name, version, created, updated, repository, stars, downloads,
        rank }`. For each
        component <component-K/> (K=1-C) read from its corresponding
        entry: <version-K/> from `version`, <updated-K/> from `updated`,
        <created-K/> from `created`, <repository-K/> from `repository`,
        <stars-K/> from `stars` (numeric or `N.A.`), <downloads-K/>
        from `downloads` (numeric or `N.A.`) and <rank-K/> from `rank`
        (numeric).

    7.  Sort, in descending order, the discovered candidate components
        <component-K/> (K=1-C) by their `rank` field and trim the result
        list to just a maximum of <getopt-option-limit/> total components,
        which establishes the final retained set <component-K/> (K=1-N,
        where N is at most <getopt-option-limit/>). All subsequent steps
        operate solely on this retained set.

    8.  For each component <component-K/> (K=1-N), research and then
        decide which *one* of *USP* (Unique Selling Point -- what makes
        it unique), *Crux* (what you should notice), or *Gotcha* (what
        you should not stumble over) is its single most distinguishing
        perspective, and remember this as an <info-K/> (K=1-N) formatted
        like `<type/>: <hint/>` where <type/> is one of `USP`, `Crux`,
        or `Gotcha` and <hint/> is a 1-6 word hint. Do not output
        anything.
    </step>

4.  <step id="STEP 4: Report Components">
    1.  Display the determined, individual components as a Markdown
        *table* with just the following <template/> and do not output
        anything else:

        <template>
        <ase-tpl-bullet-normal/> **COMPONENT HINTS**:

        | ⚑ *Component* | ▣ *Package*    | ⚖ *Hint*  |
        | :------------ | :------------- | :-------- |
        | **<name-1/>** | `<package-1/>` | <info-1/> |
        [...]
        | **<name-N/>** | `<package-N/>` | <info-N/> |
        </template>

    2.  Display the discovered components as a Markdown *table*
        with just the following <template/>:

        <template>
        <ase-tpl-bullet-normal/> **COMPONENT RANKING**:

        | ⚑ *Component* | ▣ *Package*    | ❖ *Version*  | ↓ *Downloads*      | ⎈ *Stars*      | ⏲ *Updated*      | ☆ *Created*  |
        | :------------ | :------------- | -----------: | -----------------: | -------------: | :--------------- | :----------- |
        | **<name-1/>** | `<package-1/>` | <version-1/> | **<downloads-1/>** | **<stars-1/>** | **<updated-1/>** | <created-1/> |
        [...]
        | **<name-N/>** | `<package-N/>` | <version-N/> | **<downloads-N/>** | **<stars-N/>** | **<updated-N/>** | <created-N/> |
        </template>
    </step>
</flow>

