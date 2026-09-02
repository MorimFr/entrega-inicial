# Histórico de refinamento da especificação

Este registro separa evolução de requisitos de alterações meramente editoriais. Toda mudança deve
informar motivo, impacto e evidência.

## 0.2.0 — 1 de setembro de 2026

**Gatilho:** revisão do desenho dos testes antes da implementação.

- RN-01 passou a exigir fuso horário. Sem isso, dois clientes poderiam interpretar o mesmo horário
  local de maneiras diferentes.
- RN-05 formalizou intervalos semiabertos e reservas adjacentes. A versão inicial dizia apenas
  “sem conflito”, deixando a fronteira ambígua.
- RN-06 foi refinada de “duas reservas por dia” para “duas reservas ativas pela data de início”. Isso
  define o efeito de cancelamento e de reservas que atravessam meia-noite.
- RN-07 definiu HTTP 409 para um segundo cancelamento, tornando a falha observável.
- O contrato de erro ganhou `code` estável além da mensagem, evitando testes frágeis por texto.

**Impacto:** schemas, serviço e casos de teste de períodos, adjacência, cancelamento e limite diário.

## 0.1.0 — 1 de setembro de 2026

**Gatilho:** especificação inicial do grupo.

- Definidos o problema, RF-01 a RF-06, limites de duração/capacidade, prevenção de conflitos e
  persistência em memória para a primeira iteração.

## Modelo para próximas alterações

```text
## X.Y.Z — data
Gatilho: teste, revisão ou feedback (inclua Issue/PR).
- Antes:
- Depois:
- Motivo:
Impacto: requisitos, contratos, código e testes afetados.
```

