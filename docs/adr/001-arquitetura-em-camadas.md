# ADR-001: domínio isolado e persistência em memória

- **Estado:** aceita
- **Data:** 1 de setembro de 2026

## Contexto

A entrega precisa demonstrar arquitetura, desenvolvimento iterativo e testabilidade antes de exigir
infraestrutura de produção. Acoplar regras diretamente às rotas dificultaria testes e uma futura
troca de persistência.

## Decisão

Separar adaptador HTTP, serviço de aplicação, domínio e porta de repositório. Usar um adaptador em
memória na primeira iteração e injetá-lo no serviço.

## Consequências

- regras podem ser testadas sem abrir porta ou iniciar banco;
- API e persistência podem evoluir independentemente;
- reiniciar a aplicação apaga dados;
- concorrência entre processos não é resolvida nesta iteração;
- uma futura persistência SQL deve implementar `ReservationRepository` e garantir atomicidade.

## Alternativas consideradas

- **Regras nas rotas:** menos arquivos, mas maior acoplamento e repetição.
- **Banco SQL imediato:** persistência real, porém adiciona migração e infraestrutura antes de
  validar o núcleo do problema.

