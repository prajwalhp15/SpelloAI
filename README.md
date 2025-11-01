
# Auto Spell Correction for Non‑English Words Written in English Script

This repo contains a **production‑ready, fast spell corrector** aimed at Indic languages typed in Latin/English script
(Hinglish/Marathi‑in‑English, etc.). It handles noisy spellings in large files (>=10k lines).

## Quick Start

```bash
# 1) Put your dictionary and errors files in ./data
#    - dictionary: reference.txt (one word per line, optionally "word\tfreq")
#    - errors: errors.txt (one misspelled token per line)

# 2) Build the index (optional; done lazily on first run)
python correct.py --dictionary data/reference.txt --errors data/errors.txt --out data/output.csv

# Extra knobs
python correct.py --dictionary data/reference.txt --errors data/errors.txt --out data/output.csv \
  --max_edit 2 --topk 1 --threads 4
```

**Output format** (CSV with header):
```
File_Error,Corrected
Aum,Aam
ROM,Ram
RAAM,Ram
```

---

## Why this works (Design)

Real‑world Romanized Indian words contain:
- **Vowel drift:** `a/aa`, `i/ee`, `u/oo`, `e/ai`, `o/au`
- **Aspiration drift:** `kh/k`, `ph/p`, `th/t`, `dh/d`, `bh/b`, `ch/c`, `sh/s`
- **Repeated letters & emphasis:** `raam` → `ram`, `goooood` → `good`
- **QWERTY typos & swaps** (Damerau transpositions).

We combine three ideas for **accuracy** and **speed**:

1. **Delete‑Index Search (SymSpell‑style):**  
   Precompute all strings formed by deleting up to *d* characters from every dictionary entry.  
   Lookups turn into hash table probes — extremely fast.

2. **Weighted Damerau‑Levenshtein distance:**  
   Edit cost is smaller for *expected* confusions (e.g., `aa↔a`, `ee↔i`, `oo↔u`, aspiration removal).

3. **Phonetic Key (Indic‑aware):**  
   We normalize pairs (`kh→k`, `sh→s`, `aa→a`, …), collapse duplicates, and compare phonetic keys.  
   Candidates with matching keys get a scoring **bonus**.

The final score is:
```
score = w_edit * (−edit_distance) + w_phon * [phonetic_key_match] + w_freq * log(1+freq)
```
Top‑K candidates are returned (default K=1).

### Complexity

- **Index build:** O(N * L * d) deletes (N words, average length L, max delete distance d).  
- **Query:** O(C * L) where C is candidate set size (usually small due to deletes‑filter).

---

## Files

- `correct.py` – CLI tool to correct a file using the engine.
- `spellfix/engine.py` – Core engine (delete index + weighted DL + phonetic key).
- `spellfix/phonetics.py` – Indic‑aware phonetic normalization.
- `spellfix/utils.py` – Small utilities and a fast DL distance.
- `data/reference.txt` – Sample dictionary (feel free to replace with your full list).
- `data/errors.txt` – Sample errors to test the pipeline.

---

## Notes

- The dictionary can include frequencies: `"word<TAB>count"`. Frequencies bias results to common words.
- The engine is pure‑Python, no external deps, so it runs anywhere (including coding interviews).
- For **very large** dictionaries, set `--max_edit 1` for speed, or increase `--threads`.

Good luck in your interview! 🚀
