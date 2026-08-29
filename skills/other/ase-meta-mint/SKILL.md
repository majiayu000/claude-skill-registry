---
name: ase-meta-mint
argument-hint: "[--help|-h] [--type|-t uuid|sha1|const|var|class|func|path|name] [--count|-c <count>] [<hint>]"
description: >
    Mint an identifier or a name of a requested type out of a free-text
    hint: a UUID, a SHA-1 digest, a constant, variable, function, or
    class identifier, a path component, or a product-like name. Use when
    the user wants an identifier, id, symbol, slug, or name "minted",
    "coined", "derived", or "generated" from a description.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-meta-mint">
Mint an Identifier or Name
</purpose>

<expand name="getopt"
    arg1="ase-meta-mint"
    arg2="--type|-t=(uuid|sha1|const|var|class|func|path|name) --count|-c=1">
    $ARGUMENTS
</expand>

<objective>
*Mint* an identifier or a name of the requested type out of the
following hint:
<hint><getopt-arguments/></hint>
</objective>

<flow>

1.  <step id="STEP 1: Sanity Check Usage">

    1.  Set <type><getopt-option-type/></type> and set <hint/> to
        <getopt-arguments/> with any leading and trailing whitespace
        stripped.

    2.  Determine the number of identifiers to mint: set <count/> to
        <getopt-option-count/>; if <getopt-option-count/> is
        *non-numeric*, *less than 1*, or *greater than 100*, use the
        default *1* instead.

    3.  <if condition="<hint/> is empty AND <type/> is NOT `uuid`">
        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill -- every type except `uuid`
        needs a hint to derive anything from:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-mint**, ▶ ERROR: expected a `<hint>` argument for type **<type/>**
        </template>
        </if>

    4.  Set <results></results> and <warning></warning> (set both to empty).

    </step>

2.  <step id="STEP 2: Mint Hash-Derived Identifiers" condition="<type/> is `uuid` or `sha1`">

    1.  Call the `ase_mint(type: "<type/>", hint: "<hint/>", count:
        <count/>)` tool of the `ase` MCP server and set <results/> to
        the returned lines of its `text` output, one identifier per
        line. You *MUST* *NOT* derive a UUID or a SHA-1 digest yourself
        -- only the tool hashes correctly and reproducibly.

    2.  <if condition="a line of the `text` output starts with `WARNING:`">
        Remove that line from <results/> and set <warning/> to its text
        with the leading `WARNING:` stripped -- hashing a non-empty
        hint is deterministic, so <count/> was clamped to *1*.
        </if>

    </step>

3.  <step id="STEP 3: Derive Linguistic Identifiers" condition="<type/> is `const`, `var`, `class`, `func`, `path`, or `name`">

    1.  Distill <hint/> into its *essential words*: drop filler words,
        articles, and prepositions, keep the two to four words which
        carry the actual meaning, and order them from the most general
        to the most specific one. Prefer established terminology of the
        surrounding domain over invented wording. Do not output
        anything.

    2.  Assemble <count/> *distinct* candidates from these words,
        ordered best-first, honoring the rules of <type/>:

        -   `const`: an `UPPER_SNAKE_CASE` constant identifier such as
            `FOO_BAR_QUUX` -- upper-case ASCII words joined by `_`,
            never starting with a digit.

        -   `var`: a `lowerCamelCase` variable identifier such as
            `fooBarQuux` -- the *last* part *MUST* be a *substantive*
            (`Quux`) naming *what the value is*, never a verb, as a
            variable holds a thing and not an action.

        -   `func`: a `lowerCamelCase` function identifier such as
            `fooBarQuux` -- the *first* part *MUST* be a *verb* (`foo`)
            naming *what the function does*, as a function performs an
            action and does not hold a thing.

        -   `class`: an `UpperCamelCase` class identifier such as
            `FooBarQuux` -- a substantive phrase naming the modeled
            entity, in singular form and without a `The` prefix.

        -   `path`: a `kebab-case` path component such as
            `foo-bar-quux` -- lower-case ASCII letters, digits, and `-`
            only, never starting or ending with `-`.

        -   `name`: an `UpperCamelCase` *product name* such as
            `FooBarQuux` -- optimize for a *brand*, not for a
            description: short (preferably two to three syllables),
            pronounceable, memorable, and distinctive. Coinages,
            blends, and evocative metaphors are explicitly welcome
            here, and a plain concatenation of the hint words is
            explicitly not.

        Store the candidates in <results/>. Do not output anything.

    </step>

4.  <step id="STEP 4: Render Result">

    1.  <if condition="<hint/> is empty">
        Set <hint-shown>*(none -- random UUID)*</hint-shown>.
        </if>
        <else>
        Set <hint-shown><hint/></hint-shown>.
        </else>

    2.  Output the minted identifiers of <results/>, one per line and
        each enclosed in backticks, with the following <template/>:

        <template>
        <ase-tpl-boxed title="MINT" subtitle="<type/>">
        ●   **HINT**: <hint-shown/>

        ○   `<result-1/>`
        ○   `<result-2/>`
        ○   [...]
        </ase-tpl-boxed>
        </template>

    3.  <if condition="<warning/> is non-empty">
        Additionally output the following <template/> directly below the
        box:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-mint**, ▶ WARNING: <warning/>
        </template>
        </if>

    </step>

</flow>
