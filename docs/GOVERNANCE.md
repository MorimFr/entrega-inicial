# Governança e operação no GitHub

Este documento define o processo da equipe. Os templates e o pipeline já estão versionados; as
proteções e evidências devem ser ativadas no repositório remoto por alguém com permissão de admin.

## 1. Branches

| Branch | Uso | Regra de merge |
|---|---|---|
| `main` | versão estável e avaliada | somente PR vindo de `develop` |
| `develop` | integração da sprint | somente PR de branch curta |
| `feature/<issue>-<slug>` | funcionalidade | PR para `develop` |
| `fix/<issue>-<slug>` | correção | PR para `develop` |
| `docs/<issue>-<slug>` | documentação | PR para `develop` |

Cada branch curta deve nascer de `develop` atualizado e ser removida após o merge. Não fazer push
direto em `main` ou `develop`.

O commit raiz que inicializa um repositório remoto completamente vazio é a única exceção técnica;
depois dele, `main` e `develop` recebem mudanças exclusivamente por Pull Request.

## 2. Configuração inicial autêntica

Depois de criar o repositório público e enviar o commit inicial:

1. Crie `develop` a partir de `main` e defina o trabalho diário nela.
2. Em **Settings → Branches**, mantenha proteção clássica para `main` e `develop` (ou converta para
   Rulesets sem reduzir os controles).
3. Exija Pull Request antes do merge e pelo menos 1 aprovação.
4. Descarte aprovações quando houver novos commits.
5. Exija resolução de conversas e o status check `quality`.
6. Bloqueie force push e exclusão; inclua administradores nas regras.
7. Para `main`, permita merge apenas após `develop` ter sido validada.

Tire um print das regras ativas para a submissão. Não substitua essa evidência por texto preparado.

## 3. Issues, Project e divisão de trabalho

1. Crie um GitHub Project no formato Board com colunas `Backlog`, `Ready`, `In progress`, `Review` e
   `Done`.
2. Importe `docs/project-backlog.csv` ou crie Issues a partir dos templates em `.github/ISSUE_TEMPLATE`.
3. Atribua cada Issue a um integrante real, adicione Sprint 1 e estimativa.
4. Mova o cartão com o estado real; não marque como concluído antes do PR correspondente.
5. Cada PR deve usar `Closes #N` e listar os IDs da especificação afetados.

O CSV é uma decomposição inicial; Felipe Amorim Monteiro (RA 22452139), único integrante, deve ser
atribuído às Issues no GitHub. O print do Board deve mostrar responsável, estados e escopo da sprint.

### Exceção operacional: equipe individual

O requisito de aprovação “entre membros” é impossível com um único integrante. Autoaprovação ou
conta duplicada não constituem revisão e não devem ser usadas. Antes da entrega, confirme com o
docente uma destas opções e registre a autorização:

1. professor ou monitor como revisor do Pull Request;
2. colega externo à equipe adicionado como colaborador/revisor;
3. dispensa formal da aprovação humana, mantendo PR, comentários de autorrevisão e CI obrigatório.

A opção adotada foi colaborador externo autorizado, com autor e aprovador distintos. Ela deve
aparecer no PDF e nas evidências do GitHub.

## 4. Ciclo de uma tarefa

Exemplo para a Issue 3:

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/3-criar-reserva
# implementar, testar e fazer commits pequenos
git push -u origin feature/3-criar-reserva
```

Abra PR para `develop` usando o template. O revisor autorizado para a equipe individual verifica
comportamento, testes, aderência à especificação e segurança. O autor responde aos comentários com
commit ou justificativa; o revisor aprova apenas depois do CI verde. Para tornar o histórico
avaliável, não concentre todo o trabalho em um único PR e não use outra conta própria para simular
revisão.

## 5. Convenção de commits

Formato: `tipo(escopo): resumo no imperativo`.

```text
feat(reservas): impede conflito de horários
test(api): cobre cancelamento repetido
docs(spec): esclarece intervalos adjacentes
ci(harness): publica relatório de cobertura
```

Tipos aceitos: `feat`, `fix`, `test`, `docs`, `refactor`, `ci`, `chore`.

## 6. Checklist de revisão

- Issue e requisitos (`RF-*`, `RN-*`, `RNF-*`) estão vinculados.
- Critérios de aceitação são demonstrados por testes.
- Não há regra de negócio duplicada na API.
- Erros preservam o contrato documentado.
- Não há segredo, dado pessoal ou artefato local no diff.
- Ruff, Pytest e cobertura passam no GitHub Actions.
- Mudança arquitetural tem ADR; mudança de comportamento atualiza a especificação.

## 7. Evidências para as entregas

Guardar no PDF final:

- URL pública do repositório;
- tela do Project com Issues e responsáveis;
- pelo menos dois PRs com comentários, CI verde e a forma de revisão individual autorizada;
- ruleset de `main` sem push direto;
- execução verde do workflow e conteúdo do artefato `test-output.log`;
- execução Docker do harness.

Na Sprint 2, o marco **Entrega intermediária** reúne as Issues #13 a #19. Os PRs devem mostrar a
relação entre o teste de regressão, a re-especificação 0.3.0, o adaptador SQLite, a análise crítica de
IA e os checks. O relatório não deve marcar uma Issue como concluída antes do merge que a fecha.
