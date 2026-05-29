---
name: voz-acessivel
description: Interface por voz (speech-to-text + text-to-speech)
---

Speech-to-text e text-to-speech para navegação sem digitação, removendo a barreira do analfabetismo funcional.

## Contexto

- Analfabetismo funcional atinge ~30% da população adulta brasileira
- Muitos sabem falar mas não sabem ler/escrever bem
- Voz remove barreira de letramento digital
- Web Speech API é suportada nos navegadores modernos (Chrome, Edge, Safari)

## Arquitetura

```
Cidadão fala → Speech-to-Text → Texto → Agente → Resposta → Text-to-Speech → Cidadão ouve
```

## Speech-to-Text (Ouvir o Cidadão)

### Web Speech API
```typescript
// frontend/src/services/speech-to-text.ts
export class SpeechToTextService {
  private recognition: SpeechRecognition | null = null;
  private isSupported: boolean;

  constructor() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.isSupported = !!SpeechRecognition;

    if (this.isSupported) {
      this.recognition = new SpeechRecognition();
      this.recognition.lang = 'pt-BR';
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.maxAlternatives = 3;
    }
  }

  async ouvir(): Promise<string> {
    if (!this.isSupported || !this.recognition) {
      throw new Error('Reconhecimento de voz não suportado neste navegador');
    }

    return new Promise((resolve, reject) => {
      this.recognition!.onresult = (event) => {
        const resultado = event.results[event.results.length - 1];
        if (resultado.isFinal) {
          resolve(resultado[0].transcript);
        }
      };

      this.recognition!.onerror = (event) => {
        if (event.error === 'no-speech') {
          reject(new Error('Não ouvi nada. Tente de novo.'));
        } else if (event.error === 'not-allowed') {
          reject(new Error('Preciso de permissão para usar o microfone.'));
        } else {
          reject(new Error('Não entendi. Pode repetir?'));
        }
      };

      this.recognition!.start();
    });
  }

  parar() {
    this.recognition?.stop();
  }
}
```

### Componente de Microfone
```tsx
// frontend/src/components/BotaoVoz.tsx
import { useState } from 'react';

export function BotaoVoz({ onTexto }: { onTexto: (texto: string) => void }) {
  const [ouvindo, setOuvindo] = useState(false);
  const [textoTemporario, setTextoTemporario] = useState('');
  const stt = useMemo(() => new SpeechToTextService(), []);

  const handleClick = async () => {
    if (ouvindo) {
      stt.parar();
      setOuvindo(false);
      return;
    }

    setOuvindo(true);
    try {
      const texto = await stt.ouvir();
      onTexto(texto);
    } catch (error) {
      // Mostrar mensagem de erro ao usuário
    } finally {
      setOuvindo(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      className={`
        w-16 h-16 rounded-full flex items-center justify-center
        ${ouvindo ? 'bg-red-500 animate-pulse' : 'bg-orange-500'}
        text-white text-2xl
      `}
      aria-label={ouvindo ? 'Parar de ouvir' : 'Falar'}
    >
      {ouvindo ? '⏹' : '🎙'}
    </button>
  );
}
```

## Text-to-Speech (Falar para o Cidadão)

### Serviço TTS
```typescript
// frontend/src/services/text-to-speech.ts
export class TextToSpeechService {
  private synth: SpeechSynthesis;
  private voz: SpeechSynthesisVoice | null = null;

  constructor() {
    this.synth = window.speechSynthesis;
    this.selecionarVozBrasileira();
  }

  private selecionarVozBrasileira() {
    // Esperar vozes carregarem
    const carregar = () => {
      const vozes = this.synth.getVoices();
      this.voz = vozes.find(v => v.lang === 'pt-BR')
        || vozes.find(v => v.lang.startsWith('pt'))
        || vozes[0];
    };

    if (this.synth.getVoices().length > 0) {
      carregar();
    } else {
      this.synth.onvoiceschanged = carregar;
    }
  }

  falar(texto: string, velocidade: number = 0.85) {
    // Cancelar fala anterior
    this.synth.cancel();

    const utterance = new SpeechSynthesisUtterance(texto);
    utterance.voice = this.voz;
    utterance.lang = 'pt-BR';
    utterance.rate = velocidade;    // mais lento para compreensão
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    this.synth.speak(utterance);
  }

  parar() {
    this.synth.cancel();
  }

  get falando(): boolean {
    return this.synth.speaking;
  }
}
```

### Botão "Ouvir Resposta"
```tsx
// frontend/src/components/BotaoOuvir.tsx
export function BotaoOuvir({ texto }: { texto: string }) {
  const [falando, setFalando] = useState(false);
  const tts = useMemo(() => new TextToSpeechService(), []);

  return (
    <button
      onClick={() => {
        if (falando) {
          tts.parar();
          setFalando(false);
        } else {
          tts.falar(texto);
          setFalando(true);
        }
      }}
      className="flex items-center gap-2 text-sm text-blue-600 underline"
      aria-label={falando ? 'Parar de ler' : 'Ouvir em voz alta'}
    >
      {falando ? '⏹ Parar' : '🔊 Ouvir'}
    </button>
  );
}
```

## Comandos de Voz

### Mapeamento de Intenções
```typescript
// frontend/src/services/comandos-voz.ts
const COMANDOS_VOZ: Record<string, { padrao: RegExp; acao: string }> = {
  consultar_beneficio: {
    padrao: /(?:quero|ver|consultar|saber)\s+(?:meus?\s+)?benef[ií]cios?/i,
    acao: 'navegar:/descobrir',
  },
  buscar_cras: {
    padrao: /(?:onde|achar|buscar|encontrar)\s+(?:o\s+)?cras/i,
    acao: 'tool:buscar_cras',
  },
  documentos: {
    padrao: /(?:que|quais)\s+documentos?\s+(?:preciso|levo|levar)/i,
    acao: 'tool:gerar_checklist',
  },
  dinheiro_esquecido: {
    padrao: /dinheiro\s+esquecido|pis|pasep|fgts/i,
    acao: 'tool:consultar_dinheiro_esquecido',
  },
  farmacia: {
    padrao: /farm[aá]cia|rem[eé]dio|medicamento/i,
    acao: 'tool:buscar_farmacia',
  },
  emergencia: {
    padrao: /emerg[eê]ncia|socorro|ajuda\s+urgente|viol[eê]ncia/i,
    acao: 'tool:rede_protecao',
  },
  voltar: {
    padrao: /voltar|menu|in[ií]cio|come[çc]o/i,
    acao: 'navegar:/',
  },
};

export function identificarComando(texto: string): { acao: string } | null {
  for (const [, comando] of Object.entries(COMANDOS_VOZ)) {
    if (comando.padrao.test(texto)) {
      return { acao: comando.acao };
    }
  }
  // Se não é comando, enviar como mensagem livre ao agente
  return { acao: `mensagem:${texto}` };
}
```

## Fallback para Texto
```tsx
// Se reconhecimento de voz não é suportado ou falha
export function InputComVoz({ onEnviar }: { onEnviar: (texto: string) => void }) {
  const sttSuportado = useMemo(() => {
    return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  }, []);

  return (
    <div className="flex gap-2">
      <input
        type="text"
        placeholder="Digite ou fale..."
        className="flex-1 p-3 border rounded-lg text-lg"
        onKeyDown={(e) => {
          if (e.key === 'Enter') onEnviar(e.currentTarget.value);
        }}
      />
      {sttSuportado && <BotaoVoz onTexto={onEnviar} />}
    </div>
  );
}
```

## Compatibilidade
| Navegador | STT | TTS | Notas |
|-----------|-----|-----|-------|
| Chrome (Android) | Sim | Sim | Melhor suporte |
| Chrome (Desktop) | Sim | Sim | Requer HTTPS |
| Safari (iOS) | Sim | Sim | Requer interação do usuário |
| Firefox | Não | Sim | STT não suportado |
| Samsung Internet | Sim | Sim | Funciona bem |

## Arquivos Relacionados
- `frontend/src/services/speech-to-text.ts` - Reconhecimento de voz
- `frontend/src/services/text-to-speech.ts` - Síntese de voz
- `frontend/src/services/comandos-voz.ts` - Mapeamento de comandos
- `frontend/src/components/BotaoVoz.tsx` - Botão de microfone
- `frontend/src/components/BotaoOuvir.tsx` - Botão ouvir resposta
- `frontend/src/components/InputComVoz.tsx` - Input com fallback

## Checklist
- [ ] Web Speech API detectada (feature detection)
- [ ] Fallback para texto quando voz não suportada
- [ ] Botão de microfone com feedback visual (animação)
- [ ] Voz brasileira (pt-BR) selecionada no TTS
- [ ] Velocidade de fala reduzida (0.85x) para compreensão
- [ ] Comandos de voz mapeados para ações do app
- [ ] Permissão de microfone solicitada com explicação clara
- [ ] Funciona em HTTPS (requisito do Chrome)
