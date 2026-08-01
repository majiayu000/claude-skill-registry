---
name: concepts
description: '{% include announce %}'
---

# Получить свойства навыка

{% include [announce](../_includes/announce.md) %}

Получает свойства навыка.

Идентификатор навыка можно узнать из [списка навыков](get-skill-list.md).

## Запрос {#request}

{% list tabs %}

- Боевая версия

    ```bash
    GET https://toloka.dev/api/v1/skills/<id>
    Authorization: ApiKey PlaceYourRealApiKey_Here
    ```

- Песочница

    ```bash
    GET https://sandbox.toloka.dev/api/v1/skills/<id>
    Authorization: ApiKey PlaceYourRealApiKey_Here
    ```

{% endlist %}

## Path-параметры {#path-params}

{% include [edit-skill-skill-id-table](../_includes/concepts/edit-skill/id-edit-skill/skill-id-table.md) %}

## Заголовки {#headers}

{% include [reusables-auth](../_includes/reusables/id-reusables/auth.md) %}

## Ответ {#response}

Сведения о навыке.

```json
{
  "id": "9238",
  "name": "Determining the color of an elephant",
  "private_comment": "Skill for my pool",
  "hidden": true,
  "skill_ttl_hours": 240,
  "deprecated": false,
  "owner": {
    "id": "c3a50f44cd3e1b8202465569ced289eb",
    "myself": true
  },
  "training": true,
  "created": "2021-12-01T08:37:03.387",
  "global": false
}
```

{% include [create-skill-params-table-response](../_includes/concepts/create-skill/id-create-skill/params-table-response.md) %}