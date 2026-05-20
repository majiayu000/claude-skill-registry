---
name: microservice-architect
description: "Guides the planning of a microservices architecture. Use this skill when asked to design, plan, or architect a system using microservices. This skill helps with service boundary identification, communication pattern selection, data management, and defining service contracts."
---

# Microservice Architect

## Overview

This skill provides a structured workflow for planning a microservices architecture. It helps in making key architectural decisions and producing standard deliverables.

The process is divided into four main steps. Follow them in order to ensure a comprehensive design.

## Step 1: Decompose the System into Services

The first step is to identify the boundaries of each microservice. The goal is to create services that are loosely coupled and highly cohesive.

- **Action**: Use the service decomposition template to document each proposed service.
- **Template**: `assets/templates/service_decomposition_template.md`
- **Guidelines**: Refer to `references/service_decomposition.md` for criteria on how to define service boundaries, based on principles like Domain-Driven Design.

For each potential service, copy the template and fill it out.

## Step 2: Define Communication Patterns

Once services are identified, determine how they will communicate with each other.

- **Action**: For each interaction between services, choose a suitable communication pattern.
- **Decision Matrix**: Use the matrix in `assets/templates/communication_matrix_template.md` to help select between REST, gRPC, GraphQL, and messaging.
- **Reference**: For more details on each pattern, see `references/communication_patterns.md`.

Not all services need to use the same pattern. Choose the best fit for each interaction.

## Step 3: Plan Data Management and Infrastructure

Address how data will be managed across services and what infrastructure is needed.

- **Data Ownership**: Follow the database-per-service pattern. See `references/data_patterns.md` for details on this and handling distributed transactions with the Saga pattern.
- **Infrastructure**: Plan for service discovery and an API gateway. Guidance can be found in `references/infrastructure.md`.
- **Event-Driven**: If asynchronous communication is used, review patterns for event-driven architecture in `references/event_driven.md`.

## Step 4: Create Architecture Diagrams and Service Contracts

The final step is to document the architecture and the service APIs.

- **Architecture Diagrams**: Use the C4 model to visualize the architecture. Create System Context and Container diagrams at a minimum. See `references/c4_model.md` for an explanation of the C4 model.
- **Service Contracts**: For each service, create a formal API contract.
  - **Template**: A basic OpenAPI template is available at `assets/templates/service_contract_template.json`.
  - **Guidelines**: See `references/service_contracts.md` for details on what to include in a contract and different specification formats.

## Deliverables

By the end of this process, you will have produced:
- A set of completed service decomposition documents.
- A communication matrix for service interactions.
- C4 model architecture diagrams.
- Service interface contracts for each service.
