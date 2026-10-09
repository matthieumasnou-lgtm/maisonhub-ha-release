import os, sqlite3, json, datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from threading import Lock
DB_LOCK = Lock()
DB='/data/maisonhub.db'
os.makedirs('/data',exist_ok=True)
with sqlite3.connect(DB) as db:
    db.execute('CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, text TEXT NOT NULL, created TEXT NOT NULL)')
PAGE="""<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Maison Hub Lab</title><style>body{margin:0;background:#f4f0e9;color:#1d2c34;font:16px system-ui}main{max-width:600px;margin:auto;padding:26px 18px}h1{font-size:32px}article{background:white;border-radius:20px;padding:16px;margin:12px 0;box-shadow:0 4px 20px #0001}textarea{width:100%;box-sizing:border-box;border:1px solid #ccc;border-radius:14px;padding:14px;font:inherit}button{background:#1d3939;color:white;border:0;padding:13px 20px;border-radius:13px;margin-top:10px;font-weight:700}small{color:#777}header{padding:14px;background:#1c343b;color:white;text-align:center}</style><header>MAISON HUB · LABORATOIRE</header><main><h1>Le mur familial</h1><p>Prototype privé réservé aux administrateurs Home Assistant. Ne pas y mettre de données sensibles.</p><form id="f"><textarea id="t" maxlength="1000" required placeholder="Écrire un message de test..."></textarea><button>Publier</button></form><section id="messages"></section></main><script>async function load(){let r=await fetch('api/messages');if(!r.ok)return;let a=await r.json();document.querySelector('#messages').replaceChildren(...a.map(m=>{let e=document.createElement('article');let p=document.createElement('p');p.textContent=m.text;let s=document.createElement('small');s.textContent=m.created;e.append(p,s);return e}))}document.querySelector('#f').onsubmit=async e=>{e.preventDefault();let t=document.querySelector('#t');let r=await fetch('api/messages',{method:'POST',headers:{'Content-Type':'application/json','X-MaisonHub-Request':'1'},body:JSON.stringify({text:t.value})});if(r.ok){t.value='';load()}else alert('Erreur de publication')};load();</script></html>"""
class Handler(BaseHTTPRequestHandler):
    def respond(self, status, mime, body):
        self.send_response(status)
        for k,v in [('Content-Type',mime),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Content-Length',str(len(body)))]:
            self.send_header(k,v)
        self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'self'")
        self.send_header('Referrer-Policy','no-referrer')
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        path=urlparse(self.path).path.rstrip('/')
        if path.endswith('/api/messages'):
            with sqlite3.connect(DB) as db:
                rows=db.execute('SELECT text,created FROM messages ORDER BY id DESC LIMIT 100').fetchall()
            return self.respond(200,'application/json',json.dumps([{'text':t,'created':c} for t,c in rows]).encode())
        if '/api/' in path:
            return self.send_error(404)
        return self.respond(200,'text/html; charset=utf-8',PAGE.encode())
    def do_POST(self):
        if not urlparse(self.path).path.endswith('/api/messages'):
            return self.send_error(404)
        if self.headers.get('X-MaisonHub-Request') != '1' or self.headers.get('Sec-Fetch-Site','same-origin') not in ('same-origin','none'):
            return self.send_error(403)
        if self.headers.get('Content-Type','').split(';')[0].strip().lower() != 'application/json':
            return self.send_error(415)
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<1 or n>4096: raise ValueError('length')
            payload=json.loads(self.rfile.read(n))
            text=payload['text']
            if not isinstance(text,str): raise ValueError('text type')
            text=text.strip()
            if not 1<=len(text)<=1000: raise ValueError('text')
        except (ValueError,KeyError,TypeError,AttributeError):
            return self.send_error(400)
        with DB_LOCK, sqlite3.connect(DB) as db:
            db.execute('INSERT INTO messages(text,created) VALUES (?,?)',(text,datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='minutes')))
        self.respond(201,'application/json',b'{"ok":true}')
ThreadingHTTPServer(('0.0.0.0',8099),Handler).serve_forever()
