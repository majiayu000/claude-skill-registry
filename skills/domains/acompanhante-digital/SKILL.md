---
name: acompanhante-digital
description: Modo acompanhante para agentes comunitários e familiares
---

Interface simplificada para agente comunitário ou familiar ajudar o cidadão a navegar a plataforma.

## Contexto

- 32,6% dos domicílios desconectados não têm ninguém que saiba usar internet
- 28 milhões de brasileiros não usam a internet
- Barreira é educacional, não só de infraestrutura
- Agentes comunitários de saúde (ACS) e assistentes sociais visitam famílias
- Familiar mais jovem frequentemente ajuda o mais velho

## Perfis de Acompanhante

### 1. Agente Comunitário de Saúde (ACS)
```
Contexto: Visita domiciliar, cadastra famílias, identifica vulnerabilidades
Permissões: Consultar benefícios, preencher formulários, gerar checklists
Restrições: Não acessa dados financeiros, não altera cadastro
```

### 2. Assistente Social (CRAS)
```
Contexto: Atendimento presencial no CRAS, pré-triagem, encaminhamento
Permissões: Consulta completa, pré-atendimento, carta de encaminhamento
Restrições: Não realiza cadastro (usa sistema próprio CadÚnico)
```

### 3. Familiar / Vizinho
```
Contexto: Ajuda informalmente pessoa com baixo letramento digital
Permissões: Navegação assistida, leitura de resultados
Restrições: Não vê CPF completo, não acessa dados sensíveis
```

## Interface do Modo Acompanhante

### Ativação
```tsx
// frontend/src/components/ModoAcompanhante.tsx
export function ModoAcompanhante() {
  const [ativo, setAtivo] = useState(false);
  const [perfil, setPerfil] = useState<PerfilAcompanhante | null>(null);

  return (
    <div>
      <button onClick={() => setAtivo(true)}>
        Estou ajudando alguém
      </button>

      {ativo && (
        <div className="bg-blue-50 p-4 rounded-lg">
          <h2 className="text-lg font-bold">Modo Acompanhante</h2>
          <p>Quem é você?</p>
          <div className="flex gap-2 mt-2">
            <button onClick={() => setPerfil('acs')}>
              Agente de Saúde
            </button>
            <button onClick={() => setPerfil('assistente')}>
              Assistente Social
            </button>
            <button onClick={() => setPerfil('familiar')}>
              Familiar / Amigo
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
```

### Tela Lado a Lado
```tsx
// frontend/src/components/TelaAssistida.tsx
export function TelaAssistida({ perfil }: { perfil: PerfilAcompanhante }) {
  return (
    <div className="grid grid-cols-1 gap-4">
      {/* Instruções para o acompanhante (menor, topo) */}
      <div className="bg-gray-100 p-3 rounded text-sm">
        <span className="font-bold">Para você (acompanhante):</span>
        <p>{instrucaoAtual}</p>
      </div>

      {/* Conteúdo para o cidadão (maior, centro) */}
      <div className="text-xl leading-relaxed p-4">
        {/* Texto grande, linguagem simples, botões grandes */}
        {conteudoCidadao}
      </div>

      {/* Ações rápidas do acompanhante (bottom bar) */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-2 flex gap-2">
        <button className="flex-1 py-3 bg-orange-500 text-white rounded">
          Próximo passo
        </button>
        <button className="flex-1 py-3 bg-gray-200 rounded">
          Ler em voz alta
        </button>
        <button className="py-3 px-4 bg-red-100 rounded">
          Ajuda
        </button>
      </div>
    </div>
  );
}
```

## Funcionalidades

### 1. Leitura em Voz Alta (Text-to-Speech)
```typescript
// frontend/src/services/tts-service.ts
export function lerEmVozAlta(texto: string, velocidade: number = 0.8) {
  const utterance = new SpeechSynthesisUtterance(texto);
  utterance.lang = 'pt-BR';
  utterance.rate = velocidade;  // mais lento para compreensão
  utterance.pitch = 1.0;
  speechSynthesis.speak(utterance);
}
```

### 2. Passo a Passo Guiado
```typescript
// frontend/src/components/PassoAPasso.tsx
const PASSOS_CONSULTA_BENEFICIO = [
  {
    instrucaoAcompanhante: "Peça o CPF da pessoa. Pode digitar você.",
    textoCidadao: "Vou precisar do seu CPF para ver seus benefícios.",
    campo: "cpf",
    dica: "São 11 números. Está no RG ou no cartão do CadÚnico.",
  },
  {
    instrucaoAcompanhante: "Confirme o nome que apareceu na tela.",
    textoCidadao: "Seu nome é {{nome}}? Está certo?",
    confirmacao: true,
  },
  {
    instrucaoAcompanhante: "Mostre os benefícios na tela. Leia cada um.",
    textoCidadao: "Esses são os benefícios que você tem ou pode ter:",
    componente: "ListaBeneficios",
  },
];
```

### 3. Registro de Atendimento
```python
# backend/app/models/atendimento.py
class Atendimento(Base):
    __tablename__ = "atendimentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_acompanhante: Mapped[str]  # acs, assistente, familiar
    cpf_cidadao_hash: Mapped[str]   # hash, nunca texto plano
    acoes_realizadas: Mapped[list]   # ["consulta_beneficio", "checklist"]
    timestamp: Mapped[datetime]
    municipio: Mapped[str]
    resultado: Mapped[str]           # "encaminhado_cras", "beneficio_encontrado"
```

### 4. Checklist Pré-Visita ao CRAS
```python
# backend/app/agent/tools/pre_visita_cras.py
async def gerar_checklist_pre_visita(
    beneficio: str,
    composicao_familiar: dict,
) -> dict:
    """
    Gera checklist personalizado para o cidadão levar ao CRAS.
    Acompanhante pode imprimir ou salvar no celular.
    """
    documentos = await gerar_checklist(beneficio)

    return {
        "titulo": f"O que levar ao CRAS para pedir {beneficio}",
        "documentos": documentos,
        "dicas": [
            "Leve documentos de TODOS que moram na casa",
            "Originais E cópias",
            "Se não tiver algum documento, vá assim mesmo",
            "Chegue cedo — costuma ter fila",
        ],
        "cras_proximo": await buscar_cras_proximo(),
        "pode_imprimir": True,
    }
```

## Adaptações de Interface

### Fonte Grande
```css
/* frontend/src/styles/modo-acompanhante.css */
.modo-acompanhante {
  --font-size-base: 1.25rem;   /* 20px */
  --font-size-heading: 1.75rem; /* 28px */
  --button-min-height: 56px;    /* área de toque grande */
  --button-font-size: 1.125rem; /* 18px */
  --line-height: 1.8;           /* espaçamento generoso */
}

.modo-acompanhante button {
  min-height: var(--button-min-height);
  font-size: var(--button-font-size);
  padding: 12px 24px;
  border-radius: 12px;
}
```

### Contraste Alto
```css
.modo-acompanhante.alto-contraste {
  --text-color: #000000;
  --bg-color: #FFFFFF;
  --accent-color: #0047AB;     /* azul escuro */
  --button-bg: #F99500;
  --button-text: #000000;
}
```

## Métricas de Uso
```python
# Dados anonimizados para melhorar o produto
METRICAS_ACOMPANHANTE = {
    "atendimentos_por_perfil": {},       # acs: 45%, familiar: 40%, assistente: 15%
    "funcoes_mais_usadas": [],            # consulta, checklist, cras
    "tempo_medio_atendimento": 0,
    "taxa_sucesso": 0,                    # % que encontrou benefício
    "municipios_mais_ativos": [],
}
```

## Arquivos Relacionados
- `frontend/src/components/ModoAcompanhante.tsx` - Componente principal
- `frontend/src/components/TelaAssistida.tsx` - Interface lado a lado
- `frontend/src/components/PassoAPasso.tsx` - Wizard guiado
- `frontend/src/services/tts-service.ts` - Text-to-speech
- `frontend/src/styles/modo-acompanhante.css` - Estilos acessíveis
- `backend/app/models/atendimento.py` - Modelo de atendimento
- `backend/app/agent/tools/pre_visita_cras.py` - Checklist pré-visita

## Checklist
- [ ] Botão "Estou ajudando alguém" na tela inicial
- [ ] 3 perfis de acompanhante (ACS, assistente, familiar)
- [ ] Instruções separadas para acompanhante vs. cidadão
- [ ] Text-to-speech integrado
- [ ] Fontes grandes + contraste alto
- [ ] Botões com área de toque mínima 56px
- [ ] Passo a passo guiado para consulta
- [ ] Checklist pré-visita CRAS imprimível
- [ ] Registro de atendimento (anonimizado)
- [ ] Testar com agentes comunitários reais
