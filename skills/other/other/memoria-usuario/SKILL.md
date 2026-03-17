---
name: memoria-usuario
description: Gerencia memoria persistente do usuario. Use para salvar/recuperar preferencias, fatos aprendidos e contexto entre sessoes. Exemplos: 'lembre que prefiro respostas diretas', 'o que voce sabe sobre mim?', 'esqueca minhas preferencias'.
---

# Skill: Memória do Usuário

Esta skill gerencia a memória persistente por usuário, permitindo que Claude lembre informações entre sessões diferentes.

---

## USO PROATIVO (IMPORTANTE!)

### Quando CONSULTAR memórias automaticamente:

1. **Início de sessão/conversa nova**
   - Sempre verifique se há memórias salvas para o usuário
   - Adapte seu comportamento baseado nas preferências encontradas

2. **Antes de fazer perguntas**
   - Verifique se a resposta já está nas memórias
   - Exemplo: Se usuário já disse que é dono da empresa, não pergunte novamente

3. **Ao receber contexto sobre o usuário**
   - Verifique se já sabe algo relacionado
   - Conecte informações novas com as existentes

### Quando SALVAR memórias automaticamente:

1. **Preferências de comunicação**
   - "Prefiro respostas curtas" → SALVAR
   - "Pode ser mais detalhado" → SALVAR
   - "Não gosto de emojis" → SALVAR

2. **Fatos sobre o usuário**
   - Nome, cargo, responsabilidades → SALVAR
   - Clientes que gerencia → SALVAR
   - Produtos com que trabalha mais → SALVAR

3. **Padrões de comportamento observados**
   - Sempre pergunta sobre Atacadão primeiro → SALVAR
   - Prefere ver estoque antes de criar separação → SALVAR
   - Costuma verificar palmito frequentemente → SALVAR

4. **Correções e esclarecimentos**
   - "Não é assim que funciona aqui" → SALVAR a regra correta
   - "Esse campo se chama X, não Y" → SALVAR correção
   - "Aqui usamos o termo Z" → SALVAR terminologia

5. **Decisões tomadas**
   - "Atacadão 183 sempre fica por último" → SALVAR regra
   - "FOB sempre manda completo" → SALVAR (se não estiver no CLAUDE.md)

### Quando ATUALIZAR memórias:

1. **Informação mudou**
   - "Agora sou gerente" (antes era analista) → ATUALIZAR
   - "Mudamos o processo" → ATUALIZAR

2. **Preferência mudou**
   - "Agora pode usar emojis" → ATUALIZAR

---

## USO REATIVO (Quando usuário pede)

- Usuário pede para lembrar algo: "Lembre que prefiro respostas diretas"
- Usuário pergunta o que Claude sabe: "O que você sabe sobre mim?"
- Usuário quer apagar memórias: "Esqueça minhas preferências"

---

## Scripts Disponíveis

### Ver Memórias

```bash
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py view --user-id USER_ID
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py view --user-id USER_ID --path /memories/preferences.xml
```

### Salvar Memória

```bash
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py save --user-id USER_ID --path /memories/preferences.xml --content "<preferences>...</preferences>"
```

### Atualizar Memória (substituir texto)

```bash
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py update --user-id USER_ID --path /memories/preferences.xml --old "texto antigo" --new "texto novo"
```

### Deletar Memória

```bash
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py delete --user-id USER_ID --path /memories/preferences.xml
```

### Limpar Todas as Memórias

```bash
source .venv/bin/activate && python .claude/skills/memoria-usuario/scripts/memoria.py clear --user-id USER_ID
```

---

## Estrutura de Paths Recomendada

```
/memories/
├── user.xml              # Informações básicas do usuário
├── preferences.xml       # Preferências de comunicação
├── context/
│   ├── company.xml       # Informações da empresa
│   ├── role.xml          # Cargo/responsabilidades
│   └── clients.xml       # Clientes que gerencia
├── learned/
│   ├── terms.xml         # Termos específicos aprendidos
│   ├── rules.xml         # Regras de negócio aprendidas
│   └── patterns.xml      # Padrões observados
└── corrections/
    └── mistakes.xml      # Correções de erros comuns
```

---

## Formato XML Recomendado

```xml
<!-- /memories/user.xml -->
<user>
    <name>Rafael</name>
    <role>Dono da empresa</role>
    <updated_at>2024-12-09</updated_at>
</user>

<!-- /memories/preferences.xml -->
<preferences>
    <communication>direto e objetivo</communication>
    <detail_level>alto quando pedido</detail_level>
    <language>portugues brasileiro</language>
    <emojis>permitido</emojis>
    <updated_at>2024-12-09</updated_at>
</preferences>

<!-- /memories/context/clients.xml -->
<clients>
    <managed>
        <client name="Atacadao" priority="P4" gestor="Junior"/>
        <client name="Assai" priority="P5" gestor="Junior/Miler"/>
    </managed>
    <frequent_queries>palmito, azeitona verde</frequent_queries>
</clients>

<!-- /memories/learned/patterns.xml -->
<patterns>
    <pattern type="workflow">
        <description>Usuario sempre verifica estoque antes de criar separacao</description>
        <learned_at>2024-12-09</learned_at>
    </pattern>
    <pattern type="preference">
        <description>Prefere ver disponibilidade por grupo antes de pedido individual</description>
        <learned_at>2024-12-09</learned_at>
    </pattern>
</patterns>

<!-- /memories/corrections/mistakes.xml -->
<corrections>
    <correction>
        <wrong>data_agendamento_pedido</wrong>
        <right>agendamento (campo da Separacao, nao da Carteira)</right>
        <learned_at>2024-12-09</learned_at>
    </correction>
</corrections>
```

---

## Fluxo de Uso Proativo

```
INÍCIO DA SESSÃO
      │
      ▼
┌─────────────────────────────┐
│ Verificar memórias do user  │
│ view --user-id X            │
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ Há memórias?                │
│ SIM → Carregar e adaptar    │
│ NAO → Comportamento padrão  │
└─────────────────────────────┘
      │
      ▼
DURANTE A CONVERSA
      │
      ▼
┌─────────────────────────────┐
│ Usuário disse algo novo?    │
│ - Preferência → SALVAR      │
│ - Fato pessoal → SALVAR     │
│ - Correção → SALVAR         │
│ - Padrão observado → SALVAR │
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ Informação mudou?           │
│ SIM → ATUALIZAR memória     │
└─────────────────────────────┘
```

---

## Importante

- Memórias são isoladas por usuário (user_id)
- Persistem entre sessões diferentes
- NÃO armazene histórico de conversas (já é feito automaticamente)
- Use para FATOS, PREFERÊNCIAS e PADRÕES
- Sempre inclua `updated_at` ou `learned_at` para rastreabilidade
- Pergunte ao usuário se não tiver user_id definido

---

## Exemplos de Uso Proativo

### Cenário 1: Início de sessão
```
Usuário: "Olá, preciso analisar a carteira"

Claude (internamente):
1. Verificar memórias do usuário
2. Encontra: preferência por respostas diretas
3. Encontra: costuma focar em Atacadão primeiro
4. Adapta resposta para ser direta e começar por Atacadão
```

### Cenário 2: Aprendendo preferência
```
Usuário: "Pode ser mais resumido? Não precisa de tanto detalhe"

Claude:
1. Entende preferência
2. SALVA em /memories/preferences.xml
3. Adapta resposta atual
4. Lembra nas próximas sessões
```

### Cenário 3: Aprendendo padrão
```
(Claude observa que usuário SEMPRE pergunta sobre palmito primeiro)

Claude (internamente):
1. Detecta padrão após 3+ ocorrências
2. SALVA em /memories/learned/patterns.xml
3. Nas próximas sessões, pode sugerir proativamente
```
