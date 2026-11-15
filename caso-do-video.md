# O caso do vídeo: 32 achados num servidor isca

Scan feito em 13/nov/2026 com o Nuclei v3.11.1 (imagem oficial no Docker):

```bash
nuclei -u http://honey.scanme.sh -severity critical,high -tags cve
```

- `[INF] Templates loaded for current scan: 2935`
- **32 achados**: 18 críticos + 14 altos, em 1 min 56 s.
- CVEs de produtos que não convivem no mesmo servidor: Exchange, Zimbra, Jenkins, Cisco
  HyperFlex, LogonTracer, AirMedia/wePresent e outros, **todos no mesmo IP**.

> Os CVEs são reais. O que é isca é o **alvo**. E não há fonte pública dizendo que esse host é
> "oficial" ou liberado pra scan; por isso o lab deste repo usa uma isca **local**.

## O que o `-debug` mostrou (CVE-2021-26855, "Exchange SSRF")

O template manda um cookie de SSRF apontando pra um endereço único de teste (OAST) e considera
vulnerável se esse endereço **receber uma chamada** (`matchers: interactsh_protocol` contém
`http`). Foi o que aconteceu, mas olha como:

**Requisição** (resumida):
```text
GET /owa/auth/x.js HTTP/1.1
Host: honey.scanme.sh
Cookie: X-AnonResource=true; X-AnonResource-Backend=<id>.oast.pro/ecp/default.flt?~3;
```

**Resposta** (o corpo é a própria requisição ecoada):
```text
HTTP/1.1 200 OK
Content-Length: 307
Content-Type: text/html

GET /owa/auth/x.js HTTP/1.1
Host: honey.scanme.sh
...
```

**Interação OAST** (o callback que fez o template casar):
```text
protocol: http
GET / HTTP/1.1   Host: <id>.oast.pro
User-Agent: Go-http-client/1.1
remote-address: o IP do próprio alvo
```

## Por que é isca, e não Exchange
- **Eco total:** 31 de 31 respostas registradas são `200 OK` com o request devolvido no corpo.
- **Callback de tudo:** 29 de 31 achados casaram por callback OAST, todos vindos do IP do alvo.
- **O callback é de um cliente Go** (`Go-http-client/1.1`). Exchange de verdade é IIS/.NET.
- **Nenhum cabeçalho de Exchange** na resposta; e o mesmo host "seria" Exchange, Zimbra,
  Jenkins e Cisco ao mesmo tempo.

Conclusão defensável: **parecia vulnerável a tudo, e era uma isca.** O scanner fez o trabalho
dele (apontou indícios); quem decide se é bug é a validação.
