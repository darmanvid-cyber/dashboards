#!/usr/bin/env python3
"""Genera portal.html (índice de dashboards) desde enlaces.tsv + catalogo.json. Los dashes sin entrada en el catálogo (p. ej. los por área) no aparecen."""
import json, os, datetime
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
cat=json.load(open("catalogo.json",encoding="utf-8"))
items=[]
for l in open("enlaces.tsv",encoding="utf-8"):
    p=l.rstrip("\n").split("\t")
    if len(p)<3 or p[0] not in cat["dashes"]: continue
    c=dict(cat["dashes"][p[0]]); c["prot"]=p[0] not in cat.get("abiertos",[]); c["href"]="../"+p[1]+"/"
    try: c["upd"]=datetime.date.fromtimestamp(os.path.getmtime(p[2])).isoformat()
    except Exception: c["upd"]=""
    items.append(c)
import cifrar
code=open("../dashboards_codigo.txt",encoding="utf-8").read().strip()
data={"areas":cat["areas"],"items":items,"verif":cifrar.enc(b"ok",code)}
html=open("plantilla_portal.html",encoding="utf-8").read().replace("/*DATA*/null",json.dumps(data,ensure_ascii=False))
import base64
html=html.replace("/*LOGO*/","data:image/png;base64,"+base64.b64encode(open("logo_integra.png","rb").read()).decode())
open("portal.html","w",encoding="utf-8").write(html); print(len(items),"dashes en el portal")
