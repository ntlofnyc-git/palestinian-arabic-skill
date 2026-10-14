"""pal-word — find the Palestinian word for an English word, a formal (MSA) word, or a Gulf/Egyptian word.
Order of trust: ★ your corrections > curated swap list.
Usage: pal-word now | pal-word الآن | pal-word "a lot" """
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palnorm import norm
SK = os.environ.get('PAL_SKILL', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def tsv(name):
    p = os.path.join(SK, name)
    return [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')] if os.path.exists(p) else []

def main():
    q = ' '.join(sys.argv[1:]).strip()
    if not q:
        print(__doc__); return 2
    is_ar = bool(re.search(r'[؀-ۿ]', q))
    qn = norm(q) if is_ar else q.lower()
    found = False
    for f in tsv('corrections.tsv'):
        if (is_ar and norm(f[0]) == qn) or (not is_ar and qn in (f[3] if len(f) > 3 else '').lower()):
            print(f'★ CORRECTION: {f[0]} → {f[1]}   {f[3] if len(f) > 3 else ""}'); found = True
    for f in tsv('swaps.tsv'):
        if len(f) < 4: continue
        note = f[4] if len(f) > 4 else ''
        if (is_ar and (norm(f[0]) == qn or norm(f[1]).split(' / ')[0] == qn)) or (not is_ar and re.search(r'\b' + re.escape(qn) + r'\b', note.lower())):
            print(f'SWAP [{f[2]}/{f[3]}]: {f[0]} → {f[1]}   {note}'); found = True
    if not found:
        print('no match — try a simpler English word, or the MSA form'); return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
