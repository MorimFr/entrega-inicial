# Índice de submissão — Entrega 2 (etapa intermediária)

## Identificação

- **Integrante:** Felipe Amorim Monteiro
- **RA:** 22452139
- **Repositório:** <https://github.com/MorimFr/entrega-inicial>
- **Marco:** Sprint 2 — Entrega intermediária
- **PR de implementação:** <https://github.com/MorimFr/entrega-inicial/pull/20>
- **PR de publicação/homologação:** <https://github.com/MorimFr/entrega-inicial/pull/24>
- **PDF consolidado:** `docs/ENTREGA_INTERMEDIARIA.pdf` (55/55 casos, especificação 0.4.0).

## Conteúdo consolidado

| Exigência | Evidência versionada |
|---|---|
| solução funcional | `campusflow/`, `compose.yaml`, documentação OpenAPI |
| refinamento e erro lógico | `docs/LOGICAL_ERRORS.md`, `docs/SPEC_CHANGELOG.md` |
| especificação final | `docs/SPECIFICATION.md` versão 0.4.0 |
| testes automatizados | `tests/`, `docs/evidence/test-run-intermediate-final.md` e logs em `entrega2/` |
| arquitetura e trade-offs | README e ADRs 001-004 |
| relato de experiência | `docs/EXPERIENCE_REPORT.md` |
| comparação e ética de IA | `docs/AI_ETHICS.md` |
| governança | marco/Issues #13–#19 e PRs da Sprint 2 |

## Comandos do harness

```powershell
.\scripts\test.ps1
docker compose --profile test run --rm --build tests
```

O PDF usa logs reais e links verificáveis, que satisfazem a alternativa prints/logs do enunciado.
O estado da publicação é explicitado na capa: a versão candidata requer o aceite humano do PR #24.
Somente após o merge e a conferência da main deve ser submetida a versão definitiva.

## Adaptação para equipe individual

MorimFr e SrMorim são contas do mesmo aluno. Felipe informou autorização do professor para a
autorrevisão nessa configuração. Não se afirma revisão independente ou participação de outra pessoa.

## Prints opcionais para enriquecer o relatório

1. Terminal Docker mostrando o comando, Python 3.12.15, 55 passed e cobertura 99,69%.
2. Job quality do CI final, com testes/artefatos visíveis.
3. PR #20 e PR #24 mostrando aprovação, check e merge (após a publicação).
4. Marco Sprint 2/Issues encerradas e proteção de main/develop.
5. Swagger com uma reserva criada e consultada; usar apenas identificadores fictícios.

Esses prints são opcionais porque os logs e URLs já estão no PDF. Não usar prints antigos como se
fossem da execução final de outubro.
