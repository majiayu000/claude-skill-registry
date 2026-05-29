---
name: educacao-financeira
description: Micro-lições financeiras e alerta de golpes
---

Micro-lições financeiras em linguagem de 5ª série, simuladores de orçamento e alertas contra golpes.

## Contexto

- População vulnerável é alvo preferencial de golpes (PIX falso, consignado abusivo)
- Endividamento crônico consome boa parte dos benefícios recebidos
- Educação financeira previne ciclo de pobreza
- Microcrédito produtivo pode alavancar renda

## Módulos

### 1. Orçamento Familiar Simples
```
"Para onde vai meu dinheiro?"

ENTRA:
  Bolsa Família ......... R$ {{valor_bf}}
  Trabalho .............. R$ {{renda_trabalho}}
  Outros ................ R$ {{outros}}
  TOTAL ................. R$ {{total_entrada}}

SAI:
  Aluguel / Moradia ..... R$ ___
  Comida ................ R$ ___
  Luz ................... R$ ___
  Água .................. R$ ___
  Gás ................... R$ ___
  Remédio ............... R$ ___
  Transporte ............ R$ ___
  Escola ................ R$ ___
  Celular ............... R$ ___
  TOTAL ................. R$ ___

SOBRA / FALTA: R$ ___
```

### 2. Alerta de Golpes
```python
# backend/app/agent/tools/alerta_golpes.py
GOLPES_COMUNS = [
    {
        "nome": "PIX falso do governo",
        "como_funciona": "Mandam mensagem dizendo que você tem dinheiro pra receber. Pedem pra clicar num link e colocar seus dados.",
        "como_evitar": "O governo NUNCA pede dados por WhatsApp ou SMS. Não clique em links. Consulte pelo app Caixa Tem ou vá ao CRAS.",
        "palavras_chave": ["pix", "link", "clique", "liberar", "saque"],
    },
    {
        "nome": "Empréstimo consignado abusivo",
        "como_funciona": "Oferecem empréstimo fácil pelo telefone. Descontam direto do benefício. Juros altíssimos.",
        "como_evitar": "NUNCA aceite empréstimo por telefone. Se precisar, vá pessoalmente ao banco. Compare juros.",
        "palavras_chave": ["empréstimo", "consignado", "liberado", "aprovado"],
    },
    {
        "nome": "Falso cadastro de benefício",
        "como_funciona": "Cobram pra 'dar entrada' no Bolsa Família ou BPC. O cadastro é GRATUITO.",
        "como_evitar": "Cadastro no CadÚnico é de GRAÇA no CRAS. Ninguém pode cobrar por isso.",
        "palavras_chave": ["cadastro", "taxa", "pagar", "garantido"],
    },
    {
        "nome": "Pirâmide financeira",
        "como_funciona": "Prometem multiplicar seu dinheiro se você investir e chamar mais pessoas.",
        "como_evitar": "Se parece bom demais pra ser verdade, é golpe. Ninguém multiplica dinheiro do nada.",
        "palavras_chave": ["investimento", "rendimento", "multiplicar", "indicar"],
    },
]

async def verificar_golpe(mensagem: str) -> dict | None:
    """Detecta se o usuário está descrevendo um possível golpe."""
    msg_lower = mensagem.lower()
    for golpe in GOLPES_COMUNS:
        matches = sum(1 for p in golpe["palavras_chave"] if p in msg_lower)
        if matches >= 2:
            return {
                "alerta": True,
                "golpe": golpe["nome"],
                "explicacao": golpe["como_funciona"],
                "protecao": golpe["como_evitar"],
            }
    return None
```

### 3. Micro-lições (Carrossel)
```json
[
  {
    "titulo": "Dívida boa vs. dívida ruim",
    "texto": "Dívida boa é quando você pega empréstimo pra algo que vai te dar retorno, como uma máquina de costura pro trabalho. Dívida ruim é quando compra coisa que não precisa e paga juros altos.",
    "dica": "Antes de comprar parcelado, pergunte: eu PRECISO disso?"
  },
  {
    "titulo": "Reserva de emergência",
    "texto": "Tente guardar um pouquinho todo mês. Mesmo R$10 por mês já ajuda. Em 1 ano são R$120 pra uma emergência.",
    "dica": "Guarde ANTES de gastar, não o que sobrar."
  },
  {
    "titulo": "Cuidado com o parcelamento",
    "texto": "Parcelado em 12x de R$50 parece pouco. Mas são R$600 no total. Será que vale? Sempre veja o preço à vista.",
    "dica": "Se não pode pagar à vista, talvez não possa pagar parcelado."
  },
  {
    "titulo": "Seus direitos como consumidor",
    "texto": "Comprou e não gostou? Compra pela internet tem 7 dias pra devolver. Produto com defeito: a loja TEM que trocar.",
    "dica": "Guarde sempre a nota fiscal e o comprovante."
  }
]
```

### 4. Guia de Microcrédito
```
Opções de crédito acessível:

📋 CrediAmigo (Banco do Nordeste)
  - Para: pequenos negócios no Nordeste
  - Valor: R$100 a R$21.000
  - Juros: a partir de 1,6% ao mês
  - Não precisa de garantia

📋 Agroamigo (Banco do Nordeste)
  - Para: agricultores familiares
  - Valor: até R$20.000
  - Juros: a partir de 0,5% ao mês (Pronaf B)

📋 PRONAF (qualquer banco)
  - Para: agricultura familiar
  - Valor: varia por linha
  - Juros: mais baixos do mercado

📋 Programa Nacional de Microcrédito
  - Para: MEI e informais
  - Valor: até R$21.000
  - Onde: bancos públicos e cooperativas

⚠️ NUNCA pegue empréstimo de agiota. É crime e os juros são abusivos.
```

## Implementação no Agente
```python
# Integrar no fluxo do agente
async def handle_educacao_financeira(mensagem: str, session: Session):
    # 1. Verificar se é golpe
    golpe = await verificar_golpe(mensagem)
    if golpe:
        return format_alerta_golpe(golpe)

    # 2. Identificar tema
    if "orçamento" in mensagem or "dinheiro" in mensagem:
        return await gerar_orcamento_interativo(session)
    elif "empréstimo" in mensagem or "crédito" in mensagem:
        return format_guia_microcredito()
    elif "dica" in mensagem or "aprender" in mensagem:
        return await proxima_micro_licao(session)
```

## Arquivos Relacionados
- `backend/app/agent/tools/alerta_golpes.py` - Detector de golpes
- `backend/app/agent/tools/orcamento_familiar.py` - Simulador de orçamento
- `frontend/src/data/educacao-financeira/` - Conteúdo das micro-lições
- `frontend/src/components/OrcamentoSimples.tsx` - Componente de orçamento

## Fontes
- Banco Central (Cidadania Financeira): https://www.bcb.gov.br/cidadaniafinanceira
- PROCON: https://www.procon.sp.gov.br
- CrediAmigo: https://www.bnb.gov.br/crediamigo
- PRONAF: https://www.gov.br/agricultura/pt-br/assuntos/pronaf
