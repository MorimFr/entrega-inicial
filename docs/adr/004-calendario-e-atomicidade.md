# ADR-004: calendário comum e atomicidade das reservas

- Estado: aceita para homologação da Entrega 2
- Data: 14 de outubro de 2026
- Issue: #25; regras RN-03, RN-04, RN-06, RN-07, RN-10, RN-11

## Contexto e alternativas

A comparação de datas locais de cada cliente permitia mais de duas reservas no mesmo dia do campus.
A ordenação textual ISO em SQLite não coincide com a ordem dos instantes quando há offsets distintos.
Verificações separadas da gravação também deixam uma janela de corrida, mesmo numa única API com
múltiplas threads. Apenas exigir testes sequenciais ou limitar a um worker não elimina essa janela.

## Decisão

Usar UTC-03 fixo como calendário do campus, preservar o offset de entrada e ordenar datetime pelo
instante real. Exigir tipo inteiro estrito para participantes na fronteira HTTP e no serviço.
Adicionar `transaction()` à porta: RLock em memória e `BEGIN IMMEDIATE` em SQLite. Operações SQL do
caso de uso reutilizam a mesma conexão por contexto; exceção reverte a transação e libera a conexão.

## Consequências e trade-offs

- O domínio continua sem SQL e sem FastAPI; o serviço decide regras dentro da unidade de trabalho.
- A ordem dos clientes não determina o limite diário. A política de calendário fica explícita.
- SQLite serializa escritores de instâncias distintas que apontem ao mesmo arquivo; o timeout de
  conexão é 5 segundos. Instalação distribuída entre hosts permanece fora do escopo.
- Serialização reduz throughput, mas conserva invariantes no volume esperado do demonstrador.
- A política fixa não depende de base de timezone nem de relógio real; mudança do fuso institucional
  requer refinamento. Datas de teste são constantes.
- PostgreSQL e bloqueios distribuídos foram considerados e adiados por custo operacional. Não é
  necessário um banco externo para serializar escritores locais com SQLite.
