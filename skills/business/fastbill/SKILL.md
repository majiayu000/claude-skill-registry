---
name: fastbill
description: Fastbill Buchhaltung & Rechnungen - Kunden verwalten, Rechnungen erstellen/versenden, Produkte/Artikel pflegen, Einnahmen erfassen. Nutze für "Rechnung erstellen", "Kunden anlegen", "Rechnung versenden", "offene Rechnungen", "Umsätze".
metadata: {"clawdbot":{"emoji":"🧾","requires":{"env":["FASTBILL_EMAIL","FASTBILL_API_KEY"]}}}
---

# Fastbill Skill

Verwalte Fastbill-Buchhaltung direkt aus Clawdbot: Kunden, Rechnungen, Produkte und Einnahmen.

## Setup

### 1. API-Zugangsdaten holen

1. In Fastbill einloggen → Einstellungen → API
2. API-Key kopieren (oder neu generieren)

### 2. Environment Variables setzen

```bash
export FASTBILL_EMAIL="deine@email.de"
export FASTBILL_API_KEY="dein-api-key"
```

## Verwendung

### Kunden

**Kunden auflisten:**
```bash
<skill>/scripts/fastbill.sh customer-list [limit] [offset]
```

**Kunden suchen:**
```bash
<skill>/scripts/fastbill.sh customer-search "Suchbegriff"
```

**Kunden Details:**
```bash
<skill>/scripts/fastbill.sh customer-get <customer_id>
```

**Kunden anlegen:**
```bash
<skill>/scripts/fastbill.sh customer-create '{"CUSTOMER_TYPE":"business","ORGANIZATION":"Firma GmbH","LAST_NAME":"Kontakt","EMAIL":"info@firma.de"}'
```

### Rechnungen

**Rechnungen auflisten:**
```bash
<skill>/scripts/fastbill.sh invoice-list [limit] [offset]
```

**Rechnung Details:**
```bash
<skill>/scripts/fastbill.sh invoice-get <invoice_id>
```

**Rechnungen eines Kunden:**
```bash
<skill>/scripts/fastbill.sh invoice-by-customer <customer_id>
```

**Rechnung erstellen:**
```bash
<skill>/scripts/fastbill.sh invoice-create '{"CUSTOMER_ID":"12345","ITEMS":[{"DESCRIPTION":"Beratung","UNIT_PRICE":"100.00","QUANTITY":"8"}]}'
```

**Rechnung finalisieren** (Entwurf → final):
```bash
<skill>/scripts/fastbill.sh invoice-complete <invoice_id>
```

**Rechnung als bezahlt markieren:**
```bash
<skill>/scripts/fastbill.sh invoice-setpaid <invoice_id> [datum]
```

**Rechnung per E-Mail versenden:**
```bash
<skill>/scripts/fastbill.sh invoice-send <invoice_id> <empfaenger@email.de>
```

**Rechnung stornieren:**
```bash
<skill>/scripts/fastbill.sh invoice-cancel <invoice_id>
```

### Produkte/Artikel

**Produkte auflisten:**
```bash
<skill>/scripts/fastbill.sh product-list [limit] [offset]
```

**Produkt erstellen:**
```bash
<skill>/scripts/fastbill.sh product-create '{"TITLE":"Beratungsstunde","UNIT_PRICE":"120.00","VAT_PERCENT":"19"}'
```

### Einnahmen/Ausgaben

**Einnahmen auflisten:**
```bash
<skill>/scripts/fastbill.sh revenue-list [limit] [offset]
```

### Sonstiges

**Wiederkehrende Rechnungen:**
```bash
<skill>/scripts/fastbill.sh recurring-list
```

**Rechnungsvorlagen:**
```bash
<skill>/scripts/fastbill.sh template-list
```

## Agent-Anweisungen

### Typische Anfragen

**"Zeige offene Rechnungen"**
1. `invoice-list 100` aufrufen
2. Filtern nach `STATE` != "paid"
3. Übersichtlich formatieren

**"Erstelle Rechnung für Kunde X"**
1. `customer-search "X"` für Kunden-ID
2. Items zusammenstellen (Beschreibung, Preis, Menge)
3. `invoice-create` mit JSON
4. Optional: `invoice-complete` zum Finalisieren
5. Optional: `invoice-send` zum Versenden

**"Markiere Rechnung als bezahlt"**
1. `invoice-search` oder `invoice-list` für Invoice-ID
2. `invoice-setpaid <id>` mit optionalem Datum

**"Wer schuldet uns noch Geld?"**
1. `invoice-list 100`
2. Filtern nach `STATE` = "unpaid" oder "overdue"
3. Gruppieren nach Kunde, Summen berechnen

### Formatierung

Rechnungsliste:
```
📋 Offene Rechnungen:

• RE-2026-001 | Kunde A | 1.200,00 € | fällig 15.02.
• RE-2026-002 | Kunde B | 850,00 € | überfällig seit 10.01. ⚠️

Gesamt: 2.050,00 €
```

### Zahlungsarten (PAYMENT_TYPE)

| Code | Bedeutung |
|------|-----------|
| 1 | Überweisung |
| 2 | Lastschrift |
| 3 | Bar |
| 4 | PayPal |
| 5 | Vorkasse |
| 6 | Kreditkarte |

### Rechnungsstatus (STATE)

| Status | Bedeutung |
|--------|-----------|
| draft | Entwurf |
| created | Erstellt (noch nicht versendet) |
| unpaid | Versendet, noch offen |
| overdue | Überfällig |
| paid | Bezahlt |
| canceled | Storniert |

### Kundentypen (CUSTOMER_TYPE)

| Typ | Bedeutung |
|-----|-----------|
| business | Geschäftskunde (ORGANIZATION erforderlich) |
| consumer | Privatkunde (FIRST_NAME, LAST_NAME erforderlich) |

## API-Referenz

Dokumentation: https://apidocs.fastbill.com/

**API-URL:** `https://my.fastbill.com/api/1.0/api.php`

**Authentifizierung:** HTTP Basic Auth mit Email + API-Key

**Format:** JSON (oder XML)

**Wichtige Services:**
- `customer.get/create/update/delete`
- `invoice.get/create/update/delete/complete/cancel/sendbyemail/setpaid`
- `article.get/create/update/delete`
- `revenue.get/create`
- `subscription.get` (wiederkehrende Rechnungen)
- `template.get` (Rechnungsvorlagen)

**Rate Limits:**
- Solo: 50 Calls/h
- Pro: 500 Calls/h
- Premium: 1000 Calls/h
