---
name: validation-checklist
description: 'Skill de validação pré-entrega para projetos de desenvolvimento (backend/frontend:
  tests, lint, tsc, docs, QA).'
---

---
name: validation-checklist
description: Skill de validação pré-entrega para projetos de desenvolvimento (backend/frontend: tests, lint, tsc, docs, QA).
---

# Quando usar

Após implementação pela equipe/agent de desenvolvimento, antes de entregar a task.

# Objetivo

Garantir qualidade mínima e documentação alinhada antes do handoff.

# Passos Universais

Aplicáveis a qualquer stack (backend ou frontend):

1) **Testes**: executar `npm run test` (unit + integration) sem falhas; cobrir fluxo principal e um alternativo por caso de uso.
2) **Qualidade**: `npm run lint`, `npm run format` (se existir), `npm run tsc --noEmit`.
3) **Execução manual**: subir aplicação (`npm run start`, `npm run dev`, ou comando do projeto) e validar funcionamento.
4) **Documentação**: atualizar `tasks.md` com status; criar `<numero-task>_testes_para_QA.md` no diretório da task (cenários, passos, dados, esperado).
5) **Logs/Security**: logging adequado (Winston, console estruturado); sem dados sensíveis em logs/fixtures.

# Validações Específicas por Stack

## Para projetos Backend (NestJS/Node.js)

- Validar endpoints tocados via `api.http` (auth, payload, status esperado)
- Atualizar Swagger com exemplos completos; adicionar requests no `api.http`
- Verificar DTOs, validações (class-validator) e guards/middlewares se aplicável

## Para projetos Frontend (Next.js/React)

- Validar build production (`npm run build`) sem erros
- Verificar bundle size e performance (lighthouse, bundle analyzer)
- Testar SSR/SSG se aplicável (páginas renderizadas corretamente)
- Validar rotas e páginas funcionais no navegador
- Verificar componentes visuais e responsividade

# Procedimento de falha

Se qualquer item falhar, PAUSAR e corrigir antes de entregar; registrar causa.

# Saída esperada

- Relatório curto: comandos executados e status (PASS/FAIL), endpoints validados, docs atualizadas, pendências/riscos.
