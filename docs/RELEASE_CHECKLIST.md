# Publicação final v1.0.0

## Já preparado na candidata (Issue #26)

- Código, testes de regressão, As-Built e OpenAPI da versão 1.0.0.
- Docker runtime sem ferramentas de testes e sem root; harness com relatórios persistidos.
- Logs reais, XML JUnit/coverage, demo HTTP e persistência após recriação.
- README, ADRs 001-005, retrospectiva e roteiro do vídeo.
- Gerador de PDF que distingue revisão de submissão definitiva.

## Aceite humano e vídeo

1. Gravar 3-5 min conforme `DEMO.md` e fornecer link acessível ao professor.
2. Registrar link/duração no relatório; não publicar senha ou token.
3. Conferir o diff do PR, As-Built, logs e critérios de aceite; aguardar o check `quality` verde.
4. Aprovar o último push usando a adaptação individual autorizada. As duas contas pertencem a
   Felipe; o registro é autorrevisão e não revisão independente por outro integrante.

## Somente após aprovação

1. Fazer merge do PR em `main`, sem bypass, preferindo merge commit para conservar ancestralidade.
2. Conferir CI do commit exato da main e ausência de outros PRs abertos/conflitos.
3. Conferir branch protection e fechamento da Issue/milestone da conclusão.
4. Emitir o PDF definitivo com commit, PR, CI, link do vídeo e URL da release.
5. Criar tag/release `v1.0.0` no commit aprovado; anexar PDF, logs e cobertura. Não criar tag na
   candidata nem mover uma tag estável publicada para outro commit.
6. Conferir tag, acessibilidade dos links e baixar/abrir os anexos. Submeter o PDF definitivo.

O PDF de revisão não substitui o definitivo. A publicação pode ocorrer no mesmo ciclo após o
merge, mas não é considerada concluída enquanto o vídeo e a release não existirem.
