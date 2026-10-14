# Samples: Palestinian vs Gulf vs Formal

Four everyday situations, each written three ways with the same meaning. Every version was run through `pal-check`
(casual mode). All names are made up. The texts are also in [`samples/`](samples/) so you can check them yourself:

```bash
bin/pal-check < samples/review-pal.txt
```

**Palestinian / South Levant** = the share of the dialect score that lands on the southern Levant.
**any Levant** = Palestinian + Jordanian + Syrian + Lebanese. What matters most is the verdict and the word flags.

## 1. Google review reply

A customer left a 5-star review. The business owner thanks him by name.

**Palestinian**: ✅ PASS · Palestinian / South Levant 83% · any Levant 99%

```
شكراً كتير على كلامك الحلو يا أبو محمد 🙏
مبسوطين إنّو الشغل عجبك وإنّو كل إشي خلص بوقتو.
بنستنّاك دايماً، وإذا احتجت أي إشي احكيلنا.
```

**Gulf**: ❌ FAIL · reads as Muscat · Palestinian / South Levant 5% · any Levant 11% · flagged: وايد

```
مشكور وايد على كلامك الحلو يا أبو محمد 🙏
فرحانين إن الشغل عجبك وإن كل شي خلص على الوقت.
ننتظرك دايم، وإذا احتجت أي شي كلمنا.
```

**Formal (MSA)**: ❌ FAIL · reads as Formal (MSA) · Palestinian / South Levant 0% · any Levant 0%

```
نشكرك جزيل الشكر على كلماتك اللطيفة يا أبا محمد.
يسعدنا أن العمل قد نال إعجابك وأنه تم إنجازه في الوقت المحدد.
نتطلع إلى خدمتك مجدداً، ولا تتردد في التواصل معنا لأي استفسار.
```


## 2. Greeting / catching up

Good morning to someone you haven't seen in a while.

**Palestinian**: ✅ PASS · Palestinian / South Levant 32% · any Levant 75%

```
صباح الخير! كيفك؟ إن شاء الله تمام.
صارلنا زمان ما شفناك، شو أخبارك وأخبار العيلة؟
```

**Gulf**: ❌ FAIL · reads as Doha · Palestinian / South Levant 3% · any Levant 6% · flagged: شلونك، وش

```
صباح الخير! شلونك؟ إن شاء الله زين.
من زمان ما شفناك، وش أخبارك وأخبار الأهل؟
```

**Formal (MSA)**: ❌ FAIL · reads as Formal (MSA) · Palestinian / South Levant 0% · any Levant 0%

```
صباح الخير! كيف حالك؟ أرجو أن تكون بخير.
لم نرك منذ مدة طويلة، ما أخبارك وأخبار العائلة؟
```


## 3. Introducing yourself (business)

A web designer introduces himself to a potential client.

**Palestinian**: ✅ PASS · Palestinian / South Levant 38% · any Levant 99%

```
مرحبا، أنا اسمي سامي، بشتغل بتصميم المواقع من حوالي عشر سنين.
حبّيت أعرّفك على حالي لإنّو بعرف إنّك بتدوّر على حدا يعملك موقع جديد.
إذا بدك، منقعد مع بعض على فنجان قهوة وبفرجيك شو عملت قبل.
```

**Gulf**: ❌ FAIL · reads as Formal (MSA) · Palestinian / South Levant 4% · any Levant 8% · flagged: يسوي، تبي، وش، سويت

```
هلا، أنا اسمي سامي، أشتغل في تصميم المواقع من حوالي عشر سنين.
حبيت أعرفك على نفسي لأني أدري إنك تدور أحد يسوي لك موقع جديد.
إذا تبي، نجلس مع بعض على فنجان قهوة وأوريك وش سويت قبل.
```

**Formal (MSA)**: ❌ FAIL · reads as Formal (MSA) · Palestinian / South Levant 0% · any Levant 0%

```
مرحباً، اسمي سامي، وأعمل في مجال تصميم المواقع منذ نحو عشر سنوات.
أود أن أعرّفك بنفسي، إذ علمت أنك تبحث عن شخص يصمم لك موقعاً جديداً.
إن رغبت، يمكننا أن نلتقي على فنجان قهوة لأعرض عليك أعمالي السابقة.
```


## 4. Job interview (interviewer)

The interviewer opens the interview with a woman candidate.

**Palestinian**: ✅ PASS · Palestinian / South Levant 35% · any Levant 97%

```
أهلين، تفضّلي اقعدي. بدايةً احكيلنا شوي عن حالك وعن آخر شغل اشتغلتيه.
ليش حابّة تشتغلي معنا؟ وإمتى بتقدري تبلّشي إذا اتّفقنا؟
```

**Gulf**: ❌ FAIL · reads as Aleppo · Palestinian / South Levant 18% · any Levant 89% · flagged: تبين، تقدرين (the sentence rhythm is Levant-like, the Gulf words give it away)

```
هلا، تفضلي اجلسي. أول شي كلمينا شوي عن نفسك وعن آخر شغل اشتغلتيه.
ليش تبين تشتغلين معنا؟ ومتى تقدرين تبدين إذا اتفقنا؟
```

**Formal (MSA)**: ❌ FAIL · reads as Formal (MSA) · Palestinian / South Levant 0% · any Levant 0%

```
أهلاً بكِ، تفضّلي بالجلوس. بدايةً، حدّثينا قليلاً عن نفسك وعن آخر عمل قمتِ به.
لماذا ترغبين في العمل معنا؟ ومتى يمكنك البدء في حال تم الاتفاق؟
```


## What the checker caught

- **Gulf** versions fail on words like وايد، وش، تبي، يسوي، سويت، تقدرين (the checker suggests كتير، شو، بدّك، بيعمل، عملت، بتقدري).
- **Formal (MSA)** versions score 80 to 100% Formal: correct Arabic, but nobody talks or texts like that.
- **Palestinian** versions pass with zero hard word flags.
