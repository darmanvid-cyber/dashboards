"""Pone (o actualiza) la marca discreta «® DN · vX.Y» abajo a la izquierda de un dashboard HTML. Idempotente.
Uso: python3 poner_version.py [--version 3.0] archivo.html ..."""
import re, sys
VER = "3.0"
a = sys.argv[1:]
if a[:1] == ["--version"]: VER, a = a[1], a[2:]
B = "<!--dash-version-->"; E = "<!--/dash-version-->"
blk = (B + '<div id="dash-version" aria-hidden="true" style="position:fixed;left:8px;bottom:5px;z-index:9999;'
       'font:10px/1 system-ui,-apple-system,Segoe UI,sans-serif;letter-spacing:.02em;color:inherit;opacity:.5;'
       'pointer-events:none;user-select:none">® DN · v' + VER + "</div>" + E)
for f in a:
    s = open(f, encoding="utf-8", newline="").read()
    s = re.sub(re.escape(B) + ".*?" + re.escape(E), "", s, flags=re.S)
    i = s.rfind("</body>")
    if i < 0: print("SIN </body>:", f); continue
    open(f, "w", encoding="utf-8", newline="").write(s[:i] + blk + s[i:])
    print("ok", f)
