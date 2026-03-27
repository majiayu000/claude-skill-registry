---
name: pr-shiny-main-omega
description: "{{ 𝛀𝛀𝛀 }} Create a pull request to main"
model: opus
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Bash(gh:*)", "Read", "Glob", "Grep"]
argument-hint: [screenshot files]
---

<steps>
    <step num="1">Look at the commits on this branch</step>
    <step num="2">Analyse the overall effect of these changes if merged into `main`</step>
    <step num="3">Use `<template>` to write the pull request content</step>
    <step num="4">Check for my approval; If approved, create a **DRAFT** PR to `main`. If not, incorporate changes and repeat step 3</step>
</steps>
<rules>
    <general>Use ${template} exactly</general>
    <section-specific>
        <title>
            <rule num="1">Brief & descriptive</rule>
            <rule num="2">Use title case</rule>
            <rule num="3">Be understandable to non-devs</rule>
        </title>
        <summary>Describe the PR with a non-technical, absurd metaphor.</summary>
        <tldr>List any steps devs must take after pulling this down</tldr>
        <screenshots>For each named screenshot in $ARGUMENTS, use collapsible `<details>`</screenshots>
        <changes>Break changes into files or categories depending on PR scope; use collapsible `<details>`</changes>
    </section-specific>
</rules>
<template>
    ```md
    # {{ title }}
    ## Overview
    {{ overview }}
    ## Summary
    {{ absurd metaphor }}
    > [!TIP]
    > {{ tldr }}
    ---
    <details>
        <summary><h2>Screenshots</h2></summary>
        `${screenshots in collapsible <details`>}`
    </details>
    ---
    ## Changes
    `${changes in collapsible <details`>}`
    ---
    ```
</template>
