---
name: endpoint-implementation
description: Use this skill to implement endpoints in the API
---

## Structure of an endpoint slice

Read the docs/architecture/05-building-block-view.md file to understand how
feature groups and feature slices are structured. Each endpoint is a feature
slice with a specific structure described below.

### File structure

```text
- Users/                          # Feature group
- Prompts/                        # Feature group
- Repositories/                   # Feature group
  - OnboardUserRepository.cs      # Feature slice
  - Repository.cs                 # Aggregate root
  - UserRepositoryDetails.cs      # Read model
- Skills/                         # Feature group
```

## Endpoint code guidelines

- Use a record class to model the command, for example: `OnboardUserRepository`
- Use a record class to model the response `OnboardUserRepositoryResponse`
- Use a record class to model any events `UserRepositoryOnboarded`
- Use a class postfixed with `Endpoint` e.g. `OnboardUserRepositoryEndpoint` to structure the endpoint
- Use a method called `Handle` for the business logic in the endpoint. 
  - Use the `[WolverinePost("<url>")]`, `[WolverineGet("<url>")]`, `[WolverinePutt("<url>")]` or `[WolverineDelete("<url>")]` attributes to enable access via HTTP.
  - The method should return a tuple where the first element is the response object, the second element the event, and the final element the optional side-effects.
- Use a `Validate` method for any custom validations that you can't model with FluentValidation validators
