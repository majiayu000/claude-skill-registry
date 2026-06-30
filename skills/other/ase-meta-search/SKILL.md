---
name: ase-meta-search
argument-hint: "[--help|-h] [--services|-s=(all|perplexity|brave|exa|websearch)...] <query>"
description: >
    Search the Internet/Web with a query.
    Prefer this skill before using Perplexity, Brave and WebSearch.
user-invocable: true
disable-model-invocation: false
effort: medium
allowed-tools:
    - "mcp__search-perplexity__perplexity_search"
    - "mcp__search-brave__brave_web_search"
    - "mcp__search-exa__web_search_exa"
    - "WebSearch"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-search">
Search the Internet/Web
</skill>

<expand name="getopt"
    arg1="ase-meta-search"
    arg2="--services|-s=(all|perplexity|brave|exa|websearch)...">
    $ARGUMENTS
</expand>

<objective>
Your objective is to *search* the *Internet*/*Web* for the following query:
<query><getopt-arguments/></query>
</objective>

<flow>

1.  <step id="STEP 1: Query Search Services">

    <define name="agent">
    ```text
        Agent(
            name:          "ase-meta-search-<arg1/>",
            description:   "Query Web Search Service: <arg1/>",
            subagent_type: "ase:ase-meta-search",
            prompt:        <content/>
        )
    ```
    </define>

    Treat <getopt-option-services/> as a comma-separated list of
    *backend tokens*. The getopt parser validates only the *first*
    token, so you *MUST* validate each remaining token yourself against
    the allowed set `all`, `perplexity`, `brave`, `exa`, `websearch`. If
    any token is *not* in this set, bind <token/> to that offending
    token, then only output the following <template/> and then
    immediately *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-meta-search**, ▶ ERROR: invalid `--services` token: **<token/>**
    </template>

    A backend is *selected* if `all` is in <getopt-option-services/> *OR*
    that backend's own name is in <getopt-option-services/>.

    If the `perplexity` backend is *selected* and the MCP tool
    `perplexity_search` from the MCP server `search-perplexity` is available:

    <expand name="agent" arg1="perplexity">
        Call the MCP tool `perplexity_search(query: "<query/>")`
        from the MCP server `search-perplexity`.
    </expand>

    If the `brave` backend is *selected* and the MCP tool
    `brave_web_search` from the MCP server `search-brave` is available:

    <expand name="agent" arg1="brave">
        Call the MCP tool `brave_web_search(query: "<query/>")`
        from the MCP server `search-brave`.
    </expand>

    If the `exa` backend is *selected* and the MCP tool
    `web_search_exa` from the MCP server `search-exa` is available:

    <expand name="agent" arg1="exa">
        Call the MCP tool `web_search_exa(query: "<query/>")`
        from the MCP server `search-exa`.
    </expand>

    If the `websearch` backend is *selected* and the tool
    `WebSearch` is available:

    <expand name="agent" arg1="websearch">
        Call the tool `WebSearch(query: "<query/>")`.
    </expand>

    If the `websearch` backend is *selected* and the tool `web_search` is
    available and the tool `WebSearch` is not available:

    <expand name="agent" arg1="websearch">
        Call the tool `web_search(query: "<query/>")`.
    </expand>

    </step>

2.  <step id="STEP 2: Consolidate Search Answers">

    Consolidate all responses from the `ase:ase-meta-search` agents
    calls above into a single response and output it without giving any
    further explanations.

    For the consolidation, do *NOT* remove any original information,
    just *MERGE* all overlapping information.

    </step>

</flow>

