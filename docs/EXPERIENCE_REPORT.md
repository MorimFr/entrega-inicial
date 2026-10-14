# Relato de experiência - Entrega 2

Felipe Amorim Monteiro (RA 22452139) realizou o projeto individualmente com apoio do Codex. Informou
autorização docente para usar MorimFr/SrMorim na autorrevisão dos PRs. Não houve outro integrante.

A arquitetura da Entrega 1 separou regras e persistência. Na Entrega 2, SQLite substituiu a memória
na execução da API, enquanto fixtures mantiveram testes isolados. O exercício confirmou o valor da
porta: contratos e regras permaneceram testáveis sem banco externo.

O maior aprendizado foi que cobertura alta não mede completude das regras. A suíte de 34 casos
passava, mas a homologação encontrou tipo não inteiro, ordenação por texto e limite diário por offset.
As regressões iniciais falharam 12 vezes. Depois da correção e dos casos concorrentes, são 55 testes.
Especificação 0.4.0 e ADR-004 explicitam as decisões que antes estavam implícitas.

A verificação/gravação precisava ser atômica mesmo em uma API local: várias requisições podem
executar em threads distintas. BEGIN IMMEDIATE resolveu a concorrência de escritores no mesmo banco,
com custo de serialização. Implantação entre hosts e autenticação continuam fora do escopo.

O histórico também mostrou o custo de squashes em branches duradouras: main e develop ficaram com
conteúdo equivalente e ancestralidade divergente. Um release PR consolidou a árvore e a decisão de
merge foi documentada. Não foi necessário descartar trabalho nem fazer push direto na principal.

IA auxiliou implementação e detecção, mas também havia participado da geração do código com falhas.
A homologação humana, a especificação e o harness sustentam o aceite. As outras ferramentas foram
avaliadas documentalmente; não se atribuem notas experimentais que não foram medidas.

O relato individual descreve aprendizado, decisões e desafios de organização do trabalho, em vez de
inventar experiência de colaboração entre integrantes inexistentes.
