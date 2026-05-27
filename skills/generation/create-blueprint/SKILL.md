---
name: create-blueprint
description: Create Renku blueprints for video generation workflows. Use when users want to define custom video generation pipeline using prompt producers, asset producers and compose them into a video.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Blueprint Creation Skill

This skill helps you create Renku blueprints - YAML files that define video generation workflows. Blueprints compose multiple asset generators and prompt generators using AI models into a dependency graph that generates media files and assembles them into final videos.

## Prerequisites

Before creating blueprints, ensure Renku is initialized:

1. Check if `~/.config/renku/cli-config.json` exists
2. If not, run `renku init --root=~/renku-workspace` 
3. The config file contains the `catalog` path where blueprints and producers are installed

Read `~/.config/renku/cli-config.json` to find the **catalog** path, you will be using this to locate the producers and models for the blueprint.

```bash
cat ~/.config/renku/cli-config.json
```

## How to Create Blueprints

### Step 1: Essential Questions for Requirements

Before creating a blueprint, ensure that this information is available in your context and if not ask the user for clarification using the **AskUserQuestion** tool.

#### Description of the workflow in words
The workflow is clearly stated in natural language. It includes a starting point (a prompt producer), how its outputs are used by downstream producers and how they are composed together to form the final workflow. Here is all the required information:
- Folder containing starting point plan producer, with the YAML file that describes the inputs and outputs, JSON schema file for structured content output and a TOML file that describes the system and user prompts with variable substitutions. 
- Verbal description of different types of media to be used in the video. 

Below are some examples and what you can deduce:
**IMPORTANT** If you cannot deduce or have doubts, always use the **AskUserQuestion** tool to clarify.

**Example 1**
User Prompt: Use the @link/to/folder producer to plan the documentary video. The video will optionally contain KenBurns style image transitions, video clips for richer presentation, optional video clips where an expert talks about some facts, a background audio narrative for the images and videos and a background music.

With the above user provided summary, you know:
- The exact producer to plan the overall video with the output schema that tells what artifacts (prompts, conditionals, text for audio narration etc.) it will generate.
- The producers to use for media generation: text-to-audio for narrative audio, text-to-video for optional video segments, text-to-image for optional image segments, text-to-talking-head for optional video clips with audio narration by an expert, text-to-music for music generation.
- Your final composition will be composed of 4 tracks and a user configurable number of segments. 
  - Track 1: Audio for narrative 
  - Track 2: Video for video clips and talking head videos
  - Track 3: Image for images to be used with KenBurns style effects.
  - Track 4: Music for background music
- Each segment may or may not have assets for each track depending on how the plan producer lays out the flow with the conditionals it generate.

In catalog, we have an example of this blueprint: `catalog/blueprints/documentary-talking-head`

**Example 2**
User Prompt: Use the @link/to/folder producer to plan a commercial that depicts the use a product by a character. The character image should be generated and consistent throughout. There are various video clips that depicts the use of the product. Some video clips may use audio. There should be background music.

With the above user provided summary, you know:
- The exact producer to plan the overall video with the output schema that tells what artifacts 
- The producers to use for media generation: text-to-image for character image, image-to-video for video clips and using audio (or text to be used as audio), text-to-music
- Your final composition will be composed of 2 tracks and a user configurable number of segments. 
  - Track 1: Video 
  - Track 2: Music

### Step 2: Implicit Requirements 

These are requirements that the user does not specify everytime, but you should always include. The end users using the blueprint to generate videos will always want to configure these: 

**Duration and structure?**
  - Total video length in seconds
  - Number of segments
  - Images per segment (if applicable)

**Visual style?**
  - Cinematic, anime, photorealistic, etc.
  - Aspect ratio (16:9, 9:16, 1:1)
  - Resolution (480p, 720p, 1080p)

### Step 3: Determine the Inputs and Artifacts

Based on the requirements gathering and the selected producers, determine what inputs will be needed from the user to do the full video generation.
- Minimal set of required inputs, various producers and models have default values that are already good enough. Do not overwhelm the user to specify all of those inputs and rely on the defaults when they make sense.

### Step 4: Define the Blueprint Structure

A blueprint has these sections, you will need to be filling these as you go along the process.

```yaml
meta:
  name: <Human-readable name>
  description: <Purpose and behavior>
  id: <PascalCase identifier>
  version: 0.1.0

inputs:
  - name: <PascalCase>
    description: <Purpose>
    type: <string|int|image|audio|video|json>
    required: <true|false>

artifacts:
  - name: <PascalCase>
    description: <Output description>
    type: <string|array|image|audio|video|json>
    itemType: <for arrays>
    countInput: <input name for array size>

loops:
  - name: <lowercase>
    countInput: <input providing count>
    parent: <optional parent loop>

producers:
  - name: <PascalCase alias>
    path: <relative path to producer.yaml>
    loop: <loop name or nested like segment.image>

connections:
  - from: <source>
    to: <target>
    if: <optional condition name>

conditions:
  <conditionName>:
    when: <artifact path>
    is: <value>

collectors:
  - name: <collector name>
    from: <source with loop indices>
    into: <target fan-in input>
    groupBy: <loop dimension>
    orderBy: <optional ordering dimension>
```

Use `docs/comprehensive-blueprint-guide.md` for a comprehensive explanation of the blueprints and how to connect nodes based on the requirements you gathered. You can also always use some examples from the catalog. 

- Create the blueprint in the root folder of the workspace, which you can always find in: `~/.config/renku/cli-config.json`

## Validation & Testing

### Validate Blueprint Structure
This validates that the blueprint can be parsed and structurally connect, but it does not validate that it will be producing the intended video without errors.

```bash
renku blueprints:validate <path-to-blueprint.yaml>
```

Expected output:
- `valid: true` - Blueprint structure is correct
- Node and edge counts
- Error messages if invalid

### Test with Dry Run

Create a minimal inputs file (based on the requirements and also what the producers expect)
> **IMPORTANT** Producers specify a lot of possible inputs for completeness, but most of them have default values. DO NOT PROVIDE VALUES for those defaults. 
> **IMPORTANT** Models will be picked by end user when generating a video, in the dry-run just pick one of the models in the list of supported models for that producer (in the YAML file). 

```yaml
inputs:
  InquiryPrompt: "Test prompt"
  Duration: 30
  NumOfSegments: 2
  # ... other required inputs

models:
  - model: gpt-5-mini
    provider: openai
    producerId: ScriptProducer
  # ... other model selections
```

Save this again in the root folder of the workspace.

Run dry-run:
> **IMPORTANT** Always use --dry-run, running them full will cost money as they will be calling the providers and the user will be charged and very UPSET!

```bash
renku generate --blueprint=<path> --inputs=<path> --dry-run
```

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing size for dimension "X"` | Loop not sized | Add `countInput` to loop definition |
| `Unknown loop symbol "X"` | Typo in connection | Check loop names in `loops:` section |
| `inconsistent dimension counts` | Mismatched indices | Ensure source/target dimensions align |
| `Producer graph contains a cycle` | Circular dependency | Check connections for loops |
| `Missing producer catalog entry` | Wrong producer path | Verify `path:` in producers section |

## Reference Documentation

For comprehensive information:
- [comprehensive-blueprint-guide.md](./docs/comprehensive-blueprint-guide.md) - Full YAML schema and examples

For live examples, find the catalog path in `~/.config/renku/cli-config.json` and explore:
- `<catalog>/blueprints/` - Blueprint examples
- `<catalog>/producers/` - Producer definitions
- `<catalog>/models/` - Model definitions together with their input JSON schemas

## CLI Commands Reference

```bash
# Initialize Renku workspace
renku init --root=<path>

# Validate blueprint structure
renku blueprints:validate <blueprint.yaml>

# Describe blueprint details
renku blueprints:describe <blueprint.yaml>

# List available blueprints
renku blueprints:list

# List available models for producers
renku producers:list --blueprint=<path>

# Test with dry run (no API calls)
renku generate --blueprint=<path> --inputs=<path> --dry-run

# Estimate costs
renku generate --blueprint=<path> --inputs=<path> --costs-only

# Full generation (costs money)
renku generate --blueprint=<path> --inputs=<path> --non-interactive
```
