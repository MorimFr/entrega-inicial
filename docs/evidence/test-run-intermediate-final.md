# Homologação da Entrega 2 - 14/10/2026

Implementação homologada: commit `f863ddb`, Issue #25, especificação 0.4.0, API 0.3.0.

| Ambiente | Passagem | Cobertura de linhas | Resultado |
|---|---|---|---|
| Windows / Python 3.14.7 local | 55/55 (100%) | 99,66% | exit 0 |
| Docker Linux / Python 3.12.15 | 55/55 (100%) | 99,69% | exit 0 |
| GitHub Actions / Python 3.12.15 | 55/55 (100%) | 99,69% | quality aprovado |

Os logs brutos estão em `docs/evidence/entrega2/local.log` e `docker.log`. O número de testes passou
de 26 (Entrega 1) para 34 (primeira implementação da Entrega 2) e 55 (homologação final).
Regressões iniciais: 12 falhas/1 aprovação antes das correções, extrato em `regression-before.txt`.

Comandos reproduzíveis:

```powershell
.\scripts\test.ps1
docker compose --profile test run --rm --build tests
```

O Dockerfile fixa a imagem-base Python 3.12 por digest. O Pytest também gera `test-results.xml`
(JUnit) e `coverage.xml`; CI publica esses arquivos e stdout como artefatos. 100% de passagem mede
casos aprovados sobre coletados, não cobertura. Nenhum teste anterior foi removido.

## Demonstração da aplicação integrada

Usada uma instância local exclusiva: `docker compose -p campusflow-entrega2 up -d --build --wait api`.
`python scripts/demo_api.py` exercitou health, catálogo, criação 201, consulta 200, conflito 409,
filtro de usuário 200, cancelamento 200 e repetição 409. Depois da recriação do contêiner, o comando
`python scripts/demo_api.py --reservation-id ID` confirmou o estado cancelado persistente.
Logs: `demo.log`, `persistence.log`. Apenas dados fictícios foram criados. A instância foi encerrada;
o volume de demonstração foi preservado. Nenhum serviço de outro projeto foi alterado.

## Avisos observados

O ambiente local Python 3.14 emite depreciações do FastAPI/asyncio; o Docker 3.12.15 emitiu um aviso
de depreciação do alias BlockingPortal no Starlette/AnyIO. Não são falhas; não foram ocultados.
Versões diretas estão fixadas; dependências transitivas podem variar, por isso os logs preservam
as versões efetivamente utilizadas. Não se afirma reprodutibilidade bit a bit.

## Execução verificada no GitHub

Run [38572174867](https://github.com/MorimFr/entrega-inicial/actions/runs/38572174867), commit
`f863ddb`, quality aprovado em 19 s, 55 passed e artefato `test-evidence-38572174867`.
O PR #24 terá novo check após a publicação documental/PDF. O run acima comprova o código homologado;
o aceite humano deve conferir o check do último commit também.
