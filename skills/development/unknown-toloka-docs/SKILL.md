# Удалить навык у исполнителя

{% include [announce](../_includes/announce.md) %}

Удаляет навык у исполнителя.

## Запрос {#request}

{% list tabs %}

- Боевая версия

    ```bash
    DELETE https://toloka.dev/api/v1/user-skills/<id>
    Authorization: ApiKey PlaceYourRealApiKey_Here
    ```

- Песочница

    ```bash
    DELETE https://sandbox.toloka.dev/api/v1/user-skills/<id>
    Authorization: ApiKey PlaceYourRealApiKey_Here
    ```

{% endlist %}

## Path-параметры {#path-params}

{% include [get-user-skill-skill-user-id-table](../_includes/concepts/get-user-skill/id-get-user-skill/skill-user-id-table.md) %}

## Заголовки {#headers}

{% include [reusables-auth](../_includes/reusables/id-reusables/auth.md) %}