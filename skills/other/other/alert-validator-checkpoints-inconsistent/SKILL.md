---
name: debug-validator-checkpoint-inconsistency
description: Debug validator checkpoint inconsistencies where some validators are behind others. Use when alerts mention "checkpoint inconsistency", "validators behind", or "inconsistent latest checkpoints", or when asked to debug validator sets, investigate validator delays, or troubleshoot metadata fetch failures for a chain. Defaults to default_ism app context if not specified.
---

# Debug Validator Checkpoint Inconsistency

## When to Use

1. **Alert-based triggers:**
   - Alert mentions "checkpoint inconsistency", "validator inconsistent", or "validators behind"
   - Alert names like "Inconsistent latest checkpoints in validator set"
   - Alert names containing "checkpoint inconsistency" with a threshold (e.g., "> 20")
   - Any alert referencing validator signing delays or checkpoint gaps

2. **User request triggers:**
   - "Debug the validator set on [chain]" (use `default_ism` app context if not specified)
   - "Check validator checkpoint status for [chain]"
   - "Why are validators inconsistent on [chain]?"
   - "Investigate validator delays for [app_context] on [chain]"
   - "Why is metadata fetch failing for [chain]?" (often validator-related)

## Input Parameters

| Parameter              | Required | Default       | Description                                                                                                                                                                                                                                                                                               |
| ---------------------- | -------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `origin_chain`         | Yes      | -             | The origin chain where validators are signing checkpoints (e.g., `hyperevm`, `ethereum`, `arbitrum`)                                                                                                                                                                                                      |
| `app_context`          | No       | `default_ism` | The ISM/application context (e.g., `default_ism`, `EZETH/renzo-prod`)                                                                                                                                                                                                                                     |
| `time_range`           | No       | `1h`          | How far back to investigate                                                                                                                                                                                                                                                                               |
| `environment`          | No       | `mainnet3`    | Only possible values are `mainnet3` or `testnet4`. If told it's mainnet or testnet, pick the appropriate possible value.                                                                                                                                                                                  |
| `validator`            | No       | `*`           | Optional                                                                                                                                                                                                                                                                                                  |
| `evaluation_timestamp` | No       | Now           | A timestamp to consider as the current time. A timestamp in the genuine past may be used here to eval previous scenarios. Treat this timestamp as if it were the current time for all requests to tools, e.g. when querying Prometheus metrics. Never query any metrics after the `evaluation_timestamp`. |

## A note on metrics

**CRITICAL: Use the relayer's perspective to see ALL validators (including external):**

Use the Grafana MCP server to query prometheus metrics. Use datasource uid `grafanacloud-prom` to interact with Prometheus metrics.

If a specific `evaluation_timestamp` is provided that is not Now, be sure to always behave as if `evaluation_timestamp` is the present time. This means:

- All Prometheus metrics queried should be at `evaluation_timestamp` at the very newest - never query anything past this time
- Fetching the latest Prometheus metric should mean that it's queried at the `evaluation_timestamp`
- Always use the `evaluation_timestamp` as the end time when querying any prometheus metrics, NOT the start time.

The following metric exists that shows the relayer's perspective of all validators:

```promql
hyperlane_observed_validator_latest_index{
  origin="[origin_chain]",
  destination="[destination_chain]",
  hyperlane_deployment="[environment]",
  app_context="[APP_CONTEXT]",
  validator="[validator_address]",
  hyperlane_context="hyperlane" # always use this
}
```

The metric shows the latest highest signed index by a validator as it's observed by the relayer. It's only updated by the relayer when it is attempting to process a message from that origin to that destination for the given app_context. This has the following implications:

- The metric values can be very stale, indicating false positives
- You should `max by (origin, validator, app_context)` on the metric if you want to see the latest values for each validator in that validator set
- It's possible for a different origin chain validator set to be enrolled on different destination chains. This is usually not intentional and may reflect in-progress validator set rotations, but it could also indicate an issue. Keep this in mind if you ignore the destination chain by using `max by (origin, validator, app_context)`
- It's possible that some validators are healthy and are just a couple seconds behind the rest of the pack, so the metric might show them as a tiny bit behind the rest. In this case, they aren't stalled, it's just that the relayer attempted to deliver a message shortly before the validator signed the checkpoint.

**NEVER** ignore negative values from these metrics. A `-1` value here means that the validator signatures are not accessible by the relayer. Consider this as serious as if the validator were completely down. Note that the root cause of this is one of the following:

- The validator isn't configured correctly
- The validator isn't running at all
- The relayer has issues reaching the validator's signatures for some reason

## Debugging Workflow

### Step 0: Pick the app context

Skip this step if an `app_context` was explicitly specified. Continue this step if no `app_context` was specified, even if it has a default value.

Skip this step if no specific `validator` was specified.

If any `validator` was specified, first use the `hyperlane_observed_validator_latest_index` metric to find the `app_context`s to focus on. Find the values of the `app_context` label for the metric:

```promql
hyperlane_observed_validator_latest_index{origin="[origin_chain]", validator="[validator]"}
```

If the list of app contexts includes `default_ism`, we will set the `app_context` for future use as `default_ism`. If not, pick any one of the returned values as the `app_context`.

### Step 1: Check the `hyperlane_observed_validator_latest_index` to see which validators may be behind

**First, see the highest value of each validator from the origin chain:**

Look at the following metric values for the last `time_range`, one data point every minute.

```promql
max_over_time(
    max by (validator) (
        hyperlane_observed_validator_latest_index{hyperlane_context="hyperlane", hyperlane_deployment="[environment]", origin="[origin_chain]", app_context=~"[app_context]"}
    )[3h:]
)
```

A stalled validator will both:

- Have a latest checkpoint index behind the rest (> 5 behind)
- Not have increased while the rest have increased

**Note** if a validator satisfies the above points to be a stalled validator, it is considered stalled even if it is just a few indices behind. DO NOT consider it "slightly behind" even if it's just 5 indices behind -- if it is stalled, it's stalled.

If there are no stalled validators, then skip to Step 2.

**Then, confirm that the validators are genuinely behind**

If a validator seems stalled based off the metrics we just got, the next step is to ensure that the validator is enrolled for all destination chains, and that we aren't hitting a situation where the validator is only enrolled for some destination chains with infrequent messages, so it just hasn't been updated in a while.

**Note** it's totally possible for a validator to be genuinely stalled and to also only be enrolled in a subset of destination chains. We care just as much about these validators that are stalled even if they are still enrolled when they shouldn't be.

For each potentially stalled validator:

1. Look at the list of `destination` label values for the `hyperlane_observed_validator_latest_index{origin="[origin_chain]", validator="[stalled_validator]}`
2. Compare that list of destination chains to the list of destination chains for _any_ validator: `hyperlane_observed_validator_latest_index{origin="[origin_chain]"}`. If there is no difference in the destination chains, this validator is **genuinely stalled**.
3. If there is any difference in the destination chains, surface this to the user regardless of the validators being genuinely stalled or not. If there is any difference in the chains, you can confirm if the potentially stalled validators are genuinely behind by performing step 1 but restricting `destination=~"[list of destination chains the stalled validator has, in promql compatible format]"`. If no validators seem behind once we filter for just the destination chains that the stalled validator is enrolled on, then nothing is actually stalled!

### Step 2: Discover the human-friendly identity of the validators

Perform this for all validators on the origin chain, regardless of them being stalled or not:

For each validator address:

1. Open up `typescript/sdk/src/consts/multisigIsm.ts`
2. Find the entry for the origin chain in the `defaultMultisigConfigs`. This is the latest source of truth for the validator set relating to the origin chain.
3. Looking at the list of validators for the origin chain, find the alias relating to the stalled validator address.
4. If you are unable to find a match: Sometimes it can happen where you're unable to find a match here - it could be that the stalled validator should have been removed from an ISM, so it's not reflected in the multisigIsm.ts configuration anymore, but it's still present onchain. In this case, we need to surface to the user. You may still be able to find the alias of the validator if you are able to see the validator address elsewhere in this file - it's possible for the same validator address to be used on different chains, so if the validator address matches then the alias matches.

Additionally, take note of the threshold and validator set size of the origin chain.

### Step 3: Surface to the user

Always surface the **ENTIRE** validator address (NEVER truncate), alias, latest signed checkpoint, difference from the highest latest signed checkpoint, status (e.g. healthy, stalled).

**First**, show all validators that are present in the multisigIsm.ts configuration in a table. Clearly show any validators here that are stalled, and the other non-stalled validators as healthy.

**Second**, show in a table any observed validators that are not present in the multisigIsm.ts file but are still seemingly enrolled for some destinations. Surface these as a warning, and include the list of destination chains they are still enrolled on. Clearly show any validators here that are stalled, and the other non-stalled validators as healthy. Treat any difference here from the default ISM as a possible erroneous configuration, even if you think it may be the case that a custom ISM is intentionally be used.

Then summarize the key findings:

- Are any stalled?
- Surface the threshold and validator set size. Quorum means that we have at least `threshold` validators healthy. If the # of stalled validators means that we no longer meet the threshold of healthy validators, this is extremely concerning and is **high** priority! If we are close (i.e. if one more goes down), treat this as **medium** priority. Otherwise, treat this as **low** priority unless instructions below conflict with this.
- Any stalled validators are an indication that there is some health risk at the moment. A validator that is stalled should be pinged and we should resolve this, even if we still have quorum.
- If we still have quorum (or are uncertain if we still have quorum), surface the following priority:
  - Exactly 1 validator down - **HIGH** priority (show a warning emoji)
  - Exactly 2 validators down - **MEDIUM** priority (show a warning-error emoji)
  - 3 or more validators down - **HIGH** priority (show an error emoji)
- If quorum is lost (the # of live validators is < the threshold)
  - **HIGH** priority (show an error emoji)
