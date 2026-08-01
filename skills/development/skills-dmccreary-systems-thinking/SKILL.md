---
name: skills-dmccreary-systems-thinking
description: Here is an example of how we can use the Claude Code Skill Creator Skill
  to
---

# Generate Causal Loop Diagram Skill

Here is an example of how we can use the Claude Code Skill Creator Skill to
generate a new skill that generates CLD diagrams

!!! prompt
    Use the skill-creator skill to create a new skill called 'causal-loop-microsim-generator' that will take as
    input a text description of a causal loop diagram.  The output should be a working microsim that is placed in
    the @docs/sims/{{MICROSIM_NAME}} folder.  The skill will generate the following files: 1. index.md 2. main.html
    3. {{MICROSIM_NAME}}.js for the javascript code. 4. data.json that stores a list of the nodes and edges 5.
    style.css that stores all the CSS for placement.  The JavaScript code will use the vis-network library.  To
    understand the best practices you will analyze the current causal loop diagram examples in @docs/sims.  You
    will also create a SKILL.md file but also create a detailed rules.md file in the assets area of the skills
    folder.  Remind the user to take a screen image and place it in the file {{MICROSIM_NAME}}.png.  Make sure that
    the skill updates the mkdocs.yml file to include the link to the new MicroSim in the nav MicroSim section of
    the mkdocs.yml file.  Use alphbetical ordering for the positioning of the link in the nav section of the
    mkdocs.yml file so all sims are shown in alphabetical order.

    ## Result

    [Causal Loop MicroSim Generator Skill in the Claude Skills GitHub](https://github.com/dmccreary/claude-skills/tree/main/skills/causal-loop-microsim-generator)
