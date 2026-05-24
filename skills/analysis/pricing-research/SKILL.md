---
name: pricing-research
description: "Pricing Research is a sophisticated analytical skill designed to systematically investigate price-related questions including customer price sensitivity, competitive pricing dynamics, optimal price points, value perception, and pricing strategy effectiveness."
---

# Pricing Research Skill

## Overview

This skill provides comprehensive guidance and best practices for this domain.

## Skill Description and Purpose

Pricing Research is a sophisticated analytical skill designed to systematically investigate price-related questions including customer price sensitivity, competitive pricing dynamics, optimal price points, value perception, and pricing strategy effectiveness. This skill applies rigorous quantitative methodologies—including conjoint analysis, Van Westendorp price sensitivity meter, Gabor-Granger analysis, and price elasticity modeling—alongside qualitative value research to develop evidence-based pricing recommendations.

The fundamental purpose of this skill is to transform pricing decisions from intuition-driven guesswork into data-driven strategy by revealing how customers perceive value, respond to price changes, and make trade-offs between price and product attributes. Effective pricing research directly impacts revenue, profitability, market share, and competitive positioning—making it one of the highest-leverage analytical investments an organization can make.

This skill should be deployed when organizations need to set prices for new products or services, evaluate price change impacts, understand competitive price positioning, segment customers by price sensitivity, optimize pricing architecture (tiers, bundles, versioning), assess promotional pricing effectiveness, or develop value-based pricing strategies. It is essential for product launches, pricing transformations, competitive response, and margin improvement initiatives.

The skill encompasses both primary pricing research (surveys, experiments, conjoint studies) and secondary pricing intelligence (competitive monitoring, price tracking, elasticity analysis from transaction data). It addresses business-to-consumer and business-to-business contexts, recognizing the distinct methodological requirements of each.

## Required Inputs/Parameters

**Research Design Parameters:**
- **Pricing Research Objective:** Specific pricing question to answer—optimal price point, price sensitivity measurement, competitive positioning, price segmentation, bundle optimization, promotion effectiveness, willingness to pay quantification.
- **Product/Service Definition:** Detailed specification of offering being priced including features, attributes, competitive alternatives, and value proposition. For complex products, include attribute hierarchy.
- **Market Context:** Market characteristics including competitive intensity, price transparency, customer sophistication, purchasing frequency, and pricing norms.

**Methodology Selection Parameters:**
- **Research Approach:** Primary research (survey-based), secondary analysis (transaction data), competitive intelligence, or hybrid approach. If primary research, specify methodology:
  - Van Westendorp Price Sensitivity Meter (PSM): Four-question approach for acceptable price range
  - Gabor-Granger: Direct price-purchase probability questioning
  - Conjoint Analysis: Attribute trade-off analysis including price
  - Discrete Choice Modeling: Choice-based conjoint for competitive scenarios
  - Monadic Price Testing: Direct willingness to pay for specific price points
  - A/B Price Testing: Experimental price variation analysis
- **Sample Specifications:** Target respondent profile, sample size requirements (minimum 200-400 for robust pricing research), sampling methodology, and screening criteria.

**Price Point Parameters:**
- **Price Range Definition:** Minimum and maximum prices to test, based on cost floor, competitive ceiling, and market expectations. Specify price point intervals.
- **Price Format:** How prices are expressed—annual vs. monthly, per unit vs. per usage, list price vs. discounted, currency, and rounding conventions.
- **Competitive Price References:** Known competitive price points to include in comparative analysis or choice scenarios.

**Analysis Parameters:**
- **Segmentation Requirements:** Customer segments for differential price sensitivity analysis including segmentation variables and segment definitions.
- **Elasticity Specifications:** Price elasticity calculation methodology, cross-price elasticity requirements for substitutes/complements.
- **Revenue/Profit Optimization:** Cost structure inputs for profit optimization analysis, volume constraints, capacity limitations.
- **Scenario Modeling:** Price scenarios to evaluate with specific price-volume-revenue projections.

## Expected Outputs/Deliverables

**Core Deliverables:**

1. **Price Sensitivity Analysis Report:** Comprehensive analysis of customer price sensitivity including acceptable price range (from Van Westendorp or equivalent), optimal price point, indifference price point, and marginal price thresholds. Visualized through price sensitivity curves and sensitivity meter charts.

2. **Willingness to Pay Quantification:** Rigorous estimation of customer willingness to pay including point estimates, confidence intervals, and segment-level variation. For conjoint-based studies, includes part-worth utilities for price levels and derived value metrics.

3. **Price Elasticity Analysis:** Calculation of price elasticity of demand based on transaction data analysis or survey-based estimation. Includes elasticity at current price, elasticity curve across price range, and revenue-maximizing price identification. Format: Elasticity metrics with demand curves and revenue projections.

4. **Competitive Pricing Intelligence:** Systematic documentation of competitor pricing including price points, pricing structure (tiers, features per tier), bundling strategies, promotional patterns, and price-value positioning. Includes competitive price map visualization and relative value assessment.

5. **Pricing Segmentation Analysis:** Identification of customer segments with distinct price sensitivity profiles including segment characteristics, willingness to pay by segment, optimal segment-specific pricing, and price discrimination feasibility assessment.

6. **Revenue Optimization Model:** Decision support tool for evaluating pricing scenarios showing projected volume, revenue, and profit across price points. Includes sensitivity analysis for key assumptions and scenario comparison framework.

7. **Pricing Recommendations:** Actionable pricing recommendations including recommended price point(s), pricing structure, segmentation strategy, competitive positioning, and implementation considerations with supporting rationale from research findings.

**Quality Standards:**
- Sample sizes sufficient for statistical significance (95% confidence, ±5% margin of error minimum)
- Methodology limitations explicitly acknowledged (hypothetical bias, competitive context simplification)
- Multiple methodologies triangulated where possible for robust conclusions
- Sensitivity analysis on key assumptions affecting recommendations
- Competitive data sourced and dated with collection methodology documented
- Executive summary with recommended price point(s), expected revenue impact, and confidence assessment

## Example Use Cases

**Use Case 1: SaaS Pricing Tier Optimization**
A B2B SaaS company needs to redesign its three-tier pricing structure. Pricing research includes conjoint analysis testing feature combinations and price levels, Van Westendorp analysis for each tier, competitive pricing benchmarking against 12 competitors, and customer segment analysis by company size and use case. Deliverables include optimal tier configurations with feature-price combinations, segment-based pricing recommendations, migration impact analysis for existing customers, and implementation roadmap.

**Use Case 2: New Product Launch Pricing**
A consumer electronics company launching a new product category requires pricing research to set launch price. Research combines Van Westendorp price sensitivity meter with 800 target consumers, conjoint analysis including competitive alternatives, concept-price testing at multiple price points, and reference price analysis from adjacent categories. Outputs include recommended launch price with revenue projections, price elasticity curves, competitive positioning strategy, and promotional pricing framework.

**Use Case 3: Competitive Price Response**
A retailer faces aggressive competitive price cuts and needs pricing research to inform response. Analysis includes price elasticity modeling from historical transaction data, cross-price elasticity calculation for competitive products, price perception research with current customers, and scenario modeling for various response strategies. Deliverables include recommended price response by category, margin impact projections, customer retention risk assessment, and monitoring framework for competitive pricing.

**Use Case 4: Value-Based Pricing Transformation**
A professional services firm transitioning from hourly billing to value-based pricing commissions pricing research. Research includes economic value estimation for different service outcomes, client willingness to pay by service type and client segment, competitive pricing intelligence across alternative providers, and conjoint analysis testing pricing model structures (fixed fee, success fee, hybrid). Outputs include service-specific pricing recommendations, client segment targeting, implementation sequencing, and change management considerations.

**Use Case 5: Dynamic Pricing Optimization**
An e-commerce company seeks to optimize its dynamic pricing algorithms through pricing research. Analysis includes price elasticity modeling by product category, time-of-day, and customer segment, competitive price tracking and response patterns, psychological pricing threshold identification, and A/B test analysis of pricing experiments. Deliverables include elasticity parameters for pricing algorithms, price floor and ceiling recommendations, competitive response rules, and psychological pricing guidelines.

## Prerequisites or Dependencies

**Data Access Requirements:**
- Survey platform access for primary pricing research (Qualtrics, SurveyMonkey with conjoint capabilities, specialized conjoint platforms like Sawtooth, Conjointly)
- Transaction data access for price elasticity analysis (POS data, e-commerce data, CRM)
- Competitive pricing data sources (price tracking services, competitive intelligence platforms, manual collection capabilities)
- Customer segmentation data for segment-level analysis

**Technical Dependencies:**
- Conjoint analysis software and expertise for choice-based conjoint design and analysis (Sawtooth Software, R conjoint packages, or specialized platforms)
- Statistical analysis capabilities for elasticity modeling, significance testing, and confidence interval calculation
- Revenue modeling capabilities for price-volume-profit scenario analysis
- Visualization tools for price sensitivity curves, demand curves, and competitive price maps
- Survey programming capabilities for complex pricing question formats

**Knowledge Prerequisites:**
- Understanding of pricing research methodologies (Van Westendorp, Gabor-Granger, conjoint, PSM) and their appropriate applications
- Familiarity with price elasticity concepts and calculation methodologies
- Knowledge of behavioral pricing principles (reference price effects, psychological pricing, price-quality inference)
- Understanding of value-based pricing principles and economic value estimation
- Statistical literacy for interpreting conjoint outputs and elasticity estimates

**Methodological Considerations:**
- Hypothetical bias—survey-based willingness to pay typically overstates actual purchase behavior (apply correction factors)
- Competitive context—monadic pricing research may miss competitive dynamics captured in choice-based methods
- B2B complexity—organizational buying involves multiple stakeholders with different price sensitivities
- Promotional effects—regular price research may not capture promotional price sensitivity
- Price-quality signaling—price changes affect quality perception, not just purchase probability

**Complementary Skills:**
- Statistical analysis for advanced elasticity modeling and conjoint analysis
- Competitive intelligence for comprehensive pricing landscape understanding
- Customer segmentation for price differentiation strategy
- Financial modeling for revenue and profit optimization
- Market research for value proposition and positioning context

**Ethical Considerations:**
- Avoid price discrimination based on protected characteristics
- Ensure pricing research participant consent and anonymity
- Consider fairness implications of differential pricing strategies
- Maintain competitive intelligence boundaries (no misrepresentation or improper access)
- Document methodology transparently for stakeholder trust
