# Análise comparativa e ético-técnica de agentes de IA

Data de atualização: 14/10/2026. Projeto: CampusFlow. Autor responsável: Felipe Amorim Monteiro.

## Método e alcance

Codex foi o agente utilizado na implementação e homologação. Claude Code, Cursor e Antigravity
foram avaliados documentalmente por fontes oficiais. Não foram executados benchmarks com essas
três ferramentas; não há notas de velocidade, custo ou qualidade experimental. O requisito admite
ferramentas avaliadas/utilizadas: a matriz compara adequação ao SDD e explicita o tipo de evidência.

| Ferramenta | Ponto forte documentado | Limitação/controle relevante | Impacto e evidência |
|---|---|---|---|
| Codex | contexto AGENTS.md, edição e execução de comandos/testes | limites de acesso dependem da configuração, não só do prompt | uso real: implementação e 21 novos casos; geração anterior tinha erros revelados pelo harness |
| Claude Code | fluxo de terminal com permissões e revisão das ações | permissões amplas/MCP aumentam exposição; mudanças devem ser inspecionadas | avaliação documental: candidato para SDD reproduzível, sem medida de qualidade no CampusFlow |
| Cursor | editor e agentes integrados; política de Privacy Mode | contexto pode trafegar aos serviços; modo privado não substitui minimização de dados | avaliação documental: facilita leitura de diff e iteração na IDE; sem ensaio prático |
| Antigravity | política de execução/revisão e sandbox configurável | Always Proceed amplia autonomia e risco; configurar escopo de projeto | avaliação documental: planos e revisão podem apoiar SDD; sem resultado medido |

Fontes para as capacidades/controles: [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[segurança Codex](https://learn.chatgpt.com/docs/security),
[Claude Code Security](https://code.claude.com/docs/en/security),
[Cursor Security](https://cursor.com/security),
[Antigravity Agent Settings](https://antigravity.google/docs/agent-settings).

## Impacto real na especificação e no código

O Codex auxiliou a decomposição em contratos, porta de repositório e regras numeradas; isso permitiu
comparar memória e SQLite sem duplicar os casos de uso. Porém, o código anterior assistido por IA
aceitava tipos inválidos, ordenava datas ISO incorretamente e usava calendários diferentes. Uma
afirmação de cobertura alta não revelou esses defeitos: em outubro, 13 regressões tiveram 12 falhas
antes da correção. A inspeção também apontou uma janela de corrida na gravação.

O benefício mensurável foi expandir a suíte de 34 para 55 casos e documentar regras 0.4.0/ADR-004,
com logs vinculados à execução. Não se atribui todo o resultado à ferramenta: o aluno determinou
escopo e aceitação, o harness verificou comportamento e a arquitetura delimitou a mudança.
Uma comparação experimental futura poderia entregar a mesma Issue a duas ferramentas, com o mesmo
commit, prompt, ambiente e orçamento, e medir testes, correções humanas e regressões. Esses dados
não existem neste trabalho e não foram simulados.

## 1. Alucinação e código inseguro ou destrutivo

Agentes podem omitir regras, propor APIs incorretas, instalar dependências desnecessárias ou executar
comandos que apaguem/publiquem recursos. Também podem seguir instruções maliciosas em arquivos ou
resultados externos (prompt injection). Documentação de segurança oferece permissões e isolamento;
existência da opção não prova que ela foi ativada na sessão.

Neste projeto, o controle comprovável é AGENTS.md, Issues, diff versionado, testes, transações e gates
do CI/PR. A sessão teve permissões locais amplas; não afirmamos isolamento efetivo de filesystem/rede.
Para reutilização, recomenda-se workspace isolado, permissões mínimas e aprovação de ações externas.
Instruções textuais ajudam o agente, mas não substituem limites técnicos. Testes concorrentes e de
rollback validam invariantes que testes de sucesso sequencial omitiam.

## 2. Dados, privacidade e confidencialidade

Enviar código/contexto/logs a um modelo pode expor segredos, dados pessoais e informações
confidenciais. MCPs acrescentam terceiros e permissões próprios. No Cursor, Privacy Mode reduz uso
para treinamento segundo o fornecedor; isso não equivale a proibir qualquer processamento externo.
No projeto, identificadores de teste são fictícios; `.env` e banco local ficam fora do Git e do
contexto de build Docker. Dados de identificação do aluno ficam no relatório por exigência acadêmica.

A LGPD estabelece princípios de finalidade, necessidade e segurança, e prevê medidas para proteger
dados pessoais (arts. 6 e 46). Uma futura implantação precisaria definir finalidade/base do tratamento,
acesso, retenção e direitos do titular. `user_id` informado pelo cliente não autentica ninguém;
proibir dados reais é um limite do demonstrador, não uma implementação de autorização.
[Fonte: texto oficial da LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm).

## 3. Propriedade intelectual e direitos autorais

Contrato do provedor, licença de dependência e proteção autoral são questões distintas. Os termos
OpenAI atribuem a saída ao usuário na medida permitida pela lei e alertam para similaridade e
responsabilidade de avaliação. Isso não garante originalidade nem remove direitos de terceiros.
[Fonte: Termos de Uso](https://openai.com/policies/terms-of-use/).

No Brasil, software tem regime previsto pela Lei 9.609/1998 e a Lei 9.610/1998 trata de direitos
autorais. Não presumimos que uma cláusula privada resolva a autoria de toda saída automatizada.
Como referência estrangeira, o U.S. Copyright Office estuda a contribuição humana nas obras com IA;
seus relatórios não são regra brasileira. [Lei de Software](https://www.planalto.gov.br/ccivil_03/leis/l9609.htm),
[Lei de Direitos Autorais](https://www.planalto.gov.br/ccivil_03/leis/l9610.htm),
[relatórios USCO](https://www.copyright.gov/ai/).

O aluno deve revisar licenças e procedência, preservar avisos, evitar copiar material proprietário
sem permissão e registrar contribuição humana em commits/ADRs. MIT do projeto não concede direitos
sobre material de terceiros. Antes de uso comercial, uma revisão de licenças/autoria pode ser necessária.

## 4. Homologação e revisão humana no SDD

A IA propõe; o responsável confirma intenção, contrato e risco. CI verde é condição técnica, não
aprovação acadêmica nem prova de ausência de vulnerabilidades. O processo é Issue/regra, regressão,
correção, diff humano, harness, PR e aceite. Os testes não devem ser removidos para ocultar falhas.

Felipe informou que o professor autorizou a adaptação individual: MorimFr e SrMorim são contas do
mesmo aluno e as aprovações representam autorrevisão humana. Não houve revisão independente entre
pares. A autorização é relatada pelo aluno; não há documento docente anexado. A distinção está
documentada porque transparência sobre IA e revisão é parte da ética do trabalho.

## Riscos residuais

| Risco | Mitigação comprovada/proposta | Limite restante |
|---|---|---|
| requisito omitido | IDs e regressões para contratos | requisitos humanos ainda podem ser incompletos |
| corrupção/conflito concorrente | transação local, rollback, testes | múltiplos hosts e carga elevada não homologados |
| vazamento ou comando destrutivo | minimização de contexto e privilégio mínimo recomendado | sessão local teve permissões amplas |
| violação de IP | histórico, licenças e revisão de procedência | ausência de prova automática de originalidade |
| aprovação inadequada | aceite humano e critérios explícitos | autorrevisão não oferece independência entre pares |

As fontes oficiais acima foram consultadas em 14/10/2026. Não foram copiadas extensamente; são
referências para a comparação e discussão crítica contextualizadas ao projeto.
