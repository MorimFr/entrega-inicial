# Evidência de execução do test harness — Entrega 2

## Resumo

| Ambiente | Resultado | Cobertura | Exit code |
|---|---:|---:|---:|
| Windows / Python 3.14.7 | 34 aprovados | 98,44% | 0 |
| Docker / Linux / Python 3.12.14 | 34 aprovados | 98,59% | 0 |
| GitHub Actions / Python 3.12.14 | 34 aprovados | 98,59% | 0 |

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

- **PR:** [#20 — feat: consolida Entrega 2 do CampusFlow](https://github.com/MorimFr/entrega-inicial/pull/20)
- **Primeira execução verde:** [run 33582687001](https://github.com/MorimFr/entrega-inicial/actions/runs/33582687001)
- **Commit validado:** `f2a34644adfe6e72b14db2fd0f434947f4f41838`
- **Job:** `quality`, sucesso em 16 segundos
- **Ambiente:** Ubuntu / Python 3.12.14
- **Resultado:** Ruff aprovado; 34/34 testes; cobertura 98,59%
- **Artefato:** `test-evidence-33582687001`, contendo `test-output.log` e `coverage.xml`

```text
All checks passed!
platform linux -- Python 3.12.14, pytest-8.4.1, pluggy-1.6.0
collected 34 items
Required test coverage of 90% reached. Total coverage: 98.59%
34 passed in 0.46s
```

O commit documental que registra esta própria execução dispara um novo check no mesmo PR. No PDF,
deve ser usada a execução verde associada ao commit final do PR.
