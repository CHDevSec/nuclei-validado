#!/usr/bin/env python3
"""
Servidor ISCA de laboratório (roda só na tua máquina).

Responde 200 OK pra QUALQUER caminho e devolve no corpo a requisição inteira que recebeu
(eco). É o mesmo comportamento do servidor isca do vídeo: um scanner que procura uma palavra
"refletida" na resposta vai achar, porque o servidor devolve tudo. Parece vulnerável a tudo,
e não é nada.

Não faz requisição pra fora, não executa nada, não guarda nada.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Isca(BaseHTTPRequestHandler):
    server_version = "isca-lab"
    sys_version = ""

    def _eco(self):
        n = int(self.headers.get("Content-Length") or 0)
        corpo = self.rfile.read(n) if n else b""
        req = f"{self.command} {self.path} {self.request_version}\r\n{self.headers}".encode() + corpo
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(req)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(req)

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_HEAD = _eco

    def log_message(self, fmt, *args):
        print("isca <-", self.command, self.path)


if __name__ == "__main__":
    print("isca no ar em http://0.0.0.0:8080 (Ctrl+C pra parar)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Isca).serve_forever()
