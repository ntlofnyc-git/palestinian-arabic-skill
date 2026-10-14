"""Shared Arabic normalisation for pal-check / pal-word (our own code, no deps)."""
import re
DIAC = re.compile(r'[ً-ْٰـ]')
def norm(s):
    s = DIAC.sub('', s)
    s = re.sub('[أإآٱ]', 'ا', s)
    return s.replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
TOK = re.compile(r'[ء-يٰ-ۓً-ْ]+')
def tokens(s):
    return TOK.findall(s)
