---
name: abtesting-mobile
cluster: abtesting
description: "Mobile A/B: Firebase Remote Config, Optimizely, Statsig, app store experiments, staged rollout"
tags: ["mobile","firebase","remote-config","rollout"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "mobile ab test firebase remote config staged rollout canary optimizely"
---

# abtesting-mobile

## Purpose
This skill handles A/B testing for mobile applications using tools like Firebase Remote Config, Optimizely, Statsig, and app store experiments. It focuses on feature flagging, staged rollouts, and canary releases to optimize user experiences.

## When to Use
Use this skill when you need to run experiments on mobile apps, such as testing UI changes, feature toggles, or gradual rollouts. Apply it for apps on iOS/Android to minimize risks, gather data-driven insights, or comply with app store guidelines for experiments.

## Key Capabilities
- Configure Firebase Remote Config for dynamic parameter updates without app redeployment.
- Integrate Optimizely SDK for full A/B testing cycles, including event tracking and audience segmentation.
- Use Statsig for quick feature flags and experiments with minimal setup.
- Manage staged rollouts via Firebase or app store APIs to control user exposure.
- Support canary releases by defining percentages for new features.

## Usage Patterns
To set up an A/B test, first authenticate with the service, then define parameters in a config file, fetch values in your app code, and monitor results. For Firebase, use the CLI to update configs; for Optimizely, initialize the SDK early in your app lifecycle. Always wrap experiments in try-catch blocks for error resilience. Pattern: Load config → Assign variants → Track events → Analyze data.

## Common Commands/API
For Firebase Remote Config:
- CLI: `firebase rc:fetch --token $FIREBASE_API_KEY` to fetch parameters.
- API Endpoint: POST to `https://firebaseremoteconfig.googleapis.com/v1/projects/{projectId}/remoteConfig` with JSON body like `{"parameters": {"feature_flag": {"defaultValue": {"value": "true"}}}}`.
- Code Snippet (Swift for iOS):
  ```
  let remoteConfig = RemoteConfig.remoteConfig()
  remoteConfig.fetch { status, error in
      if status == .success { remoteConfig.activate() }
  }
  ```

For Optimizely:
- CLI: `optimizely project create --apiKey $OPTIMIZELY_API_KEY --name "MobileExperiment"`.
- API Endpoint: GET `https://api.optimizely.com/v2/experiments` to list experiments.
- Code Snippet (Android Kotlin):
  ```
  OptimizelyManager.getInstance().optimizely.start { userId, attributes ->
      val variation = optimizely.decide(userId, "experimentKey")
      // Apply variation
  }
  ```

For Statsig:
- CLI: `statsig config set --key $STATSIG_API_KEY --feature "newFeature" --value true`.
- API Endpoint: POST to `https://api.statsig.com/v1/evaluate` with body `{"userID": "123", "featureKey": "feature"}`.
- Code Snippet (General JS for React Native):
  ```
  import Statsig from 'statsig-react-native';
  Statsig.initialize('your-sdk-key').then(() => {
      const value = Statsig.checkGate('feature_gate');
  });
  ```

## Integration Notes
Integrate by adding SDKs via package managers (e.g., `pod 'Firebase/RemoteConfig'` for iOS or `implementation 'com.optimizely.ab:android-sdk:4.0.0'` for Android). Use environment variables for auth: set `$FIREBASE_API_KEY` in your CI/CD pipeline. For config formats, use JSON files like:
```
{
  "parameters": {
    "color_scheme": {
      "defaultValue": { "value": "blue" },
      "description": "A/B test for app theme"
    }
  }
}
```
Ensure apps handle offline scenarios by caching configs. For multi-tool setups, prioritize Firebase for simple flags and Optimizely for complex experiments.

## Error Handling
Handle authentication errors by checking for 401 responses and retrying with refreshed tokens. For Firebase, catch `NSError` with code 3 (network error) and fallback to default values. In code:
```
try {
    remoteConfig.fetchAndActivate { status, error in
        if let error = error { print("Error: \(error.localizedDescription)") }
    }
} catch { print("Fetch failed: \(error)") }
```
For Optimizely, log decision errors and use a default variation. Common issues: Invalid API keys—verify with `echo $OPTIMIZELY_API_KEY`; Network failures—implement exponential backoff.

## Concrete Usage Examples
Example 1: Set up a staged rollout for a new feature using Firebase.
- Steps: Export `$FIREBASE_API_KEY`, run `firebase rc:set --project myapp --params '{"rollout_percent": 50}'`, then in app code, fetch and check the value to enable the feature for 50% of users.

Example 2: Run an A/B test with Optimizely for button color.
- Steps: Create an experiment via `optimizely experiment create --apiKey $OPTIMIZELY_API_KEY --key "buttonColorTest" --variations '["red", "blue"]'`, integrate SDK, and in code, use the decided variation to set the button color and track clicks.

## Graph Relationships
- Related to: abtesting cluster (e.g., abtesting-web for web variants)
- Connected via: mobile tag (links to skills like mobile-analytics)
- Dependencies: Requires firebase and optimizely clusters for full functionality
- Overlaps: With rollout tag, shares edges to deployment skills
