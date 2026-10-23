# Governança da Entrega 2

## Equipe e adaptação autorizada

Felipe Amorim Monteiro, RA 22452139, é o único integrante. `MorimFr` é a conta principal e
`SrMorim` é uma segunda conta da mesma pessoa. Em 14/10/2026, Felipe informou que o professor
autorizou essa adaptação para o trabalho individual. A autorização é relatada pelo aluno;
não há documento do professor anexado a este repositório.

As aprovações nas duas contas representam **autorrevisão humana**, não revisão independente entre
pares. O autor continua responsável por ler o diff, validar critérios e homologar as saídas da IA.
O relatório final explicita a adaptação em vez de afirmar que existe outro integrante ou colaborador.

Alguns documentos históricos da Entrega 1 usaram a expressão "colaborador externo" antes desse
esclarecimento. A caracterização correta para esta entrega é a adaptação individual descrita acima;
os artefatos anteriores foram preservados como histórico, não como comprovação de um segundo membro.

## Fluxo de branches

- `feature/*` e `fix/*`: tarefas vinculadas a Issues.
- `develop`: integração da sprint via PR, exemplificada pelo PR #20.
- `release/*`: consolidação da árvore validada em develop e promoção via PR para main.
- `main`: versão acadêmica publicada, sempre promovida por PR.

A branch `release/entrega-intermediaria` e o PR #24 foram necessários devido à diferença de
ancestralidade de squashes prévios. Merge commits foram habilitados em 14/10 para futuros merges de
branches duradouras; squash continua disponível para tarefas curtas. Não há necessidade de reescrever
o histórico já publicado nem fazer push direto em main/develop.

## Proteções verificáveis

Em 14/10/2026, a auditoria encontrou main/develop sem proteção e sem rulesets ativos. As proteções
clássicas foram reaplicadas via API, com configuração versionada em
`.github/branch-protection.json` (nome consolidado na Entrega 3):

- PR obrigatório, uma aprovação, descarte de aprovação após novo commit;
- aprovação do último push revisável, por conta diferente da conta que fez o push;
- check `quality`, branch atualizada e resolução de conversas;
- administradores sujeitos às regras; force push e exclusão desabilitados.

Esses controles conferem contas e checks; não verificam independência entre pessoas. Essa diferença
está coberta pela adaptação individual informada pelo aluno.

## Sprint, critérios e revisão

O marco Sprint 2 contém Issues #13-#19, #21 e #25, atribuídas a MorimFr. Cada tarefa tem critérios de
aceitação e referência a requisitos. Fechar tarefas concluídas em develop com evidência do PR
correspondente; reservar o aceite da publicação/PDF para a promoção final. Não criar comentários ou
aprovações que não tenham ocorrido.

Antes de aprovar, conferir:

1. regra e contrato HTTP atendidos, inclusive erros e bordas;
2. regressão, changelog e ADR para comportamento/arquitetura alterados;
3. nenhum segredo ou banco real no diff; dados de teste fictícios;
4. Ruff, Pytest e Docker aprovados; CI do commit atual verde;
5. leitura humana de transações, rollback, fuso e restrições da solução.

Commits usam `tipo(escopo): resumo`. Logs e referências ficam em `docs/evidence/entrega2/`.

## Encerramento (Entrega 3)

Sprint 3 / Issue #26: release/entrega-final -> PR para main, quality e autorrevisão humana autorizada.
A tag v1.0.0 aponta somente ao commit aprovado. Após a publicação não devem restar PRs abertos ou
conflitos. Documentos anteriores são históricos; SPECIFICATION.md e README indicam o As-Built final.
