# Evidência de execução do test harness

## Execução local comprovada

- **Data:** 1 de setembro de 2026
- **Comando:** `.\scripts\test.ps1`
- **Sistema:** Windows, Python 3.14.7
- **Resultado:** Ruff aprovado; 26 testes aprovados; cobertura de 99,39%.
- **Exit code:** 0

```text
All checks passed!
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Monteiro\Documents\ceub\entrega-inicial
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.2, cov-6.2.1
collected 26 items

tests\api\test_reservations_api.py ........                              [ 30%]
tests\unit\test_reservation_service.py ..................                [100%]

=============================== tests coverage ================================
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
campusflow\__init__.py         0      0   100%
campusflow\api.py             46      0   100%
campusflow\domain.py          11      0   100%
campusflow\errors.py          18      0   100%
campusflow\repository.py      29      1    97%   72
campusflow\schemas.py         13      0   100%
campusflow\service.py         47      0   100%
--------------------------------------------------------
TOTAL                        164      1    99%
Coverage XML written to file coverage.xml
Required test coverage of 90% reached. Total coverage: 99.39%
======================= 26 passed, 54 warnings in 0.40s ========================
```

Os avisos vêm de uma API do `asyncio` usada pelo FastAPI que está depreciada no Python 3.14; não são
falhas da aplicação. O CI e o contêiner usam Python 3.12, versão-base declarada pelo projeto.

## Ambiente Docker

O arquivo Compose foi validado com sucesso por `docker compose --profile test config --quiet`. A CLI
Docker está instalada, mas o daemon Linux não estava disponível nesta máquina durante esta execução;
por isso não há alegação de teste em contêiner neste registro. Assim que o Docker Desktop estiver
ativo, produzir a evidência com:

```text
docker compose --profile test run --rm --build tests
```

## GitHub Actions

Execução real do Pull Request #10:

- **Workflow:** `Test harness`
- **Run:** [33577382487](https://github.com/MorimFr/entrega-inicial/actions/runs/33577382487)
- **Commit:** `b9915b3a495033d12555d564cef889905ff74962`
- **Ambiente:** Ubuntu / Python 3.12.14
- **Job `quality`:** sucesso em 20 segundos
- **Resultado:** Ruff aprovado; 26 testes aprovados; cobertura 99,48%
- **Artefato:** `test-evidence-33577382487` (`test-output.log` e `coverage.xml`)

```text
All checks passed!
platform linux -- Python 3.12.14, pytest-8.4.1, pluggy-1.6.0
collected 26 items
Required test coverage of 90% reached. Total coverage: 99.48%
============================== 26 passed in 0.34s ==============================
```
