#!/usr/bin/env python3
"""Cifra un HTML con el código (PBKDF2-SHA256 200k + AES-256-GCM) y lo envuelve en una página que pide el código.
Uso: python3 cifrar.py <codigo_file> <html_in> <html_out>      |  como módulo: enc(bytes,codigo) -> base64"""
import sys, os, base64, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
IT=200000
def enc(data: bytes, code: str) -> str:
    salt=os.urandom(16); iv=os.urandom(12)
    key=hashlib.pbkdf2_hmac("sha256",code.encode(),salt,IT,32)
    return base64.b64encode(salt+iv+AESGCM(key).encrypt(iv,data,None)).decode()
JS='''async function dec(code,b){const d=Uint8Array.from(atob(b),c=>c.charCodeAt(0)),salt=d.slice(0,16),iv=d.slice(16,28),ct=d.slice(28);
const km=await crypto.subtle.importKey("raw",new TextEncoder().encode(code),"PBKDF2",false,["deriveKey"]);
const key=await crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:%d,hash:"SHA-256"},km,{name:"AES-GCM",length:256},false,["decrypt"]);
return new TextDecoder().decode(await crypto.subtle.decrypt({name:"AES-GCM",iv},key,ct));}''' % IT
def wrapper(b64: str) -> str:
    return '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Acceso protegido</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0e1913;color:#eef1ee;font:15px system-ui,sans-serif}
.b{background:#16251c;border:1px solid #243a2c;border-radius:20px;padding:28px;max-width:340px;width:90%;text-align:center}
input{width:100%;padding:11px 14px;border-radius:12px;border:1px solid #2f4a39;background:#0e1913;color:#fff;font:inherit;margin:14px 0 10px;text-align:center}
button{width:100%;padding:11px;border:0;border-radius:12px;background:#5fa01f;color:#fff;font:700 15px system-ui;cursor:pointer}#e{color:#ff8a8a;min-height:20px;font-size:13px}</style></head>
<body><div class="b" id="b"><div style="font-size:34px">🔒</div><h3 style="margin:6px 0">Dashboard protegido</h3><div style="color:#9fb3a5;font-size:13px">Ingresa el código de acceso</div>
<input id="c" type="password" placeholder="Código" autofocus><button id="g">Entrar</button><div id="e"></div></div>
<script>const P="'''+b64+'''";
'''+JS+'''
async function go(code,silent){try{const h=await dec(code,P);try{sessionStorage.setItem("dashcode",code)}catch(e){}document.open();document.write(h);document.close();}catch(e){if(!silent)document.getElementById("e").textContent="Código incorrecto"}}
document.getElementById("g").onclick=()=>{document.getElementById("e").textContent="Verificando…";go(document.getElementById("c").value,false)};
document.getElementById("c").onkeydown=e=>{if(e.key==="Enter")document.getElementById("g").click()};
let s=null;try{s=sessionStorage.getItem("dashcode")}catch(e){}if(s)go(s,true);
</script></body></html>'''
if __name__=="__main__":
    code=open(sys.argv[1],encoding="utf-8").read().strip()
    html=open(sys.argv[2],"rb").read()
    open(sys.argv[3],"w",encoding="utf-8").write(wrapper(enc(html,code)))
