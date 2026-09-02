# CampusFlow — Entrega inicial

> Documento-fonte do PDF de submissão. Preencha os campos marcados, anexe os prints indicados e
> exporte como um único PDF antes de cada integrante enviar o mesmo arquivo no Moodle.

## 1. Repositório

**Link direto:** <https://github.com/MorimFr/entrega-inicial>

**Visibilidade:** público ou acesso concedido aos professores.

## 2. Integrantes

| Nome completo | RA | Responsabilidade principal na Sprint 1 |
|---|---|---|
| Felipe Amorim Monteiro | 22452139 | Especificação, implementação, testes, CI e documentação |

O trabalho possui um único integrante. Por isso, a aprovação “entre membros” descrita no enunciado
não pode ocorrer literalmente. Para não fabricar evidência, a revisão deve ser solicitada ao
professor, monitor ou colaborador externo autorizado, conforme orientação prévia do docente.

## 3. Resumo técnico

O CampusFlow é uma API de reserva de salas de estudo. A solução usa Python 3.12, FastAPI e Pydantic,
com regras isoladas em um serviço de aplicação e persistência em memória atrás de uma interface. A
arquitetura permite testar regras sem infraestrutura externa e substituir o adaptador de persistência
em iterações futuras.

O desenvolvimento segue SDD: requisitos e regras numeradas em `docs/SPECIFICATION.md` orientam os
contratos, testes e implementação. Refinamentos causados pela revisão dos testes estão em
`docs/SPEC_CHANGELOG.md`, e decisões estruturais estão em `docs/adr/`.

O Codex foi usado como agente auxiliar de código. `AGENTS.md` fornece ao agente a especificação como
fonte de verdade, limites arquiteturais e comandos de validação. Toda contribuição, inclusive gerada
por IA, deve passar por Issue, Pull Request, CI e aprovação humana.

## 4. Execução do harness

### Ambiente padronizado (recomendado)

```bash
docker compose --profile test run --rm tests
```

### Ambiente local

```powershell
.\scripts\setup.ps1
.\scripts\test.ps1
```

O harness executa Ruff, testes unitários e testes dos contratos HTTP. O Pytest gera `coverage.xml` e
falha se a cobertura do pacote ficar abaixo de 90%. No GitHub, o workflow `Test harness` repete a
validação em cada PR e publica log/cobertura como artefato.

## 5. Evidências

### 5.1 Pipeline GitHub Actions

O workflow `Test harness` executou com sucesso no Pull Request #10 em Python 3.12.14: Ruff aprovado,
26 testes aprovados e cobertura de 99,48%. Execução:
<https://github.com/MorimFr/entrega-inicial/actions/runs/33577382487>. O artefato
`test-evidence-33577382487` contém `test-output.log` e `coverage.xml`.

`INSERIR PRINT: execução verde acima, com URL e hash do commit visíveis.`

### 5.2 Log do test harness

Execução local comprovada em 1 de setembro de 2026: Ruff aprovado, **26 testes aprovados**, cobertura
total de **99,39%** e exit code 0. O log integral está em `docs/evidence/test-run.md`. Substituir ou
complementar com o artefato `test-output.log` do GitHub Actions após o primeiro PR.

### 5.3 Execução no Docker

Execução comprovada com Docker Desktop 4.86.0/engine 29.7.2 e Python 3.12.14: imagem construída,
contêiner criado, **26 testes aprovados**, cobertura de **99,48%** e exit code 0. Comando:

```text
docker compose --profile test run --rm --build tests
```

O log textual integral está em `docs/evidence/test-run.md`.

### 5.4 Governança e trabalho em equipe

`INSERIR PRINT: GitHub Project com Issues, responsáveis e estados.`

`INSERIR PRINT: PR com comentários, CI verde e revisão do professor/monitor/colaborador autorizado
para a equipe individual.`

`INSERIR PRINT: ruleset da branch main exigindo PR e status check.`

## 6. Checklist antes de exportar

- [ ] URL do repositório abre sem pedir acesso indevido.
- [x] Nome e RA do integrante estão corretos.
- [ ] Badge e links do README apontam para o repositório real.
- [ ] Issues/Project mostram divisão real da sprint.
- [ ] A forma de revisão para equipe individual foi confirmada com o docente e evidenciada.
- [ ] Workflow do commit entregue está verde.
- [ ] Prints estão legíveis e mostram contexto/URL.
- [ ] Campos `PREENCHER` e `INSERIR PRINT` foram removidos.
- [x] O PDF final será enviado pelo único integrante.
