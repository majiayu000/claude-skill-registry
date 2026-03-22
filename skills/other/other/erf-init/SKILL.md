---
name: erf-init
description: Создать пустой внешний отчёт 1С (scaffold XML-исходников)
argument-hint: <Name> [Synonym] [--with-skd]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /erf-init — Создание нового отчёта

Генерирует минимальный набор XML-исходников для внешнего отчёта 1С: корневой файл метаданных и каталог отчёта.

## Usage

```
/erf-init <Name> [Synonym] [SrcDir] [--with-skd]
```

| Параметр  | Обязательный | По умолчанию | Описание                              |
|-----------|:------------:|--------------|---------------------------------------|
| Name      | да           | —            | Имя отчёта (латиница/кириллица)       |
| Synonym   | нет          | = Name       | Синоним (отображаемое имя)            |
| SrcDir    | нет          | `src`        | Каталог исходников относительно CWD   |
| --WithSKD | нет          | —            | Создать пустую СКД и привязать к MainDataCompositionSchema |

## Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/erf-init/scripts/init.ps1 -Name "<Name>" [-Synonym "<Synonym>"] [-SrcDir "<SrcDir>"] [-WithSKD]
```

## Что создаётся

```
<SrcDir>/
├── <Name>.xml          # Корневой файл метаданных (4 UUID)
└── <Name>/
    └── Ext/
        └── ObjectModule.bsl  # Модуль объекта с 3 регионами
```

При `--WithSKD` дополнительно:

```
<SrcDir>/<Name>/
    Templates/
    ├── ОсновнаяСхемаКомпоновкиДанных.xml        # Метаданные макета
    └── ОсновнаяСхемаКомпоновкиДанных/
        └── Ext/
            └── Template.xml                      # Пустая СКД
```

- Корневой XML содержит `MetaDataObject/ExternalReport` с пустыми `DefaultForm`, `MainDataCompositionSchema` и `ChildObjects`
- При `--WithSKD` — `MainDataCompositionSchema` заполняется ссылкой на макет, `ChildObjects` содержит `<Template>`
- ClassId фиксирован: `e41aff26-25cf-4bb6-b6c1-3f478a75f374`
- Файл создаётся в UTF-8 с BOM

## Дальнейшие шаги

- Добавить форму: `/form-add`
- Добавить макет: `/template-add`
- Добавить справку: `/help-add`
- Собрать ERF: `/erf-build`
