#!/usr/bin/env bash
# Valida UM achado do Nuclei na isca local: roda só aquele template com -debug e mostra a
# requisição e a resposta de verdade. Uso: ./validar.sh [template-id]  (padrão: o que acendeu aqui)
set -euo pipefail
cd "$(dirname "$0")"
ID="${1:-CVE-2026-77806}"
docker compose up -d isca >/dev/null
docker compose run --rm nuclei -u http://isca:8080 -id "$ID" -ni -debug -nc
docker compose down >/dev/null
