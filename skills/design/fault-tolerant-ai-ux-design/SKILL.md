---
name: fault-tolerant-ai-ux-design
description: A framework for designing user interfaces that match the performance of AI/ML models. Use this when launching generative AI features, balancing "discovery" vs. "recall" in feeds, or determining how much density a UI requires based on algorithm accuracy.
---

# Fault-Tolerant AI UX Design

When building products powered by machine learning or generative AI, the user interface must be a direct reflection of the algorithm's performance. Most product failures in AI occur when the UI assumes 100% accuracy (the "Silver Button" trap) while the model only delivers 20% accuracy. This framework helps you design interfaces that turn algorithmic errors into acceptable user experiences.

## Core Principles

### 1. Map UI Density to Hit Rate
The number of options presented to a user should be the inverse of your model's hit rate.
- **Low Hit Rate (e.g., 20%):** If your model is only right 1 out of 5 times, you must show at least 5 items simultaneously. This ensures the user likely sees one relevant "hit" without feeling the product is broken.
- **High Hit Rate (e.g., 90%+):** You can afford a "Silver Button" or "Single Play" UI where the algorithm makes a definitive choice for the user.

### 2. Balance Recall vs. Discovery
Identify if the user is in a "Recall" mode or a "Discovery" mode to determine UI density and media richness.
- **Recall (90% of most sessions):** Users want to get back to a known session, playlist, or document. Use high-density UIs (lists, small icons) to allow for quick scanning.
- **Discovery (10% of sessions):** Users want to "break their taste bubble." Use low-density, high-pixel UIs (large cards, auto-playing video/audio) because the user needs more context to evaluate a new, unknown suggestion.

### 3. Build "Escape Hatches"
Always provide a low-friction path for the user to tell the AI it is wrong. In the generative era, this means:
- **Zero-Intent Handling:** For users who "don't know what they want," provide a mechanism to cycle through candidates quickly (e.g., a "skip" or "DJ" button).
- **Manual Overrides:** Ensure the "Library" or "Search" (Recall tools) are never more than one tap away when an AI-driven discovery experiment fails.

## Implementation Steps

### Step 1: Quantify the Prediction Error
Before designing the UI, determine the "Success Rate" of your model. If you are suggesting a new genre of music or a new style of image:
- How many attempts does it take for a user to "save" or "like" one item?
- If the answer is 4, your UI candidate pool must be 4+.

### Step 2: Set the "Magic Trick" Threshold
Identify the "magic trick" your product pulls. For Spotify's AI DJ, the magic was: "How did they record this voice saying my specific name and my specific music tastes?" 
- **Action:** Strip away all non-essential features (weather, news, UI clutter) to focus entirely on the "magic" moment.

### Step 3: Design for Habit Breakage
When redesigning a feed for AI discovery, do not move the "Recall" buttons.
- Users have "muscle memory" for their physical desktop (where they keep their "pencils" and "notebooks"). 
- If you move the "Recall" tools to prioritize "Discovery," users will perceive the AI as an obstacle rather than a feature.

## Examples

**Example 1: Generative Image Tool (e.g., Mid Journey)**
- **Context:** Initial generation is slow and hit rate is moderate.
- **Application:** Instead of generating one high-res image (High risk of failure), the UI generates 4 low-res thumbnails simultaneously.
- **Output:** The user has a 4x higher chance of seeing one "hit," satisfying the "Fault-Tolerant" requirement.

**Example 2: Spotify AI DJ**
- **Context:** Solving the "Zero Intent" use case where users are bored but don't know what to search for.
- **Application:** A single button triggers a generative voice. If the recommendation is bad, a single tap on the "DJ" icon immediately switches the "context" or "vibe."
- **Output:** The "Escape Hatch" (tapping the DJ) is so low-friction that the algorithm’s inevitable misses don't ruin the session.

## Common Pitfalls

- **The "Silver Button" Fallacy:** Designing a single-action UI for a model that has a high prediction error. This results in users thinking the product is "broken" rather than "learning."
- **Product Jealousy:** Copying a "Discovery" feed (like TikTok or YouTube) for a product that users primarily use for "Recall" (like a utility or library). 
- **The "Peeing in the Pants" Analogy:** Choosing a short-term UI win (like a high-engagement discovery feed) that feels "warm and nice" initially but eventually "freezes" and alienates your power users who just want to find their saved work.
- **Over-Explaining the Tech:** Including too much introductory text or "how it works" info. The goal is the "Magic Trick"—the technology should "get out of the way" of the content.