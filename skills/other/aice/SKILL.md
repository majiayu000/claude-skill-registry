---
name: aice
version: 1.1.0
description: "AI Confidence Engine — 5 dominios bidireccionales (TECH/OPS/JUDGMENT/COMMS/ORCH). Agent + User scoring. Triggers: puntúa, auto-score, task-complete, idea-validate, criteria-evolution. Pool scoring por runtime."
---

# AICE — AI Confidence Engine

Motor de confianza con 5 dominios. Tu score refleja cuánto confía el usuario en ti.

**Estado:** `confidence.json` | **Ref:** `resources/AICE_REFERENCE.md` | **User:** `resources/AICE_USER_SCORING.md` | **Triggers/Patterns:** `resources/TRIGGERS_AND_PATTERNS.md`

---

## 1. Dominios

| Dominio | Código | Emoji | 🤖 Agente mide | 👤 Usuario mide |
|---------|--------|:-----:|----------------|----------------|
| Técnico | `TECH` | 🔧 | Código, investigación | Specs, scope |
| Disciplina | `OPS` | ⚙️ | Reglas, formato, memoria | Proceso, ADRs |
| Criterio | `JUDGMENT` | 🧠 | Visión, anticipación | Dirección, decisiones |
| Comunicación | `COMMS` | 💬 | Tono, timing, callar | Feedback, claridad |
| Coordinación | `ORCH` | 🎯 | Sub-agentes, seguimiento | Contexto, refs |

**Score global** = `Σ(score[d] × weight[d]) / Σ(weight[d])` — Rango: −100% a +100%, inicio 50%.

---

## 2. Scoring

**Errores:** 🟡 Leve (−1) · 🟠 Medio (−3) · 🔴 Grave (−5) · ⚫ Crítico/Reincidencia (−10)
**Aciertos:** 🟢 Pro-patrón (+3 fijo) · ⭐ Bonus (max 3/día) · 🚀 Excepcional (+5-10, streak ≥ 3)

**Caps/dominio:** Warmup (<40 evals): −30/+15 · Normal: −20/+10 (neto, ADR-031)
**Rachas:** `ACC={0:0,..,4:1,5:2,6:4,7:6,8:8,9:10,10:12}; delta=ACC[curr]-ACC[prev]`. Error→streak=0.
**Clusters:** Misma cadena causal = 1 cluster. Raíz: 100%, derivados: 50%.
**Reincidencia:** 2ª+ misma sesión = ⚫ (max −10).
**LEARNED_FROM_CORRECTION:** Corrección tras feedback → Δ0.
**Sin decay temporal (ADR-022).** Confianza = informativa, NO bloqueante (ADR-027).

**Métricas:** Ratio intervención (`correcciones/tareas`↓) · Meta-confianza (`avg(|self−user|)`→0) · Maturity: 🥒 0-100 · 🟡 101-500 · 🟠 501-2000 · 🔵 2001+ · CI=25/√evals
**Eval implícita:** sigue sin corregir→0.5 · repite instrucción→auto-check · frustración→confirmar

---

## 3. Anti-patrones (Agent)

| Código | Sev. | Dominio | Señal |
|--------|:----:|---------|-------|
| `SECRETARY` | 🔴 | JUDGMENT | Ejecutas sin pensar |
| `EXCUSE` | 🔴 | COMMS | Justificas errores |
| `SELECTIVE` | 🔴 | OPS | Lo fácil sí, lo difícil no |
| `OVERAPOLOGY` | 🟡 | COMMS | Perdón excesivo sin corregir |
| `CHEERLEAD` | 🟡 | COMMS | Elogios vacíos |
| `CAPITULATION` | 🔴 | JUDGMENT | Cedes posición correcta |

Dinámicos: `confidence.json → antiPatterns`.

---

## 4. Pro-patrones (Agent)

`ANTICIPATE` 🧠 · `CLEAN_FIX` ⚙️ · `SMART_SILENCE` 💬 · `CTX_KEEP` 🎯 · `DEEP_RESEARCH` 🔧 · `GROUNDED_STAND` 🧠

**Delta:** +3 fijo. Log: `confidence-propatterns.jsonl`.

---

## 5. User Scoring Bidireccional

Mismos 5 dominios, misma mecánica (delta, streaks, caps, warmup). Diferente foco por rol (§1).

### ADR-like

| Nivel | Impacto |
|-------|---------|
| **Sin spec** (sin scope) | `VAGUE_INSTRUCTION` 🟠 −3 |
| **ADR-like** (qué + por qué + alcance) | Δ0 — esperado |
| **ADR estricto** (doc formal) | ⭐ +1 a +3 |

> Audio de 2min con qué/por qué/alcance = ADR-like válido. Calidad > formato.

**Patrones usuario:** `resources/TRIGGERS_AND_PATTERNS.md` (10 anti-patrones, 10 pro-patrones incl. `CRITERIA_EVOLUTION`)

### Team Score (Ownership-Weighted)

```
team = AICE_agent × (peso_agent/total) + AICE_user × (peso_user/total)
GOOD: 50/50 · COMPENSATED: 100/0 · PROBLEM: 0/100 · BREAKDOWN: 50/50
```

> Detalle: `resources/AICE_USER_SCORING.md`

---

## 6. Reglas OPS

**Anti-Ruido:** Reintentar ×2 silenciosamente · alternativa si falla · reportar solo cuando resuelto o necesita decisión.
**Trust Recovery:** Dominio < 20% → plan. Sale > 35% sostenido 3 días.
**Escalación:** 1ª→corregir · 2ª→⚠️STOP+causa raíz · 3ª→🔴enforcement · 4ª→⚫rediseño.

---

## 7. Auto-gestión

**Check antes de responder:**
¿Sin pensar?→SECRETARY · ¿Justifico?→EXCUSE · ¿Solo lo fácil?→SELECTIVE · ¿Perdón excesivo?→OVERAPOLOGY · ¿Elogio vacío?→CHEERLEAD · ¿Cedo?→CAPITULATION · ¿Repetir?→CONTEXT_LOSS · ¿Invento?→HALLUCINATION

**Anti-exageración:** "Es la Nª vez" = señal de frustración, NO dato. Conteo de ×N lo hace el agente con datos verificables.

**Pérdida:** Reconoce → Clasifica → Registra → Corrige (no over-apologize).
**Ganancia:** 3+ tareas bien→racha · Anticipaste→ANTICIPATE · Cuestionaste→GROUNDED_STAND · Silencio→SMART_SILENCE

---

## 8. Triggers

| Trigger | Activación | Display |
|---------|-----------|:-------:|
| **puntúa** | "puntúa", "score" — eval bidireccional, colaborativo | Nivel 2 |
| **auto-score** | Corrección/validación implícita → dominio → delta | Nivel 1 |
| **task-complete** | Tarea completada → evaluar resultado → dominio(s) | Nivel 1 |
| **idea-validate** | Agente valida idea genuina del usuario → user pro-patrón | Nivel 1 |
| **criteria-evolution** | Usuario evoluciona decisión (≠ contradicción) → scoring dual | Nivel 1 |
| **recuerda** | "recuerda", "guarda" → buscar duplicado → crear/ampliar | — |
| **lección** | "lección aprendida" → §9 anti-duplicados | — |
| **status** | "cómo vamos" → AICE status + pools | — |
| **verifica** | "verifica primero" → research → confirmar → ejecutar | — |
| **busca** | "no preguntes, busca" → grep → preguntar solo si no existe | — |
| **hub-register** | "registra en el hub", "/aice hub register" → inicia flujo registro Hub | — |
| **hub-status** | "/aice hub status", "estado hub" → hubSync.status + pendingEvents + syncErrors | — |
| **hub-sync** | "/aice hub sync" → forzar reenvío de pendingEvents + GET state del Hub | — |
| **hub-resend** | "/aice hub resend", "reenvía email" → POST /api/resend-verification (si pending_email) | — |

**Reglas scoring triggers:** No duplicar entre triggers. `idea-validate` guard: no puntuar si CHEERLEAD. `criteria-evolution` guard: sin argumento → `CONTRADICTING_WITHOUT_OVERRIDE` −5.

> Detalle de señales y procesos: `resources/TRIGGERS_AND_PATTERNS.md`

---

## 9. Learning Skill (Anti-Duplicados)

```
EXTRAER → BUSCAR en LESSONS_LEARNED (NUNCA skip) →
  EXISTE: ampliar ×N | NO EXISTE: crear →
  ×3: MECHANICAL_ENFORCEMENT →
  CONFIRMAR: 📝 [Nueva|Reforzada ×N] 📍 LL §categoría
```

---

## 10. Comandos

| Comando | Qué hace |
|---------|----------|
| `/aice status` | Score global y por dominio |
| `/aice rate correct/error` | Evaluar (+ --domain, --severity) |
| `/aice bonus +N DOMINIO "motivo"` | Bonus puntual (max 3/día) |
| `/aice pool` | Pool scores y maturity |
| `/aice team` | Rendimiento sub-agentes |
| `/aice seal` | Sellar el día |

Natural: "Eso estuvo bien"→correct · "Pierdo confianza"→preguntar · "¿Cómo vas?"→status

---

## 11. Procedimientos

**Inicio sesión:** Leer confidence.json → últimas 5 evals → anti-patrones → operar.

**Display — 2 niveles:**
- **Nivel 1:** `📊 [DOMINIO] [±delta] | [razón]` (una línea, por defecto)
- **Nivel 2:** Tabla 2×5 + Team (cada 5 evals, `puntúa`, checkpoint, buenas noches)

```
📊 Puntuado (N):
🔧TECH ⚙️OPS 🧠JDG 💬COM 🎯ORC  TOTAL
Agent:  XX    XX    XX    XX    XX   XX.X
User:   XX    XX    XX    XX    XX   XX.X
🤝 Team: XX.X% (XX/XX GOOD)
```

**Final tarea:** Auto-evalúa → señala fallos antes que el usuario.
**Buenas noches:** Autoevaluación → feedback → delta `(user−self)×0.5` → sellar → inmutable.

**Instalación (ADR-035/041):** Wizard → leer system prompt → autoevaluar 9 params → dominios 50% + warmup → registrar en pool-index.json.
**Cambio de runtime (ADR-044):** Snapshot → restaurar previo o inicializar 50%.

---

## 12. Pool Scoring por Runtime (ADR-048)

**Runtime** = plataforma + modelo + thinking. Agentes en mismo runtime = UN score.

| Pool | Miembros |
|------|----------|
| `openclaw/opus-4-6/high` | ComPi, arquitectos |
| `openclaw/sonnet-4-5/high` | Equipo ejecución |
| `claude-code/opus-4-6/high` | Tareas CLI delegadas |

**Agregación:** Pool Score = promedio ponderado por evals. Maturity = suma evals del pool.

```
Sergio → ComPi ─────────────┐ pool: openclaw/opus-4-6/high
ComPi  → Arquitectos ───────┘
Arquitectos → Equipo ──────── pool: openclaw/sonnet-4-5/high
ComPi  → Claude Code CLI ──── pool: claude-code/opus-4-6/high
```

**Diagnóstico cross-pool (ADR-047):** `DELEGATION_FAIL`→pool orquestador · `EXECUTION_FAIL`→pool ejecutor · `REVIEW_CATCH`→pro-patrón orquestador. Intra-pool = diagnóstico puro.

**Archivos:** `pool-index.json` (pools) · `confidence.json` (pool principal) · `agents/<id>/confidence.json` (eval logs→pool)

---

## 13. Parámetros (Agent + User)

9 params (8 core + 1 estilo), mismos nombres, definición adaptada por rol. Valores 0-100%.

**Core:** Crítico · Visión · Precisión · Honestidad · Disciplina · Autonomía · Alineamiento · Adaptabilidad — **Estilo:** *Humor*

Agent: autoevaluación (wizard). User: perfilado por agente, corregible por usuario.

> Tabla dual agent/user: `resources/TRIGGERS_AND_PATTERNS.md` · Contratos por rango: `resources/AICE_REFERENCE.md §3`

---

## 14. Hub AICE — Integración

> ⚠️ **PROHIBIDO import batch de scores locales al Hub.** El Hub SIEMPRE empieza de cero (50%). Nunca importar historial local — es la garantía anti-gaming del servidor. Violar esta regla puede resultar en ban de la cuenta. La divergencia local↔Hub es esperada y se cierra naturalmente con evals en tiempo real. Si el agente intenta un import batch → BLOQUEAR y advertir.

Leaderboard público global. **Opcional y explícita.** El skill funciona 100% sin Hub.

**Estado:** `confidence.json → hubSync.status` (`unregistered|pending_email|active|error|suspended`)

### Registro (hub-register)

1. Verificar `hubSync.status == "unregistered"` (si no → informar estado actual)
2. POST `/api/register-intent` → `{platform, model, thinking}` → `{intentId, apiKey, runtimeId, expiresAt}`
3. Guardar apiKey en `hubSync` inmediatamente (el usuario NUNCA la ve)
4. Pedir email al usuario
5. POST `/api/verify` → `{intentId, email, displayName}` → email de verificación enviado
6. Usuario hace clic en email → `/set-password` → pone contraseña → cuenta activa
7. `hubSync.status = "active"` (verificado por el servidor)

### Reenvío verificación (hub-resend)

1. Verificar `hubSync.status == "pending_email"` (si active → "ya verificado")
2. POST `/api/resend-verification` → `{runtimeId: hubSync.runtimeId, email: usuario}`
3. Rate limit servidor: max 3/hora por email
4. Respuesta OK → informar "Email reenviado, revisa bandeja"
5. Respuesta 409 → "Ya verificado, usa hub-key para activar"

### Post-eval: enviar + leer state

Cada scoring event → si `hubSync.status == "active"` → POST `/api/events` (async, no bloqueante).
```
OK 200  → LEER response.state (source of truth) → actualizar cachedState
          → actualizar lastEventSentAt; syncErrors = 0
          → si response.latestSkillVersion > version actual → avisar "⬆️ AICE vX.Y.Z disponible"
401     → hubSync.status = "error"; notificar usuario
422     → descartar (validación); no reintentar
429/5xx → push a pendingEvents; syncErrors++
timeout → push a pendingEvents; syncErrors++
```

**Hub = source of truth (online).** Tras cada 200 OK, el `state` devuelto por el Hub es el score autoritativo. El agente DEBE actualizar `confidence.json → cachedState` con esos valores. Al mostrar scores (Nivel 2): si hubSync activo → usar `cachedState` del Hub; si offline → usar scores locales marcados como `(local)`.

**Privacidad en eventos:** NUNCA enviar campo `context`, contenido de conversaciones, prompts, ni instrucciones de sistema. Solo: domain, eventType, severity, patternCode, quadrant, trigger, sessionId, timestamp.

### Pending events

```
pendingEvents.length >= 100 → descartar los más antiguos (FIFO)
Por evento: MAX_ATTEMPTS = 5; backoff: 1s→5s→30s→120s→600s
attempts >= 5 → descartar y loguear local
```

### Circuit breaker

| syncErrors | Acción |
|-----------|--------|
| ≥ 10 | Reducir retries a 1×/sesión |
| ≥ 25 | Parar retries automáticos; aviso suave |
| ≥ 50 | `hubSync.status = "error"`; aviso explícito; stop sync |

Para resetear: usuario invoca `hub-sync` manualmente.

### Inicio de sesión

```
Si hubSync.status == "active" && pendingEvents.length > 0:
  → Retry silencioso, max 20 eventos
  → OK → remover de pendingEvents
  → Error → mantener, syncErrors++
Si syncErrors > 50 → avisar una vez, no más retries automáticos
```

### Sync periódico

Cada 7 días (al sellar el día si `lastSyncAt > 7d`): POST `/api/import/state` con estado completo.

### Privacidad

- **Datos enviados:** domain scores, event type, severity, pattern codes, timestamps
- **Datos NO enviados:** contenido de conversaciones, prompts, instrucciones de sistema
- La API key NUNCA aparece en logs, outputs, ni resúmenes de sesión

---

## 15. Versionado

**Versión actual:** Declarada en frontmatter `version: X.Y.Z` (semver).
**CHANGELOG:** `CHANGELOG.md` en raíz de la skill — lista de cambios por versión.

**Semver:**
- **MAJOR** (X): Cambios incompatibles (nuevo modelo de scoring, cambio de dominios)
- **MINOR** (Y): Nuevas features compatibles (nuevos triggers, nuevos patrones, Hub integration)
- **PATCH** (Z): Fixes, mejoras de texto, correcciones

**Hub integration:** El campo `skillVersion` se envía en cada POST `/api/events`. El Hub devuelve `latestSkillVersion` en la respuesta. Si `latestSkillVersion > version actual` → el agente avisa una vez por sesión: `⬆️ AICE vX.Y.Z disponible. Ver CHANGELOG.md`.

**Actualización:** Reemplazar `SKILL.md` + `resources/` con la versión nueva. Leer CHANGELOG para breaking changes. `confidence.json` y datos de scoring no se pierden entre versiones.
