---
name: meta-remove
description: Удалить объект метаданных из конфигурации 1С. Используй когда пользователь просит удалить, убрать объект из конфигурации
argument-hint: <ConfigDir> -Object <Type.Name>
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# /meta-remove — удаление объекта метаданных

Безопасно удаляет объект из XML-выгрузки конфигурации. Перед удалением проверяет ссылки на объект в реквизитах, коде и других метаданных. Если ссылки найдены — удаление блокируется.

## Использование

```
/meta-remove <ConfigDir> -Object <Type.Name>
```

## Параметры

| Параметр   | Обязательный | Описание                                        |
|------------|:------------:|-------------------------------------------------|
| ConfigDir  | да           | Корневая директория выгрузки (где Configuration.xml) |
| Object     | да           | Тип и имя объекта: `Catalog.Товары`, `Document.Заказ` и т.д. |
| DryRun     | нет          | Только показать что будет удалено, без изменений |
| KeepFiles  | нет          | Не удалять файлы, только дерегистрировать       |
| Force      | нет          | Удалить несмотря на найденные ссылки            |

## Команда

```powershell
powershell.exe -NoProfile -File .claude/skills/meta-remove/scripts/meta-remove.ps1 -ConfigDir "<путь>" -Object "Catalog.Товары"
```

## Что делает

1. **Находит файлы объекта**: `{TypePlural}/{Name}.xml` и `{TypePlural}/{Name}/`
2. **Проверяет ссылки** (блокирует при наличии, если нет `-Force`):
   - XML-типы в реквизитах других объектов: `CatalogRef.Имя`, `DocumentRef.Имя` и т.д.
   - BSL-код: `Справочники.Имя`, `Catalogs.Имя`, вызовы общих модулей
   - Журналы документов, подписки на события, определяемые типы
3. **Удаляет из Configuration.xml**: убирает из `<ChildObjects>`
4. **Очищает подсистемы**: рекурсивно удаляет из `<Content>`
5. **Удаляет файлы**: XML-файл и каталог объекта

## Поддерживаемые типы

Catalog, Document, Enum, Constant, InformationRegister, AccumulationRegister, AccountingRegister, CalculationRegister, ChartOfAccounts, ChartOfCharacteristicTypes, ChartOfCalculationTypes, BusinessProcess, Task, ExchangePlan, DocumentJournal, Report, DataProcessor, CommonModule, ScheduledJob, EventSubscription, HTTPService, WebService, DefinedType, Role, Subsystem, CommonForm, CommonTemplate, CommonPicture, CommonAttribute, SessionParameter, FunctionalOption, FunctionalOptionsParameter, Sequence, FilterCriterion, SettingsStorage, XDTOPackage, WSReference, StyleItem, Language

## Вывод (объект без ссылок)

```
=== meta-remove: Catalog.Устаревший ===

[FOUND] Catalogs/Устаревший.xml
[FOUND] Catalogs/Устаревший/ (8 files)

--- Reference check ---
[OK]    No references found

--- Configuration.xml ---
[OK]    Removed <Catalog>Устаревший</Catalog> from ChildObjects
[OK]    Configuration.xml saved

--- Subsystems ---
[OK]    Removed from subsystem 'Справочники'

--- Files ---
[OK]    Deleted directory: Catalogs/Устаревший/
[OK]    Deleted file: Catalogs/Устаревший.xml

=== Done: 4 actions performed (1 subsystem references removed) ===
```

## Вывод (объект со ссылками — блокировка)

```
=== meta-remove: Catalog.Валюты ===

[FOUND] Catalogs/Валюты.xml
[FOUND] Catalogs/Валюты/ (4 files)

--- Reference check ---
[WARN]  Found 3 reference(s) to Catalog.Валюты:

        Documents/СчетНаОплату.xml
          pattern: CatalogRef.Валюты
        InformationRegisters/КурсыВалют.xml
          pattern: CatalogRef.Валюты
        CommonModules/РаботаСВалютами/Ext/Module.bsl
          pattern: Справочники.Валюты

[ERROR] Cannot remove: object has 3 reference(s).
        Use -Force to remove anyway, or fix references first.
```

Код возврата: 0 = успешно, 1 = ошибки или найдены ссылки.

## Проверяемые ссылки

| Категория | Паттерны поиска |
|-----------|----------------|
| XML-типы реквизитов | `CatalogRef.Name`, `DocumentRef.Name`, `EnumRef.Name` и др. |
| BSL-код (рус.) | `Справочники.Name`, `Документы.Name`, `Перечисления.Name` и др. |
| BSL-код (англ.) | `Catalogs.Name`, `Documents.Name`, `Enums.Name` и др. |
| Общие модули | `Name.` (вызовы методов), `<Handler>Name.`, `<MethodName>Name.` |

Ссылки из Configuration.xml, ConfigDumpInfo.xml и подсистем НЕ считаются блокирующими — они очищаются автоматически.

## Примеры

```powershell
# Проверка ссылок + dry run
... -ConfigDir C:\WS\tasks\cfsrc\acc_8.3.24 -Object "Catalog.Устаревший" -DryRun

# Удалить объект без ссылок
... -ConfigDir C:\WS\tasks\cfsrc\acc_8.3.24 -Object "Catalog.Устаревший"

# Принудительно удалить несмотря на ссылки
... -ConfigDir C:\WS\tasks\cfsrc\acc_8.3.24 -Object "Catalog.Устаревший" -Force

# Только дерегистрировать (файлы оставить)
... -ConfigDir C:\WS\tasks\cfsrc\acc_8.3.24 -Object "Report.Старый" -KeepFiles

# Удалить общий модуль
... -ConfigDir src -Object "CommonModule.МойМодуль"
```

## Когда использовать

- **Рефакторинг**: удаление неиспользуемых объектов
- **Очистка**: удаление временных/тестовых объектов
- **Перенос**: удаление объекта перед пересозданием с другой структурой
