# CampusFlow — Entrega inicial

## Identificação

- **Integrante:** Felipe Amorim Monteiro
- **RA:** 22452139
- **Repositório público:** <https://github.com/MorimFr/entrega-inicial>
- **Relatório para o Moodle:** [`ENTREGA_INICIAL_FINAL.pdf`](ENTREGA_INICIAL_FINAL.pdf)

## Resumo

O CampusFlow é uma API de reserva de salas de estudo desenvolvida com Python 3.12, FastAPI e
Pydantic. A arquitetura separa contratos HTTP, casos de uso, domínio e persistência em memória. A
especificação SDD contém requisitos numerados, regras de negócio, contratos, componentes e
rastreabilidade para os testes.

O Codex foi usado como agente auxiliar. `AGENTS.md` mantém as regras do fluxo SDD e os comandos de
validação. Toda contribuição passou por testes, GitHub Actions, revisão de colaborador diferente do
autor e Pull Request.

## Execução do harness

```text
docker compose --profile test run --rm --build tests
```

Resultados comprovados:

- 26 testes aprovados;
- cobertura de 99,48% no Docker e GitHub Actions;
- Ruff aprovado;
- Python 3.12.14 no ambiente padronizado;
- logs e `coverage.xml` publicados como artefato do CI.

## Evidências incluídas no PDF

1. construção da imagem e execução dos testes no Docker;
2. resultado final do harness e cobertura;
3. execuções verdes do GitHub Actions;
4. Issues e milestone da Sprint 1;
5. PR #10 de feature para `develop`, com aprovação;
6. PR #11 de `develop` para `main`, com aprovação e checks;
7. conteúdo final da branch `main`;
8. proteção da branch `main`;
9. proteção da branch `develop`.

Os PNGs originais estão em `docs/evidence/screenshots/`, e o log textual está em
`docs/evidence/test-run.md`.
