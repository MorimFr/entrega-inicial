# Evidência de execução do test harness — Entrega 2

## Resumo

| Ambiente | Resultado | Cobertura | Exit code |
|---|---:|---:|---:|
| Windows / Python 3.14.7 | 34 aprovados | 98,44% | 0 |
| Docker / Linux / Python 3.12.14 | 34 aprovados | 98,59% | 0 |
| GitHub Actions / Python 3.12 | aguardando execução do PR | — | — |

Todos os testes coletados passaram. “100% de passagem” significa `34 passed / 34 collected`; a
cobertura de linhas é uma métrica distinta e permanece acima do gate obrigatório de 90%.

## Execução local

- **Data:** 1 de setembro de 2026
- **Comandos:** `python -m ruff check .` e `python -m pytest`

```text
All checks passed!
collected 34 items
tests\api\test_reservations_api.py ..........                            [ 29%]
tests\integration\test_sqlite_repository.py ...                         [ 38%]
tests\unit\test_reservation_service.py .....................            [100%]
TOTAL                               257      4    98%
Required test coverage of 90% reached. Total coverage: 98.44%
34 passed, 91 warnings in 0.66s
```

Os avisos são de depreciação do `asyncio` emitidos pelo FastAPI sob Python 3.14 local. O runtime
declarado e usado no Docker/CI é Python 3.12, onde eles não aparecem.

## Ambiente padronizado Docker

- **Comando:** `docker compose --profile test run --rm --build tests`
- **Imagem-base:** `python:3.12-slim`

```text
platform linux -- Python 3.12.14, pytest-8.4.1, pluggy-1.6.0
collected 34 items
tests/api/test_reservations_api.py ..........                            [ 29%]
tests/integration/test_sqlite_repository.py ...                          [ 38%]
tests/unit/test_reservation_service.py .....................             [100%]
TOTAL                               284      4    99%
Required test coverage of 90% reached. Total coverage: 98.59%
34 passed in 0.93s
```

**Resultado:** imagem construída, contêiner criado, suíte completa aprovada, cobertura acima do gate
e exit code 0.

## O que a suíte da Entrega 2 acrescentou

- regressão RN-03 para participantes `0` e `-1`;
- listagem por usuário, filtro `active`/`cancelled`, resultado vazio e query inválida;
- persistência da reserva e do cancelamento entre instâncias SQLite;
- reinício da aplicação FastAPI sobre o mesmo banco;
- consultas de sala, disponibilidade e ausência no adaptador persistente.

## GitHub Actions

Esta seção será atualizada com URL, commit e artefato reais depois que o PR da Sprint 2 disparar o
workflow. A evidência não será preenchida antecipadamente.
