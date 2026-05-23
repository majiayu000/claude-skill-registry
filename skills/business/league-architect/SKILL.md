---
name: league-architect
description: Especialista em Regras de Negócio, Formatos de Liga SaaS, Lógica Financeira e Disputas do Super Cartola. Guardião das regras oficiais, fórmulas de cálculo, premiações e punições. Use para criar/ajustar configs de liga, calcular finanças, definir regras de disputas ou validar implementações de negócio.
---

# League Architect Skill

## 🎯 Missão
Garantir precisão absoluta nas regras de negócio e cálculos financeiros do Super Cartola Manager.

---

## 1. 📊 Regras Financeiras Críticas

### 1.1 Precisão Decimal

```javascript
// OBRIGATÓRIO: Truncar em 2 casas decimais
function formatarValor(valor) {
  return Number(valor.toFixed(2));
}

// UI: Vírgula brasileira
function formatarParaUI(valor) {
  return valor.toFixed(2).replace('.', ',');
}

// Exemplos
formatarValor(105.4045) // 105.40
formatarParaUI(105.40)  // "105,40"
```

### 1.2 Mitos & Micos da Rodada

```javascript
const BONUS_RODADA = {
  mito: {
    valor: 20.00,
    descricao: '1º lugar da rodada',
    posicao: 1
  },
  mico: {
    valor: -20.00,
    descricao: 'Último lugar da rodada',
    posicao: 'ultima'  // Calculado dinamicamente
  }
};

function calcularMitoMico(participantes, rodada) {
  // Ordenar por pontuação
  const sorted = participantes
    .filter(p => p.pontos_rodada > 0)  // Excluir inativos
    .sort((a, b) => b.pontos_rodada - a.pontos_rodada);
  
  if (sorted.length === 0) return [];
  
  const mito = sorted[0];
  const mico = sorted[sorted.length - 1];
  
  return [
    { participante_id: mito._id, tipo: 'mito', valor: 20.00 },
    { participante_id: mico._id, tipo: 'mico', valor: -20.00 }
  ];
}
```

### 1.3 Zonas Financeiras (Tabela 32 Times)

```javascript
const ZONAS_32_TIMES = {
  // G-Zones (Premiação)
  G1:  { min: 1,  max: 1,  valor: 100.00, descricao: 'Campeão/Mito' },
  G2:  { min: 2,  max: 2,  valor: 60.00,  descricao: 'Vice' },
  G3:  { min: 3,  max: 3,  valor: 40.00,  descricao: '3º Lugar' },
  G4:  { min: 4,  max: 6,  valor: 20.00,  descricao: 'Top 6' },
  G5:  { min: 7,  max: 9,  valor: 10.00,  descricao: 'Top 9' },
  G6:  { min: 10, max: 11, valor: 5.00,   descricao: 'Top 11' },
  
  // Zona Neutra
  NEUTRO: { min: 12, max: 21, valor: 0, descricao: 'Zona Neutra' },
  
  // Z-Zones (Punição)
  Z1:  { min: 22, max: 22, valor: -5.00,   descricao: 'Z1' },
  Z2:  { min: 23, max: 24, valor: -10.00,  descricao: 'Z2-Z3' },
  Z3:  { min: 25, max: 27, valor: -20.00,  descricao: 'Z4-Z6' },
  Z4:  { min: 28, max: 30, valor: -40.00,  descricao: 'Z7-Z9' },
  Z5:  { min: 31, max: 31, valor: -60.00,  descricao: 'Penúltimo' },
  Z6:  { min: 32, max: 32, valor: -100.00, descricao: 'Lanterna/Mico' }
};

function calcularPremiacaoPosicao(posicao, totalParticipantes) {
  // Validar tabela correta
  if (totalParticipantes !== 32) {
    console.warn('Tabela de 32 times aplicada a liga com', totalParticipantes);
  }
  
  // Buscar zona
  for (const [zona, config] of Object.entries(ZONAS_32_TIMES)) {
    if (posicao >= config.min && posicao <= config.max) {
      return {
        zona,
        valor: config.valor,
        descricao: config.descricao
      };
    }
  }
  
  return { zona: 'NEUTRO', valor: 0, descricao: 'Fora da tabela' };
}
```

### 1.4 Acertos Financeiros (CRÍTICO)

```javascript
/**
 * FÓRMULA OFICIAL:
 * saldoAcertos = totalPagamentos - totalRecebimentos
 * 
 * - PAGAMENTO: Participante PAGOU à liga → AUMENTA saldo (quita dívida)
 * - RECEBIMENTO: Participante RECEBEU da liga → DIMINUI saldo (usa crédito)
 */

function calcularSaldoAcertos(participanteId, ligaId, temporada) {
  const acertos = await AcertoFinanceiro.find({
    participante_id: participanteId,
    liga_id: ligaId,
    temporada
  });
  
  let totalPagamentos = 0;
  let totalRecebimentos = 0;
  
  acertos.forEach(acerto => {
    if (acerto.tipo === 'pagamento') {
      totalPagamentos += acerto.valor;
    } else if (acerto.tipo === 'recebimento') {
      totalRecebimentos += acerto.valor;
    }
  });
  
  return formatarValor(totalPagamentos - totalRecebimentos);
}

// Exemplo: Devedor quitando dívida
const exemplo = {
  saldoTemporada: -203.46,   // Deve R$203,46
  pagamento: 204.00,         // Paga R$204,00
  
  // Cálculo
  saldoAcertos: 204.00 - 0,  // = +204.00
  saldoFinal: -203.46 + 204.00  // = +0.54 (troco a receber)
};
```

---

## 2. 🏆 Formatos de Liga

### 2.1 SuperCartola (32 Times)

```javascript
const LIGA_SUPERCARTOLA = {
  id: '684cb1c8af923da7c7df51de',
  nome: 'SuperCartola',
  formato: '32_times',
  temporada: '2026',
  
  config: {
    min_participantes: 32,
    max_participantes: 32,
    
    inscricao: {
      valor: 200.00,
      moeda: 'BRL'
    },
    
    disputas: [
      'pontos_corridos',
      'mata_mata',
      'artilheiro',
      'luva_de_ouro',
      'melhor_do_mes',
      'top10_mitos',
      'top10_micos'
    ],
    
    zonas: ZONAS_32_TIMES,
    
    premiacoes: {
      pontos_corridos: {
        primeiro: 1000.00,
        segundo: 500.00,
        terceiro: 300.00
      },
      mata_mata: {
        campeao: 800.00,
        vice: 400.00
      }
    }
  }
};
```

### 2.2 Cartoleiros do Sobral (Dinâmica R30+)

```javascript
const LIGA_SOBRAL = {
  id: '684d821cf1a7ae16d1f89572',
  nome: 'Cartoleiros do Sobral',
  formato: 'dinamico',
  temporada: '2026',
  
  config: {
    min_participantes: 4,
    max_participantes: 6,
    
    // REGRA R30+: A partir da rodada 30, reduz para 4 times
    regra_r30: {
      rodada_inicio: 30,
      participantes_ativos: 4,
      
      // Inativos são EXCLUÍDOS do cálculo
      excluir_inativos: true
    },
    
    zonas_variavel: {
      // Com 6 participantes (rodadas 1-29)
      6: {
        G1: { min: 1, max: 1, valor: 50.00 },
        G2: { min: 2, max: 2, valor: 20.00 },
        NEUTRO: { min: 3, max: 4, valor: 0 },
        Z1: { min: 5, max: 5, valor: -20.00 },
        Z2: { min: 6, max: 6, valor: -50.00 }
      },
      
      // Com 4 participantes (rodadas 30+)
      4: {
        G1: { min: 1, max: 1, valor: 40.00 },
        G2: { min: 2, max: 2, valor: 15.00 },
        Z1: { min: 3, max: 3, valor: -15.00 },
        Z2: { min: 4, max: 4, valor: -40.00 }
      }
    }
  }
};

function calcularPremiacaoSobral(posicao, rodada, participantes) {
  const config = LIGA_SOBRAL.config;
  
  // Determinar qual tabela usar
  const totalAtivos = rodada >= config.regra_r30.rodada_inicio
    ? config.regra_r30.participantes_ativos
    : participantes.length;
  
  const zonas = config.zonas_variavel[totalAtivos];
  
  // Buscar zona
  for (const [zona, regra] of Object.entries(zonas)) {
    if (posicao >= regra.min && posicao <= regra.max) {
      return {
        zona,
        valor: regra.valor,
        descricao: `${zona} (${totalAtivos} times)`
      };
    }
  }
  
  return { zona: 'NEUTRO', valor: 0 };
}
```

---

## 3. 🎮 Disputas Específicas

### 3.1 Pontos Corridos

```javascript
const PONTOS_CORRIDOS_CONFIG = {
  pontos_vitoria: 3,
  pontos_empate: 1,
  pontos_derrota: 0,
  
  criterios_desempate: [
    'pontos_acumulados',
    'vitorias',
    'saldo_pontos',  // Pontos marcados - sofridos
    'pontos_marcados',
    'confronto_direto'
  ]
};

function calcularClassificacaoPontosCorridos(participantes, rodadas) {
  const tabela = participantes.map(p => ({
    participante_id: p._id,
    nome: p.nome,
    pontos: 0,
    jogos: 0,
    vitorias: 0,
    empates: 0,
    derrotas: 0,
    pontos_marcados: 0,
    pontos_sofridos: 0,
    saldo: 0
  }));
  
  // Processar cada rodada
  rodadas.forEach(rodada => {
    const ranking = rodada.ranking.sort((a, b) => b.pontos - a.pontos);
    
    ranking.forEach((item, index) => {
      const participante = tabela.find(t => t.participante_id.equals(item.participante_id));
      
      participante.jogos++;
      participante.pontos_marcados += item.pontos;
      
      // Vitória se 1º lugar
      if (index === 0) {
        participante.pontos += PONTOS_CORRIDOS_CONFIG.pontos_vitoria;
        participante.vitorias++;
      }
      // Empate se mesma pontuação do anterior
      else if (item.pontos === ranking[index - 1].pontos) {
        participante.pontos += PONTOS_CORRIDOS_CONFIG.pontos_empate;
        participante.empates++;
      }
      // Derrota
      else {
        participante.derrotas++;
      }
    });
  });
  
  // Calcular saldo
  tabela.forEach(t => {
    t.pontos_sofridos = tabela
      .filter(other => !other.participante_id.equals(t.participante_id))
      .reduce((sum, other) => sum + other.pontos_marcados, 0) / (tabela.length - 1);
    
    t.saldo = t.pontos_marcados - t.pontos_sofridos;
  });
  
  // Ordenar por critérios de desempate
  return tabela.sort((a, b) => {
    if (a.pontos !== b.pontos) return b.pontos - a.pontos;
    if (a.vitorias !== b.vitorias) return b.vitorias - a.vitorias;
    if (a.saldo !== b.saldo) return b.saldo - a.saldo;
    return b.pontos_marcados - a.pontos_marcados;
  });
}
```

### 3.2 Mata-Mata

```javascript
const MATA_MATA_FASES = {
  32: ['oitavas', 'quartas', 'semi', 'final'],
  16: ['oitavas', 'quartas', 'semi', 'final'],
  8:  ['quartas', 'semi', 'final'],
  4:  ['semi', 'final']
};

function gerarChaveamentoMataMata(participantes, criterio = 'pontos_corridos') {
  const numParticipantes = participantes.length;
  const fases = MATA_MATA_FASES[numParticipantes];
  
  if (!fases) {
    throw new Error(`Número inválido de participantes: ${numParticipantes}`);
  }
  
  // Ordenar por critério
  const classificados = [...participantes].sort((a, b) => {
    return b[criterio] - a[criterio];
  });
  
  // Gerar confrontos da primeira fase
  const primeiraFase = fases[0];
  const confrontos = [];
  
  for (let i = 0; i < classificados.length / 2; i++) {
    confrontos.push({
      fase: primeiraFase,
      confronto: i + 1,
      mandante: classificados[i],
      visitante: classificados[classificados.length - 1 - i],
      data_inicio: null,
      data_fim: null
    });
  }
  
  return { fases, confrontos };
}
```

### 3.3 Top 10 (Mitos & Micos)

```javascript
/**
 * Top 10 Mitos: Ranking histórico de mitos da rodada
 * Top 10 Micos: Ranking histórico de micos da rodada
 */

function calcularTop10(tipo, rodadas) {
  const contador = {};
  
  rodadas.forEach(rodada => {
    const ranking = rodada.ranking.sort((a, b) => b.pontos - a.pontos);
    
    let vencedor;
    if (tipo === 'mitos') {
      vencedor = ranking[0];  // 1º lugar
    } else {
      vencedor = ranking[ranking.length - 1];  // Último lugar
    }
    
    if (vencedor) {
      const id = vencedor.participante_id.toString();
      contador[id] = (contador[id] || 0) + 1;
    }
  });
  
  // Converter para array e ordenar
  return Object.entries(contador)
    .map(([id, count]) => ({ participante_id: id, quantidade: count }))
    .sort((a, b) => b.quantidade - a.quantidade)
    .slice(0, 10);
}
```

---

## 4. 💰 Fluxo Financeiro Completo

```javascript
/**
 * Cálculo do saldo final de um participante
 * 
 * FÓRMULA:
 * saldoFinal = saldoRodadas + saldoDisputas + saldoAcertos
 */

async function calcularSaldoCompleto(participanteId, ligaId, temporada) {
  // 1. Saldo das rodadas (mitos, micos, posições)
  const rodadas = await Rodada.find({
    participante_id: participanteId,
    liga_id: ligaId,
    temporada
  });
  
  const saldoRodadas = rodadas.reduce((sum, r) => {
    return sum + (r.ganho_rodada || 0);
  }, 0);
  
  // 2. Saldo das disputas (PC, MM, Top10, etc)
  const premiacoes = await Premiacao.find({
    participante_id: participanteId,
    liga_id: ligaId,
    temporada
  });
  
  const saldoDisputas = premiacoes.reduce((sum, p) => {
    return sum + (p.valor || 0);
  }, 0);
  
  // 3. Acertos financeiros (pagamentos/recebimentos)
  const saldoAcertos = await calcularSaldoAcertos(
    participanteId,
    ligaId,
    temporada
  );
  
  // 4. Somar tudo
  const saldoTotal = formatarValor(
    saldoRodadas + saldoDisputas + saldoAcertos
  );
  
  return {
    saldoRodadas: formatarValor(saldoRodadas),
    saldoDisputas: formatarValor(saldoDisputas),
    saldoAcertos: formatarValor(saldoAcertos),
    saldoTotal,
    
    // Breakdown detalhado
    breakdown: {
      rodadas: rodadas.map(r => ({
        rodada: r.rodada_num,
        ganho: r.ganho_rodada
      })),
      disputas: premiacoes.map(p => ({
        disputa: p.disputa,
        valor: p.valor
      })),
      acertos: await AcertoFinanceiro.find({
        participante_id: participanteId,
        liga_id: ligaId,
        temporada
      }).select('tipo valor descricao data')
    }
  };
}
```

---

## 5. 📋 Validações de Negócio

```javascript
// Validações críticas a executar
const VALIDACOES_NEGOCIO = {
  // 1. Soma zero (o que sai de uns entra em outros)
  async validarSomaZero(ligaId, temporada) {
    const participantes = await Participante.find({ liga_id: ligaId, temporada });
    
    const somaTotal = participantes.reduce((sum, p) => {
      return sum + (p.saldo_temporada || 0);
    }, 0);
    
    const tolerance = 0.10;  // R$0,10 de tolerância por arredondamentos
    
    if (Math.abs(somaTotal) > tolerance) {
      console.error(`⚠️  Soma não é zero: R$ ${somaTotal.toFixed(2)}`);
      return false;
    }
    
    return true;
  },
  
  // 2. Todas rodadas processadas
  async validarRodadas(ligaId, temporada) {
    const config = await SystemConfig.findOne({ tipo: 'temporada' });
    const rodadaAtual = config.rodada_atual;
    
    for (let i = 1; i < rodadaAtual; i++) {
      const count = await Rodada.countDocuments({
        liga_id: ligaId,
        temporada,
        rodada_num: i
      });
      
      if (count === 0) {
        console.error(`⚠️  Rodada ${i} não processada`);
        return false;
      }
    }
    
    return true;
  },
  
  // 3. Posições únicas
  async validarPosicoes(ligaId, temporada, rodada) {
    const rodadas = await Rodada.find({
      liga_id: ligaId,
      temporada,
      rodada_num: rodada
    });
    
    const posicoes = rodadas.map(r => r.posicao);
    const uniquePosicoes = new Set(posicoes);
    
    if (posicoes.length !== uniquePosicoes.size) {
      console.error(`⚠️  Posições duplicadas na rodada ${rodada}`);
      return false;
    }
    
    return true;
  }
};
```

---

**STATUS:** ⚖️ League Architect - LAWS ENFORCED

**Versão:** 2.0

**Última atualização:** 2026-01-17
