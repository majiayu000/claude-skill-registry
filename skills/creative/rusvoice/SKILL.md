---
name: rusvoice
description: 'Prepare Russian text for text-to-speech and see what the pipeline will
  do to it before synthesis: stress marks, a brand dictionary, hard ''e'' in loanwords,
  abbreviations read letter by letter, numbers spelled out. Ships a CLI whose core
  runs on the bare standard library.'
---
# rusvoice: слой правки текста перед синтезом

Клонировать голос умеет открытый код. Дефицитен слой ПЕРЕД синтезом: ударения,
бренды, заимствования, аббревиатуры, числа. И возможность увидеть результат до
того, как его услышишь.

## Установка

```bash
pip install rusvoice                    # ядро: explain / lint / dict / doctor
pip install "rusvoice[accent,ui]"       # + ударения (RUAccent) и экран
pip install "rusvoice[voice,accent]"    # + сам синтез (F5)
```

Ядро зависимостей не имеет и ставится куда угодно. Экстра `voice` тянет torch,
веса качаются при первом запуске, около 2,5 ГБ: предупреди человека до того, как
запускать установку.

## Главная команда

```bash
rusvoice explain "Компания Knight Capital потеряла 440 миллионов, ТЗ было на MVP."
```

Печатает вход, выход и что сделал каждый слой, а внизу честно говорит, чего в
окружении нет. Вот эта нижняя часть и есть смысл затеи: без неё окружение
промолчало бы, а озвучка вышла бы с неверными ударениями.

## Остальное

- `rusvoice lint scenario.json`: находит места, где тракт прочтёт не то, и
  подсказывает, что дописать в словарь.
- `rusvoice dict add brands Netlify Нетлифай`: пополнить словарь.
  `dict hear brands Netlify` даёт услышать запись, а не прочитать её.
- `rusvoice doctor`: что доступно именно этому интерпретатору.
- `rusvoice say "реплика" --out o.wav`: синтез, если стоит экстра `voice`.

## Как себя вести

**Запускай тем же интерпретатором, каким пойдёт синтез.** RUAccent и F5 обычно
живут в другом окружении, и `doctor` показывает это честно: в этом половина его
смысла. Проверь `doctor` прежде, чем обещать человеку правильные ударения.

Не переписывай текст за автора ради удобства синтеза. Задача слоя в том, чтобы
диктор прочитал написанное правильно, а не в том, чтобы упростить фразу.

Если читаешь вывод из своего кода на Windows, указывай кодировку явно:
`subprocess.run(..., text=True, encoding="utf-8")`. Без неё Python декодирует по
кодировке системы и отдаёт `None`, что выглядит как «CLI ничего не напечатал».

## Рядом

[github.com/ilyautov](https://github.com/ilyautov), лаборатория
[AI Frontier](https://aifrontier.tech).
