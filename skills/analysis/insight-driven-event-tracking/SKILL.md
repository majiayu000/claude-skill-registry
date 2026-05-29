---
name: insight-driven-event-tracking
description: Transform raw data into actionable insights by shifting from tracking "what happened" to "why it happened." Use this skill when designing instrumentation specs for new features, auditing analytics dashboards that provide no clear direction, or diagnosing sudden drops in conversion.
---

# Insight-Driven Event Tracking

Most analytics efforts fail because they track "entertainment" (data that is interesting but doesn't change behavior) rather than "news" (information that forces a change in the real world). This framework shifts instrumentation from simple event logging to capturing the context necessary to explain user intent.

## The Core Principles

### 1. Observation vs. Insight
*   **Observation:** A raw fact from the database (e.g., "Power users book 4x more than new users"). This has no context and offers no clear action.
*   **Insight:** An observation plus the "Why" (e.g., "Power users convert at 2x the rate when they see at least 5 drivers on the map"). This tells you exactly what lever to pull (increase supply density).

### 2. The Physics of the Growth Model
Before tracking, define the "physics" of your specific universe to identify where levers actually exist:
*   **Market:** Who are the users and suppliers?
*   **Product:** What is the core value proposition?
*   **Model:** How do you charge or capture value?
*   **Channel:** How do users find you? (e.g., In Southeast Asia, Gojek’s physical drivers in green jackets were a primary growth channel).

## The Instrumentation Workflow

### Step 1: Identify the "Step Before"
Instead of focusing solely on the conversion event (e.g., "Purchased"), focus on the step immediately preceding it. This is where the most friction exists. 
*   **Goal:** Identify the "Hand-Raiser" approach—actions where a user signals intent but hasn't committed.

### Step 2: Define Contextual Properties
A bad tracking spec has many unique event names with zero properties. A high-value spec has few events with many properties. For every core action, you must track the context:
*   **Supply state:** What did the user see? (e.g., Number of drivers, items in stock).
*   **Friction state:** Was there a voucher? Was the API slow?
*   **User state:** Is this a first-time user? Are they connected via social?

### Step 3: Run the "News Test"
For every event/property in your spec, ask: "If this number changes by 20%, what specific action will I take tomorrow?" If you don't have an answer, you are tracking entertainment, not news.

## Examples

**Example 1: Ride-Hailing Map Load**
*   **Context:** A user opens the app to book a ride.
*   **Bad Tracking:** Event: `map_loaded`.
*   **Insight-Driven Tracking:** Event: `map_viewed`
    *   Property `drivers_visible`: 2 (Critical for understanding conversion)
    *   Property `surge_multiplier`: 1.5x
    *   Property `estimated_pickup_time`: 8 mins
    *   Property `is_new_user`: True
*   **Output:** Analysis reveals users with `drivers_visible` < 3 have a 50% drop in conversion. Action: Re-route supply to those specific GPS coordinates.

**Example 2: Social App Onboarding**
*   **Context:** A user is prompted to find friends on a social app.
*   **Bad Tracking:** Event: `search_clicked`.
*   **Insight-Driven Tracking:** Event: `friend_search_performed`
    *   Property `api_latency_ms`: 1200ms
    *   Property `results_count`: 0
    *   Property `search_query_length`: 3
*   **Output:** Data shows a 30% drop-off when `api_latency_ms` > 800ms. Action: Invest in search API optimization rather than changing the UI.

## Benchmarks for Success
When analyzing the resulting data, use these "Decacorn" benchmarks to evaluate health:
*   **Free Products:** Aim for ~60% Week 1 retention. The curve should flatten high.
*   **Paid Products:** Aim for 20-30% Week 1 retention.
*   **The "Friend Test":** For early startups, retention among friends and family should be near 80%. If you can't retain people who care about you, you won't retain strangers.

## Common Pitfalls to Avoid
*   **Tracking OKRs instead of Journeys:** Knowing your North Star metric is down is "entertainment." Knowing it's down because of a 40% failure rate in the SMS OTP provider is "news."
*   **Ignoring the "Pause" Option:** In subscription models, users often churn because they have "too much" of a product. Adding a "Pause/Snooze" button is often more effective than reactivation emails.
*   **Waiting for Scale to Experiment:** You can run experiments with a sample size as low as 30. The results won't be as precise, but the underlying trends and "direction of travel" are usually visible and actionable.
*   **Over-complicating Tools:** Don't spend 6 months integrating a complex CRM if a Python script hitting a Twilio API and a CSV can validate the hypothesis in 4 hours.