---
name: kling-studio
version: 1.1.0
author: "wells1137"
emoji: "🎬"
tags:
  - video-generation
  - kling
  - kling-3-omni
  - reference-to-video
  - multi-shot
  - video-editing
description: >
  Full-featured Kling 3.0 Omni video generation skill. Covers text-to-video, image-to-video,
  video editing (base mode), video reference (feature mode), multi-shot generation, and
  audio-synced video. Includes validated API constraint rules and prompt engineering guide.
homepage: https://github.com/wells1137/media-skills/tree/main/skills/kling-studio
metadata:
  openclaw:
    emoji: "🎬"
    primaryEnv: KLING_ACCESS_KEY
    requires:
      env:
        - KLING_ACCESS_KEY
        - KLING_SECRET_KEY
      bins:
        - python3
---

# Kling 3.0 Omni Video Generator

This skill enables the generation and manipulation of videos using the Kling 3.0 Omni model. It provides a structured workflow for constructing API requests based on user intent, ensuring compliance with the model's complex parameter constraints.

## Reference Files

This skill includes the following reference files:

- `references/api_reference.md` — **Complete official API parameter reference**, including all fields, types, constraints, mutual exclusion rules (R1–R10), capability matrix, and invocation examples. **Read this file before constructing any API call.**
- `references/prompt_guide.md` — Kling 3.0 Omni prompt writing principles, official formula, template syntax, and few-shot examples for all major scenarios.
- `scripts/kling_api.py` — Python utility class for JWT authentication, task creation, and polling.

---

## Core Capabilities

- **Text-to-Video**: Generate a video from a textual description.
- **Image-to-Video**: Animate a static image with a descriptive prompt.
- **Video-to-Video (Editing)**: Modify an existing video based on a prompt (e.g., change subject, style).
- **Video-to-Video (Reference)**: Use an existing video as a reference for camera movement and style.
- **Multi-shot Generation**: Create a video with multiple distinct scenes or shots.
- **Audio Generation**: Generate video with synchronized audio, including speech and sound effects.

---

## Workflow: From User Intent to API Call

To correctly use the Kling API, you MUST follow this decision-making workflow to construct the API payload. The process is divided into two main stages: **Prompt Design** and **Parameter Construction**.

### Stage 1: Prompt Design

Before constructing the API call, you must first design the prompt(s) based on the user's request. The quality of the prompt is the single most important factor for a good result.

1.  **Consult the Prompting Guide**: Read `/home/ubuntu/skills/kling-studio/references/prompt_guide.md` to understand the core principles, official formula, and few-shot examples for writing effective prompts.

2.  **Identify the Scenario**: Determine which of the following scenarios the user is requesting:
    -   Single-shot video (from text, image, or video)
    -   Multi-shot video (storyboard with multiple scenes)

3.  **Write the Prompt(s)**:
    -   For **single-shot**, write a single, detailed prompt following the guide's formula.
    -   For **multi-shot**, write a separate prompt for each shot/scene.
    -   **Use Template Syntax**: If the user provides reference images, elements, or videos, you MUST use the `<<<image_1>>>`, `<<<element_1>>>`, `<<<video_1>>>` template syntax in the prompt to explicitly reference them. This is a core feature of the Omni model.

### Stage 2: Parameter Construction

Once the prompt(s) are ready, construct the final API request payload by following this decision tree. This ensures all parameter constraints and interdependencies, discovered through extensive testing, are respected.

```mermaid
graph TD
    A[Start] --> B{Multi-shot or Single-shot?};
    B -- Multi-shot --> C[Set `multi_shot: true`];
    B -- Single-shot --> D[Set `multi_shot: false`];

    C --> E{Set `shot_type: "customize"`};
    E --> F[Construct `multi_prompt` array from prompts];
    F --> G[Calculate total duration from `multi_prompt`];
    G --> H[Set top-level `duration`];
    H --> Z[Final Payload];

    D --> I{Video input provided?};
    I -- Yes --> J{Editing or Reference?};
    I -- No --> K[Text/Image-to-Video Path];

    J -- Editing --> L[Set `refer_type: "base"`];
    J -- Reference --> M[Set `refer_type: "feature"`];

    L --> N[Ignore `duration` parameter];
    M --> O[Set `aspect_ratio`];
    N --> P{Audio handling};
    O --> P;

    K --> Q{Audio handling};
    P --> R{Audio handling};

    subgraph R [Audio Handling]
        direction LR
        R1{Want audio output?} -- Yes --> R2[Set `sound: "on"`];
        R1 -- No --> R3[Set `sound: "off"`];
        R2 --> R4{Video input exists?};
        R4 -- Yes --> R5[ERROR: `sound:on` is incompatible with video input];
        R4 -- No --> R6[OK];
    end

    Q --> Z;
    R6 --> Z;
    R3 --> Z;
    R5 --> Stop([Stop/Error]);
```

#### Key Parameter Rules (from testing)

This is not an exhaustive list, but a summary of the most critical, non-obvious rules that you MUST follow. For a complete guide, refer to the `prompt_guide.md`.

| Parameter | Rule |
| :--- | :--- |
| `refer_type` | **MUST be explicit**. Do not omit. Defaults to `base` but this is unreliable. Use `base` for editing, `feature` for reference. |
| `duration` | **Ignored in `base` mode**. In `customize` mode, it MUST equal the sum of `multi_prompt` durations. |
| `sound` | **Incompatible with `video_list`**. Cannot be `on` if a reference video is provided. |
| `shot_type` | **MUST be `customize`** for `multi_shot: true` with the Omni model. `intelligence` is not supported. |
| `multi_prompt` | `index` MUST start from 1. Total duration MUST match top-level `duration`. Max 6 shots. |
| `aspect_ratio` | **Required for `feature` mode**. |
| `image_list` | Max 7 images without video input, **max 4 images with video input**. |

---

## Execution

To execute a video generation task, use the provided Python script which handles authentication and polling.

1.  **Set Environment Variables**: Ensure `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` are set.

2.  **Construct the Payload**: Follow the workflow above to create the JSON payload for the API call.

3.  **Run the Script**:

    ```python
    from kling_api import KlingAPI

    # Get keys from environment
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    api = KlingAPI(access_key, secret_key)

    # Your constructed payload
    payload = {
        "model_name": "kling-v3-omni",
        # ... other parameters based on the workflow ...
    }

    # Create and poll the task
    task_response = api.create_omni_video_task(payload)
    if task_response and task_response.get("code") == 0:
        task_id = task_response.get("data", {}).get("task_id")
        print(f"Task created: {task_id}")
        result = api.poll_for_completion(task_id)
        if result:
            print("Final video URL:", result.get("videos", [{}])[0].get("url"))
    ```

This structured approach ensures that all the nuances and constraints of the Kling 3.0 Omni API are handled correctly, leading to fewer errors and more predictable results.
