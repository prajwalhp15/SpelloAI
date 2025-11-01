
import math

# Keyboard adjacency (QWERTY) for mild substitution bonus
_KEYBOARD_NEIGHBORS = {
    'q':'was', 'w':'qes', 'e':'wrd', 'r':'etf', 't':'ryg', 'y':'tuh', 'u':'yij', 'i':'uok', 'o':'ipk', 'p':'o;',
    'a':'qwsxz', 's':'qweadzx', 'd':'ersfcx', 'f':'rtdgcv', 'g':'tyfhvb', 'h':'yugjbn', 'j':'uikhmn', 'k':'iojlm,',
    'l':'opk;.,', 'z':'asx', 'x':'zsdc', 'c':'xdfv', 'v':'cfgb', 'b':'vghn', 'n':'bhjm', 'm':'njk,'
}

VOWEL_EQUIV = [
    ("aa","a"), ("ee","i"), ("oo","u"), ("ae","e"), ("ai","e"), ("ay","e"),
    ("au","o"), ("aw","o"),
]

ASPIRATE_EQUIV = [
    ("kh","k"), ("gh","g"), ("ch","c"), ("jh","j"), ("th","t"), ("dh","d"), ("ph","p"), ("bh","b"), ("sh","s"), ("zh","j")
]

SUB_EQUIV = VOWEL_EQUIV + ASPIRATE_EQUIV

def is_neighbor(a, b):
    a = a.lower(); b = b.lower()
    if a == b: return True
    return b in _KEYBOARD_NEIGHBORS.get(a, '')
    

def weighted_damerau_levenshtein(s1, s2):
    """Damerau-Levenshtein with **domain-aware weights**.
    Costs:
      - exact = 0
      - typical vowel/aspiration confusion = 0.25
      - keyboard neighbor substitution = 0.6
      - normal substitution = 1.0
      - insertion/deletion = 1.0
      - transposition = 0.75
    """

    s1 = s1.lower(); s2 = s2.lower()
    len1, len2 = len(s1), len(s2)
    if s1 == s2: return 0.0
    if len1 == 0: return float(len2)
    if len2 == 0: return float(len1)

    # DP with rolling rows
    prev = [i for i in range(len2 + 1)]
    cur = [0] * (len2 + 1)
    prev2 = None

    # helpers to check multi‑char confusions like "aa" vs "a"
    def equiv_prefix(i, j):
        for a,b in SUB_EQUIV:
            if s1.startswith(a, i) and s2.startswith(b, j):
                return len(a), len(b), 0.25
            if s1.startswith(b, i) and s2.startswith(a, j):
                return len(b), len(a), 0.25
        return 0,0,1.0  # fallthrough

    for i in range(1, len1 + 1):
        cur[0] = i
        for j in range(1, len2 + 1):
            c1, c2 = s1[i-1], s2[j-1]
            cost = 0.0 if c1 == c2 else (0.6 if is_neighbor(c1, c2) else 1.0)

            # substitution
            sub = prev[j-1] + cost

            # insertion/deletion
            ins = cur[j-1] + 1.0
            dele = prev[j] + 1.0

            # equivalence (aa ~ a, kh ~ k, ...)
            ai, bj, ecost = equiv_prefix(i-1, j-1)
            if ai:
                sub = min(sub, prev[j-1] + ecost)  # treat as soft substitution

            # transposition
            if i>1 and j>1 and s1[i-1]==s2[j-2] and s1[i-2]==s2[j-1]:
                trans = prev2[j-2] + 0.75
                cur[j] = min(sub, ins, dele, trans)
            else:
                cur[j] = min(sub, ins, dele)
        prev, prev2, cur = cur, prev, [0]*(len2+1)
    return float(prev[len2])
