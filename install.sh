#!/usr/bin/env bash
# install.sh: sets up the pal-check engine inside this folder.
#  1. a Python venv in .venv/ with CAMeL Tools 1.6.0 (MIT) WITHOUT torch/transformers
#     (the dialect-ID model only needs scikit-learn + kenlm, so the install stays small)
#  2. the CAMeL Lab DID-26 dialect-ID model, downloaded from CAMeL Lab's own release
#     and checked against its published sha256, into .camel-data/
# Needs: python 3.11 to 3.14, curl, unzip. Linux or macOS. Optional: bubblewrap (sandbox).
set -euo pipefail
ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PY="${PYTHON:-python3}"
DATA="$ROOT/.camel-data"
MODEL_URL="https://github.com/CAMeL-Lab/camel-tools-data/releases/download/2026.06.08/dialectid_model26-1.1.2.zip"
MODEL_SHA="0d45188e4dc3955ed1b49b41fed54756e244d8974ac38ef92f9e35cdcbff36a5"
CAT_URL="https://raw.githubusercontent.com/CAMeL-Lab/camel-tools-data/main/catalogue-1.6.json"

sha() { if command -v sha256sum >/dev/null; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }

echo "==> venv"
[ -x "$ROOT/.venv/bin/python" ] || "$PY" -m venv "$ROOT/.venv"
V="$ROOT/.venv/bin/python"
"$V" -m pip install -q --upgrade pip
"$V" -m pip install -q --no-deps "camel-tools==1.6.0"
# camel-tools deps minus torch/transformers (not needed for dialect ID).
# scikit-learn is pinned: the model pickle was built with 1.9.x.
"$V" -m pip install -q "scikit-learn==1.9.*" "numpy>=2" scipy pandas "dill>=0.4" "cachetools>=6" \
  "camel-kenlm>=2026.2.7" docopt editdistance emoji future muddler pyrsistent regex requests six tabulate tqdm

echo "==> CAMeL DID-26 model (~275 MB download, from CAMeL Lab)"
M="$DATA/data/dialectid/model26"
if [ ! -d "$M/lm/word" ]; then
  mkdir -p "$DATA"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  curl -fL --retry 3 -o "$TMP/m.zip" "$MODEL_URL"
  [ "$(sha "$TMP/m.zip")" = "$MODEL_SHA" ] || { echo "sha256 mismatch on model zip, aborting" >&2; exit 1; }
  mkdir -p "$M"; unzip -q "$TMP/m.zip" -d "$TMP/x"
  SRC="$(dirname "$(find "$TMP/x" -name 'did_pretrained_*.dill' | head -1)")"
  cp -r "$SRC"/. "$M"/
fi
[ -f "$DATA/catalogue.json" ] || curl -fsSL -o "$DATA/catalogue.json" "$CAT_URL"

echo "==> smoke test"
"$ROOT/bin/pal-check" "شو الأخبار؟ بدك نطلع نشرب قهوة بكرا المسا؟" || true
echo
echo "Done. Put $ROOT/bin on your PATH, or call bin/pal-check directly."
