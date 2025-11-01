from collections import defaultdict, Counter
from math import log
from .utils import weighted_damerau_levenshtein
from .phonetics import phonetic_key, normalize_token


class DeleteIndexSpellfix:
    def __init__(self, max_edit=2, prefix_len=20):
        self.max_edit = max_edit
        self.prefix_len = prefix_len
        self.dictionary = {}      # word -> freq
        self.deletes = defaultdict(set)  # delete_key -> {word}
        self._phon = {}           # cache: word -> phonetic key

    def _key(self, w):
        if w not in self._phon:
            self._phon[w] = phonetic_key(w)
        return self._phon[w]

    def add_dictionary_entry(self, word, freq=1):
        word = word.strip()
        if not word:
            return
        self.dictionary[word] = self.dictionary.get(word, 0) + int(freq)
        for d in self._generate_deletes(word):
            self.deletes[d].add(word)

    def _generate_deletes(self, word):
        # all strings from deleting up to max_edit characters
        queue = set([word[:self.prefix_len]])
        results = set()
        for _ in range(self.max_edit):
            new = set()
            for w in queue:
                for i in range(len(w)):
                    deleted = w[:i] + w[i + 1:]
                    if deleted and deleted not in results:
                        results.add(deleted)
                        new.add(deleted)
            queue = new
        return results or {word}

    def build_from_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if '\t' in line:
                    w, fr = line.split('\t', 1)
                    self.add_dictionary_entry(w, int(fr) if fr.isdigit() else 1)
                else:
                    self.add_dictionary_entry(line, 1)

    def lookup(self, word, topk=1):
        w = word.strip()
        if not w:
            return []
        w_norm = normalize_token(w)
        if w_norm in self.dictionary:
            return [(w_norm, 0.0)]

        candidates = set()
        # exact deletes from word
        queue = set([w_norm])
        for _ in range(self.max_edit):
            new = set()
            for s in queue:
                for i in range(len(s)):
                    d = s[:i] + s[i + 1:]
                    if not d:
                        continue
                    for cand in self.deletes.get(d, ()):
                        candidates.add(cand)
                    new.add(d)
            queue = new

        if not candidates:
            # fall back to all dict words with same first letter
            first = w_norm[:1]
            candidates = [dw for dw in self.dictionary.keys() if dw[:1] == first]

        scores = []
        wkey = phonetic_key(w_norm)
        for c in candidates:
            ed = weighted_damerau_levenshtein(w_norm, c)
            # score with phonetic and frequency bonuses
            bonus = 0.0
            if phonetic_key(c) == wkey:
                bonus += 1.0
            freq = self.dictionary.get(c, 1)
            score = -ed + 0.15 * log(1 + freq) + 0.7 * bonus
            scores.append((c, score, ed, freq))

        scores.sort(key=lambda x: (-x[1], x[2], -x[3], x[0]))
        return [(c, ed) for c, _, ed, _ in scores[:topk]]


# ✅ Alias for compatibility with API
SpellCorrector = DeleteIndexSpellfix
