---
name: projecoes-readmodels
description: Archived skill guidance for projecoes-readmodels.
---

---

name: projecoes-read-models
description: Use para criar projeções como 9BOX, dashboards e visões de leitura otimizadas para decisão.
--------------------------------------------------------------------------------------------------------

# Instruções da Skill

Trabalhe exclusivamente no **lado de leitura** do sistema.
Tudo aqui deve ser **derivado** e **reconstruível**.

## Regras e Passos

1. **Modelagem (M):**

   * Defina tabelas de projeção (`nine_box_projections`, dashboards).
   * Nunca trate projeção como fonte da verdade.

2. **Ação (A):**

   * Crie Projectors que reagem a eventos (`AxesUpdated`).

3. **Lógica (L):**

   * Converta scores contínuos em bandas (low / mid / high).
   * Determine quadrante apenas na projeção.

4. **Teste (T):**

   * Teste reconstrução completa a partir de eventos simulados.

## Uso de Ferramentas

* Utilize scripts da pasta `/scripts/projections` se existirem.
* Evite lógica complexa em queries SQL.