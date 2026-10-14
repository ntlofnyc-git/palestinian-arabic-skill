"""pal-check — does this Arabic sound genuinely Palestinian? Runs via bin/pal-sbx (sandboxed if bwrap is installed).
Scores the text and each sentence with a 26-way Arabic dialect-ID model (25 cities + MSA), aggregates, and flags
Gulf / Egyptian / North-Levant / MSA words using the skill's swaps.tsv + your own corrections.tsv.
Usage: pal-check [--formal] [--json] "text"   (or text on stdin)"""
import sys, os, re, json, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palnorm import norm, tokens

SK = os.environ.get('PAL_SKILL', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NAMES = {'JER': 'Jerusalem', 'AMM': 'Amman', 'SAL': 'Salt', 'DAM': 'Damascus', 'ALE': 'Aleppo', 'BEI': 'Beirut',
         'MSA': 'Formal (MSA)', 'RIY': 'Riyadh', 'JED': 'Jeddah', 'DOH': 'Doha', 'MUS': 'Muscat', 'SAN': "Sana'a",
         'BAG': 'Baghdad', 'BAS': 'Basra', 'MOS': 'Mosul', 'CAI': 'Cairo', 'ALX': 'Alexandria', 'ASW': 'Aswan',
         'KHA': 'Khartoum', 'TRI': 'Tripoli', 'BEN': 'Benghazi', 'TUN': 'Tunis', 'SFX': 'Sfax', 'ALG': 'Algiers',
         'RAB': 'Rabat', 'FES': 'Fes'}
SOUTH = {'JER', 'AMM', 'SAL'}
NORTH = {'DAM', 'ALE', 'BEI'}

def load_tsv(name):
    rows = []
    p = os.path.join(SK, name)
    if not os.path.exists(p):
        return rows
    for line in open(p, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        rows.append(line.rstrip('\n').split('\t'))
    return rows

def build_lex():
    lex = {}  # normalized phrase tuple -> (replacement, from, level, note, src)
    for f in load_tsv('swaps.tsv'):
        if len(f) >= 4:
            lex[tuple(norm(f[0]).split())] = (f[1], f[2], f[3], f[4] if len(f) > 4 else '', 'swap')
    for f in load_tsv('corrections.tsv'):  # your corrections win
        if len(f) >= 2:
            lex[tuple(norm(f[0]).split())] = (f[1], 'CORRECTION', 'hard', f[3] if len(f) > 3 else '', 'correction')
    return lex

PREFIXES = ('و', 'ف', 'ب', 'ل', 'وب', 'ول', 'فب')

def flag_words(text, lex):
    toks = [norm(t) for t in tokens(text)]
    raw = tokens(text)
    flags, i = [], 0
    maxn = max((len(k) for k in lex), default=1)
    while i < len(toks):
        hit = None
        for n in range(maxn, 0, -1):
            seq = tuple(toks[i:i + n])
            if len(seq) < n:
                continue
            if seq in lex:
                hit = (n, seq, ''); break
            for p in PREFIXES:  # وتقدرين / بالحين etc.
                if seq[0].startswith(p) and len(seq[0]) - len(p) >= 3:
                    s2 = (seq[0][len(p):],) + seq[1:]
                    if s2 in lex:
                        hit = (n, s2, p); break
            if hit:
                break
        if hit:
            n, key, p = hit
            rep, frm, lvl, note, src = lex[key]
            flags.append({'word': ' '.join(raw[i:i + n]), 'use': rep, 'from': frm, 'level': lvl, 'note': note, 'src': src})
            i += n
        else:
            i += 1
    return flags

def gulf_fem_heuristic(text, already):
    out = []
    for t in tokens(text):
        n = norm(t)
        for p in ('', 'و'):
            m = n[len(p):] if n.startswith(p) else None
            if m and re.fullmatch(r'ت\w{2,5}ين', m) and t not in already:
                out.append({'word': t, 'use': 'بت' + m[1:-1], 'from': 'GULF?', 'level': 'soft',
                            'note': 'looks like a Gulf 2nd-person-fem verb (-ين). Palestinian drops the ن: بتـ…ي', 'src': 'heuristic'})
                break
    return out

def segments(text):
    text = re.sub(r'https?://\S+|\$\w+|[A-Za-z0-9_@#*/.:=?&%-]{3,}', ' ', text)
    parts = re.split(r'[\n.!?؟؛:••]+|،(?=\s)', text)
    segs = []
    for p in parts:
        tk = tokens(p)
        if len(tk) >= 2:
            segs.append(' '.join(tk))
    return segs

def main():
    args = sys.argv[1:]
    formal = '--formal' in args
    as_json = '--json' in args
    args = [a for a in args if a not in ('--formal', '--json')]
    text = ' '.join(args) if args else sys.stdin.read()
    if not tokens(text):
        print('pal-check: no Arabic text given'); return 2
    with contextlib.redirect_stderr(io.StringIO()):
        from camel_tools.dialectid import DIDModel26
        model = DIDModel26.pretrained()
    segs = segments(text) or [' '.join(tokens(text))]
    whole = re.sub(r'https?://\S+|\$\w+', ' ', text)
    whole = re.sub(r'[^\u0600-\u06FF\s.!?،,]', ' ', whole)
    clean = lambda x: re.sub(r'[\u064B-\u0652\u0670\u0640]', '', x)
    preds = model.predict([clean(whole)] + [clean(s) for s in segs])
    agg = preds[0].scores
    per = []
    for s, p in zip(segs, preds[1:]):
        per.append({'text': s, 'top': p.top, 'south_levant': round(sum(p.scores.get(c, 0) for c in SOUTH), 2)})
    top = max(agg, key=agg.get)
    sl = sum(agg.get(c, 0) for c in SOUTH)
    lev = sl + sum(agg.get(c, 0) for c in NORTH)
    lex = build_lex()
    flags = flag_words(text, lex)
    flags += gulf_fem_heuristic(text, {f['word'] for f in flags})
    hard = [f for f in flags if f['level'] == 'hard']
    soft = [f for f in flags if f['level'] == 'soft' and not (formal and f['from'] == 'MSA')]
    if formal:
        ok = not hard and (lev + agg.get('MSA', 0)) >= 0.6 and lev >= 0.2
        fail = bool(hard) or (lev + agg.get('MSA', 0)) < 0.4
    else:
        ok = not hard and lev >= 0.7 and len(soft) <= 1 and (top in SOUTH or sl >= 0.2)
        fail = bool(hard) or lev < 0.5
    verdict = 'PASS' if ok else ('FAIL' if fail else 'CLOSE')
    res = {'verdict': verdict, 'mode': 'formal' if formal else 'casual', 'top_city': NAMES.get(top, top),
           'south_levant_pct': round(sl * 100), 'levant_pct': round(lev * 100),
           'scores': {NAMES.get(k, k): round(v * 100) for k, v in sorted(agg.items(), key=lambda x: -x[1])[:6]},
           'sentences': [dict(x, top=NAMES.get(x['top'], x['top'])) for x in per], 'flags': flags}
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1)); return 0 if ok else 1
    icon = {'PASS': '✅', 'CLOSE': '🟡', 'FAIL': '❌'}[verdict]
    print(f"{icon} {verdict} — sounds most like: {res['top_city']}  |  Palestinian / South Levant: {res['south_levant_pct']}%  |  any Levant: {res['levant_pct']}%  [{res['mode']} mode]")
    print('   scores: ' + ' · '.join(f'{k} {v}%' for k, v in res['scores'].items()))
    bad = [x for x in per if x['top'] not in SOUTH | NORTH and len(x['text'].split()) >= 3]
    if bad:
        print('   sentences that do NOT read as Levantine:')
        for x in bad:
            print(f"     • [{NAMES.get(x['top'], x['top'])}, SL {round(x['south_levant']*100)}%] {x['text'][:90]}")
    if flags:
        print('   word flags (→ Palestinian):')
        for f in flags:
            star = '★ CORRECTION' if f['src'] == 'correction' else f"{f['from']}/{f['level']}"
            print(f"     • {f['word']} → {f['use']}   ({star}{': ' + f['note'] if f['note'] else ''})")
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
