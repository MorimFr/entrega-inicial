# Uso de IA no fluxo SDD

## Ferramenta e finalidade

Foi utilizado **Codex**, agente de engenharia de software da OpenAI, como apoio na Entrega 1. O agente
ajudou a transformar o enunciado em componentes, contratos, testes e documentação versionada. Ele
não substitui aprovação dos integrantes nem é fonte de requisitos: `docs/SPECIFICATION.md` é a fonte
de verdade do projeto.

O arquivo raiz `AGENTS.md` dá ao agente contexto permanente sobre SDD, limites arquiteturais e gates
de qualidade. Isso segue o mecanismo oficial em que o Codex lê `AGENTS.md` no início do trabalho e
aplica instruções do escopo do projeto. Referência: [documentação oficial do
Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Prompt inicial registrado

```text
Vamos fazer a entrega de um trabalho da faculdade. Faça tudo que for necessário para cumprir:
repositório e governança; especificação técnica SDD; agente de IA e ambiente padronizado; test
harness, casos principais/borda e evidências de execução. A entrega deve permitir instalação,
execução e revisão pelo grupo.
```

## Decomposição solicitada ao agente

```text
Escolha um problema real de escopo pequeno. Numere requisitos e regras; defina entradas, saídas e
erros; separe domínio, casos de uso, persistência e HTTP; escreva testes determinísticos para cenário
feliz, erros e fronteiras; execute lint e testes; documente decisões e refinamentos sem inventar
nomes, Issues, PRs, aprovações ou logs.
```

## Protocolo de uso pela equipe

1. O integrante fornece ao agente a Issue, IDs da especificação e critérios de aceitação.
2. O agente propõe testes e implementação na branch da Issue.
3. O autor inspeciona o diff e executa `scripts/test.ps1` ou `make test`.
4. Outro integrante revisa o PR; saída da IA não conta como aprovação humana.
5. Se o teste revelar ambiguidade, o grupo decide e registra em `SPEC_CHANGELOG.md` antes do merge.
6. Prompts ou decisões relevantes são resumidos no PR para auditabilidade.

## Verificações obrigatórias sobre saídas da IA

- conferir cada comportamento contra uma regra numerada;
- validar que casos de borda não foram omitidos;
- rejeitar dependências ou escopo não solicitados;
- não inserir credenciais ou dados pessoais no prompt;
- executar o harness em ambiente limpo;
- exigir revisão humana de alguém diferente do autor.

## Resultado desta iteração

O agente propôs uma arquitetura em camadas e uma suíte inicial. A revisão orientada pelos testes
identificou ambiguidades em fuso horário, adjacência de intervalos, limite diário e segundo
cancelamento. O refinamento correspondente está registrado na versão 0.2.0 da especificação. A
aceitação técnica é determinada pelos comandos reproduzíveis e respectivos logs, não pela afirmação
do agente.

## Continuidade na Entrega 2

O agente recebeu o enunciado da etapa intermediária e a instrução de continuar no mesmo repositório,
cumprir os requisitos e identificar ao final as evidências visuais necessárias. Antes da correção,
foi solicitado que comparasse serviço, contratos e testes. O teste de regressão da RN-03 foi
executado isoladamente e falhou para `0` e `-1`; somente depois o serviço foi alterado.

O Codex também apoiou a implementação do adaptador SQLite, a ampliação da suíte e a documentação
crítica. Claude Code, Cursor e Antigravity **não foram executados**: foram comparados por fontes
oficiais em [`AI_ETHICS.md`](AI_ETHICS.md). Essa distinção evita transformar pesquisa documental em
uma alegação falsa de experiência prática.

Todas as ações no GitHub continuam sujeitas a check automatizado e revisão humana por conta distinta.
