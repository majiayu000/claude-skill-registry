---
name: free-apis-catalog
description: Use when suggesting APIs for a project, looking for free data sources, building weekend projects that need external data, or when the user needs weather, news, finance, sports, ML, or entertainment data without paid subscriptions
---

# Free public APIs catalog

A curated list of 1000+ free, legal public APIs organized by category. Many require no auth.

## Quick reference by category

### Finance and crypto
CoinGecko, CoinCap, Alpha Vantage, Open Exchange Rates, FRED (Federal Reserve Economic Data)

### News and media
NewsAPI, GNews, TheNewsAPI, MediaStack, New York Times API
- Headlines, RSS, aggregators, real-time sentiment

### Weather and geolocation
- **Open-Meteo** — fully free, no API key required
- OpenWeatherMap, WeatherAPI, Visual Crossing
- Temperature, precipitation, forecasts, historical data for any coordinates

### Sports
API-Football, TheSportsDB, PandaScore, ESPN API
- Results, team form, player stats, historical league data

### ML and text analysis
Hugging Face Inference API, Cohere
- Classification, sentiment, summarization, embeddings — pre-trained models

### Entertainment
TMDB (movies/TV), RAWG (games), MusicBrainz (music)
- Charts, ratings, metadata

### Also available (in the full catalog)
Politics, law, health, science, transport, government open data

## Evaluating APIs from the catalog

| Field | What to check |
|-------|---------------|
| Auth | "No" = no registration needed |
| CORS | Matters for browser frontend, irrelevant for backend scripts |
| Limits | Most free APIs have daily caps — usually enough for personal tools |

## Weekend project ideas

- **News alerts**: NewsAPI + keyword filter + Telegram bot (2-3 hours)
- **Sentiment signal**: News feed + Hugging Face sentiment model + score -1 to +1
- **Weather dashboard**: Open-Meteo + historical data + forecast for target city
- **Sports aggregator**: Team form, injuries, home advantage in one view

## Usage tip

For any new project needing external data: check this catalog first before assuming you need a paid API. Feed the full list to an agent and ask what's useful for the specific task — it will find connections you'd miss manually.

## Attribution

Based on ["1000+ Free APIs That Will Replace Your Paid Subscriptions"](https://x.com/qwerty_ytrevvq) by [@qwerty](https://x.com/qwerty_ytrevvq) on X (Mar 10, 2026). Original thread catalogs free public APIs across finance, news, weather, sports, ML, entertainment, and more, with evaluation criteria and build ideas.
