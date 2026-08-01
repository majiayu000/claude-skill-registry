---
name: concepts-toloka-docs
description: '{% include announce %}'
---

# Задать значение навыка

{% include [announce](../_includes/announce.md) %}

Задает значение навыка.

{% note alert "Ограничение" %}

Можно отправить не более 100 000 таких запросов в день.

{% endnote %}

## Запрос {#request}

{% list tabs %}

- Боевая версия

    ```bash
    PUT https://toloka.dev/api/v1/user-skills
    Authorization: ApiKey PlaceYourRealApiKey_Here
    Content-Type: application/json
    ```

- Песочница

    ```bash
    PUT https://sandbox.toloka.dev/api/v1/user-skills
    Authorization: ApiKey PlaceYourRealApiKey_Here
    Content-Type: application/json
    ```

{% endlist %}

## Заголовки {#headers}

{% include [reusables-auth-content](../_includes/reusables/id-reusables/auth-content.md) %}

## Тело запроса {#body}

```json
{
  "skill_id": 32,
  "user_id": "566ec2b0ff0deeaae5f9d500",
  "value": 59.7,
  "reason": "High-quality performance of tasks"
}
```

#|
||**Параметр** | **Описание**||
||**skill_id** | **string \| обязательный**

Идентификатор навыка.||
||**user_id** | **string \| обязательный**

Идентификатор исполнителя.||
||**value** | **float \| обязательный**

Дробное значение навыка. Минимум — 0, максимум — 100.||
||**reason** | **string**

Причина изменения или назначения навыка.||
|#

## Ответ {#response}

Обновленное значение навыка.

```json
{
  "id": "43",
  "skill_id": "32",
  "user_id": "566ec2b0ff0deeaae5f9d500",
  "value": 60,
  "exact_value": 59.7,
  "created": "2021-06-17T09:30:11.681",
  "modified": "2021-05-19T10:52:22.130"
}
```

#|
||**Параметр** | **Описание**||
||**id** | **string**

Идентификатор навыка исполнителя, присваивается паре «навык-исполнитель»||
||**skill_id** | **string**

Идентификатор навыка.||
||**user_id** | **string**

Идентификатор исполнителя.||
||**value** | **integer**

Целое значение навыка (`exact_value`, округленное до ближайшего целого).
 Минимум — 0, максимум — 100.||
||**exact_value** | **float**

Дробное значение навыка. Минимум — 0, максимум — 100.||
||**created** | **string**

Дата и время по UTC, когда исполнителю был впервые присвоен навык с заданным значением. Формат даты ISO 8601: `YYYY-MM-DDThh:mm:ss[.sss]`.||
||**modified** | **string**

Дата и время по UTC, когда изменился уровень навыка у исполнителя. Формат даты ISO 8601: `YYYY-MM-DDThh:mm:ss[.sss]`.||
|#