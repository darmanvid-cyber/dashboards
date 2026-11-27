"""Pone (o actualiza) el botón «← Dashboards» (vuelve al portal) en un dashboard HTML. Idempotente.
Uso: python3 poner_volver.py <ruta_relativa_al_portal> archivo.html ..."""
import re, sys
href=sys.argv[1]; B="<!--portal-back-->"; E="<!--/portal-back-->"
blk=(B+'<a id="portal-back" href="'+href+'" style="position:fixed;right:10px;bottom:10px;z-index:9999;padding:7px 12px;border-radius:999px;'
 'background:#2a78d6;color:#fff;font:600 13px/1 system-ui,-apple-system,Segoe UI,sans-serif;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,.3)">← Dashboards</a>'+E)
for f in sys.argv[2:]:
    s=open(f,encoding="utf-8",newline="").read()
    s=re.sub(re.escape(B)+".*?"+re.escape(E),"",s,flags=re.S)
    i=s.rfind("</body>")
    if i<0: print("SIN </body>:",f); continue
    open(f,"w",encoding="utf-8",newline="").write(s[:i]+blk+s[i:])
