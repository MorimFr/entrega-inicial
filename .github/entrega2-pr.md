## Resultado

Publica a Entrega 2 do CampusFlow: API persistente, consulta por usuário e homologação das regras.
Corrige participantes não inteiros, ordenação de datas com offsets diferentes e limite diário no
calendário do campus. Criação/cancelamento usam transação atômica, conservando invariantes mesmo sob
concorrência local.

Closes #19
Closes #25

As Issues #13-#18 e #21 foram concluídas nos PRs #20/#22; a promoção final preserva a implementação.

## Aceitação e validação

- [x] RN-03/RN-06/RN-10/RN-11 e especificação 0.4.0 atualizadas com regressões.
- [x] Falhas antes da correção preservadas em commit de teste: 12 failed, 1 passed.
- [x] Ruff aprovado, 55/55 testes locais, cobertura 99,66%.
- [x] Docker Python 3.12.15: 55/55, cobertura 99,69%.
- [x] Demonstração HTTP e preservação após recriação do contêiner aprovadas.
- [x] ADR-004, README, erros lógicos, relato e comparação/ética de IA consolidados.
- [x] CI publica stdout, cobertura e JUnit; falhas propagam código de saída.
- [ ] Homologação humana final do commit atual.

## Revisão e equipe individual

Felipe informou autorização docente para usar a própria conta secundária SrMorim na autorrevisão.
MorimFr e SrMorim são a mesma pessoa; não se alega revisão independente entre pares. O relatório
explicita essa adaptação. Proteções de main/develop exigem PR, quality e uma aprovação.

## Evidências

- `docs/evidence/test-run-intermediate-final.md`
- `docs/evidence/entrega2/` (logs brutos e snapshot do GitHub)
- `docs/ENTREGA_INTERMEDIARIA.pdf`
- `docs/AI_ETHICS.md`

O histórico anterior usava squash em branches duradouras. A branch de release consolida os dois
históricos sem descartar conteúdo; use merge commit nesta promoção.
