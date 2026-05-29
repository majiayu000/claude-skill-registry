---
name: surveymonkey
description: Create surveys and collect responses via SurveyMonkey API. Manage surveys, view results, and export data.
metadata: {"clawdbot":{"emoji":"📋","requires":{"env":["SURVEYMONKEY_ACCESS_TOKEN"]}}}
---

# SurveyMonkey

Survey and feedback platform.

## Environment

```bash
export SURVEYMONKEY_ACCESS_TOKEN="xxxxxxxxxx"
```

## List Surveys

```bash
curl "https://api.surveymonkey.com/v3/surveys" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## Get Survey Details

```bash
curl "https://api.surveymonkey.com/v3/surveys/{survey_id}/details" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## Get Responses

```bash
curl "https://api.surveymonkey.com/v3/surveys/{survey_id}/responses/bulk" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN"
```

## Create Survey

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Customer Feedback"}'
```

## Add Page to Survey

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys/{survey_id}/pages" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Page 1"}'
```

## Add Question

```bash
curl -X POST "https://api.surveymonkey.com/v3/surveys/{survey_id}/pages/{page_id}/questions" \
  -H "Authorization: Bearer $SURVEYMONKEY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "family": "single_choice",
    "subtype": "vertical",
    "headings": [{"heading": "How satisfied are you?"}],
    "answers": {"choices": [{"text": "Very satisfied"}, {"text": "Satisfied"}, {"text": "Not satisfied"}]}
  }'
```

## Links
- Dashboard: https://www.surveymonkey.com
- Docs: https://developer.surveymonkey.com/api/v3/
