# Lab: Nuclei contra uma isca local

- `isca.py`: servidor HTTP mínimo (Python, sem dependência). Responde `200 OK` pra qualquer
  caminho e devolve a requisição inteira no corpo. Não faz requisição pra fora nem executa nada.
- `docker-compose.yml`: sobe a isca e o Nuclei na mesma rede Docker. O Nuclei roda os
  templates `cve` de severidade `critical,high` contra `http://isca:8080`, com `-ni` (sem
  callback pra fora), e grava o resultado em `resultados/scan.jsonl`.
- `validar.sh`: roda **um** template com `-debug` pra ver a prova crua.

## Rodar

```bash
docker compose up --abort-on-container-exit
cat resultados/scan.jsonl
./validar.sh                 # padrão: CVE-2026-77806
./validar.sh CVE-XXXX-YYYY   # qualquer outro id que tenha acendido
docker compose down
```

Na primeira vez o Nuclei baixa os templates (precisa de internet pra isso, só pra baixar).

## Quer ver a isca sozinha?

```bash
python3 isca.py
curl -s http://localhost:8080/qualquer/coisa -d 'echo oi'
```

Tu vai receber de volta a tua própria requisição. É só isso que ela faz.
