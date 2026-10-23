# Especificação definitiva - SDD As-Built do CampusFlow

**Versão:** 1.0.0
**Estado:** As-Built da candidata final; aceite pela homologação do PR da Issue #26
**Última atualização:** 23 de outubro de 2026

## 1. Problema e objetivo

Salas de estudo compartilhadas são recursos escassos. Agendamentos informais geram reservas
simultâneas, ocupação acima da capacidade e ausência de uma fonte única de disponibilidade. O
CampusFlow oferece uma API determinística para reservar essas salas e rejeitar estados inválidos
antes de serem registrados.

Na solução final, o sistema mantém contratos HTTP e regras isoladas, persiste reservas em
SQLite e permite consulta das reservas pelo identificador de usuário informado. O
adaptador em memória permanece disponível para testes determinísticos. Autenticação institucional e
interface gráfica continuam fora do escopo.

## 2. Atores e termos

- **Usuário:** aluno identificado por `user_id` opaco, sem cadastro nesta iteração.
- **Sala:** recurso com identificador, nome e capacidade positiva.
- **Reserva ativa:** intervalo confirmado que bloqueia a sala e conta no limite diário.
- **Reserva cancelada:** registro preservado para consulta, mas que não bloqueia horários nem limites.
- **Intervalo:** faixa semiaberta `[starts_at, ends_at)`; o instante final não pertence à reserva.

## 3. Requisitos funcionais

| ID | Requisito | Critério verificável |
|---|---|---|
| RF-01 | Listar salas | `GET /rooms` retorna catálogo e capacidades. |
| RF-02 | Criar reserva | Entrada válida gera ID único, estado `active` e HTTP 201. |
| RF-03 | Consultar reserva | ID existente retorna todos os campos e estado atual. |
| RF-04 | Cancelar reserva | Reserva ativa passa a `cancelled` e deixa de bloquear a sala. |
| RF-05 | Consultar disponibilidade | API informa se uma sala está livre em determinado intervalo. |
| RF-06 | Verificar saúde | `GET /health` retorna `{"status":"ok"}`. |
| RF-07 | Listar reservas do usuário | `GET /reservations?user_id=...` retorna as reservas do usuário e aceita filtro por estado. |
| RF-08 | Preservar reservas | Reservas e cancelamentos permanecem disponíveis após reiniciar a API. |

## 4. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | `starts_at` e `ends_at` são obrigatórios, incluem fuso horário e `ends_at > starts_at`. |
| RN-02 | A duração máxima de uma reserva é 2 horas; exatamente 2 horas é permitido. |
| RN-03 | `attendees` é inteiro positivo estrito: booleanos, frações e strings são rejeitados. Não pode exceder a capacidade da sala. |
| RN-04 | Duas reservas ativas da mesma sala não podem se sobrepor. |
| RN-05 | Intervalos adjacentes são permitidos: uma reserva pode começar no fim de outra. |
| RN-06 | Cada usuário pode manter no máximo 2 reservas ativas pela data de início no calendário do campus (UTC-03 fixo), independentemente do offset enviado pelo cliente. |
| RN-07 | Cancelamento é idempotente apenas quanto ao estado: segunda tentativa é conflito explícito. |
| RN-08 | Canceladas não bloqueiam intervalo e não contam para RN-06. |
| RN-09 | Sala ou reserva inexistente produz erro de recurso não encontrado. |
| RN-10 | A listagem filtra estritamente por `user_id`, ordena pelo instante real de início/ID (não pelo texto ISO) e aceita filtro `active` ou `cancelled`. |
| RN-11 | Verificações e gravação da criação/cancelamento compartilham uma transação; requisições concorrentes não violam conflito, limite diário ou cancelamento único. |

### Algoritmo de conflito

Para uma nova reserva `N` e cada reserva ativa existente `E` da mesma sala, há conflito quando:

```text
N.starts_at < E.ends_at AND N.ends_at > E.starts_at
```

## 5. Requisitos não funcionais

| ID | Requisito | Métrica/validação |
|---|---|---|
| RNF-01 | Reprodutibilidade | Aplicação e testes executam com Docker/Compose. |
| RNF-02 | Testabilidade | Domínio não depende do framework; cobertura automatizada mínima de 90%. |
| RNF-03 | Qualidade | Ruff sem violações e Pytest sem falhas no CI. |
| RNF-04 | Portabilidade | Python 3.12; execução documentada em Windows, Linux e macOS. |
| RNF-05 | Auditabilidade | Regras têm IDs estáveis e rastreabilidade para casos de teste. |
| RNF-06 | Segurança básica | Nenhum segredo/dado pessoal real versionado; entradas validadas. |
| RNF-07 | Durabilidade local | SQLite preserva dados entre reinícios; o arquivo fica fora do Git e em volume Docker. |

## 6. Contratos de entrada e saída

Todos os corpos usam JSON e datas usam ISO 8601 com offset (`Z` é aceito). Erros de domínio usam:

O offset de entrada é preservado na resposta, mas o cálculo do dia converte para UTC-03.
O contrato exige um número JSON inteiro para `attendees`; coerção de strings/booleanos não é aceita.
Datas de entrada exigem strings ISO 8601 com separador T; números Unix/epoch, inclusive strings
numéricas, são rejeitados no body e na consulta de disponibilidade. Identificadores são opacos,
sem trim/normalização: room_id de 1-50 caracteres, user_id de 1-100. Campos extras no body são
ignorados pelo padrão Pydantic; não são persistidos. Não existe cadastro/autenticação do usuário.

```json
{
  "code": "reservation_conflict",
  "message": "A sala já está reservada nesse intervalo."
}
```

### `GET /health`

- **200:** `{"status":"ok"}`.

### `GET /rooms`

- **200:** lista de `{ "id": string, "name": string, "capacity": integer }`.

### `POST /reservations`

Entrada:

```json
{
  "room_id": "sala-a",
  "user_id": "aluno-123",
  "starts_at": "2026-09-10T10:00:00-03:00",
  "ends_at": "2026-09-10T11:00:00-03:00",
  "attendees": 3
}
```

- **201:** reserva com `id`, campos de entrada e `status: "active"`.
- **404 / `room_not_found`:** sala não existe.
- **409 / `reservation_conflict`:** RN-04.
- **409 / `daily_limit_exceeded`:** RN-06.
- **422 / `invalid_period`, `duration_limit_exceeded`, `invalid_attendee_count`, `room_capacity_exceeded`:** RN-01 a RN-03.
- **422 FastAPI:** formato/tipo/campo obrigatório inválido.

### `GET /reservations?user_id={id}&status={active|cancelled}`

- `user_id` é obrigatório; `status` é opcional.
- **200:** lista ordenada de reservas do usuário; pode ser vazia.
- **422 FastAPI:** `user_id` ausente/vazio ou estado fora do enum.

### `GET /reservations/{id}`

- **200:** reserva completa.
- **404 / `reservation_not_found`:** ID não existe.

### `DELETE /reservations/{id}`

- **200:** reserva completa com `status: "cancelled"`.
- **404 / `reservation_not_found`:** ID não existe.
- **409 / `already_cancelled`:** RN-07.

### `GET /rooms/{id}/availability?starts_at=...&ends_at=...`

- **200:** `{ "room_id", "starts_at", "ends_at", "available": boolean }`.
- **404 / `room_not_found`:** sala não existe.
- **422 / `invalid_period`:** RN-01.

O OpenAPI gerado em `/openapi.json` é a representação executável complementar destes contratos.
O snapshot definitivo é `docs/openapi.json`, exportado por `scripts/export_openapi.py`. O CI executa
o modo `--check` para rejeitar divergência entre documento e API. A versão do pacote e API vem de
`campusflow.__version__`, sem números duplicados na implementação.
As descrições 422 declaradas são explícitas, independentes do nome HTTPStatus da versão Python.

## 7. Componentes e APIs internas

| Componente | Responsabilidade | Dependências permitidas |
|---|---|---|
| `domain.py` | Entidades `Room`, `Reservation` e estado | biblioteca padrão |
| `errors.py` | Taxonomia estável de erros de domínio | nenhuma |
| `repository.py` | Porta de persistência e adaptador em memória | domínio |
| `sqlite_repository.py` | Adaptador persistente, schema e índices SQLite | domínio, biblioteca padrão |
| `service.py` | Casos de uso e RN-01 a RN-11 | domínio, erros, porta |
| `time_policy.py` | Data do campus em UTC-03 fixo | biblioteca padrão |
| `schemas.py` | Modelos públicos de entrada/saída | Pydantic, domínio |
| `api.py` | Rotas, injeção e tradução erro/HTTP | FastAPI, serviço, schemas |

A interface `ReservationRepository` define operações isoladas. Testes unitários/API injetam um
adaptador em memória novo a cada caso; a aplicação publicada usa SQLite e os testes de integração
recriam o adaptador sobre o mesmo arquivo para provar a durabilidade.

## 8. Estado e invariantes

Estados permitidos:

```text
criação válida -> ACTIVE -> cancelamento -> CANCELLED
```

Não há transição de `CANCELLED` para `ACTIVE`. Os invariantes RN-01 a RN-06 são verificados antes de
persistir. Falhas não geram gravação parcial.

## 9. Estratégia de testes e rastreabilidade

| Regra/requisito | Camada principal de teste | Cenários |
|---|---|---|
| RF-01, RF-03, RF-06 | API | sucesso e 404 |
| RF-02, RN-01 a RN-03 | serviço + API | válido, fronteira e inválido |
| RN-04, RN-05 | serviço + API | sobreposição e adjacência |
| RN-06, RN-08 | serviço | terceira reserva e cancelamento |
| RF-04, RN-07 | serviço + API | cancelar e repetir |
| RF-05, RN-09 | serviço + API | ocupado, livre, cancelado, sala ausente |
| RF-07, RN-10 | serviço + API | todos os estados, filtro, vazio e consulta inválida |
| RF-08, RNF-07 | integração | recriação do repositório e cancelamento persistente |
| RN-03, RN-06, RN-10 | memória + SQLite + HTTP | tipo estrito, fronteira de dia e ordenação com offsets distintos |
| RN-11 | concorrência + SQLite | criação, limite, cancelamento, instâncias independentes e rollback |
| RNF-02, RNF-03 | CI | cobertura ≥ 90%, Ruff e Pytest |

## 10. Critérios de aceite da iteração

1. Todos os contratos descritos respondem conforme esta especificação.
2. Casos felizes, erros e limites têm testes automatizados determinísticos.
3. `ruff` e `pytest` passam localmente e no contêiner.
4. CI executa em Pull Requests sem permitir ocultar falhas.
5. Alterações de comportamento atualizam este documento e `SPEC_CHANGELOG.md`.

## 11. Fora do escopo e evolução

Ficam para iterações futuras: autenticação institucional, autorização por token, banco gerenciado,
implantação distribuída entre hosts, cadastro de salas, notificações, recorrência, interface web e política de
antecedência. Nesta versão, `user_id` é um identificador opaco informado pelo cliente, não uma prova
de identidade; essa limitação impede classificar a API como pronta para produção pública.

SQLite garante serialização de escritores no mesmo arquivo via `BEGIN IMMEDIATE`. Um banco em
volume local atende à implantação acadêmica; não se assume coordenação entre hosts ou filesystem de
rede. O calendário UTC-03 é fixo nesta entrega; mudança institucional de fuso demanda re-especificação.

## 12. Implantação e operação efetivamente entregues

| Item | As-Built |
|---|---|
| Entrada de execução | uvicorn campusflow.api:app, porta interna 8000, um processo |
| Compose API | target runtime, usuário campusflow sem privilégios, loopback 127.0.0.1 |
| Porta do host | CAMPUSFLOW_PORT; padrão 8000 |
| Banco Docker | CAMPUSFLOW_DATABASE_PATH=/app/data/campusflow.db, volume campusflow-data |
| Banco Python local | variável CAMPUSFLOW_DATABASE_PATH; padrão data/campusflow.db |
| Catálogo | sala-a (Sala A, 4) e sala-b (Sala B, 8); inicialização INSERT OR IGNORE |
| Lifecycle | create_app inicializa schema/banco na importação/partida; falha de caminho/permissão impede partida |
| Health | GET /health é liveness, não teste de disponibilidade contínua do banco |
| Timeout SQLite | conexão 5 s; criação/cancelamento usam BEGIN IMMEDIATE |
| Harness | target tests, Ruff + Pytest; exporta artifacts/test-output.log, junit.xml, coverage.xml e htmlcov/ |
| Demonstração | profile demo chama a API pelo HTTP da rede Compose, dados fictícios |
| Base | Python 3.12-slim fixada por digest no Dockerfile |

Não se rejeitam datas passadas: política de antecedência não foi especificada. A disponibilidade
informa ausência de conflito no intervalo; não garante elegibilidade de criação por duração,
capacidade ou limite do usuário. As verificações completas são realizadas no POST.

Logs históricos e PDFs das entregas anteriores são preservados como evidências datadas. A referência
final é esta especificação, o OpenAPI versionado, o README e a release estável aprovada.
