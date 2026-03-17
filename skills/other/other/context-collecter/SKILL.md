---
name: context-collecter
description: >
  Zbiera, zapisuje i ładuje kontekst osobisty i firmowy w 20 warstwach informacyjnych.
  Tryb zapisu: "zapamiętaj że...", "zapisz że...", "zanotuj...", "dodaj do kontekstu...".
  Tryb briefingu: "zbierz kontekst o...", "przeprowadź wywiad o...", "uzupełnij warstwę...",
  "wyciągnij ze mnie info o...", "zbierz info o mojej roli / firmie / zespole",
  "opowiedz mi o swojej [kategorii]".
  Tryb montowania: "zamontuj kontekst...", "załaduj kontekst o...", "pokaż kontekst...",
  "daj mi kontekst o...", "co wiesz o mnie...", "podsumuj mój kontekst...".
  Tryb edycji: "popraw...", "zmień to że...", "usuń wpis...", "zaktualizuj...".
  Zawsze komunikuje się po polsku.
---

# Context Collecter

Skill do zarządzania kontekstem osobistym i firmowym w 20 warstwach informacyjnych.

**Zawsze komunikuje się po polsku.**

---

## Przechowywanie danych

Ścieżka bazowa: `~/.claude/context/`

- `~/.claude/context/private/` — 10 warstw prywatnych
- `~/.claude/context/company/` — 10 warstw firmowych

**Linki między warstwami:** `[[company/technologia]]`, `[[private/relacje]]`
Przy wczytywaniu warstwy — automatycznie podążaj za linkami do powiązanych warstw.

---

## Warstwy prywatne (`~/.claude/context/private/`)

| Plik | Zawartość |
|------|-----------|
| `tozsamosc.md` | Kim jestem, background, dane bazowe |
| `wartosci.md` | Core values, filozofia życiowa |
| `cele.md` | Cele krótko i długoterminowe |
| `rodzina.md` | Struktura rodziny, bliskie osoby |
| `zdrowie.md` | Stan zdrowia, nawyki, aktywność |
| `finanse-osobiste.md` | Sytuacja finansowa, cele, nawyki |
| `hobby.md` | Pasje, aktywności, czas wolny |
| `styl-zycia.md` | Codzienne rutyny, preferencje |
| `rozwoj.md` | Nauka, umiejętności, książki |
| `relacje.md` | Sieć kontaktów, ważne osoby |

## Warstwy firmowe (`~/.claude/context/company/`)

| Plik | Zawartość |
|------|-----------|
| `firma.md` | Misja, wizja, etap, historia |
| `moja-rola.md` | Tytuł, odpowiedzialności, zakres decyzji |
| `zespol.md` | Struktura, kluczowe osoby, dynamika |
| `produkty.md` | Oferta, rozwiązywane problemy, plany |
| `klienci.md` | ICP, segmenty, kluczowe konta |
| `procesy.md` | Workflow, narzędzia, rytm pracy |
| `strategia.md` | Kierunek, OKRy, priorytety |
| `technologia.md` | Tech stack, narzędzia, infrastruktura |
| `finanse-firmy.md` | Model biznesowy, przychody, funding |
| `wyzwania.md` | Aktualne problemy, blokery, focus |

---

## Format pliku warstwy

Wolna forma Markdown. Każdy wpis opatrz komentarzem z typem i datą:

```markdown
<!-- static | 2026-02-18 -->
Treść stała, nie zmienia się w czasie.

<!-- dynamic | 2026-02-18 | deadline: 2026-02-21 -->
Treść czasowa powiązana z datą lub terminem.
```

**Zasady:**
- Unikaj duplikacji — przed zapisem sprawdź czy info już istnieje
- Daty w formacie `YYYY-MM-DD`
- `static` = dane stałe (imię, wartości, rola)
- `dynamic` = dane czasowe (spotkania, zadania, cele z terminem)
- Jeśli plik warstwy nie istnieje — utwórz go z nagłówkiem `# [Nazwa warstwy]` przed pierwszym zapisem

**Przykłady static vs dynamic:**

| Warstwa | Przykład static | Przykład dynamic |
|---------|----------------|-----------------|
| `cele.md` | "Chcę zbudować własny produkt" | "Q1 2026: zatrudnić 2 developerów" |
| `zespol.md` | "Anna Kowalska – CTO, prawa ręka" | "Rozmowa z Anną 20.02 o awansie" |
| `zdrowie.md` | "Nie jem glutenu" | "Trening biegowy — plan na marzec" |

---

## Obsługa przeterminowanych wpisów

Przy każdym wczytaniu warstwy: sprawdź wpisy `dynamic` z miniętą datą `deadline`.

Dla każdego przeterminowanego wpisu zapytaj użytkownika:
> "Wpis z [data]: '[treść]' — termin minął. Zostawić jako historię czy usunąć?"

---

## Tryb 1: Quick Save

**Wyzwalacze:** "zapamiętaj że...", "zapisz że...", "zanotuj...", "dodaj do kontekstu..."

### Workflow

1. Przeanalizuj treść wiadomości — oceń o czym jest informacja
2. Wczytaj 1-2 najbardziej prawdopodobne warstwy
3. Sprawdź przeterminowane wpisy (patrz wyżej)
4. Zbadaj istniejące dane pod kątem:
   - **Konfliktu** — np. inne spotkanie w tym samym terminie
   - **Uzupełnienia** — powiązana info już istnieje (dopytaj o szczegóły)
   - **Braku powiązań** — nowa, izolowana informacja
5. **ZAWSZE** zaproponuj warstwę i zapytaj o potwierdzenie przed zapisem:
   > "Chcę to zapisać na warstwie [nazwa]. Czy to OK, czy wolisz inną warstwę?"
6. Jeśli konflikt — pokaż istniejący wpis, wymuś decyzję:
   > "Na tej warstwie jest już: '[treść]'. Nadpisać, dopisać obok, czy pominąć?"
7. Po potwierdzeniu — zapisz z timestampem i oznaczeniem `static`/`dynamic`

---

## Tryb 2: Briefing

**Wyzwalacze:** "zbierz kontekst o...", "przeprowadź wywiad o...", "uzupełnij warstwę...",
"wyciągnij ze mnie info o...", "zbierz info o mojej roli / firmie / zespole",
"opowiedz mi o swojej [kategorii]"

### Workflow

1. Zidentyfikuj warstwę z wiadomości użytkownika
2. Wczytaj istniejące dane z tej warstwy
3. Podążaj za linkami `[[...]]` do powiązanych warstw
4. Na podstawie ilości danych zaproponuj tryb:
   - Mało danych (lub brak) → zaproponuj **głęboki wywiad**
   - Dużo danych → zaproponuj **szybki skan** (tylko uzupełnienie luk)
5. Zadawaj pytania **jedno po jednym**, czekaj na odpowiedź przed następnym
6. **Głęboki wywiad:** Pytania pogłębiające, eksploruj granice wiedzy, drąż "dlaczego"
7. **Szybki skan:** Tylko kluczowe luki — pomijaj to co już wiesz
8. Po każdej odpowiedzi — zaproponuj warstwę do zapisu i potwierdź
9. Po zakończeniu — podsumuj co zostało zebrane lub zaktualizowane

**Szczegółowe pytania per kategoria:**
- `references/private-categories.md` — pytania dla 10 warstw prywatnych
- `references/company-categories.md` — pytania dla 10 warstw firmowych

---

## Tryb 3: Load/Mount

**Wyzwalacze:** "zamontuj kontekst...", "załaduj kontekst...", "pokaż kontekst...",
"daj mi kontekst o...", "co wiesz o mnie...", "podsumuj mój kontekst..."

### Workflow

1. Jeśli zakres nie jest sprecyzowany — zapytaj:
   > "Co dokładnie chcesz załadować? Wszystkie warstwy, konkretną kategorię czy wybrany temat?"
2. Wczytaj odpowiednie warstwy zgodnie z odpowiedzią
3. Podążaj za linkami `[[...]]` do powiązanych warstw
4. **Cicho załaduj** — wczytaj zawartość plików do kontekstu, nie wypisuj surowej treści. Potwierdź tylko co zostało załadowane (krok 5).
5. Potwierdź krótko co zostało załadowane:
   > "Kontekst firmowy załadowany (10 warstw). Mogę teraz odpowiadać z pełnym kontekstem."
6. Sprawdź przeterminowane wpisy dynamic w każdej załadowanej warstwie

### Przegląd warstw

**Wyzwalacze:** "co wiesz o mnie?", "podsumuj mój kontekst", "jakie warstwy masz wypełnione?"

1. Sprawdź które pliki istnieją w `private/` i `company/`
2. Dla każdego istniejącego pliku — pokaż nazwę warstwy i datę ostatniej aktualizacji
3. Wyświetl zwięzłe podsumowanie:
   > "Mam dane w 6/20 warstwach: tożsamość, wartości, moja-rola, technologia, strategia, wyzwania."
4. Zapytaj: "Chcesz załadować pełen kontekst z którejś warstwy?"

### Granularność ładowania

| Polecenie | Co ładuje |
|-----------|-----------|
| "zamontuj wszystko" | Wszystkie warstwy z namespace'u |
| "zamontuj kontekst o firmie" | Wszystkie 10 warstw firmowych |
| "zamontuj tylko technologię" | `company/technologia.md` |
| "zamontuj z technologii tylko [temat]" | Konkretna sekcja/fraza z pliku |
| "zamontuj mój prywatny kontekst" | Wszystkie 10 warstw prywatnych |

---

## Tryb 4: Edit / Delete

**Wyzwalacze:** "popraw...", "zmień to że...", "usuń wpis...", "zaktualizuj...", "skoryguj..."

### Workflow

1. Zidentyfikuj warstwę której dotyczy zmiana
2. Wczytaj aktualną zawartość tej warstwy
3. Znajdź wpis który ma być zmieniony lub usunięty — pokaż go użytkownikowi:
   > "Znalazłem: '[treść wpisu]' (warstwa: [nazwa], data: [data]). To ten wpis?"
4. Poczekaj na potwierdzenie że to właściwy wpis
5. Dla **edycji** — pokaż proponowaną zmianę i zapytaj o potwierdzenie:
   > "Zmienię na: '[nowa treść]'. Zatwierdzić?"
6. Dla **usunięcia** — wymuś potwierdzenie:
   > "Usunąć ten wpis trwale? Tego nie można cofnąć."
7. Po potwierdzeniu — wprowadź zmianę i zapisz plik
