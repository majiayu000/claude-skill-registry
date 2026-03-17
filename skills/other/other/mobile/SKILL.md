---
name: mobile
cluster: mobile
description: "Root mobile: native vs cross-platform decisions, app store guidelines, mobile UX principles"
tags: ["mobile","ios","android"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "mobile app ios android native cross-platform ux"
---

## mobile

## Purpose
This skill helps OpenClaw assist in mobile app development by evaluating native (e.g., Swift for iOS, Kotlin for Android) vs. cross-platform (e.g., React Native, Flutter) approaches, ensuring compliance with app store guidelines (e.g., Apple's App Store Review Guidelines, Google Play Policies), and applying mobile UX principles like touch-friendly designs and responsive layouts.

## When to Use
Use this skill when starting a new mobile project, refactoring existing apps, or optimizing for platforms; for example, when deciding between native for performance-critical apps or cross-platform for faster development. Apply it during design phases for UX audits or when preparing app submissions to avoid rejections.

## Key Capabilities
- Analyze native vs. cross-platform trade-offs: Compare build times, maintenance, and performance using metrics like app size and startup speed.
- Validate against app store guidelines: Check for issues like data privacy compliance (e.g., GDPR alignment) or in-app purchase rules via automated scans.
- Enforce mobile UX principles: Generate recommendations for layouts, such as ensuring button sizes > 44x44 pixels for iOS, or using Material Design components for Android.
- Provide code generation: Output snippets for platform-specific features, like handling permissions in Android Manifest or SwiftUI views.
- Integration with tools: Query external APIs for real-time guideline updates, e.g., fetching Apple guidelines via unofficial scrapers (not recommended for production).

## Usage Patterns
Invoke this skill via OpenClaw's CLI or API by prefixing commands with the skill ID, e.g., `openclaw mobile [subcommand]`. Always pass required parameters like platform and project type. For decisions, use interactive mode to refine inputs based on user feedback. Example: Pipe outputs to other skills for chaining, like combining with a "testing" skill for automated UX tests. Handle asynchronous operations by checking response status codes.

## Common Commands/API
Use the OpenClaw CLI for quick tasks or the REST API for programmatic access. Authentication requires setting `$OPENCLAW_API_KEY` as an environment variable.

- CLI Command: `openclaw mobile decide --platform ios --type native-vs-cross --factors performance,cost`
  - Output: JSON with pros/cons, e.g., {"native": "Faster performance but higher cost", "cross": "Shared codebase but potential UI inconsistencies"}.
  - Code Snippet:
    ```
    response = subprocess.run(['openclaw', 'mobile', 'decide', '--platform', 'android', '--type', 'cross'], capture_output=True)
    print(response.stdout.decode())
    ```

- CLI Command: `openclaw mobile validate --app-path /path/to/app --store apple`
  - Flags: `--store` (apple/google) for guideline checks; `--app-path` for local file analysis.
  - Code Snippet:
    ```
    import os
    os.system('openclaw mobile validate --app-path ./myapp --store google')
    # Checks for policies like ad compliance and returns exit code 0 if pass
    ```

- API Endpoint: POST /api/v1/skills/mobile/decide
  - Body: JSON like {"platform": "ios", "type": "ux-principles", "query": "button sizing"}
  - Response: 200 OK with data, e.g., {"recommendation": "Use .frame(width: 50, height: 50) for buttons"}.
  - Code Snippet:
    ```
    import requests
    headers = {'Authorization': f'Bearer {os.environ.get("OPENCLAW_API_KEY")}'}
    response = requests.post('https://api.openclaw.ai/api/v1/skills/mobile/decide', json={"platform": "android"}, headers=headers)
    print(response.json()['advice'])
    ```

- Config Format: Use YAML for custom profiles, e.g.,
  ```
  mobile:
    defaultPlatform: android
    uxRules:
      minButtonSize: 48
  ```
  Load via: `openclaw mobile config --file path/to/config.yaml`.

## Integration Notes
Integrate by wrapping OpenClaw calls in your build scripts or IDE extensions. For example, in a CI/CD pipeline, add a step like `openclaw mobile validate` before deployment. If using VS Code, install the OpenClaw extension and bind to keyboard shortcuts. For API integrations, ensure `$OPENCLAW_API_KEY` is set securely via secrets management. Handle rate limits by caching responses; OpenClaw enforces 100 requests/min, so implement retry logic with exponential backoff.

## Error Handling
Common errors include authentication failures (HTTP 401) if `$OPENCLAW_API_KEY` is missing or invalid—fix by verifying the env var and regenerating keys. For invalid inputs, like unsupported platforms, expect HTTP 400 with details; parse the error JSON and prompt for corrections. Platform-specific issues, e.g., iOS guideline mismatches, return structured errors like {"code": "APP_STORE_101", "message": "Privacy policy missing"}—use try-except blocks in scripts:
  ```
  try:
      result = requests.post(url, headers=headers)
      result.raise_for_status()
  except requests.exceptions.HTTPError as e:
      print(f"Error: {e.response.json()['message']}. Retrying...")
  ```
Always log errors with timestamps for debugging, and fallback to default behaviors if API is down.

## Graph Relationships
- Related to: "ios" skill (child node for iOS-specific implementations)
- Related to: "android" skill (sibling node for Android optimizations)
- Connected via: "ux-design" cluster (parent for shared UX principles)
- Links to: "app-store" external resource for guideline references
