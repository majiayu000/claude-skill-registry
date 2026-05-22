---
name: heroku
description: Manage Heroku apps, dynos, and add-ons via CLI and API. Deploy and scale applications.
metadata: {"clawdbot":{"emoji":"🟣","requires":{"env":["HEROKU_API_KEY"]}}}
---
# Heroku
Platform as a Service.
## Environment
```bash
export HEROKU_API_KEY="xxxxxxxxxx"
```
## CLI Commands
```bash
heroku apps
heroku create app-name
heroku logs --tail -a app-name
heroku ps -a app-name
heroku ps:scale web=1 -a app-name
heroku config -a app-name
heroku config:set KEY=value -a app-name
```
## API - List Apps
```bash
curl "https://api.heroku.com/apps" \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3"
```
## API - Restart Dynos
```bash
curl -X DELETE "https://api.heroku.com/apps/{app}/dynos" \
  -H "Authorization: Bearer $HEROKU_API_KEY" \
  -H "Accept: application/vnd.heroku+json; version=3"
```
## Links
- Dashboard: https://dashboard.heroku.com
- Docs: https://devcenter.heroku.com/articles/platform-api-reference
