# Retrospectiva de encerramento

Felipe Amorim Monteiro (RA 22452139), equipe individual. Data: 23/10/2026.

O projeto evoluiu de API em memória para API SQLite persistente, com transações atômicas,
calendário comum do campus, contratos HTTP, testes concorrentes e execução Docker simplificada.
IDs RF/RN/RNF conectaram especificação, implementação e testes. As-Built registra o que foi
construído, incluindo os limites do escopo local.

Codex auxiliou decomposição, código, inspeção, documentação e regressões. O ganho observado foi
executar mais ciclos de hipótese, reprodução e validação. Não houve medição de uma referência manual:
não declaramos porcentagem de produtividade nem comparação temporal experimental. A suíte evoluiu
de 26 para 55 e, na candidata final, 63 casos; isso mede alcance da validação, não prova causal.

A IA também participou do código com falhas: validação só no HTTP, ordenação textual de datas,
limite diário por offset e coerção de epoch. A leitura humana do diff e o harness foram essenciais.
Cobertura alta não garante que a especificação esteja completa.

SQLite resolveu durabilidade com baixa complexidade, mas serializa escritores. Datas exigiram uma
política UTC-03 explícita. Squashes em branches duradouras causaram divergência de ancestralidade;
merge commits passaram a ser usados na promoção de releases. Na versão final, runtime e harness
foram separados, com usuário sem privilégios na API e porta publicada somente em loopback.

MorimFr e SrMorim são contas do mesmo aluno; a adaptação individual foi autorizada pelo professor
conforme relato registrado. Os PRs demonstram autorrevisão, não independência entre pares.
Checks, proteção de branches e registros ajudam a disciplina, mas não substituem julgamento humano.

A principal lição é que uma release estável deve apontar ao commit aprovado e ter contratos,
evidências e limitações coerentes. Vídeo e logs devem refletir a aplicação real, sem simulações.
