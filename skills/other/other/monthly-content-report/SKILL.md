---
name: monthly-content-report
description: Genera el informe mensual de correlación entre contenido publicado en X, visitas a /cursos/expert/ai en Umami y ventas de AI Expert. Cruza métricas para identificar qué contenido impulsa conversiones. Úsalo cuando Antonio pida el informe mensual, el análisis de ventas del mes, o quiera saber qué posts funcionan mejor para vender.
---

# Monthly Content Report — Correlación contenido → tráfico → ventas

Genera un informe mensual que cruza:
1. **Posts de X** publicados en el período (via bird CLI)
2. **Tráfico** a `/cursos/expert/ai` en Umami (pageviews diarios)
3. **Ventas** de AI Expert registradas en Google Sheets

El objetivo es entender qué contenido genera tráfico y conversiones reales.

## Configuración requerida

Fichero `~/.config/skills/config.json` bajo clave `monthly_content_report`:

```json
{
  "monthly_content_report": {
    "umami_url": "<your-umami-url>",
    "umami_user": "<umami-username>",
    "umami_pass": "<umami-password>",
    "umami_website_id": "<umami-website-id>",
    "umami_path": "<path-to-track>",
    "thrivecart_api_key": "<api_key>",
    "thrivecart_product_id": 0
  }
}
```

## Fuentes de datos

### 1. Posts de X (bird CLI)
```bash
bird timeline --count 200 --since YYYY-MM-DD --until YYYY-MM-DD
```
Filtrar solo posts propios (no RTs), obtener: fecha, texto, likes, RTs, replies, impresiones.

### 2. Tráfico Umami
Script: `scripts/umami-pageviews.js`

```bash
node scripts/umami-pageviews.js --start YYYY-MM-DD --end YYYY-MM-DD
```

Autenticación: POST `/api/auth/login` → JWT
Pageviews: `GET /api/websites/{id}/pageviews?startAt=&endAt=&unit=day&timezone=Europe/Madrid&path=eq.%2Fcursos%2Fexpert%2Fai`

Salida: array `[{date, pageviews, sessions}]`

### 3. Ventas (ThriveCart API)
Script: `scripts/thrivecart-sales.js`

```bash
node scripts/thrivecart-sales.js --start YYYY-MM-DD --end YYYY-MM-DD --json
```

- Producto AI Expert: ID `9`
- Filtrar `transaction_type == "charge"` → primera compra (único o primer plazo)
- Ignorar `rebill` (plazos posteriores) y `failed`
- Campo `related_to_recur: true` indica pago a plazos
- Campos útiles: `date`, `customer.email`, `customer.name`, `amount_str`, `item_pricing_option_name`

## Workflow del agente

1. **Determinar período**: por defecto el mes anterior completo. Preguntar si quiere otro rango.

2. **Obtener datos en paralelo**:
   - Posts de X del período
   - Pageviews diarios de Umami
   - Ventas del período del Sheet

3. **Correlacionar**:
   - Para cada día con ventas: ¿qué posts se publicaron ese día o los 2-3 días anteriores?
   - Para cada post: ¿cuánto subió el tráfico el día de publicación y los siguientes?
   - Calcular correlación entre engagement de posts y picos de tráfico
   - Identificar posts publicados dentro de los 7 días previos a cada venta

4. **Generar informe** con estructura:
   ```
   ## Resumen mes [MES YYYY]
   - Total ventas: X (€ total)
   - Total visitas /cursos/expert/ai: X
   - Posts publicados: X
   - Conversión estimada: X%

   ## Posts con mayor impacto en tráfico
   [tabla: fecha | texto (100 chars) | likes | RTs | pico tráfico siguiente día | variación %]

   ## Días de venta y contenido previo
   [para cada venta: fecha venta, posts publicados en los 7 días anteriores]

   ## Top posts del mes (por engagement)
   [top 5 por likes+RTs]

   ## Insights y recomendaciones
   [qué temáticas/formatos correlacionan mejor con ventas]
   ```

5. **Guardar** en `~/Documents/aipal/reports/monthly-content-report/YYYY-MM.md`

6. **Enviar** resumen compacto por Telegram

## Registro en el vault (paso final obligatorio)

Después de guardar el informe completo en `~/Documents/aipal/reports/monthly-content-report/YYYY-MM.md`, añadir una entrada al fichero `~/Documents/aipal/10-areas/contenido/learnings.md`. Si el fichero no existe, crearlo.

**Formato del bloque a añadir** (append, nunca truncar):

```markdown
## YYYY-MM — Informe mensual

- **Ventas**: X unidades / €X.XXX
- **Visitas /cursos/expert/ai**: X pageviews
- **Posts publicados**: X
- **Top posts por correlación con ventas**: [títulos o fragmentos]
- **Patrón detectado**: [breve descripción del patrón contenido→ventas más claro del mes]
- **Temáticas con mejor rendimiento**: [lista]
- **Temáticas con peor rendimiento**: [lista]
- **Informe completo**: `reports/monthly-content-report/YYYY-MM.md`
```

Este registro permite que futuras sesiones (y otras skills como weekly-newsletter) conozcan qué contenido convierte sin necesidad de releer el informe completo.

## Notas importantes

- Umami auth con `path=eq.%2Fcursos%2Fexpert%2Fai` (formato URL de Umami v2+, NO `url=` ni `filters=`)
- Solo contar **primera compra** en ventas a plazos
- Los posts de X via bird son solo los propios, no RTs ni respuestas
- Correlación no es causalidad: señalar posibles relaciones, no afirmarlas

## Scripts auxiliares

- `scripts/umami-pageviews.js` — Obtiene pageviews de Umami por día
- `scripts/correlate.js` — Cruza datos y genera tabla de correlación

## Ejecución manual

```bash
# Informe del mes anterior
node scripts/monthly-report.js

# Informe de un mes específico
node scripts/monthly-report.js --month 2026-01
```
