# Índice de submissão — Entrega 2 (etapa intermediária)

## Identificação

- **Integrante:** Felipe Amorim Monteiro
- **RA:** 22452139
- **Repositório:** <https://github.com/MorimFr/entrega-inicial>
- **Marco:** Sprint 2 — Entrega intermediária

## Conteúdo consolidado

| Exigência | Evidência versionada |
|---|---|
| solução funcional | `campusflow/`, `compose.yaml`, documentação OpenAPI |
| refinamento e erro lógico | `docs/LOGICAL_ERRORS.md`, `docs/SPEC_CHANGELOG.md` |
| especificação final | `docs/SPECIFICATION.md` versão 0.3.0 |
| testes automatizados | `tests/`, `docs/evidence/test-run-intermediate.md` |
| arquitetura e trade-offs | README e ADRs 001–003 |
| relato de experiência | `docs/EXPERIENCE_REPORT.md` |
| comparação e ética de IA | `docs/AI_ETHICS.md` |
| governança | marco/Issues #13–#19 e PRs da Sprint 2 |

## Comandos do harness

```powershell
.\scripts\test.ps1
docker compose --profile test run --rm --build tests
```

O PDF final será gerado a partir deste conteúdo após anexar evidências visuais reais da execução,
dos PRs revisados e da governança. Prints não serão simulados nem substituídos por montagens.
