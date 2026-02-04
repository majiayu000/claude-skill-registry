---
name: migrate
description: Migracja sesji Claude Code z innego urządzenia (Windows/Android). Triggers: migrate, przenieś sesje, importuj
---

Uzytkownik chce zmigrowac konwersacje Claude Code z innego komputera.

## KROK 1: Uruchom GUI

**Ścieżki (sprawdź w kolejności):**
1. `D:\Projekty StriX\KFG\scripts\migrate\migrate_gui.py`
2. `C:\Users\kamil\projekty\KFG\scripts\migrate\migrate_gui.py`
3. `~/.templates/scripts/migrate_gui.py` (installed via desktop/install.ps1)

```powershell
# Znajdź i uruchom
$paths = @(
    "D:\Projekty StriX\KFG\scripts\migrate\migrate_gui.py",
    "C:\Users\kamil\projekty\KFG\scripts\migrate\migrate_gui.py",
    "$env:USERPROFILE\.templates\scripts\migrate_gui.py"
)
foreach ($path in $paths) {
    if (Test-Path $path) {
        Start-Process pythonw -ArgumentList $path
        break
    }
}
```

Poinformuj usera: "Otworzylem okno migracji. Wybierz konwersacje i kliknij 'Migruj wybrane'. Daj znac jak skonczysz."

## KROK 2: Po zakonczeniu przez usera
Przeczytaj wynik:
```python
import json
from pathlib import Path
import os

result_file = Path(os.environ["USERPROFILE"]) / ".claude" / "migration_result.json"
if result_file.exists():
    with open(result_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Status: {data['status']}")
    if data['result']:
        r = data['result']
        print(f"Zmigrowano: {r['success']}/{r['total']}")
        print(f"Session IDs: {r['session_ids'][:3]}")
```

Pokaz userowi wynik i session_id do `claude --resume <id>`
