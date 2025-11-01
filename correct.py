
import argparse, csv, os, sys, time
from spellfix.engine import DeleteIndexSpellfix

def parse_args():
    ap = argparse.ArgumentParser(description="Auto spell correction for non‑English words in English script")
    ap.add_argument("--dictionary", required=True, help="Path to reference.txt (word or 'word\\tfreq' per line)")
    ap.add_argument("--errors", required=True, help="Path to errors.txt (one token per line)")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--max_edit", type=int, default=2)
    ap.add_argument("--topk", type=int, default=1)
    ap.add_argument("--threads", type=int, default=1, help="Reserved for future parallel build")
    return ap.parse_args()

def main():
    args = parse_args()
    t0 = time.time()
    engine = DeleteIndexSpellfix(max_edit=args.max_edit)
    engine.build_from_file(args.dictionary)
    t1 = time.time()
    print(f"Built index in {t1-t0:.3f}s | dictionary size={len(engine.dictionary)} deletes={len(engine.deletes)}")

    with open(args.errors, "r", encoding="utf-8") as fin, \
         open(args.out, "w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout)
        writer.writerow(["File_Error","Corrected"])
        cnt = 0
        for line in fin:
            token = line.strip()
            if not token: 
                continue
            resc = engine.lookup(token, topk=args.topk)
            best = resc[0][0] if resc else token
            writer.writerow([token, best])
            cnt += 1
        t2 = time.time()
    print(f"Corrected {cnt} tokens in {t2-t1:.3f}s ⇒ {args.out}")

if __name__ == "__main__":
    main()
