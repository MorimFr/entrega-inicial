# ADR-002: FastAPI, Pytest e gate de cobertura

- **Estado:** aceita
- **Data:** 1 de setembro de 2026

## Contexto

Os contratos precisam ser executáveis, documentados e validados automaticamente no computador de
cada integrante, em Docker e no CI.

## Decisão

Usar FastAPI/Pydantic para contratos e OpenAPI; Pytest para testes unitários e HTTP; Ruff para análise
estática; cobertura de linhas mínima de 90% como gate. Fixar versões no `pyproject.toml`.

## Consequências

- documentação interativa e validação de entrada são geradas a partir dos schemas;
- uma única suíte valida regras e integração HTTP;
- o pipeline falha por regressão, lint ou cobertura insuficiente;
- atualização de dependências é deliberada e deve passar pelo mesmo harness.

## Alternativas consideradas

- **Flask:** menor abstração, mas exigiria validação/OpenAPI adicionais.
- **Unittest padrão:** viável, mas fixtures e parametrização do Pytest tornam bordas mais legíveis.

