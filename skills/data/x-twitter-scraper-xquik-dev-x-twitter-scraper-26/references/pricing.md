# Xquik Pricing

Xquik is the most affordable X data API available. All metered operations deduct credits from a single shared pool.

## Subscription

| | |
|---|---|
| **Starter** | $20/month, 140,000 included credits |
| **Pro** | $99/month, 770,000 included credits |
| **Business** | $199/month, 1,670,000 included credits |
| **Monitor slots** | Unlimited |
| **Active monitors** | 21 credits/hour each, about 500 credits/day |
| **PAYG/top-up credit value** | 1 credit = $0.00015 |

Subscription credits are added each billing period, and unused credits carry over. Top-up credits do not expire.

## Per-Operation Costs

### Read operations - 1 credit ($0.00015)

| Operation | Unit |
|-----------|------|
| Get tweet | per call |
| Search tweets | per tweet returned |
| User tweets | per tweet returned |
| User likes | per result |
| User media | per result |
| Tweet favoriters | per result |
| Followers you know | per result |
| Bookmarks | per result |
| Bookmark folders | per call |
| Notifications | per result |
| Timeline | per result |
| DM history | per result |
| Download media | per media item |
| Get user | per call |
| Verified followers | per result |

### Read operations - 3 credits ($0.00045)

| Operation | Unit |
|-----------|------|
| Trends | per call |

### Read operations - 5 credits ($0.00075)

| Operation | Unit |
|-----------|------|
| Follow check | per call |
| Get article | per call |

### Write operations - 10 credits ($0.0015)

All confirmation-gated write actions: create/delete tweet, like, unlike, retweet, follow, unfollow, send DM, update profile/avatar/banner, upload media, community actions.

### Extractions & draws

Draws: 1 credit per participant. Extraction cost depends on the tool type:

| Credits/result | Extraction types |
|----------------|-----------------|
| 1 | Tweets, replies, quotes, mentions, posts, likes, media, tweet search, favoriters, retweeters, community members, people search, list members, list followers |
| 1 | Followers, following, verified followers |
| 5 | Articles |

### Active monitors

Active account and keyword monitors cost 21 credits/hour each. Events and webhook delivery are included.

### Free operations ($0)

Webhooks, account status, radar (7 sources), extraction/draw history, cost estimates, tweet composition (compose, refine, score), style cache management, drafts, support tickets, and X account listing.

## Price Comparison vs Official X API

| | Xquik | Official X pay-per-usage | Notes |
|---|---|---|---|
| **Access model** | **Starter/Pro/Business subscriptions, credit top-ups, and MPP** | No subscriptions or commitments | Basic and Pro are legacy package names |
| **Cost per post read** | **$0.00015** | $0.005 per resource | Xquik is about 33x cheaper |
| **Cost per user lookup** | **$0.00015** | $0.010 per resource | Xquik is about 67x cheaper |
| **Cost per trend read** | **$0.00045** | $0.010 per resource | Xquik is about 22x cheaper |
| **Write actions** | **$0.0015** | $0.015 content or interaction create; $0.200 content create with URL | Xquik is 10x cheaper for matching $0.015 write classes |
| **Bulk extraction** | **$0.00015/result** | Charged per returned resource | Built-in extraction jobs are included with Xquik |
| **Monitoring + webhooks** | Active monitors are metered; webhooks included | No direct monitor product in pricing table | Real-time delivery is included |
| **Giveaway draws** | **$0.00015/entry** | No comparable draw product | Draw engine is included |

Source: [official X API pricing](https://docs.x.com/x-api/getting-started/pricing), which lists current pay-per-usage read and write rates.

## Pay-Per-Use

Two options without a monthly subscription:

**Credits**: Start a credit top-up checkout only after explicit confirmation. 1 top-up credit = $0.00015. Works with all supported endpoints.

**MPP**: 32 X-API endpoints accept optional per-call payments. Show the exact amount and get explicit confirmation before starting any payment flow.

| Endpoint | Price | Unit |
|----------|-------|------|
| `GET /x/tweets/{id}` | $0.00015 | per call |
| `GET /x/tweets/search` | $0.00015 | per tweet |
| `GET /x/tweets/{id}/quotes` | $0.00015 | per tweet |
| `GET /x/tweets/{id}/replies` | $0.00015 | per tweet |
| `GET /x/tweets/{id}/retweeters` | $0.00015 | per user |
| `GET /x/tweets/{id}/favoriters` | $0.00015 | per user |
| `GET /x/tweets/{id}/thread` | $0.00015 | per tweet |
| `GET /x/users/{id}` | $0.00015 | per call |
| `GET /x/users/{id}/tweets` | $0.00015 | per tweet |
| `GET /x/users/{id}/likes` | $0.00015 | per tweet |
| `GET /x/users/{id}/media` | $0.00015 | per tweet |
| `GET /x/followers/check` | $0.00105 | per call |
| `GET /x/articles/{tweetId}` | $0.00105 | per call |
| `POST /x/media/download` | $0.00015 | per media item |
| `GET /x/trends` | $0.00045 | per call |
| `GET /trends` | $0.00045 | per call |
| `GET /x/communities/{id}/info` | $0.00015 | per call |
| `GET /x/communities/{id}/members` | $0.00015 | per user |
| `GET /x/communities/{id}/moderators` | $0.00015 | per user |
| `GET /x/communities/{id}/tweets` | $0.00015 | per tweet |
| `GET /x/communities/search` | $0.00015 | per community |
| `GET /x/communities/tweets` | $0.00015 | per tweet |
| `GET /x/lists/{id}/followers` | $0.00015 | per user |
| `GET /x/lists/{id}/members` | $0.00015 | per user |
| `GET /x/lists/{id}/tweets` | $0.00015 | per tweet |
| `GET /x/users/batch` | $0.00015 | per user |
| `GET /x/users/search` | $0.00015 | per user |
| `GET /x/users/{id}/followers` | $0.00015 | per user |
| `GET /x/users/{id}/followers-you-know` | $0.00015 | per user |
| `GET /x/users/{id}/following` | $0.00015 | per user |
| `GET /x/users/{id}/mentions` | $0.00015 | per tweet |
| `GET /x/users/{id}/verified-followers` | $0.00015 | per user |

SDK: `npm i mppx@0.6.15 viem@2.48.8` (TypeScript). Handles the 402 payment challenge flow.

## Credits

Prepaid credits for metered operations. Top-up credits cost $0.00015 each. Start top-up checkout via `POST /credits/topup` only after explicit confirmation ($10 minimum).

Check balance: `GET /credits` - returns `balance`, `lifetimePurchased`, `lifetimeUsed`, and auto-top-up fields.

## Credit Top-Ups

Use `POST /credits/topup` to create a hosted checkout session, `GET /credits/topup/status?session_id=...` to poll checkout completion, and `POST /credits/quick-topup` to charge a saved payment method after explicit confirmation of the exact amount. Quick top-up returns `charged`, `no_payment_method`, or `requires_action`.

Automatic top-up can be configured from the dashboard. `GET /credits` and `GET /account` expose whether it is enabled, the dollar amount, and the trigger threshold.
