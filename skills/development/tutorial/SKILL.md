---
name: tutorial
description: Добро пожаловать, путник! \
---

# Первый навык

Добро пожаловать, путник! \
Здесь будет представлено, как можно взаимодействовать с `API Алисы` и отвечать на его запросы.

## База

Перед тем, как начать разработку навыка для Алисы, важно знать [официальную документацию](https://yandex.ru/dev/dialogs/alice/doc/){:target="_blank"} и принцип работы навыков.

Взаимодействие с Алисой происходит через [webhook](https://www.google.com/search?q=%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA+%D1%8D%D1%82%D0%BE){:target="_blank"}'и (или облачные функции) -
Яндекс отправляет запрос с новым событие навыка, он что-то думает и возвращает ответ. Навыки не опрашивают Алису на предмет новых сообщений, действий и так далее. \
Здесь нет [pooling](https://www.google.com/search?q=%D0%BF%D1%83%D0%BB%D0%B8%D0%BD%D0%B3+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D1%8D%D1%82%D0%BE){:target="_blank"}'а,
поэтому нельзя узнать, принял ли Яндекс ваш ответ без ошибок (но не всегда).

!!! warning "Важно"
    Именно из-за вебхуков все хэндлеры (и мидлвари) обязаны что-то вернуть, иначе Алиса завершит сессию пользователя.

## Типизация

На момент создания библиотеки разработчики постарались перевести все json-объекты из документации в модели pydantic'а, которые и являются подсказками типов. \
В моделях не учтены все возможные ограничения Алисы (например, размер всего ответа),
поэтому обязательно уточняйте их в официальной документации и тестируйте свои навыки.

## Первые шаги

Начнём с написания простого эхо-навыка.
Для начала работы следует ознакомиться с основными классами фреймворка: `Skill`, `Dispatcher`, и `OneSkillAiohttpRequestHandler`.

```python
from aiohttp import web
from aliceio import Dispatcher, Skill
from aliceio.types import AliceResponse, Message, Response  # О типах чуть позже
from aliceio.webhook.aiohttp_server import OneSkillAiohttpRequestHandler, setup_application

dp = Dispatcher()
skill = Skill(skill_id="...")
```

При иницализации навыка нужно указать его айди (обязательно) и OAuth Token (опицонально). \
Первый позволяет игнорировать запросы, адресованные не этому навыку, а второй даёт возможность взаимодействовать с файлами ваших навыков.

Теперь в диспетчер можно добавить нужный обработчик:

```python
@dp.message()
async def message_handler(message: Message) -> AliceResponse:
    if message.session.new:
        text = "Привет!"
    else:
        text = message.original_text
    return AliceResponse(response=Response(text=text))
```

Разберём этот фрагмент построчно:

`#!python @dp.message()` - это декоратор, который регистрирует функцию-обработчик, которая сработает, если сообщение будет отвечать заданным фильтрам.
Здесь их нет, поэтому функция будет срабатывать на каждое сообщение.

`#!python async def message_handler(message: Message) -> AliceResponse:` - сигнатура функции-обработчика, в которой первым аргументом всегда будет текущее событие.
Эта функция возвращает `#!python AliceResponse`, но фреймворк поддерживает и другие варианты.

`#!python if message.session.new:` - проверяем, первое ли это сообщение в текущей сессии (т.е. пользователь только открыл навык).
Если это так, то вместо эха будет приветствие.

`#!python return AliceResponse(response=Response(text=text))` - возвращаем полный объект, который ждёт Алиса.
Вместо него можно вернуть просто `#!python Response` или `#!python str`, которая станет текстом.

## Запуск

Теперь надо как-то запустить эту шайтан-машину, чтобы она принимала запросы от Алисы. \
Для этого напишем простую точку входа, которая будет чуть модифицирована в дальнейшем:

```python
def main() -> None:
    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    # Навык принимает запросы по пути http://127.0.01:80/alice
    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()
```


## Примеры

* [echo_skill.py](https://github.com/K1rL3s/aliceio/blob/master/examples/echo_skill.py){:target="_blank"}
* [echo_skill_ssl.py](https://github.com/K1rL3s/aliceio/blob/master/examples/echo_skill_ssl.py){:target="_blank"}
* [fast_start.py](https://github.com/K1rL3s/aliceio/blob/master/examples/fast_start.py){:target="_blank"}

Полный код из этой главы:

```python
from aiohttp import web

from aliceio import Dispatcher, Skill
from aliceio.types import AliceResponse, Message, Response
from aliceio.webhook.aiohttp_server import OneSkillAiohttpRequestHandler, setup_application


dp = Dispatcher()
skill = Skill(skill_id="...", oauth_token="...")


@dp.message()
async def message_handler(message: Message) -> AliceResponse:
    if message.session.new:
        text = "Привет!"
    else:
        text = message.original_text
    return AliceResponse(response=Response(text=text))


def main() -> None:
    app = web.Application()
    requests_handler = OneSkillAiohttpRequestHandler(
        dispatcher=dp,
        skill=skill,
    )

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80
    WEBHOOK_PATH = "/alice"

    requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, skill=skill)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
```
