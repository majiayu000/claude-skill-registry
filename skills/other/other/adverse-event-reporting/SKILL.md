---
name: adverse-event-reporting
description: Guide veterinary adverse drug event reporting through FDA CVM and query the openFDA animal adverse event database. Use when a suspected adverse drug reaction occurs in an animal.
---

# Veterinary Adverse Event Reporting

## Overview

Support adverse drug event reporting for veterinary products through FDA CVM channels and query existing adverse event data from the openFDA database. Pharmacovigilance in veterinary medicine follows different pathways than human medicine, with reporting through FDA CVM Form 1932a rather than MedWatch.

## When to Use

- An animal experienced a suspected adverse reaction to a drug, vaccine, or pesticide product
- User wants to check reported adverse events for a veterinary product
- User asks how to report a veterinary adverse event
- User asks about adverse event patterns for a specific drug in animals
- Keywords: adverse event, adverse reaction, side effect, report, ADE, pharmacovigilance, FDA report, vaccine reaction

## Key Resources

- **FDA CVM Adverse Event Reporting:** https://www.fda.gov/animal-veterinary/safety-health/report-problem
- **openFDA Animal & Veterinary Adverse Events API:** https://open.fda.gov/apis/animalandveterinary/event/
- **FDA CVM Safety Reporting Portal** for electronic submission

## Workflow

### Querying Existing Adverse Event Data

1. Search the openFDA animal adverse events endpoint by drug name, species, or reaction type.
2. Aggregate results by reaction type, species, and outcome severity.
3. Present findings with appropriate context (reporting bias, denominator unknown).
4. Note any FDA safety communications or label changes resulting from adverse event signals.

### Reporting a New Adverse Event

1. Gather required information:
   - Animal signalment (species, breed, age, weight, sex)
   - Product involved (name, manufacturer, lot number if available)
   - Adverse event description (signs, timing, severity)
   - Outcome (recovered, ongoing, died)
   - Concurrent medications
   - Whether the veterinarian considers the event drug-related
2. Guide the user through FDA CVM reporting options:
   - Online: FDA Safety Reporting Portal
   - Phone: 1-888-FDA-VETS (1-888-332-8387)
   - Manufacturer reporting (companies are required to forward reports to FDA)

## Limitations

- openFDA adverse event data represents spontaneous reports, not incidence rates. Reporting rates are unknown.
- Absence of adverse event reports does not mean a product is safe.
- Adverse event reports do not establish causality.
- The openFDA API has rate limits and data may lag behind real-time reporting.
