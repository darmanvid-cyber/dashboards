#!/bin/bash
# Copia los dashboards más recientes a carpetas con nombre aleatorio y los sube a GitHub Pages.
# Uso: bash publicar.sh ["mensaje"]      (lee enlaces.tsv: slug <TAB> token <TAB> origen)
cd "$(dirname "$0")" || exit 1
while IFS=$'\t' read -r slug token src; do
  [ -f "$src" ] || { echo "FALTA: $src"; continue; }
  mkdir -p "$token"
  # noindex: que Google no lo indexe aunque alguien publique el enlace
  python3 - "$src" "$token/index.html" <<'PY'
import sys
s = open(sys.argv[1], encoding='utf-8').read()
if 'name="robots"' not in s:
    s = s.replace('<head>', '<head><meta name="robots" content="noindex,nofollow">', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s)
PY
done < enlaces.tsv
printf 'User-agent: *\nDisallow: /\n' > robots.txt
touch .nojekyll
git add -A
git diff --cached --quiet && { echo "Sin cambios que publicar."; exit 0; }
git commit -q -m "${1:-Actualizar dashboards}" && git push -q && echo "Publicado."
