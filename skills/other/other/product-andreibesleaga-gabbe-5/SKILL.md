---
name: green-software
description: Carbon efficiency, sustainable architecture choices, and GreenTech goals.
role: prod-ethicist
triggers:
  - green software
  - sustainability
  - carbon footprint
  - energy efficiency
  - eco-mode
---

# green-software Skill

This skill guides the reduction of the system's environmental impact.

## 1. Principles (Green Software Foundation)
1.  **Carbon Efficiency**: Emit the least amount of carbon per unit of work.
2.  **Energy Efficiency**: Consume the least amount of electricity.
3.  **Carbon Awareness**: Do more work when the electricity is clean (low carbon intensity) and less when it's dirty.

## 2. Architectural Choices
- **Serverless vs Always-On**: Serverless scales to zero (0 energy) when idle.
- **Compiled vs Interpreted**: Rust/Go consume ~50% less energy than Python/Node for compute-heavy tasks.
- **Data Minimization**: Sending less data = less network energy.

## 3. Operations
- **Region Selection**: Host in regions with low carbon intensity (e.g., AWS Sweden/Canada > Virginia).
- **Joy of Delete**: Aggressively delete unused data (don't pay storage energy cost forever).

## 4. Carbon Aware Computing
- Utilize APIs like `ElectricityMaps` or `WattTime`.
- **Batch Jobs**: Schedule heavy cron jobs for 2 AM (or whenever local grid is greenest).
- **"Eco-Mode"**: UI toggle that reduces animations and video quality to save battery/energy.
