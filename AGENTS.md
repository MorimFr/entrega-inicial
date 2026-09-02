# Instruções para agentes de código

## Fonte de verdade

1. Leia `docs/SPECIFICATION.md` antes de alterar comportamento.
2. Trate os IDs `RF-*`, `RN-*`, `RNF-*` e os contratos HTTP como obrigatórios.
3. Se código e especificação divergirem, não decida silenciosamente: proponha a alteração em
   `docs/SPEC_CHANGELOG.md` e atualize testes, especificação e implementação no mesmo PR.

## Fluxo SDD

1. Vincule a alteração a uma Issue e aos IDs da especificação.
2. Escreva ou ajuste o teste que demonstra o critério de aceitação.
3. Faça a menor implementação que satisfaça o contrato.
4. Execute `python -m ruff check .` e `python -m pytest`.
5. Registre decisões estruturais duradouras em `docs/adr/`.

## Limites arquiteturais

- `domain.py` não depende de FastAPI nem de persistência.
- `service.py` concentra regras de negócio e depende apenas da porta de repositório.
- `api.py` converte HTTP em chamadas de serviço; não duplica regras de negócio.
- Use injeção de dependência para tornar adaptadores substituíveis.
- Nunca remova um teste apenas para fazer o pipeline passar.

## Qualidade e segurança

- Python 3.12, tipagem explícita nas interfaces públicas e formatação compatível com Ruff.
- Testes devem ser determinísticos; não dependem de rede, relógio real ou ordem de execução.
- Não registre segredos, tokens, dados pessoais reais ou arquivos `.env`.
- Mantenha cobertura mínima de 90% e inclua cenário feliz, erro e borda para cada regra nova.
- Responda e documente em português do Brasil; código e identificadores podem ficar em inglês.

