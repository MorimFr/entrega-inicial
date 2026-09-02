# ADR-003: SQLite como adaptador persistente local

- **Estado:** aceita
- **Data:** 1 de setembro de 2026

## Contexto

A primeira iteração usava exclusivamente memória e perdia reservas em cada reinício. A Entrega 2
exige solução integrada e refinada, mas o escopo acadêmico não justifica operar um servidor de banco
externo. A arquitetura já possuía uma porta substituível.

## Decisão

Usar SQLite da biblioteca padrão como adaptador padrão da API. O arquivo é configurado por
`CAMPUSFLOW_DATABASE_PATH`, ignorado pelo Git e montado em volume nomeado no Docker. Manter o
adaptador em memória para testes unitários/API e validar SQLite em testes de integração com arquivos
temporários.

## Consequências e trade-offs

- reservas e cancelamentos sobrevivem ao reinício sem serviço externo;
- instalação continua pequena e reproduzível;
- a porta do domínio não depende de SQL;
- consultas ganham índices por sala/usuário, estado e início;
- SQLite é adequado a uma única instância e baixa concorrência, mas não resolve coordenação entre
  múltiplos processos;
- as checagens de conflito e gravação ainda não formam uma transação distribuída; produção exigiria
  autenticação, transação atômica e banco gerenciado.

## Alternativas consideradas

- **Manter apenas memória:** menor código, porém perde dados e não atende RF-08.
- **PostgreSQL:** melhor concorrência e operação multi-instância, mas introduz credenciais, serviço,
  migrações e custo operacional desproporcionais à etapa.
- **Acoplar SQL ao serviço:** menos classes, porém quebraria testabilidade e a decisão do ADR-001.
