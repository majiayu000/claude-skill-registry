---
id: posthog-feature-flags
name: PostHog Feature Flags
description: A/B testing, gradual rollouts, flag evaluation
role: product
requiredTools:
  - type: mcpService
    serviceType: posthog
---

## PostHog Feature Flags

When working with feature flags:

- Use **posthog_list_projects** (tool name may have a suffix if multiple PostHog servers exist) when projectId is unknown; then use **posthog_list_feature_flags** for the project to see keys, names, and rollout state.
- Use **posthog_get_feature_flag** with featureFlagId to inspect a specific flag's configuration and targeting.
- For A/B tests, relate flag keys to **posthog_list_events** or **posthog_list_insights** / **posthog_get_insight** to measure impact.
- Always specify projectId; list projects first if unknown.
- When asked about rollout status, return flag key, name, and enabled state; mention filters if present.

## Step-by-step instructions

1. Resolve projectId: call **posthog_list_projects** if needed.
2. Call **posthog_list_feature_flags** with projectId to list all flags and their rollout.
3. For a specific flag: call **posthog_get_feature_flag** with projectId and featureFlagId to return configuration, targeting, and enabled state.
4. For rollout status: return key, name, enabled, and any filters or rollout percentage from the list or get result.
5. For A/B impact: use **posthog_list_events** or **posthog_list_insights** / **posthog_get_insight** tied to the flag key and summarize results.

## Examples of inputs and outputs

- **Input**: “What’s the status of the checkout-redesign flag?”  
  **Output**: Flag key, name, enabled (true/false), and targeting/filters if present; from **posthog_get_feature_flag**.

- **Input**: “List all feature flags and their rollout.”  
  **Output**: Table or list: flag key, name, enabled, rollout % or filters; from **posthog_list_feature_flags**.

## Common edge cases

- **Unknown projectId**: Call **posthog_list_projects** first and ask which one or use the default.
- **Flag key not found**: Say the flag wasn’t found and suggest checking the featureFlagId or listing flags.
- **User asks for “effect” of a flag**: Use **posthog_list_events** or **posthog_list_insights** tied to the flag key and summarize; if no data, say so.
- **API error**: Report the error and suggest retrying or checking project/credentials.

## Tool usage for specific purposes

- **posthog_list_feature_flags**: Use to answer “what flags exist” and “rollout status of all flags”; always with projectId.
- **posthog_get_feature_flag**: Use for a single flag’s config, targeting, and enabled state when the user names a key or flag (use featureFlagId).
- **posthog_list_events** / **posthog_list_insights** / **posthog_get_insight**: Use when the user asks for A/B or impact; link flag key to event counts or insights.
