---
name: skill-creator
description: Template para criar novas skills
---

Template e guia para criar skills no padrao do Ta na Mao.

## Estrutura de uma Skill

```markdown
# Skill: Nome da Skill

Descricao breve do que a skill faz.

## Comandos/Acoes Principais
[Lista de comandos ou acoes]

## Como Usar
[Exemplos praticos]

## Arquivos Relacionados
[Arquivos do projeto relevantes]

## Troubleshooting (opcional)
[Problemas comuns e solucoes]
```

## Template Basico

```markdown
# Skill: [Nome]

[Descricao em 1-2 linhas]

## Comandos
\`\`\`bash
# Comando principal
comando exemplo

# Variacoes
comando --flag
\`\`\`

## Exemplos

### Caso de Uso 1
\`\`\`
[exemplo]
\`\`\`

### Caso de Uso 2
\`\`\`
[exemplo]
\`\`\`

## Arquivos
- `caminho/arquivo1.py` - Descricao
- `caminho/arquivo2.py` - Descricao

## Dicas
- Dica 1
- Dica 2
```

## Categorias de Skills

| Categoria | Foco | Exemplo |
|-----------|------|---------|
| Dominio | Beneficios sociais | beneficio-checker.md |
| Desenvolvimento | Codigo e testes | run-tests.md |
| Infraestrutura | Deploy e ops | deploy.md |
| Dados | Processamento | csv-analyzer.md |
| Escrita | Documentacao | linguagem-simples.md |
| Seguranca | Protecao | defense-in-depth.md |

## Boas Praticas

1. **Nome**: Use kebab-case (palavras-separadas-por-hifen)
2. **Extensao**: Sempre `.md`
3. **Localizacao**: `.claude/skills/`
4. **Linguagem**: Portugues (projeto brasileiro)
5. **Exemplos**: Sempre incluir comandos que funcionam
6. **Concisao**: Direto ao ponto, sem enrolacao

## Integracao com MCP

Se a skill usa um MCP server:

```markdown
## Dependencia MCP

Utiliza o MCP `nome-do-mcp` configurado em `.mcp.json`.

### Acoes Disponiveis
\`\`\`
mcp__nome__acao1
mcp__nome__acao2
\`\`\`
```

## Checklist Nova Skill

- [ ] Arquivo criado em `.claude/skills/`
- [ ] Nome em kebab-case
- [ ] Descricao clara
- [ ] Exemplos funcionais
- [ ] Adicionado ao README.md
- [ ] Testado manualmente
