# Relato sintético de experiência — Entrega 2

## Contexto

Felipe Amorim Monteiro (RA 22452139) desenvolveu o CampusFlow como equipe individual, usando um
colaborador autorizado distinto para revisão de Pull Requests. A segunda iteração continuou no mesmo
repositório para preservar Issues, decisões, commits, testes e refinamentos da Entrega 1.

## Aprendizados

1. **A camada HTTP não substitui o domínio.** O novo teste direto revelou que participantes não
   positivos eram barrados pelo Pydantic, mas aceitos pelo serviço. A correção tornou RN-03 válida em
   qualquer adaptador.
2. **Portas arquiteturais pagam o custo na iteração seguinte.** A persistência SQLite foi adicionada
   sem reescrever regras nem os testes de API, confirmando a utilidade do ADR-001.
3. **100% de passagem não significa ausência de risco.** Cobertura alta mede linhas exercitadas, não
   completude de requisitos, segurança, concorrência ou autorização.
4. **IA acelera verificação, não transfere responsabilidade.** O agente ajudou a localizar a
   divergência e executar o ciclo, mas especificação, revisão do diff, proteção de branch e decisão de
   merge permaneceram humanas.

## Desafios e trade-offs

- SQLite resolveu durabilidade local com baixa complexidade, mas não foi apresentado como banco de
  produção distribuído.
- A consulta por `user_id` completa um fluxo de uso, porém sem autenticação o identificador não prova
  identidade; a limitação foi explicitada em vez de ocultada.
- Uma equipe individual não consegue realizar revisão “entre membros”. O processo registra autor e
  colaborador revisor distintos, sem chamar autoaprovação de revisão por pares.
- As quatro ferramentas de IA não foram executadas artificialmente apenas para preencher a matriz:
  uso real e avaliação documental foram separados.

## Resultado

A iteração passou de um demonstrador volátil para uma API persistente e consultável, ampliou o
harness de 26 para 33 testes e registrou o vínculo entre falha, re-especificação, correção e evidência.
O principal aprendizado foi que governança e teste são mecanismos de contenção do erro — humano ou
gerado por IA — e não meros anexos da implementação.
