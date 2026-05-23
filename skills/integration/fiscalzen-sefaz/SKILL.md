---
type: skill
name: Fiscalzen SEFAZ
description: "Integrações SEFAZ (NF-e/CT-e/MDF-e) no padrão FiscalZen: DistDFe, Manifestação e eventos — com certificados A1, SOAP, retry/backoff e persistência no produto."
skillSlug: fiscalzen-sefaz
phases: [E, V]
generated: 2026-01-28
status: filled
scaffoldVersion: "2.0.0"
---

## 🏗️ Contexto do Projeto (como o FiscalZen é estruturado)
- Monorepo com **pnpm-workspace** + **Turborepo**
- Código em **TypeScript** (ESM `"type": "module"`)
- Backend: **Fastify 4** (apps/api)
- Jobs: **BullMQ** (workers + scheduler)
- Persistência: **Drizzle ORM** + PostgreSQL
- Cache/queues: Redis
- Logging: **Pino**
- Pacote fiscal principal: `@fiscalzen/sefaz-client` (NF-e/CT-e/MDF-e)
- Parser fiscal: `@fiscalzen/xml-parser` (usado pelo sefaz-client e api)

✅ Regra: alterações de SEFAZ geralmente tocam **packages/** (cliente) e/ou **apps/api/** (orquestração + persistência).

---

## 🎯 Objetivo (o que esta skill resolve)
Aplicar mudanças relacionadas a SEFAZ mantendo consistência com a codebase:
- Preferir abstrações internas (`@fiscalzen/sefaz-client`) em vez de reimplementar SOAP/assinatura/certificado
- Validar certificado e permissões no backend antes de chamar SEFAZ
- Respeitar retry/backoff e throttling
- Persistir eventos e atualizar documentos do jeito do produto
- Garantir validação (unit/integration + homolog)

---

## 🧭 Onde mexer (mapa rápido)

### Cliente SEFAZ (packages/sefaz-client)
- `packages/sefaz-client/src/client.ts` → política de timeout/retry/backoff, `https.Agent`, `dispose()`, logging
- `packages/sefaz-client/src/soap-client.ts` + `src/soap/envelope.ts` → SOAP + envelope
- `packages/sefaz-client/src/services/*` → implementações por domínio:
  - `nfe-distdfe.ts` (DistDFe NF-e)
  - `cte-distdfe.ts`, `mdfe-distdfe.ts` (DistDFe CT-e/MDF-e)
  - `manifestacao.ts` (eventos do destinatário)
  - `event-query.ts` (consulta eventos)
  - `cte-events.ts` (eventos CT-e)
- `packages/sefaz-client/src/types.ts` → contratos + erros tipados (`SefazError`, `TimeoutError`, `CertificadoError`, etc.)
- `packages/sefaz-client/src/certificate.ts` → A1 (PFX), cache/invalidação, validações
- `packages/sefaz-client/src/signature.ts` → digest/assinatura (helpers)

### Produto (apps/api)
- `apps/api/src/modules/manifestacao/service.ts` → fluxo real de manifestação + persistência
- `apps/api/src/modules/certificates/*` → validação de certificados (gate antes de SEFAZ)
- `apps/api/src/modules/documents/*` → documento + status/manifestações
- `apps/api/src/jobs/queues.ts` → criação/agenda de jobs SEFAZ
- `apps/api/src/modules/nsu/*` + `packages/database/src/schema/nsu-control.ts` → controle de NSU/sync

---

## ✅ Regras obrigatórias (gates)

### 1) Sempre validar certificado antes de chamar SEFAZ (no produto)
Se a chamada vier do `apps/api`, **não chame SEFAZ sem passar pelo gate**:
- empresa existe
- `company.certificate` e `company.certificatePassword` existem
- certificado **não expirou**
- (se aplicável) tenantId correto (multi-tenant)

### 2) Não vazar segredo (PFX/senha)
- nunca logar senha do certificado
- nunca logar buffer do PFX
- ao logar erro, sanitize campos sensíveis

### 3) TLS estrito
- não desabilitar validação TLS (`rejectUnauthorized`)

### 4) Erros externos padronizados
No `apps/api`, problemas da SEFAZ devem virar erro de serviço externo (padrão do projeto), mantendo mensagem útil.

---

## 🔁 Retry/Backoff e Throttling (padrão FiscalZen)

### Ponto único de política: `packages/sefaz-client/src/client.ts`
✅ Regra: se você precisar mudar retry/backoff/timeout, faça **no client** (não espalhe retry pelos services).

### Throttling (ex.: cStat 656)
Recomendação de implementação consistente:
- tratar como erro recuperável
- aplicar retry com backoff exponencial + jitter
- evitar tempestade: preferir job/queue para processar em série por empresa/UF

---

## 📦 DistDFe (Golden Path) — como fazer no FiscalZen

### Cenários típicos
- Consulta por **último NSU** (sync contínuo)
- Consulta por **NSU específico**
- Consulta por **chave** (pontual)

### Padrão de implementação
1) Validar parâmetros (CNPJ, chave, nsu/ultNSU)
2) Montar request XML conforme tipo de consulta
3) Enviar via `SoapClient` / `SefazClient` (abstração interna)
4) Parsear retorno (cStat/xMotivo/ultNSU/maxNSU)
5) Extrair `docZip` e:
   - decodificar
   - detectar schema
   - derivar tipo/chave usando `@fiscalzen/xml-parser`
6) Retornar `DistDFeResponse` consistente
7) Se estiver no produto (apps/api): persistir e atualizar controle de NSU

### Regras de robustez
- `nsu` e `ultNSU` sempre como string com 15 dígitos (`padStart(15,'0')`)
- docZip inválido **não deve derrubar o lote inteiro** (registrar erro e seguir)
- ao tratar throttling, preferir política central no client

---

## 🧾 Manifestação do Destinatário (Golden Path) — padrão do produto

### Passo a passo (apps/api)
1) obter empresa com certificado (gate)
2) buscar documento por chave **com tenantId**
3) montar `CertificadoA1` no formato do `@fiscalzen/sefaz-client`
4) usar `env.SEFAZ_AMBIENTE`
5) chamar o client do pacote
6) se `sucesso=false`: lançar `ExternalServiceError('SEFAZ', xMotivo)`
7) persistir em `documentEvents` + atualizar `documents.manifestacao`

### Regras específicas
- eventos devem ser idempotentes na camada do produto (não duplicar o mesmo evento sem necessidade)
- manter rastreabilidade (documentId/chave/tipoEvento/protocolo/dataRegistro)

---

## 🧪 Validação (Fase V) — mínimo obrigatório

### Unit / pacote (sefaz-client)
- validar `validateParams` (CNPJ/chave)
- validar montagem de request por ultNSU/nsu/chave
- validar parsing de resposta (cStat e campos)
- validar docZip: sucesso e falha isolada

### Integration / produto (apps/api)
- empresa sem certificado → erro de validação
- certificado expirado → erro de validação
- documento inexistente → NotFound
- retorno `sucesso=false` da SEFAZ → ExternalServiceError
- persistência: criou event + atualizou documento

### Homologação
- testar ao menos:
  - DistDFe por ultNSU
  - Manifestação (um evento)
  - cenário de throttling (se possível reproduzir)

---

## 🧰 Prompt templates (como invocar a skill)

**Manifestação (produto)**
> “Aplique a skill `fiscalzen-sefaz` para ajustar o fluxo de manifestação em `apps/api`.  
> Preserve o gate de certificado + multi-tenant e mapeie falhas SEFAZ para erro externo padrão. Atualize persistência em `documentEvents` e `documents.manifestacao`.”

**DistDFe (pacote)**
> “Aplique a skill `fiscalzen-sefaz` para modificar `packages/sefaz-client/src/services/nfe-distdfe.ts`.  
> Preserve validações, padStart(15) e parsing docZip com `@fiscalzen/xml-parser`. Se tratar 656, preferir política central no client.”

---
