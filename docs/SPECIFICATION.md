# Especificação técnica — CampusFlow

**Versão:** 0.2.0  
**Estado:** aprovada para a Entrega 1  
**Última atualização:** 1 de setembro de 2026

## 1. Problema e objetivo

Salas de estudo compartilhadas são recursos escassos. Agendamentos informais geram reservas
simultâneas, ocupação acima da capacidade e ausência de uma fonte única de disponibilidade. O
CampusFlow oferece uma API determinística para reservar essas salas e rejeitar estados inválidos
antes de serem registrados.

Nesta iteração, o sistema é um demonstrador executável: persiste em memória, expõe contratos HTTP e
prioriza regras isoladas e testáveis. Autenticação, banco de dados e interface gráfica estão fora do
escopo.

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

## 4. Regras de negócio

| ID | Regra |
|---|---|
| RN-01 | `starts_at` e `ends_at` são obrigatórios, incluem fuso horário e `ends_at > starts_at`. |
| RN-02 | A duração máxima de uma reserva é 2 horas; exatamente 2 horas é permitido. |
| RN-03 | `attendees` é inteiro positivo e não pode exceder a capacidade da sala. |
| RN-04 | Duas reservas ativas da mesma sala não podem se sobrepor. |
| RN-05 | Intervalos adjacentes são permitidos: uma reserva pode começar no fim de outra. |
| RN-06 | Cada usuário pode manter no máximo 2 reservas ativas cuja data de início seja o mesmo dia. |
| RN-07 | Cancelamento é idempotente apenas quanto ao estado: segunda tentativa é conflito explícito. |
| RN-08 | Canceladas não bloqueiam intervalo e não contam para RN-06. |
| RN-09 | Sala ou reserva inexistente produz erro de recurso não encontrado. |

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

## 6. Contratos de entrada e saída

Todos os corpos usam JSON e datas usam ISO 8601 com offset (`Z` é aceito). Erros de domínio usam:

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
- **422 / `invalid_period`, `duration_limit_exceeded`, `room_capacity_exceeded`:** RN-01 a RN-03.
- **422 FastAPI:** formato/tipo/campo obrigatório inválido.

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

## 7. Componentes e APIs internas

| Componente | Responsabilidade | Dependências permitidas |
|---|---|---|
| `domain.py` | Entidades `Room`, `Reservation` e estado | biblioteca padrão |
| `errors.py` | Taxonomia estável de erros de domínio | nenhuma |
| `repository.py` | Porta de persistência e adaptador em memória | domínio |
| `service.py` | Casos de uso e RN-01 a RN-09 | domínio, erros, porta |
| `schemas.py` | Modelos públicos de entrada/saída | Pydantic, domínio |
| `api.py` | Rotas, injeção e tradução erro/HTTP | FastAPI, serviço, schemas |

A interface `ReservationRepository` define operações isoladas. Testes podem injetar um adaptador
novo a cada caso; uma futura implementação SQL deve cumprir a mesma porta.

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
| RNF-02, RNF-03 | CI | cobertura ≥ 90%, Ruff e Pytest |

## 10. Critérios de aceite da iteração

1. Todos os contratos descritos respondem conforme esta especificação.
2. Casos felizes, erros e limites têm testes automatizados determinísticos.
3. `ruff` e `pytest` passam localmente e no contêiner.
4. CI executa em Pull Requests sem permitir ocultar falhas.
5. Alterações de comportamento atualizam este documento e `SPEC_CHANGELOG.md`.

## 11. Fora do escopo e evolução

Ficam para iterações futuras: autenticação institucional, autorização, persistência SQL, concorrência
distribuída, cadastro de salas, notificações, recorrência, interface web e política de antecedência.

