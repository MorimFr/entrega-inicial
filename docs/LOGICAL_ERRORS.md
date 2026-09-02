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
