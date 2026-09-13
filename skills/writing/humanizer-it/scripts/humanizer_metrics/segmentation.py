"""Segmentazione frasi/parole senza dipendenze (sostituisce razdel del RU).

Per le metriche di ritmo (lunghezza delle frasi, burstiness) la tokenizzazione
è abbastanza indipendente dalla lingua: basta spezzare sulla punteggiatura
forte. Niente modelli, niente install — funziona col solo Python stdlib, così
lo scanner gira ovunque.
"""

from __future__ import annotations

import re

# Confine di frase: punteggiatura forte seguita da spazio (o fine testo).
# Niente gestione fine delle abbreviazioni (sig., ecc.): per la dispersione
# delle lunghezze il rumore residuo è trascurabile.
_SENT_SPLIT = re.compile(r"(?<=[.!?…])[\s ]+")

# Parola: lettere (con accentate) o cifre, con apostrofo interno (l'IA, dell').
_WORD_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+(?:['’][A-Za-zÀ-ÿ0-9]+)?")


def sentenize(text: str) -> list[str]:
    """Lista di frasi non vuote."""
    return [s for s in (part.strip() for part in _SENT_SPLIT.split(text)) if s]


def word_count(text: str) -> int:
    """Numero di token-parola in un frammento."""
    return len(_WORD_RE.findall(text))
