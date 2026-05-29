---

name: filament-decisao-9box
description: Use para criar páginas, widgets e resources no Filament focados em decisão, nunca em avaliação subjetiva.
----------------------------------------------------------------------------------------------------------------------

# Instruções da Skill

Filament é **UI**, não domínio.

## Regras e Passos

1. **Ação (A):**

   * Crie Pages customizadas para:

     * Mapa 9BOX
     * Dashboard de Pessoa
     * Dashboard de Contexto

2. **Lógica (L):**

   * Consuma apenas Read Models.
   * Para escrita, chame Actions explícitas.

3. **UX:**

   * Nunca usar linguagem de “avaliar”, “nota”, “classificação”.
   * Priorizar evidências, histórico e contexto.

4. **Teste (T):**

   * Teste permissões, filtros e carregamento correto de dados.

## Uso de Ferramentas

* Use Livewire apenas como orquestrador.
* Alpine.js apenas para estado visual local.