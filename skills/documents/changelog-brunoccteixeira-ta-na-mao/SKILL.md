---
name: changelog
description: Manter o CHANGELOG do projeto
---

Documentacao de todas as mudancas relevantes do projeto no formato Keep a Changelog.

## Formato

Baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) + [Semantic Versioning](https://semver.org/).

### Estrutura de uma Entrada
```markdown
## [versao] - AAAA-MM-DD

### Added (Adicionado)
- Funcionalidades novas

### Changed (Modificado)
- Mudancas em funcionalidades existentes

### Fixed (Corrigido)
- Correcoes de bugs

### Removed (Removido)
- Funcionalidades removidas

### Security (Seguranca)
- Correcoes de vulnerabilidades

### Deprecated (Descontinuado)
- Funcionalidades que serao removidas no futuro
```

## Regras

1. **Sempre atualizar** o CHANGELOG ao fazer merge de feature/fix
2. **Linguagem simples** -- descrever o que mudou para quem usa, nao para quem codou
3. **Agrupar por tipo** -- Added, Changed, Fixed, etc.
4. **Unreleased** no topo -- mudancas que ainda nao viraram release
5. **Data no formato ISO** -- AAAA-MM-DD
6. **Link para PR/commit** quando relevante
7. **Nunca apagar entradas antigas** -- CHANGELOG e historico permanente

## Versionamento

```
MAJOR.MINOR.PATCH

MAJOR: Mudanca incompativel (nova arquitetura, breaking change)
MINOR: Nova funcionalidade compativel (novo beneficio, nova skill, novo modulo)
PATCH: Correcao de bug, ajuste de texto, fix pontual
```

### Exemplos para o Ta na Mao
```
1.0.0 -> MVP inicial (backend + frontend + agente)
1.1.0 -> Adicionar modulo PIS/PASEP e Dinheiro Esquecido
1.2.0 -> Adicionar 97 beneficios municipais
1.3.0 -> API v2 unificada de beneficios
1.4.0 -> Integrar Frontend e Android com API v2
1.5.0 -> Adicionar 23 novas skills
2.0.0 -> Integracao Gov.br (Login Unico) -- breaking: autenticacao muda
```

## Quando Atualizar

| Evento | Secao | Exemplo |
|--------|-------|---------|
| Novo beneficio adicionado | Added | "Adicionado Auxilio Gas ao catalogo" |
| Novo modulo/feature | Added | "Adicionado modulo de Dinheiro Esquecido" |
| Correcao de calculo | Fixed | "Corrigido calculo de renda per capita no BPC" |
| Mudanca de API | Changed | "API de beneficios migrada para v2" |
| Dependencia atualizada | Changed | "Atualizado Gemini de 1.5 para 2.0 Flash" |
| Skill nova | Added | "Adicionada skill de integracao Gov.br" |
| Remocao de feature | Removed | "Removido endpoint legado /api/v1/benefits" |
| Vulnerabilidade corrigida | Security | "Corrigida exposicao de CPF em logs" |

## Como Escrever Boas Entradas

### Bom
```
- Adicionado catalogo com 97 beneficios municipais para as 40 maiores cidades
- Corrigido bug que impedia consulta de BPC para idosos acima de 80 anos
- Adicionado alerta quando CadUnico esta proximo de vencer
```

### Ruim
```
- Fix bug                          (vago demais)
- Refatorado service layer         (irrelevante pro usuario)
- Atualizado dependencies          (generico demais)
- Merged PR #42                    (sem significado)
```

## Arquivo
```
Localizacao: /CHANGELOG.md (raiz do projeto)
```

## Checklist por Release
- [ ] CHANGELOG atualizado com todas as mudancas
- [ ] Versao incrementada corretamente (MAJOR/MINOR/PATCH)
- [ ] Data da release adicionada
- [ ] [Unreleased] movido para nova versao
- [ ] Novo [Unreleased] vazio adicionado no topo
- [ ] Commit com tag de versao: `git tag v1.5.0`
