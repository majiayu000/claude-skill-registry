---
name: formulare-checkout-ecommerce
description: "Prüft Formulare, Login, Suche, Warenkorb, Checkout, Zahlungsstrecke und elektronische Verträge in Webshops. Fokus BFSG/E-Commerce, Fehlermeldungen, Labels, Pflichtfelder, Zeitlimits und Bestellabschluss. Output: Checkout-Audit."
---

# Formulare, Checkout, E-Commerce

Nutze diesen Skill für Webshops, Buchungsstrecken, Login-Portale und digitale Vertragsabschlüsse.

## Prüfpfad

1. Produkt oder Dienstleistung finden.
2. In Warenkorb oder Buchungsstrecke legen.
3. Registrierung oder Gastbestellung.
4. Adresse, Versand, Zahlungsart.
5. Fehler provozieren.
6. Zusammenfassung prüfen.
7. Bestellung/Vertragsschluss und Bestätigung.

## Typische Fehler

- Pflichtfelder nur farblich markiert.
- Fehlermeldung erscheint, wird aber nicht fokussiert oder vorgelesen.
- Captcha ohne Alternative.
- Zahlungsanbieter ist nicht tastaturbedienbar.
- Zeitlimit löscht Warenkorb.
- AGB/Datenschutz-PDF ist nicht barrierefrei.
- Button-Beschriftung unklar: "Weiter" statt "Zahlungspflichtig bestellen" im richtigen Kontext.

## Output

| Schritt | Barriere | Rechts-/Nutzerrisiko | Fix |
| --- | --- | --- | --- |

## Schneller Arbeitsmodus

- Lege den Scope fest: Website, App, PDF, Checkout, Formular, Intranet oder öffentliche Stelle; dazu Normrahmen BFSG/BITV/WAD/EN 301 549/WCAG.
- Beurteile nicht nur formal, sondern aus Nutzersicht: Tastatur, Screenreader, Zoom/Reflow, Kontrast, Fehlermeldungen, Zeitlimits und Dokumentzugang.
- Automatische Scanner sind nur Startpunkt. Markiere False Positives, manuelle Nachpruefung und reproduzierbare Testschritte.
- Formuliere Fixes als Entwickler-Tickets mit Komponente, Problem, Nutzerwirkung, Normbezug, Prioritaet und Re-Test.

## Ausgabeformat

- Befund.
- Nutzerwirkung.
- Norm-/Kriteriumsbezug.
- Konkreter Fix.
- Prioritaet und Nachweis fuer die Dokumentation.
