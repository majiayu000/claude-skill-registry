# /// script
# requires-python = ">=3.10"
# ///
"""Pronounce Minoan transliterations in IPA.

Usage:
    uv run pronounce.py "ya-ta-nu ku-pa-nu"
    uv run pronounce.py "Rabbatu Atiratu Yammi" --stress
"""

import sys
import re

CONSONANT_IPA = {
    "p": "p", "b": "b", "t": "t", "d": "d",
    "k": "k", "g": "g", "q": "q",
    "s": "s", "z": "z", "sh": "ʃ",
    "ṣ": "sˤ", "ṭ": "tˤ",
    "r": "r", "l": "l", "m": "m", "n": "n",
    "y": "j", "w": "w",
    "h": "h", "ḥ": "ħ", "kh": "ħ",
    "ʿ": "ʕ", "ʾ": "ʔ",
}

VOWEL_IPA = {
    "a": "a", "ā": "aː", "e": "e", "ē": "eː",
    "i": "i", "ī": "iː", "o": "o", "ō": "oː",
    "u": "u", "ū": "uː",
}

def tokenize(text: str) -> list[str]:
    text = text.strip().lower()
    text = text.replace("-", " ")
    return text.split()

def word_to_ipa(word: str) -> str:
    ipa = []
    i = 0
    chars = word
    while i < len(chars):
        if i + 1 < len(chars) and chars[i:i+2] in CONSONANT_IPA:
            ipa.append(CONSONANT_IPA[chars[i:i+2]])
            i += 2
        elif chars[i] in CONSONANT_IPA:
            ipa.append(CONSONANT_IPA[chars[i]])
            i += 1
        elif i + 1 < len(chars) and chars[i:i+2] in VOWEL_IPA:
            ipa.append(VOWEL_IPA[chars[i:i+2]])
            i += 2
        elif chars[i] in VOWEL_IPA:
            ipa.append(VOWEL_IPA[chars[i]])
            i += 1
        else:
            ipa.append(chars[i])
            i += 1
    return "".join(ipa)

def add_stress(ipa_word: str) -> str:
    vowels = [m for m in re.finditer(r"[aeiou]ː?", ipa_word)]
    if len(vowels) < 2:
        return ipa_word
    penult = vowels[-2]
    return ipa_word[:penult.start()] + "ˈ" + ipa_word[penult.start():]

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run pronounce.py \"text\" [--stress]")
        sys.exit(1)

    text = sys.argv[1]
    show_stress = "--stress" in sys.argv

    words = tokenize(text)
    results = []
    for w in words:
        ipa = word_to_ipa(w)
        if show_stress:
            ipa = add_stress(ipa)
        results.append(ipa)

    print(f"Input:  {text}")
    print(f"IPA:    /{' '.join(results)}/")

if __name__ == "__main__":
    main()
