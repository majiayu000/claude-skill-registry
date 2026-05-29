---

name: agregadores-performance-potencial
description: Use para implementar serviços de agregação que calculam os eixos de Performance e Potencial a partir de evidências.
--------------------------------------------------------------------------------------------------------------------------------

# Instruções da Skill

Implemente **serviços puros**, determinísticos e testáveis.
Agregadores **não escrevem no banco** e **não conhecem UI**.

## Regras e Passos

1. **Modelagem (M):**

   * Identifique dimensões do eixo (ex.: Entrega, Qualidade, Autonomia).
   * Defina pesos e normalização por complexidade de contexto.

2. **Lógica (L):**

   * Implemente agregadores separados:

     * `PerformanceAggregator`
     * `PotentialAggregator`
   * Garanta a regra: *Potencial só cresce com progressão de complexidade*.

3. **Integração:**

   * Receba evidências via eventos.
   * Retorne DTOs (`AxesResult`), nunca Models.

4. **Teste (T):**

   * Teste cálculos com múltiplos contextos e ciclos.
   * Teste teto de potencial sem progressão.

## Uso de Ferramentas

* Use classes em `app/Domains/Aggregation`.
* Não use Eloquent dentro dos testes de cálculo (prefira mocks ou collections).
