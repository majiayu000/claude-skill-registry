---
name: auto-init
description: CCv2 inicjalizacja trybu auto - wywiad + CONTINUITY + VALIDATION. Triggers: auto-init, auto init, inicjuj auto, plan auto
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Task
---

# /auto-init - CCv2 Auto Mode Initialization v2.6 (Hybrid + Min10 + MandatoryDelegation)

## ⛔ KRYTYCZNE - PRZECZYTAJ NAJPIERW!

**DO ZADAWANIA PYTAŃ MUSISZ UŻYĆ NARZĘDZIA `AskUserQuestion`!**

```
AskUserQuestion(
  questions: [
    { question: "...", header: "Cel", options: [...], multiSelect: false }
  ]
)
```

- ❌ NIE WOLNO pisać pytań jako zwykły tekst
- ❌ NIE WOLNO wypisywać opcji A) B) C) D) w wiadomości
- ✅ MUSISZ użyć tool AskUserQuestion
- ✅ CZEKAJ na odpowiedź przed kontynuacją

---

Przeprowadź GŁĘBOKI wywiad i utwórz pliki CONTINUITY.md + VALIDATION.md dla trybu autonomicznego.

**FILOZOFIA:**
- CONTINUITY = maksymalnie rozbudowany (dla resume po /clear)
- VALIDATION = prosty + priorytety (dla iteracji)

---

## Faza 1: Rozpoznanie kontekstu

### 1.1 Sprawdź istniejące pliki:
```
Glob: logs/CONTINUITY.md, VALIDATION.md, README.md, package.json, requirements.txt
```
- Czy projekt istnieje? Jaka struktura?
- Czy są już pliki CCv2?

### 1.2 Jeśli CONTINUITY.md lub VALIDATION.md ISTNIEJĄ:

**WAŻNE:** Użytkownik wywołał /auto-init mimo że pliki istnieją = chce NOWY PLAN.

1. **Przeczytaj istniejące pliki** i znajdź:
   - Nieukończone taski `[ ]` z VALIDATION.md
   - Nieukończone taski `[ ]` i `[→]` z CONTINUITY.md State
   - Open Questions bez odpowiedzi
   - Blokery które nie zostały rozwiązane

2. **Zapytaj użytkownika (AskUserQuestion):**
   ```
   Znalazłem istniejące pliki CCv2:
   - logs/CONTINUITY.md (Status: [status])
   - VALIDATION.md ([X] ukończonych / [Y] total)

   Nieukończone z obecnych plików:
   - [ ] task 1
   - [ ] task 2
   - [→] task 3 (w trakcie)

   Co chcesz zrobić?
   ```

   **Opcje:**
   - "Zastąp całkowicie" - nowy plan, stare pliki zarchiwizowane
   - "Przenieś nieukończone" - nowy plan + nieukończone taski z poprzedniego
   - "Anuluj" - nie rób nic

3. **Jeśli "Zastąp całkowicie":**
   - Przenieś stare pliki do `logs/archive/CONTINUITY-[data].md`
   - Kontynuuj wywiad od nowa

4. **Jeśli "Przenieś nieukończone":**
   - Zapisz listę nieukończonych tasków
   - Kontynuuj wywiad
   - W Fazie 4 dodaj nieukończone do nowych plików (sekcja "Przeniesione z poprzedniego planu")

### 1.3 Sprawdź dostępne szablony:
```
~/.templates/validation/
├── web-frontend.md
├── web-backend.md
├── api-rest.md
├── android-app.md
├── cli-tool.md
├── python-script.md
├── documentation.md
├── pwa-capacitor.md
├── flutter-app.md
├── go-app.md
├── rust-app.md
├── devops.md
```

---

## Faza 2: GŁĘBOKI WYWIAD (MINIMUM 10 rund, do 20)

### ⚠️ DLACZEGO TAK DUŻO PYTAŃ?

**CCv2 Philosophy:** Im więcej szczegółów w CONTINUITY i VALIDATION:
- ✅ Lepszy resume po /clear (nie tracimy kontekstu)
- ✅ Mniej zgadywania podczas pracy autonomicznej
- ✅ Mniej "nie wiem" i błędnych założeń
- ✅ Wyższe prawdopodobieństwo poprawnego wyniku końcowego

**5 rund = za mało.** W 5 rundach użytkownik nie przekaże wszystkiego co istotne.

### ⚠️ OBOWIĄZKOWE: Użyj narzędzia AskUserQuestion!

**MUSISZ użyć `AskUserQuestion` tool do zadawania pytań!**
- NIE pisz pytań jako zwykły tekst
- NIE zakładaj odpowiedzi
- CZEKAJ na odpowiedzi użytkownika przed kontynuacją
- Zadawaj 2-4 pytania na raz (multiSelect gdzie sensowne)
- **MINIMUM 10 rund** - nie kończ wcześniej nawet jeśli wydaje się że masz dość info

### ZASADY WYWIADU:
- ✅ Pytaj o CEL BIZNESOWY i EFEKT KOŃCOWY
- ✅ Pytaj o funkcjonalności z perspektywy UŻYTKOWNIKA
- ✅ Pytaj o obawy, ryzyka, blokery
- ✅ Pytaj o priorytety (MVP vs Full)
- ✅ Pytaj o zależności i integracje
- ✅ DYNAMICZNIE generuj pytania na podstawie odpowiedzi
- ❌ NIE pytaj o techniczne szczegóły (frameworki, biblioteki)
- ❌ NIE zakładaj - PYTAJ

### FORMAT:
1. Użyj `AskUserQuestion` z 2-4 pytaniami
2. Przeanalizuj odpowiedzi
3. Wygeneruj follow-up pytania na podstawie odpowiedzi
4. Powtarzaj dopóki masz PEŁNY obraz projektu

---

### RUNDA 1: Wizja projektu
1. "Co dokładnie ma powstać? Opisz efekt końcowy tak jakbyś pokazywał gotowy produkt."
2. "Jaki problem to rozwiązuje? Dlaczego to budujesz?"
3. "Kto będzie tego używał? (ty, klient, zespół, publiczność)"

---

### RUNDA 2: Użytkownicy i kontekst
4. "Opisz typowego użytkownika - kim jest, co robi, czego potrzebuje?"
5. "W jakim kontekście będą używać produktu? (praca, dom, w ruchu)"
6. "Czy użytkownicy mają specjalne potrzeby? (dostępność, język, urządzenia)"

**DYNAMICZNE:** Jeśli użytkownik wspomniał o "klientach" → pytaj o ich branżę, wielkość, oczekiwania

---

### RUNDA 3: Funkcjonalności core
7. "Jakie są 3-5 NAJWAŻNIEJSZYCH funkcji? (te bez których produkt nie ma sensu)"
8. "Co użytkownik ma móc zrobić krok po kroku? (user journey)"
9. "Czy są funkcje które MUSZĄ działać offline?"

**DYNAMICZNE:** Dla każdej wymienionej funkcji → "Opisz dokładniej jak ma działać [funkcja X]"

---

### RUNDA 4: Funkcjonalności szczegółowe
10. "Czy potrzebna jest rejestracja/logowanie użytkowników?"
11. "Czy są dane do przechowywania? Jakie?"
12. "Czy potrzebne są powiadomienia? (email, push, SMS)"
13. "Czy potrzebna jest integracja z innymi systemami?"

**DYNAMICZNE:**
- Jeśli logowanie → "OAuth, email/hasło, czy oba?"
- Jeśli dane → "Czy dane są wrażliwe? (GDPR, medyczne, finansowe)"
- Jeśli integracje → "Z jakimi systemami? Czy mają API?"

---

### RUNDA 5: UI/UX (jeśli ma interfejs)
14. "Jak ma wyglądać? Masz referencje, mockupy, inspiracje?"
15. "Czy ma być responsywne? (mobile, tablet, desktop)"
16. "Czy jest design system / brand guidelines do przestrzegania?"
17. "Jakie są najważniejsze ekrany/widoki?"

**DYNAMICZNE:**
- Jeśli mockupy → "Gdzie są? Czy mogę je zobaczyć?"
- Jeśli brand → "Jakie kolory, fonty, styl?"

---

### RUNDA 6: MVP vs Full scope
18. "Co MUSI być w pierwszej wersji (MVP)? (bez czego nie ma sensu wypuszczać)"
19. "Co może poczekać na v2, v3?"
20. "Gdybyś miał tylko 1 dzień - co byś zbudował?"
21. "Gdybyś miał tydzień - co dodatkowo?"

**DYNAMICZNE:** Dla każdej funkcji MVP → "Czy ta funkcja ma dependencies?"

---

### RUNDA 7: Kryteria sukcesu
22. "Po czym poznasz że projekt jest GOTOWY?"
23. "Jakie metryki będą świadczyć o sukcesie? (użytkownicy, konwersja, czas)"
24. "Czy są konkretne benchmarki do osiągnięcia? (np. Lighthouse 90%+)"
25. "Kto będzie akceptował że projekt jest 'done'?"

**DYNAMICZNE:**
- Jeśli metryki → "Jakie konkretne liczby?"
- Jeśli akceptacja → "Czy jest formalny proces review?"

---

### RUNDA 8: Ryzyka i obawy
26. "Co Cię NAJBARDZIEJ martwi w tym projekcie?"
27. "Co może pójść nie tak? (techniczne, biznesowe, ludzkie)"
28. "Czy były już próby zbudowania czegoś podobnego? Co poszło nie tak?"
29. "Jakie są największe unknowns?"

**DYNAMICZNE:** Dla każdego ryzyka → "Jak możemy to zmitigować?"

---

### RUNDA 9: Blokery i zależności
30. "Czy są rzeczy które mogą ZABLOKOWAĆ pracę? (dostępy, dane, decyzje)"
31. "Czy czekasz na coś od kogoś? (API, design, content)"
32. "Czy są zewnętrzne serwisy od których zależysz?"
33. "Czy potrzebujesz dostępu do czegoś czego nie masz?"

**DYNAMICZNE:**
- Jeśli blokery → "Kiedy się spodziewasz rozwiązania?"
- Jeśli zewnętrzne API → "Czy masz dokumentację? Klucze API?"

---

### RUNDA 10: Ograniczenia
34. "Czy są ograniczenia czasowe? (deadline, milestone)"
35. "Czy są ograniczenia budżetowe? (hosting, API, licencje)"
36. "Czy są ograniczenia technologiczne? (musi być X, nie może być Y)"
37. "Czy są ograniczenia prawne? (GDPR, HIPAA, branżowe)"

**DYNAMICZNE:**
- Jeśli deadline → "Co się stanie jeśli go nie dotrzymasz?"
- Jeśli GDPR → "Jakie dane osobowe? Gdzie przechowywane?"

---

### ✅ CHECKPOINT: MINIMUM 10 RUND OSIĄGNIĘTE

**Po rundzie 10 możesz przejść do Fazy 3, ALE:**
- Rundy 11-20 są ZALECANE dla złożonych projektów
- Jeśli projekt ma: integracje, płatności, użytkowników, security → KONTYNUUJ
- Jeśli projekt prosty (1-2 dni pracy) → możesz zakończyć

**Przed zakończeniem wywiadu ZAWSZE zapytaj:**
> "Czy jest coś o czym nie zapytałem a powinienem wiedzieć?"

---

### RUNDA 11: Środowisko i deployment
38. "Gdzie ma działać? (chmura, własny serwer, lokalnie)"
39. "Czy są wymagania dot. hostingu? (region, certyfikaty)"
40. "Jak ma wyglądać proces wdrożenia?"
41. "Czy potrzebujesz CI/CD?"

**DYNAMICZNE:**
- Jeśli chmura → "AWS, GCP, Azure, Vercel, inne?"
- Jeśli CI/CD → "GitHub Actions, GitLab CI, inne?"

---

### RUNDA 12: Testowanie i jakość
42. "Jak chcesz testować? (automatyczne, manualne, oba)"
43. "Czy są krytyczne ścieżki które MUSZĄ być przetestowane?"
44. "Czy potrzebujesz testów wydajnościowych?"
45. "Kto będzie robił QA?"

---

### RUNDA 13: Dokumentacja i maintenance
46. "Czy potrzebna jest dokumentacja? (techniczna, użytkownika, API)"
47. "Kto będzie utrzymywał projekt po zakończeniu?"
48. "Czy przewidujesz regularne aktualizacje?"

---

### RUNDA 14: Konkurencja i inspiracje
49. "Czy są podobne produkty na rynku? Co robią dobrze/źle?"
50. "Czy masz przykłady które Ci się podobają? (linki, screenshoty)"
51. "Czym Twój produkt ma się wyróżniać?"

**DYNAMICZNE:** Jeśli konkurencja → "Co chcesz zrobić LEPIEJ niż oni?"

---

### RUNDA 15: Monetyzacja (jeśli dotyczy)
52. "Czy produkt ma zarabiać? Jak?"
53. "Czy jest model freemium/premium?"
54. "Czy potrzebna jest integracja płatności?"

**DYNAMICZNE:**
- Jeśli płatności → "Stripe, PayPal, inne? Subskrypcje czy jednorazowe?"
- Jeśli freemium → "Co jest free, co premium?"

---

### RUNDA 16: Analityka i monitoring
55. "Czy potrzebujesz analityki? (Google Analytics, custom)"
56. "Jakie metryki chcesz śledzić?"
57. "Czy potrzebujesz error trackingu? (Sentry)"
58. "Czy potrzebujesz logów/auditu?"

---

### RUNDA 17: Bezpieczeństwo
59. "Czy są dane wrażliwe? (hasła, finansowe, medyczne)"
60. "Czy potrzebna jest szyfrowanie?"
61. "Czy są wymagania compliance? (SOC2, ISO)"
62. "Czy potrzebujesz rate limiting / ochrony przed botami?"

---

### RUNDA 18: Skalowanie (jeśli dotyczy)
63. "Ile użytkowników spodziewasz się? (teraz, za rok)"
64. "Czy są peak times? (święta, kampanie)"
65. "Czy system musi się automatycznie skalować?"

---

### RUNDA 19: Komunikacja i współpraca
66. "Czy pracujesz sam czy w zespole?"
67. "Jak będziemy się komunikować podczas projektu?"
68. "Jak często chcesz widzieć postępy?"
69. "Czy są stakeholderzy do informowania?"

---

### RUNDA 20: Podsumowanie i weryfikacja
70. "Czy jest coś o czym nie zapytałem a powinienem wiedzieć?"
71. "Czy moje zrozumienie projektu jest poprawne? [podsumuj]"
72. "Czy są pytania do mnie zanim zaczniemy?"

---

### DYNAMICZNE PYTANIA FOLLOW-UP:

Dla KAŻDEJ odpowiedzi sprawdź czy wymaga dopytania:

| Jeśli użytkownik mówi... | Zapytaj dodatkowo... |
|--------------------------|---------------------|
| "użytkownicy" | Kim są? Ilu? Skąd przyjdą? |
| "dane" | Jakie? Gdzie? Jak dużo? Wrażliwe? |
| "integracja" | Z czym? Czy mają API? Dokumentację? |
| "mobile" | iOS, Android, oba? PWA czy native? |
| "szybko" | Jaki deadline? Co jeśli później? |
| "prosty" | Prosty dla kogo? Co to znaczy? |
| "jak X" | Pokaż X. Co dokładnie z X? |
| "później" | Kiedy? Co blokuje teraz? |
| "nie wiem" | Kto wie? Kiedy się dowiesz? |
| "zależy" | Od czego? Jakie opcje? |

---

## Faza 3: Analiza i wybór szablonu

### 3.1 Na podstawie wywiadu określ:
- **Typ projektu:** frontend / backend / fullstack / mobile / CLI / script
- **Złożoność:** simple (1-2 dni) / medium (tydzień) / complex (więcej)
- **MVP scope:** co jest absolutnie konieczne
- **Blokery:** co może zatrzymać pracę
- **Ryzyka:** co może pójść nie tak

### 3.2 Wybierz i dostosuj szablon:
1. Przeczytaj najbliższy szablon z `~/.templates/validation/`
2. DODAJ punkty specyficzne dla projektu (z wywiadu)
3. USUŃ punkty nieistotne dla tego projektu
4. OZNACZ priorytety (🔴 MVP, 🟡 ważne, 🟢 v2)

---

## Faza 4: Generowanie plików

### 4.1 CONTINUITY.md (logs/CONTINUITY.md) - ROZBUDOWANY

```markdown
# Continuity Ledger - [Nazwa Projektu]

## Aktywna Sesja

**Urządzenie:** [PC/Android - wykryj z platform]
**Start:** [YYYY-MM-DD HH:MM]
**Cel:** [1-2 zdania z wywiadu - CEL BIZNESOWY]
**Status:** IN_PROGRESS
**Kontekst:** ~5% (updated: [HH:MM])

---

## Goal (Success Criteria)

Co musi być prawdą, żeby zadanie było DONE:
- [ ] [Kryterium 1 z wywiadu]
- [ ] [Kryterium 2 z wywiadu]
- [ ] [Kryterium 3 z wywiadu]

---

## Constraints (Wymagania techniczne)

- [Constraint 1 z wywiadu - np. "Mobile responsive"]
- [Constraint 2 z wywiadu - np. "Lighthouse 95%+"]
- [Constraint 3 z wywiadu - np. "GDPR compliant"]

---

## Phases (z estimated effort)

- [→] **Phase 1: [nazwa]** (~Xh) - [krótki opis]
- [ ] **Phase 2: [nazwa]** (~Xh) - [krótki opis]
- [ ] **Phase 3: [nazwa]** (~Xh) - [krótki opis]

**Total estimated:** ~XXh

---

## State (Postęp)

### Phase 1: [nazwa]

- [→] [Pierwszy task - CURRENT]
- [ ] [Task 2]
- [ ] [Task 3]

**Znaczniki:** `[x]` = done, `[→]` = CURRENT, `[ ]` = todo

---

## MVP Scope (z wywiadu)

**MUST HAVE (MVP):**
- [funkcja 1]
- [funkcja 2]

**SHOULD HAVE (v1.1):**
- [funkcja 3]

**COULD HAVE (v2):**
- [funkcja 4]

---

## Key Decisions (z wywiadu)

| Decyzja | Powód | Alternatywy |
|---------|-------|-------------|
| [decyzja 1] | [dlaczego] | [co odrzucone] |
| [decyzja 2] | [dlaczego] | [co odrzucone] |

---

## Open Questions (UNCONFIRMED)

### ❓ BLOCKING (muszę wiedzieć żeby kontynuować)
- [ ] [pytanie krytyczne]

### 💭 CLARIFICATION (warto wyjaśnić)
- [ ] [pytanie do wyjaśnienia]

---

## Working Set

**Pliki:**
- [plik1] - [opis]
- [plik2] - [opis]

**Branch:** [main/feature-X]

**Komendy testowe:**
```bash
[komenda testowa z wywiadu]
```

---

## Blokery

### 🛑 BLOCKING NOW
- [ ] [bloker który zatrzymuje pracę TERAZ]

### ⚠️ BLOCKING NEXT PHASE
- [ ] [bloker dla kolejnej fazy]

---

## Dependencies (z wywiadu)

### External (poza naszą kontrolą)
- [ ] [API/serwis] - status: [ready/waiting/unknown]

### Internal (nasza decyzja)
- Phase 2 wymaga Phase 1
- [inna zależność]

---

## Risks (z wywiadu)

| Risk | Impact | Mitigation |
|------|--------|------------|
| [risk 1] | High/Med/Low | [jak zmitigować] |

---

## Notatki

[Ważne informacje z wywiadu które nie pasują do innych sekcji]
- [notatka 1]
- [notatka 2]

---

## Przeniesione z poprzedniego planu (jeśli dotyczy)

> Poniższe taski zostały przeniesione z poprzedniego CONTINUITY.md ([data]):

- [ ] [task 1 - nieukończony]
- [ ] [task 2 - nieukończony]

> Open Questions z poprzedniego planu:
- [ ] [pytanie bez odpowiedzi]

---

## Context Management

### Thresholds
- **60%** - zwiększ delegowanie do agentów
- **70%** - zapisz stan, rozważ /clear
- **80%** - MUSISZ zapisać i /clear
- **90%** - KRYTYCZNE, natychmiast /clear

### Przed /clear (OBOWIĄZKOWE)
1. Zaktualizuj WSZYSTKIE sekcje powyżej
2. Oznacz current task jako `[→]`
3. Zapisz Open Questions
4. Dopiero potem `/clear`

### Po /clear
1. Powiedz: "resume"
2. Claude czyta CONTINUITY.md
3. Weryfikuje stan vs rzeczywistość
4. Kontynuuje od `[→]`
```

---

### 4.2 VALIDATION.md (./VALIDATION.md) - SZCZEGÓŁOWE CHECKPOINTY

**⚠️ KRYTYCZNE:** Każdy checkpoint musi być:
- **TESTOWALNY** - jasne kryterium PASS/FAIL
- **SZCZEGÓŁOWY** - nie "PDF działa" ale "tekst nie ucięty, logo widoczne, kolory poprawne"
- **OBEJMUJĄCY EDGE CASES** - polskie znaki, długi tekst, puste dane

**❌ ZŁE checkpointy (zbyt ogólne):**
```
- [ ] PDF export działa
- [ ] Formularz działa
- [ ] Strona wygląda OK
```

**✅ DOBRE checkpointy (szczegółowe, testowalne):**
```
### PDF Export
- [ ] PDF generuje się bez błędów
- [ ] PDF otwiera się w Chrome, Firefox, Adobe
- [ ] Tekst min 10pt, czytelny
- [ ] Tekst nie ucięty, nie wychodzi poza marginesy
- [ ] Polskie znaki (ą,ę,ó) wyświetlają się poprawnie
- [ ] Logo KMYLPENTER w nagłówku
- [ ] Kolory brand (#3A90C8) poprawnie renderowane
- [ ] Tabele/listy nie rozjeżdżają się
- [ ] Rozmiar PDF < 5MB
```

**Dla KAŻDEJ funkcji rozpisz checkpointy w kategoriach:**
1. **Funkcjonalność** - czy działa podstawowa funkcja
2. **Wygląd/UI** - layout, typography, branding, kolory
3. **Edge cases** - długi tekst, puste dane, polskie znaki
4. **Responsywność** - mobile, tablet, desktop (jeśli dotyczy)
5. **Accessibility** - kontrast, aria-labels, keyboard (jeśli dotyczy)

**⚠️ MINIMUM checkpointów per sekcja:**
- **🔴 MVP funkcja:** minimum 8-12 checkpointów każda
- **🟡 IMPORTANT funkcja:** minimum 5-8 checkpointów każda
- **🟢 NICE TO HAVE:** minimum 3-5 checkpointów każda

**Budujemy plany na dni/tygodnie pracy. Obszerny plik = lepszy plan.**
**Nie oszczędzaj na checkpointach - każdy szczegół to mniej błędów później.**

---

```markdown
# VALIDATION: [Nazwa Projektu]

**Cel:** [cel z wywiadu]
**Status:** IN_PROGRESS

---

## 🔴 MVP (CRITICAL)

### [Kategoria 1 - np. Core Features]
- [ ] [checkpoint SZCZEGÓŁOWY - testowalny]
- [ ] [checkpoint SZCZEGÓŁOWY - testowalny]
- [ ] [checkpoint SZCZEGÓŁOWY - testowalny]

### [Kategoria 2 - np. UI/UX]
- [ ] [checkpoint SZCZEGÓŁOWY - testowalny]
- [ ] [checkpoint SZCZEGÓŁOWY - testowalny]

---

## 🟡 IMPORTANT (v1.0)

### [Kategoria 3 - np. Quality]
- [ ] [checkpoint]
- [ ] [checkpoint]

### [Kategoria 4 - np. Testing]
- [ ] [checkpoint]
- [ ] [checkpoint]

---

## 🟢 NICE TO HAVE (v2)

### [Kategoria 5 - np. Extras]
- [ ] [checkpoint]
- [ ] [checkpoint]

---

## 📦 Przeniesione z poprzedniego planu (jeśli dotyczy)

> Nieukończone z poprzedniego VALIDATION.md ([data]):

- [ ] [checkpoint - nieukończony]
- [ ] [checkpoint - nieukończony]

---

## DONE Criteria

### MVP Done
- [ ] Wszystkie 🔴 checkboxy ✅
- [ ] [Kryterium z Goal w CONTINUITY]
- [ ] Brak blocking bugs

### Full Done
- [ ] Wszystkie 🔴 + 🟡 checkboxy ✅
- [ ] [Dodatkowe kryterium]
```

---

## Faza 4.5: DELEGACJA - Rozszerzenie checkpointów (KRYTYCZNE)

### Dlaczego delegacja?

Agent główny ma "context fatigue" - robi wywiad + template + pliki.
Dedykowany agent skupiony na JEDNYM zagadnieniu:
- Myśli głęboko o edge cases
- Nie pomija accessibility, responsywności
- Produkuje 3-5x więcej checkpointów

**Wynik:** 52 checkpointów → 180+ checkpointów (sprawdzone empirycznie)

---

### ⚠️ KIEDY DELEGACJA JEST OBOWIĄZKOWA (nie opcjonalna!)

**MUSISZ delegować jeśli KTÓRYKOLWIEK warunek jest spełniony:**

| Warunek | Sprawdzenie | Akcja |
|---------|-------------|-------|
| **Checkpointy < minimum** | Sekcja 🔴 MVP ma <8 checkpointów | → DELEGUJ tę sekcję |
| **Duży projekt** | Złożoność = "complex" (>2 dni) | → DELEGUJ wszystkie sekcje MVP |
| **UI/Frontend** | Projekt ma interfejs użytkownika | → DELEGUJ (accessibility, responsywność) |
| **Integracje** | Projekt ma zewnętrzne API/serwisy | → DELEGUJ (error handling, edge cases) |

**NIE MOŻESZ pominąć delegacji** jeśli którykolwiek warunek powyżej jest spełniony.

**Możesz pominąć delegację TYLKO jeśli WSZYSTKIE są prawdziwe:**
- Projekt prosty (1-2 dni)
- Brak UI (CLI, script, konfiguracja)
- Brak integracji zewnętrznych
- Każda sekcja MVP ma ≥8 szczegółowych checkpointów

---

### 4.5.1 Dla KAŻDEJ sekcji 🔴 MVP w VALIDATION.md:

**Uruchom osobnego agenta Task(Explore):**

```
Task(subagent_type="Explore"):
    "KONTEKST: Rozszerzamy VALIDATION.md dla projektu [nazwa].
    Branding: [kolory, fonty z wywiadu].

    ZADANIE:
    Przeczytaj VALIDATION.md i dla sekcji '[NAZWA SEKCJI]'
    rozpisz SZCZEGÓŁOWE, TESTOWALNE checkpointy (minimum 8-12).

    Każdy checkpoint musi mieć jasne kryterium PASS/FAIL.

    Rozpisz w kategoriach:
    1. Funkcjonalność (podstawowe działanie)
    2. Wygląd/UI (layout, branding, kolory, typography)
    3. Edge cases (długi tekst, puste dane, polskie znaki, błędne dane)
    4. Responsywność (mobile 320px, tablet 768px, desktop 1200px)
    5. Accessibility (kontrast WCAG AA, focus visible, aria-labels)
    6. Error handling (co gdy błąd, timeout, brak danych)

    FORMAT: Zwróć TYLKO rozszerzoną sekcję markdown:
    ### [Nazwa Sekcji]
    - [ ] checkpoint 1
    - [ ] checkpoint 2
    ..."
```

---

### 4.5.2 Równoległe uruchomienie agentów

**Dla efektywności uruchom 3-4 agentów RÓWNOLEGLE:**

```
# Przykład dla 6 sekcji MVP:
Agent 1: V2 Engine Test + Backend API
Agent 2: Landing Page + Raport UI
Agent 3: PDF Export + Progress UX
Agent 4: i18n + Optimization + Security
```

**Każdy agent dostaje 1-3 sekcje do rozszerzenia.**

---

### 4.5.3 Zbierz wyniki i zaktualizuj VALIDATION.md

1. Poczekaj na wszystkie agenty
2. Zbierz rozszerzone sekcje
3. Zastąp oryginalne sekcje w VALIDATION.md rozszerzonymi
4. Sprawdź czy każda sekcja MVP ma minimum 8 checkpointów

---

### 4.5.4 Walidacja końcowa

Po delegacji sprawdź:
- [ ] Każda sekcja 🔴 MVP ma ≥8 checkpointów
- [ ] Każda sekcja 🟡 IMPORTANT ma ≥5 checkpointów
- [ ] Checkpointy są TESTOWALNE (nie ogólne)
- [ ] Zawierają edge cases, accessibility, responsywność

**Jeśli sekcja ma <8 checkpointów → uruchom agenta ponownie dla tej sekcji.**

---

## Faza 5: Potwierdzenie

Pokaż użytkownikowi:

```
✅ CCv2 Auto-Init Complete (v2.5 + Agent Delegation)

📋 Utworzone pliki:
- logs/CONTINUITY.md - rozbudowany stan sesji (dla resume)
- VALIDATION.md - szczegółowa checklista rozszerzona przez agentów

🤖 Delegacja agentów:
- [X] sekcji rozszerzonych przez dedykowanych agentów
- [Y] checkpointów wygenerowanych (vs ~50 bez delegacji)

---

🎯 Cel: [cel z wywiadu]

📊 Phases:
1. [→] [phase 1] (~Xh)
2. [ ] [phase 2] (~Xh)
3. [ ] [phase 3] (~Xh)

⏱️ Total estimated: ~XXh

---

📈 MVP Scope (🔴):
- [funkcja 1]
- [funkcja 2]

🛑 Blockers:
- [bloker 1] - [status]

⚠️ Risks:
- [risk 1]

---

🚀 Gotowe do pracy!

Powiedz:
- "auto" - rozpocznij pracę autonomiczną
- "status" - pokaż postęp
- "resume" - wznów po /clear
```

---

## Wskazówki implementacyjne

### Wywiad:
- **MINIMUM 10 rund** - nie kończ wcześniej, nawet jeśli wydaje się że masz dość
- **Nie kończ wywiadu przedwcześnie** - lepiej za dużo pytań niż za mało
- **Zapisuj WSZYSTKO** - nawet pozornie nieistotne informacje
- **Pytaj "dlaczego"** - zrozum motywację, nie tylko wymagania
- **Weryfikuj zrozumienie** - podsumuj i potwierdź
- **CCv2 Philosophy:** Więcej szczegółów = wyższe prawdopodobieństwo sukcesu

### CONTINUITY.md:
- **Rozbudowany** - im więcej kontekstu, tym lepszy resume
- **Aktualizuj często** - co 15-30 min lub po ważnym kroku
- **`[→]` marker** - ZAWSZE oznacz current task przed /clear
- Zawiera: Goal, Constraints, Phases, State, MVP, Decisions, Questions, Working Set, Blockers, Dependencies, Risks, Context Management

### VALIDATION.md:
- **SZCZEGÓŁOWE checkpointy** - każdy musi być testowalny (PASS/FAIL)
- **Priorytety** - 🔴 MVP / 🟡 Important / 🟢 Nice
- **DONE Criteria** - kiedy można powiedzieć "gotowe"
- Bazuj na szablonach z `~/.templates/validation/`
- Dodaj checkboxy specyficzne dla projektu (z wywiadu)

**Dla każdej funkcji rozpisz:**
1. Funkcjonalność (czy działa)
2. Wygląd/UI (layout, branding, kolory)
3. Edge cases (długi tekst, polskie znaki, puste dane)
4. Responsywność (jeśli UI)
5. Accessibility (jeśli UI)

**❌ ZŁE:** `- [ ] PDF działa`
**✅ DOBRE:** `- [ ] Tekst nie ucięty, polskie znaki OK, logo w nagłówku`

### Istniejące pliki (re-init):
- Jeśli pliki CCv2 istnieją → użytkownik chce NOWY PLAN
- **ZAWSZE pytaj** co zrobić z nieukończonymi taskami
- Opcje: zastąp całkowicie / przenieś nieukończone / anuluj
- Przy "Przenieś" → dodaj sekcję "Przeniesione z poprzedniego planu"
- Przy "Zastąp" → archiwizuj stare do `logs/archive/`

### Estimated effort:
- Simple task: 1-2h
- Medium task: 4-8h
- Complex task: 2-5 dni
- Dodaj 20% buffer na nieoczekiwane problemy

### Priorytety:
- 🔴 **MVP/CRITICAL** - bez tego produkt nie działa
- 🟡 **IMPORTANT** - potrzebne dla v1.0 release
- 🟢 **NICE TO HAVE** - może poczekać na v2
