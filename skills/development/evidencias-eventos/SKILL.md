---

name: evidencias-e-eventos
description: Use para implementar registro de evidências, eventos de domínio e listeners no Laravel.
----------------------------------------------------------------------------------------------------

# Instruções da Skill

Implemente **fatos imutáveis** e **eventos explícitos**, respeitando o ciclo de vida do Laravel.

O agente deve priorizar:

* Clareza semântica
* Auditabilidade
* Reconstrução de estado por eventos

## Regras e Passos

1. **Modelagem (M):**

   * Defina o que é Evidência e o que não é.
   * Garanta imutabilidade por código (model boot / constraints).

2. **Ação (A):**

   * Crie Actions (casos de uso) para registrar evidências.
   * Utilize o Service Container para injeção de dependências.

3. **Lógica (L):**

   * Dispare eventos de domínio (`EvidenceRecorded`, `CycleClosed`).
   * Não calcule scores dentro da Action.

4. **Teste (T):**

   * Crie testes que validem:

     * Evidência não pode ser alterada
     * Evento é disparado corretamente

## Uso de Ferramentas

* Use `php artisan make:event` e `make:listener` apenas após validação conceitual.
* Prefira Pest para testes.