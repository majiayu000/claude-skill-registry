---
name: faker
# prettier-ignore
description: Use when writing Vague (.vague) files that need realistic test data using faker generators for names, emails, addresses, dates, and more
---

# Faker Plugin for Vague

## Quick Start

```vague
schema User {
  id: uuid()
  name: fullName()
  email: email()
  phone: phone()
  city: city()
}
```

## Core Principles

- Use shorthand generators for common cases (no `faker.` prefix needed)
- Use full namespace `faker.module.method()` for less common generators

## Common Shorthand Generators

`uuid()`, `email()`, `phone()`, `firstName()`, `lastName()`, `fullName()`, `companyName()`, `city()`, `country()`, `countryCode()`, `zipCode()`, `streetAddress()`, `url()`, `avatar()`, `iban()`, `currencyCode()`, `pastDate()`, `futureDate()`, `sentence()`, `paragraph()`

## Full Namespace Example

```vague
schema Employee {
  title: faker.person.jobTitle()
  bio: faker.lorem.sentences(3)
  cardNumber: faker.finance.creditCardNumber()
}
```

## Reference Files

For complete generator list: [references/generators.md](references/generators.md)
