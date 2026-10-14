# Inspeção de erros lógicos e estratégias de correção

Este documento registra falhas reais observadas durante o ciclo; limitações conhecidas não são
apresentadas como bugs e resultados não foram inventados.

## ERRO-01 — RN-03 aplicada apenas na fronteira HTTP

- **Origem:** Issue [#13](https://github.com/MorimFr/entrega-inicial/issues/13).
- **Comportamento esperado:** o serviço deve rejeitar qualquer quantidade não positiva.
- **Comportamento observado:** chamadas diretas ao `ReservationService` aceitavam `0` e `-1`, pois
  apenas o `Field(ge=1)` do Pydantic protegia a rota HTTP.
- **Causa raiz:** uma regra de negócio foi parcialmente delegada ao adaptador de entrada.
- **Teste que revelou:**
  `python -m pytest tests/unit/test_reservation_service.py -k non_positive --no-cov`.

```text
collected 20 items / 18 deselected / 2 selected
tests\unit\test_reservation_service.py FF
E   Failed: DID NOT RAISE <class 'campusflow.errors.DomainError'>
2 failed, 18 deselected
```

- **Correção:** validação `attendees <= 0` no serviço e erro estável
  `invalid_attendee_count`; o schema continua rejeitando entradas inválidas cedo, mas deixou de ser
  a única proteção.
- **Prevenção:** regressão parametrizada com `0` e `-1`; RN-03 e contrato 422 refinados na versão
  0.3.0 da especificação.

## ERRO-02 — cobertura não coletada no primeiro contêiner

- **Origem:** refinamento do harness da Entrega 1, consolidado na Entrega 2.
- **Comportamento observado:** os 26 testes passavam no contêiner, mas o comando executável `pytest`
  não carregava o mesmo contexto de cobertura usado pelo módulo Python e o gate reportava 0%.
- **Causa operacional:** diferença entre o atalho instalado e `python -m pytest` no ambiente da
  imagem.
- **Correção:** `compose.yaml` passou a executar `python -m pytest`, alinhando Docker, execução local
  e CI.
- **Evidência posterior:** 26 aprovados e 99,48% no Docker da Entrega 1; o log permanece em
  `docs/evidence/test-run.md`.

## Conclusão do loop SDD

Nos dois casos, a correção não foi “fazer o teste passar” isoladamente. O ciclo foi:

```text
falha observável -> regra/contrato revisado -> implementação mínima -> regressão -> suíte completa
```

A homologação só ocorre quando especificação, código e testes descrevem o mesmo comportamento.

## Homologação final - 14/10/2026 (Issue #25)

Comando antes das correções: `python -m pytest tests/integration/test_homologation.py --no-cov -q`.
Resultado real: **12 failed, 1 passed**. O commit `7808618` preserva os testes anteriores à correção.

| Falha | Evidência inicial | Causa | Correção e prevenção |
|---|---|---|---|
| ERRO-03: tipo de participantes | bool/float aceitos; string causa TypeError; HTTP responde 201 | coerção HTTP e checagem somente de sinal | inteiro estrito no schema e serviço; 9 casos nos dois adaptadores/HTTP |
| ERRO-04: ordenação | SQLite retorna 08:00-03 antes de 10:00Z | ORDER BY de texto ISO | converter para datetime e ordenar instante/ID; regressão nos dois adaptadores |
| ERRO-05: limite diário | terceira reserva aceita em UTC-03 ao escrever duas datas como dia seguinte em Z | `.date()` no offset de cada registro | calendário UTC-03 comum; regressão nos dois adaptadores |
| ERRO-06: janela de corrida | inspeção mostra checagens e gravação em conexões distintas | ausência de unidade de trabalho | transaction na porta; tests concorrentes de criação, limite, cancelamento e instâncias distintas |

ERRO-06 foi identificado estruturalmente; não se afirma que um incidente em produção foi observado.
Os testes concorrentes confirmam o estado final, sem depender de qual thread vence. Testes de rollback
confirmam que uma falha não deixa gravação parcial. A suíte final mantém todos os testes anteriores.
