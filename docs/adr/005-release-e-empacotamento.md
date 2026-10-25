# ADR-005: versão única e empacotamento final

- Estado: implementada na candidata à homologação
- Data: 23/10/2026; Issue #26

## Decisão

Definir 1.0.0 em campusflow.__version__, consumida por pacote e OpenAPI. Docker multi-stage:
runtime instala apenas aplicação e usa usuário sem privilégios; tests acrescenta dependências dev.
Compose publica em 127.0.0.1, conserva SQLite no volume e exporta stdout, JUnit, XML/HTML de coverage
para artifacts/. Um harness Python único executa Ruff e Pytest localmente, no Docker e no CI.

## Trade-offs

- Separar imagens reduz ferramentas no runtime; tests é maior, mas valida a mesma base/aplicação.
- Porta local corresponde ao escopo acadêmico sem autenticação. Exposição externa exigiria
  autenticação/autorização e revisão de segurança.
- Digest da base e versões diretas fixadas reduzem variação; não se afirma build bit a bit, pois
  transitivas/build tools podem mudar. Os manifests reais são anexados à execução.
- As-Built e OpenAPI são artefatos da release. A tag v1.0.0 será criada somente no commit aprovado.
- Vídeo é gravação real do aluno (3-5 minutos), não prova simulada pelo agente.
