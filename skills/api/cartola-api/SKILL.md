---
name: cartola-api
description: Base de conhecimento aprofundada de TODAS as APIs públicas e autenticadas do Cartola FC (api.cartolafc.globo.com / api.cartola.globo.com). Use quando precisar consultar endpoints, estrutura de resposta, campos de dados, autenticação via X-GLB-Token, scouts, posições, clubes, mercado, ligas, times, rodadas, atletas ou qualquer integração com a API oficial do Cartola. Participante de teste premium - Paulinett Miranda (ID 13935277).
---

# Cartola API - Knowledge Base

Base de conhecimento completa das APIs oficiais do Cartola FC.
Fonte: [caRtola Wiki - Lista de links para API](https://github.com/henriquepgomide/caRtola/wiki/Lista-de-links-para-API-do-Cartola-Oficial)

## Base URLs

A API migrou de domínio ao longo dos anos:
- **Atual (2024+):** `https://api.cartola.globo.com`
- **Legado:** `https://api.cartolafc.globo.com`

Ambos podem funcionar. O sistema usa `api.cartola.globo.com` no `cartolaApiService.js`.

## Participante de Teste (Premium)

| Campo | Valor |
|-------|-------|
| **Nome** | Paulinett Miranda |
| **Time ID** | `13935277` |
| **Time** | Urubu Play F.C. |
| **Status** | Assinante Premium (Cartola PRO) |
| **Endpoint teste** | `GET /time/id/13935277` |

## Referências Detalhadas

- **Endpoints completos:** Ver [references/api-endpoints.md](references/api-endpoints.md) para lista completa de todos endpoints públicos e autenticados
- **Schemas de resposta:** Ver [references/response-schemas.md](references/response-schemas.md) para estrutura JSON de cada endpoint

## Quick Reference - Endpoints Mais Usados

### Públicos (sem autenticação)
| Endpoint | Descrição |
|----------|-----------|
| `GET /mercado/status` | Status do mercado, rodada atual, fechamento |
| `GET /atletas/mercado` | Todos atletas disponíveis no mercado |
| `GET /atletas/pontuados` | Pontuação da rodada atual |
| `GET /atletas/pontuados/{rodada}` | Pontuação de rodada específica |
| `GET /time/id/{id}` | Dados do time (escalação atual) |
| `GET /time/id/{id}/{rodada}` | Dados do time em rodada específica |
| `GET /time/slug/{slug}` | Time por slug |
| `GET /times?q={query}` | Buscar times por nome |
| `GET /liga/{slug}` | Dados de uma liga pública |
| `GET /ligas?q={query}` | Buscar ligas por nome |
| `GET /clubes` | Todos os clubes do Brasileirão |
| `GET /rodadas` | Lista das 38 rodadas |
| `GET /partidas` | Próximas partidas |
| `GET /partidas/{rodada}` | Partidas de rodada específica |
| `GET /esquemas` | Formações táticas disponíveis |
| `GET /mercado/destaques` | Jogadores mais escalados |
| `GET /pos-rodada/destaques` | Destaques pós-rodada |

### Autenticados (requer `X-GLB-Token`)
| Endpoint | Descrição |
|----------|-----------|
| `GET /auth/time` | Time do usuário logado |
| `GET /auth/time/info` | Info detalhada do time logado |
| `GET /auth/ligas` | Ligas do usuário logado |
| `GET /auth/liga/{slug}` | Liga específica (com dados privados) |
| `POST /auth/time/salvar` | Salvar escalação |

## Autenticação

```
Header: X-GLB-Token: <token>
```

O token é obtido via login Globo.com (OAuth). Para endpoints `/auth/*` é obrigatório.

## Integração no Projeto

O serviço `services/cartolaApiService.js` implementa:
- Retry com backoff exponencial (1s, 2s, 4s)
- Cache via NodeCache (TTL 5min padrão)
- Timeout de 15s
- Validação de scout data
- Detecção dinâmica de rodada atual

### Métodos Disponíveis

```javascript
import cartolaApi from '../services/cartolaApiService.js';

await cartolaApi.obterStatusMercado()                    // /mercado/status
await cartolaApi.obterTimesLiga(ligaId)                  // /liga/{id}
await cartolaApi.obterDadosTimeRodada(timeId, rodada)    // /time/id/{id}/{rodada}
await cartolaApi.buscarTimePorNome(query, limit)         // /times?q=
await cartolaApi.buscarTimePorId(timeId)                 // /time/id/{id}
await cartolaApi.buscarTimePorIdCompleto(timeId)         // /time/id/{id} (raw)
await cartolaApi.coletarGolsLiga(ligaId, rodada)         // Coleta gols via /atletas/pontuados
await cartolaApi.getRodadaStatus(rodada)                 // Status derivado do mercado
```

## Mapeamentos Críticos

### Posições (posicao_id)
| ID | Posição | Abreviação |
|----|---------|------------|
| 1 | Goleiro | GOL |
| 2 | Lateral | LAT |
| 3 | Zagueiro | ZAG |
| 4 | Meia | MEI |
| 5 | Atacante | ATA |
| 6 | Técnico | TEC |

### Status do Mercado (status_mercado)
| Código | Status |
|--------|--------|
| 1 | Mercado aberto |
| 2 | Mercado fechado |
| 4 | Manutenção |
| 6 | Fim de temporada |
| 15 | Mercado em atualização |

### Scouts Principais
| Sigla | Significado | Pontos |
|-------|-------------|--------|
| G | Gol | +8.0 |
| A | Assistência | +5.0 |
| FT | Finalização na trave | +3.5 |
| FD | Finalização defendida | +1.2 |
| FF | Finalização pra fora | +0.8 |
| FS | Falta sofrida | +0.5 |
| PE | Passes errados | -0.3 |
| I | Impedimento | -0.1 |
| FC | Falta cometida | -0.3 |
| GC | Gol contra | -3.0 |
| CV | Cartão vermelho | -3.0 |
| CA | Cartão amarelo | -1.0 |
| SG | Sem gol sofrido (goleiro/zagueiro) | +5.0 |
| DD | Defesa difícil | +3.0 |
| GS | Gol sofrido | -1.0 |
| DS | Desarme | +1.2 |
| PP | Pênalti perdido | -4.0 |
| DP | Defesa de pênalti | +7.0 |
| PC | Passe completo (>30) | +0.3 |
