
import re

_REP = [
    ('aa','a'), ('ii','i'), ('ee','i'), ('oo','u'),
    ('kh','k'), ('gh','g'), ('ch','c'), ('jh','j'),
    ('th','t'), ('dh','d'), ('ph','p'), ('bh','b'),
    ('sh','s'), ('zh','j'), ('rr','r'),
    ('wh','w'), ('qu','k'), ('ck','k'), ('x','ks'), ('z','j')
]

_VOWELS = "aeiou"

def normalize_token(tok: str) -> str:
    s = tok.lower().strip()
    s = re.sub(r'[^a-z]', '', s)
    if not s: return s
    for a,b in _REP:
        s = s.replace(a,b)
    # collapse duplicates
    s = re.sub(r'(.)\1+', r'\1', s)
    # collapse vowel runs to single vowel
    s = re.sub(r'[aeiou]+', lambda m: m.group(0)[0], s)
    return s

def phonetic_key(tok: str) -> str:
    s = normalize_token(tok)
    if not s: return s
    # drop vowels except first char to create a consonant skeleton
    first = s[0]
    tail = re.sub(r'[aeiou]', '', s[1:])
    return first + tail
