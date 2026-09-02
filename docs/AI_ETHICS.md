# Análise comparativa e ético-técnica de agentes de IA

**Data da análise:** 1 de setembro de 2026
**Escopo:** desenvolvimento de software orientado por especificação (SDD) no CampusFlow.

## Método e limite da comparação

O **Codex foi a única ferramenta executada no repositório**. Claude Code, Cursor e Google
Antigravity foram avaliados por documentação oficial, sem ensaio controlado; por isso, este texto não
atribui notas de velocidade, qualidade ou custo que não tenham sido medidos. A comparação identifica
capacidades e riscos relevantes ao mesmo fluxo SDD, e não declara um vencedor universal.

## Matriz comparativa

| Ferramenta | Forma de trabalho e contexto | Controles relevantes | Impacto provável no SDD | Evidência no projeto |
|---|---|---|---|---|
| **Codex** | Agente atua sobre workspace/terminal; `AGENTS.md` mantém regras e fonte de verdade. | Limites de filesystem/rede, aprovações e logs de ações conforme configuração. | Bom encaixe para ciclo especificação → teste → implementação → execução, com diff revisável. | **Uso real:** decomposição, teste de regressão RN-03, código, testes e documentação; todo resultado passou por harness e Git. |
| **Claude Code** | Agente de terminal com ferramentas permitidas/bloqueadas, modos de permissão e saída estruturada. | `--allowedTools`, `--disallowedTools`, modo de planejamento e prompts; a própria CLI sinaliza risco ao ignorar permissões. | Pode automatizar tarefas e CI com granularidade de ferramentas; exige política explícita para Bash e MCP. | **Avaliação documental:** não instalado nem executado neste trabalho. |
| **Cursor** | IDE com autocomplete, edição inline, agente, terminal, regras de projeto e agentes em segundo plano. | Permissões de CLI e Privacy Mode; agentes remotos têm acesso ao repositório e internet conforme configuração. | Feedback visual favorece revisão incremental; o modo em segundo plano amplia produtividade e superfície de exfiltração. | **Avaliação documental:** não instalado nem executado neste trabalho. |
| **Google Antigravity** | Plataforma/IDE/CLI agentic com projetos, planos, artefatos e permissões por escopo. | Listas deny/ask/allow, sandbox, revisão de artefatos e opção de telemetria. | Planejamento e projetos isolados combinam com SDD; modos irrestritos aumentam o risco operacional. | **Avaliação documental:** não instalado nem executado neste trabalho. |

### Leitura crítica do impacto real do Codex

O benefício observado não foi simplesmente “gerar mais código”. O agente tornou barato comparar
especificação, serviço e testes e encontrou a RN-03 aplicada apenas no HTTP. O risco simétrico é
aceitar uma alteração extensa porque ela parece coerente. Neste ciclo, o controle efetivo veio do
teste que falhou, da inspeção do diff, da porta de repositório e da revisão humana — não da confiança
na resposta textual do modelo.

## 1. Alucinação, código inseguro e ações destrutivas

Agentes podem inventar APIs, pressupor requisitos, escolher dependências inexistentes ou produzir
código que passa em casos felizes e falha em bordas. Como também executam terminal, uma alucinação
pode deixar de ser apenas texto e modificar arquivos, publicar dados ou remover recursos. Documentos
oficiais das próprias ferramentas oferecem sandbox, permissões e revisão justamente porque essa
capacidade cria risco.

Controles adotados no CampusFlow:

1. `docs/SPECIFICATION.md` é fonte de verdade com IDs estáveis; o agente não cria requisitos em
   silêncio.
2. Mudança de comportamento exige teste que falha antes e atualização do changelog.
3. Escrita fica limitada ao workspace; segredos e `.env` não entram no contexto nem no Git.
4. Comandos destrutivos, acesso fora do projeto e publicação externa exigem autorização humana.
5. Ruff, Pytest, cobertura, Docker e GitHub Actions fornecem sinais independentes do texto da IA.
6. Nenhum modo equivalente a `--dangerously-skip-permissions` deve ser usado em repositório real.

Testes reduzem, mas não eliminam, risco: uma suíte pode confirmar uma especificação incompleta. Por
isso, revisão de regra, modelagem de ameaça e inspeção do diff continuam obrigatórias.

## 2. Privacidade, confidencialidade e vazamento de dados

Código-fonte, prompts, logs, nomes de clientes, chaves e dados de produção podem ser enviados ao
provedor ou a integrações MCP. A LGPD considera tratamento um conjunto amplo de operações, incluindo
acesso, armazenamento, transmissão e processamento; enviar contexto a um modelo deve ter finalidade,
base e minimização, não ser tratado como uma cópia “invisível”. Modos de privacidade variam por
produto e plano, e integrações podem ter termos próprios.

Política prática para este projeto:

- usar apenas identificadores fictícios (`aluno-1`) em código, testes e prompts;
- nunca fornecer token, `.env`, banco real, RA além do necessário ao relatório, ou dado de terceiro;
- conferir configuração de retenção/treinamento e rota dos dados antes de usar ferramenta nova;
- limitar indexação e leitura às pastas necessárias;
- revisar MCPs/plugins como terceiros independentes e conceder privilégio mínimo;
- revogar credenciais e registrar incidente se um segredo for exposto.

O arquivo SQLite local e o volume Docker são excluídos do Git. Em produção, `user_id` seria dado
pseudônimo, não anônimo; autenticação, autorização, retenção e exclusão precisariam ser definidas.

## 3. Propriedade intelectual e direitos autorais

Termos contratuais podem atribuir ao usuário direitos que o fornecedor detenha sobre a saída, mas
isso não garante três coisas: que a saída seja original, que não infrinja direitos de terceiros ou
que conteúdo puramente gerado por IA receba proteção autoral em todas as jurisdições. A própria
natureza probabilística permite saídas semelhantes para usuários diferentes. O U.S. Copyright
Office, por exemplo, distingue material gerado por IA de contribuição humana protegível; o contexto
brasileiro deve ser validado juridicamente para uso comercial.

Controles adotados:

- Felipe é responsável por selecionar, revisar, modificar e homologar cada alteração;
- dependências são explícitas e suas licenças devem ser verificadas antes de distribuição;
- não solicitar reprodução de repositório proprietário, livro, aula ou código sem licença;
- manter histórico de commits/PRs para evidenciar contribuição e decisão humanas;
- conservar a licença do projeto sem afirmar que ela licencia material de terceiros;
- fazer revisão de similaridade/licenças quando o risco ou o destino comercial justificar.

## 4. Centralidade da homologação e revisão humana

No fluxo SDD, a IA é uma proponente. A homologação pertence à pessoa responsável porque somente ela
pode confirmar intenção, impacto jurídico, adequação ao contexto e aceitação do risco. O gate usado é:

```text
Issue + regra -> proposta/teste -> diff humano -> harness -> PR -> revisão humana -> merge
```

CI verde é condição necessária, não aprovação ética ou de produto. No grupo individual, um
colaborador autorizado distinto revisa os PRs; autoaprovação não é apresentada como revisão entre
pares. Qualquer saída da IA pode ser rejeitada mesmo que compile.

## Matriz de riscos e respostas

| Risco | Probabilidade/impacto | Controle | Risco residual |
|---|---|---|---|
| Regra inventada ou omitida | média / alto | IDs, changelog, teste de borda e revisão | especificação humana pode continuar incompleta |
| Comando destrutivo | baixa-média / alto | sandbox, deny/ask, privilégio mínimo, backup/Git | aprovação humana equivocada |
| Exfiltração por prompt injection/MCP | média / alto | rede limitada, contexto mínimo, integrações aprovadas | dependência comprometida ou conteúdo malicioso |
| Segredo ou dado pessoal no prompt | média / alto | `.gitignore`, dados fictícios, revisão e política de incidentes | erro manual antes da detecção |
| Código vulnerável apesar de testes | média / alto | lint, testes, revisão, futura análise de segurança | falhas fora do modelo de ameaça |
| Violação de licença/IP | baixa-média / alto | proveniência, licenças e revisão de similaridade | incerteza jurídica entre jurisdições |

## Fontes oficiais consultadas

- OpenAI, [Running Codex safely](https://openai.com/index/running-codex-safely/) e
  [Termos de Uso](https://openai.com/policies/terms-of-use/).
- Anthropic, [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage)
  e [dados em produtos comerciais](https://support.anthropic.com/en/articles/9267385-does-anthropic-act-as-a-data-processor-or-controller).
- Cursor, [Privacy & Security](https://docs.cursor.com/account/privacy),
  [CLI permissions](https://docs.cursor.com/cli/reference/permissions) e
  [Background Agents](https://docs.cursor.com/background-agent).
- Google, [Antigravity Agent Settings](https://antigravity.google/docs/agent-settings),
  [Permissions](https://antigravity.google/docs/permissions) e
  [Data Collection Settings](https://antigravity.google/docs/settings).
- Governo Federal, [visão geral da LGPD](https://www.gov.br/int/pt-br/acesso-a-informacao/lgpd).
- U.S. Copyright Office,
  [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/).

As páginas foram consultadas na data desta análise; configurações e termos devem ser revistos antes
de cada adoção, pois podem mudar.
