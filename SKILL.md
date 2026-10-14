---
name: palestinian-arabic
description: Use WHENEVER you write, draft, translate or rewrite ANY Arabic (WhatsApp/SMS, captions, ads, emails, review replies, call/voice scripts, site copy). Output must be in a genuine Palestinian voice, never Gulf, Egyptian or stiff formal Arabic. Includes the pal-check scorer (which city it sounds like + bad-word flags), pal-word lookup (swap list + your corrections), your own corrections, and an example bank.
---

# Palestinian Arabic: Palestinian voice

When anyone asks for Arabic, it comes out in a **genuine Palestinian voice**, the way a Palestinian writes on WhatsApp.
Never **Gulf** (الحين، وايد، أبغى، زين، حق، تقدرين),
never **Egyptian** (دلوقتي، عايز، بتاع، كده), and no stiff **MSA** (التي، لدينا، سوف، نموذجاً، الرجاء) unless the register is formal.

Tools live in this skill's `bin/` folder (run `install.sh` once). Below, `pal-check` means `<skill dir>/bin/pal-check`.

## The loop (before ANY Arabic leaves you)
1. Write it in the Palestinian voice (rules below). Unsure of a word? `pal-word <english | MSA | gulf word>`
2. `pal-check "<text>"` (or `pal-check < file`). For formal-but-warm text: `pal-check --formal`.
3. Fix every flag (★ CORRECTION and `hard` flags = always; `soft` = swap unless the register is formal). Re-run.
4. Deliver only on ✅ PASS. 🟡 CLOSE = Levantine but with soft flags or weak South-Levant share: fix the words, re-check.
   ❌ FAIL = Gulf/Egyptian/MSA. Never ship a FAIL.
5. Don't mention the checker to the person the text is for.

**How to read the score.** The checker uses a 26-way dialect-ID model (the same sentences in 25 Arab cities + MSA).
It is very reliable at Levant vs Gulf/Egypt/MSA. It is NOT reliable at telling one Levantine city from another on short
texts (2 to 3 lines often bounce between Amman/Aleppo/Beirut). So the gate is: Levant ≥70% + Palestinian / South-Levant
share present + zero hard flags. Word rules (swaps + corrections) are what make it *Palestinian*. Don't contort natural
phrasing to chase a higher score.

## Corrections (highest priority)
- **Plain everyday Palestinian that everyone understands.** No heavy slang, no obscure village/Bedouin words.
- Rejected words live in `corrections.tsv` (e.g. دوس→اضغط، تظبّط، براحتك، مجدول). pal-check flags them as ★ CORRECTION.
- **When the user corrects a word, save it immediately:** `pal-learn "<wrong>" "<right>" "<short note>"`. Every later
  pal-check / pal-word picks it up.
- Voice scripts: same words, short sentences, no em-dashes (TTS reads them badly).

## Palestinian voice cheat-sheet
| meaning | ✅ Palestinian | ❌ avoid |
|---|---|---|
| now | هلّأ | الحين، دلوقتي، الآن، هلق |
| what / why / where / when | شو / ليش / وين / إمتى | وش، ايه، ماذا، لماذا، أين، فين |
| I want / you want / she wants | بدّي / بدّك / بدها | أبغى، أبي، عايز، أريد، تريدين |
| very, a lot | كتير | وايد، واجد، مره، أوي، جداً |
| good / nice | منيح / حلو | زين، كويس، جيد |
| this / this(f) / these / that | هاد / هاي (هادي) / هدول / هداك | هذا، هذه، هذي، ده، دي، هيدا |
| thing / everything / nothing | إشي / كل إشي / ولا إشي | شيء، حاجة |
| here | هون | هني، هنا |
| mine / yours / hers | تبعي / تبعك / تبعها | حقي، بتاعي |
| like this | هيك | كذا، جذي، كده |
| we / you (pl) | إحنا / إنتو | نحن، أنتم |
| will | رح | سوف، سـ، هـ |
| there is / isn't | في / ما في | يوجد، مفيش |
| only / also | بس / كمان | فقط، أيضاً |
| tomorrow / yesterday | بكرا / مبارح | غداً، باجر، أمس |
| anyone / nobody | حدا / ولا حدا (ما حدا) | أحد، لا أحد |
| because / so that | عشان / لإنّو | منشان، علشان(ok) |
| which/that | اللي | التي، الذي |
| we have | عنّا | لدينا |
| please | لو سمحت / ياريت | الرجاء، من فضلك (ok formal) |

**Grammar markers that scream Palestinian:**
- Present tense takes **ب**: بعرف، بتقدري، بنكمّل، بيعمل (not أعرف / تقدرين / نكمل).
- **2nd-person feminine drops the ن**: بتقدري، بتحبي، بتختاري (Gulf: تقدرين، تحبين ❌).
- Future = **رح** (رح أبعتلك). Negation = **مش** (nouns/adjectives) / **ما** (verbs: ما بعرف).
- Object suffixes: إلك، إلها، إلنا; "him" = ـو (بعرفو، تبعو).
- Spell the dialect the Palestinian way: هلّأ، بكرا، كتير، منيح، إشي، هاد، لحالو. Keep ق spelled ق in normal writing
  (city speakers pronounce it ء, but only spell it ء in set words like هلّأ).
- Short sentences. WhatsApp-natural. Emojis fine for consumer brands.

## Registers
- **WhatsApp / SMS / casual**: full dialect (examples.md §0, §2, §5).
- **Brand captions**: warm, premium, personal, dialect-forward. A touch of MSA is fine for product facts
  (عيار 21، حجر طبيعي) but sentences stay Palestinian. CTA → WhatsApp (احكيلنا عالواتساب). §1.
- **Review replies**: grateful, personal, use the reviewer's name, invite back. §3.
- **Formal-but-warm** (business clients, partners): polite dialect with respectful forms (أستاذ، إن شاء الله تكون بخير،
  شكراً إلك على ثقتك). Check with `pal-check --formal`. §4.
- **Pure MSA**: only when explicitly asked (legal pages, official letters). Then this skill doesn't apply; say so.

## Tools
- `pal-check [--formal] [--json] "text"`: verdict + city scores + per-sentence + word flags with the Palestinian fix.
- `pal-word now` / `pal-word الآن` / `pal-word وايد`: corrections ★ → swap list.
- `pal-learn "<wrong>" "<right>" "<note>"` / `pal-learn --list`: your corrections (`corrections.tsv`).

## Files
- `swaps.tsv`: curated Gulf/Egyptian/North-Levant/MSA → Palestinian list (~200). Add rows when you notice a new one.
- `corrections.tsv`: your corrections. Wins over everything.
- `examples.md`: example bank (before/after + approved samples).
- `SAMPLES.md`: real-world scenarios written three ways (Palestinian vs Gulf vs Formal) with checker verdicts.
