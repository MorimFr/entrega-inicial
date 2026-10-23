# Execução da candidata v1.0.0 - Issue #26

Data: 23/10/2026. Estes são resultados reais da branch `release/entrega-final`, não uma
declaração antecipada de release publicada ou de vídeo gravado.

## Harness padronizado

```powershell
docker compose --profile test run --rm --build tests
```

- Ruff: aprovado.
- Python 3.12.15 / Linux; pytest 8.4.1.
- **63/63 aprovados, 0 falhas, 0 erros, 0 ignorados (100% de passagem).**
- **327/328 linhas executáveis cobertas = 99,70%**, gate mínimo 90%.
- API, serviço, schemas, SQLite, domínio e política de tempo: 100% de linhas cobertas.
- Porta/adaptador em memória: uma linha não executada, tratamento defensivo de recurso ausente
  em `repository.py:100`; não é uma falha observada nem trecho morto a remover.
- Um aviso de depreciação de dependência Starlette/AnyIO foi mantido na saída; não é teste falho.
- Não se coletou cobertura de branches. Cobertura de linhas não comprova ausência de bugs.

Fontes: `docker.log`, `junit.xml`, `coverage.xml`. A duração JUnit e o timestamp estão no XML;
o resumo do console pode arredondar o tempo total de outra forma. O HTML navegável é gerado em
`artifacts/htmlcov/index.html`; artefatos de CI ficam no workflow correspondente.

## Validações adicionais

- `local.log`: 63 aprovados com Python 3.14.7 no host, cobertura 99,67%. Resultado complementar;
  a base de homologação é o Python 3.12 do contêiner. Avisos de depreciação não foram escondidos.
- `demo.log`: chamadas HTTP reais à API Compose. Sucesso 200/201, conflito 409, cancelamento,
  filtro por usuário e entrada inválida 422, usando apenas dados fictícios.
- `persistence.log`: a reserva cancelada continuou consultável depois de `--force-recreate`.
- `runtime.log`: usuário uid 999 (não root), pacote/API 1.0.0 e pytest ausente no runtime.
- `dependencies.log`: versões efetivamente instaladas no target tests; runtime tem manifest em
  `runtime.log`. Não se promete build bit a bit: transitivas/build tools ainda têm resolução dinâmica.

O teste operacional usou projeto Compose isolado `campusflow-final-validation`, porta 18000, e
foi encerrado com `down` sem excluir volume. Logs Docker conservam os IDs e mensagens originais.

## Integridade e aceite

`python scripts/export_openapi.py --check` e `docker compose config --quiet` aprovados. Inspeção
de arquivos versionados não encontrou bancos, `.env`, bytecode ou padrões de credenciais privadas.
Isso é higiene básica, não uma auditoria de segurança completa.

O PR final deve ser aprovado por autorrevisão humana na adaptação individual informada. Depois
do merge, executar/verificar o CI da main e vincular a tag v1.0.0 ao commit aprovado. O vídeo real
de 3-5 minutos e seu link continuam necessários antes da emissão do PDF definitivo.
