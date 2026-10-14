# Palestinian Arabic skill

**Write Arabic in a genuine Palestinian voice, not Gulf, Egyptian or stiff formal Arabic.**

A small toolkit (and a ready-made [Claude skill](https://docs.claude.com/en/docs/claude-code/skills)) for writing Arabic
that sounds Palestinian, the way people actually write on WhatsApp, instead of Gulf, Egyptian or formal Arabic (MSA).

It gives you three command-line tools:

- **`pal-check`**: scores a text. How Palestinian / Levantine does it sound, and which words give it away as Gulf,
  Egyptian, North-Levant or MSA (with the Palestinian word to use instead). Verdict: ✅ PASS / 🟡 CLOSE / ❌ FAIL.
- **`pal-word`**: "what's the Palestinian word for…?" Look up an English, MSA, Gulf or Egyptian word and get the
  Palestinian form from the curated swap list and your own corrections.
- **`pal-learn`**: save your own corrections ("don't use X, use Y"). They override everything else from then on.

```
$ bin/pal-check "دوس هون الحين وايد"
❌ FAIL — sounds most like: Doha  |  Palestinian / South Levant: 1%  |  any Levant: 1%  [casual mode]
   word flags (→ Palestinian):
     • دوس → اضغط   (★ CORRECTION: "press": دوس is less clear to many readers, use اضغط)
     • الحين → هلّأ   (GULF/hard: now)
     • وايد → كتير   (GULF/hard: a lot / very)

$ bin/pal-check "شو الأخبار؟ بدك نطلع نشرب قهوة بكرا المسا؟"
✅ PASS — sounds most like: Damascus  |  Palestinian / South Levant: 49%  |  any Levant: 100%  [casual mode]
```

## Real-world samples

Four everyday situations, each written three ways, run through `pal-check`. Full texts and scores: **[SAMPLES.md](SAMPLES.md)**.

| scenario | Palestinian | Gulf | Formal (MSA) |
|---|---|---|---|
| Google review reply | ✅ PASS | ❌ FAIL | ❌ FAIL |
| Greeting / catching up | ✅ PASS | ❌ FAIL | ❌ FAIL |
| Introducing yourself (business) | ✅ PASS | ❌ FAIL | ❌ FAIL |
| Job interview (interviewer) | ✅ PASS | ❌ FAIL | ❌ FAIL |

For example, the Google review reply:

```
شكراً كتير على كلامك الحلو يا أبو محمد 🙏
مبسوطين إنّو الشغل عجبك وإنّو كل إشي خلص بوقتو.
بنستنّاك دايماً، وإذا احتجت أي إشي احكيلنا.
```

## How the checker works

1. **Dialect scores** come from a 26-way Arabic dialect-ID model (the same sentences written in 25 Arab cities plus MSA).
   The text is scored as a whole and sentence by sentence.
2. **Word flags** come from `swaps.tsv` (~200 hand-curated Gulf / Egyptian / North-Levant / MSA → Palestinian swaps),
   your `corrections.tsv`, and a small heuristic for Gulf feminine verbs (تقدرين → بتقدري).
3. **Verdict**: PASS needs ≥70% Levantine, some Palestinian / South-Levant share, zero hard flags and at most one soft
   flag. `--formal` mode relaxes the MSA rules for polite business text.

**Honest limit:** the model is very good at Levant vs Gulf vs Egypt vs MSA. It **cannot** reliably tell one Levantine
city from another on short texts: two or three lines often bounce between Amman, Aleppo and Beirut. That's why the gate
is "Levantine + Palestinian / South-Levant share present + clean words", not a single city score. The word lists are
what make the text specifically Palestinian. Don't twist natural phrasing just to chase a higher score.

## Quick start

Needs Python 3.11 to 3.14, `curl`, `unzip`. Linux or macOS. Optional: [bubblewrap](https://github.com/containers/bubblewrap).

```bash
git clone https://github.com/ntlofnyc-git/palestinian-arabic-skill.git
cd palestinian-arabic-skill
./install.sh                 # local venv + downloads the dialect-ID model (~275 MB)
bin/pal-check < tests/before-setup-msg.txt
bin/pal-check < tests/after-setup-msg.txt
bin/pal-check < samples/review-pal.txt
bin/pal-word now
bin/pal-learn "مجدول" "محجوز" "too formal"
```

Pip may print a warning about torch/transformers. That's expected: they aren't needed for dialect ID, so the install
skips them.

**Sandbox:** if `bwrap` is installed, `pal-check` and `pal-word` run with no network, no access to your home directory
and a read-only copy of this folder. Set `PAL_NO_SANDBOX=1` to run without it (e.g. on macOS).

## Use it as a Claude skill

Copy (or clone) this folder into your skills directory and run the installer there:

```bash
git clone https://github.com/ntlofnyc-git/palestinian-arabic-skill.git ~/.claude/skills/palestinian-arabic
~/.claude/skills/palestinian-arabic/install.sh
```

Claude reads `SKILL.md`: the Palestinian-voice rules, a cheat-sheet, registers (WhatsApp, brand captions, review
replies, formal-but-warm) and the write → check → fix loop. `examples.md` has before/after samples.

## Repo layout

| path | what |
|---|---|
| `SKILL.md` | the skill: rules, cheat-sheet, registers, workflow |
| `swaps.tsv` | curated wrong → Palestinian word list with level (hard/soft) |
| `corrections.tsv` | your own corrections (highest priority), managed with `pal-learn` |
| `SAMPLES.md`, `samples/` | real-world scenarios: Palestinian vs Gulf vs Formal, with checker verdicts |
| `examples.md`, `tests/` | example bank and sample texts (all names made up) |
| `bin/`, `lib/` | the tools (`pal-check`, `pal-word`, `pal-learn`, sandbox wrapper `pal-sbx`) |
| `install.sh` | sets up `.venv/` and downloads the model into `.camel-data/` |

## License

[MIT](LICENSE).
