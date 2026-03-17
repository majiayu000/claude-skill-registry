---
name: revenuecat
description: RevenueCat metrics, customer data, and documentation search. Use when querying subscription analytics, MRR, churn, customers, or RevenueCat docs.
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "😻",
        "requires": { "bins": ["curl"], "env": ["RC_API_KEY"] },
        "primaryEnv": "RC_API_KEY",
      },
  }
---

# RevenueCat

Query RevenueCat metrics and search documentation.

## Config

Set `RC_API_KEY` environment variable, which should be a v2 secret API key.

## Context

Query the RevenueCat API (`GET /projects`) to get information about the project you have access to. Your RevenueCat API key allows access to a single project. Use the project ID in subsequent API calls.

## API Access

```bash
{baseDir}/scripts/rc-api.sh <endpoint>
```

Example: `{baseDir}/scripts/rc-api.sh /projects` to list projects.

## Local API Reference

Start with `{baseDir}/references/api-v2.md` for auth, pagination, and common patterns. Then load the domain file you need:

| Domain             | File                               | Covers                                                                                                   |
| ------------------ | ---------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Customers          | `references/customers.md`          | CRUD, attributes, aliases, entitlements, subscriptions, purchases, invoices, virtual currencies, actions |
| Subscriptions      | `references/subscriptions.md`      | List, get, transactions, cancel, refund, management URL                                                  |
| Products           | `references/products.md`           | CRUD, create in store, test prices                                                                       |
| Offerings          | `references/offerings.md`          | Offerings, packages, package products                                                                    |
| Entitlements       | `references/entitlements.md`       | CRUD, attach/detach products                                                                             |
| Purchases          | `references/purchases.md`          | List, get, refund, entitlements                                                                          |
| Projects           | `references/projects.md`           | Projects, apps, API keys, StoreKit config                                                                |
| Metrics            | `references/metrics.md`            | Overview metrics, charts, chart options                                                                  |
| Paywalls           | `references/paywalls.md`           | Paywall creation                                                                                         |
| Integrations       | `references/integrations.md`       | Integrations CRUD                                                                                        |
| Virtual Currencies | `references/virtual-currencies.md` | Virtual currencies CRUD                                                                                  |
| Error Handling     | `references/error-handling.md`     | Error handling                                                                                           |
| Rate Limits        | `references/rate-limits.md`        | Rate limits                                                                                              |

Only load the reference file relevant to the current task — don't load them all.

## Remote Documentation Search

The RevenueCat documentation is available at https://www.revenuecat.com/docs. Use https://www.revenuecat.com/docs/llms.txt and /sitemap.xml as a guide to the content that is available. Add .md to the end of a documentation URL to get the markdown version of the page.
