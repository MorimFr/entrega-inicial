# Encerramento - Entrega 3

Felipe Amorim Monteiro - RA 22452139. Equipe individual.

| Exigência | Evidência |
|---|---|
| Release estável | v1.0.0, a publicar no commit aprovado da main |
| Histórico e proteção | [PR #27](https://github.com/MorimFr/entrega-inicial/pull/27) da Issue #26, main protegida, sem outros PRs pendentes |
| As-Built | SPECIFICATION.md 1.0.0 e openapi.json conferido no CI |
| Testes e coverage | 63/63 aprovados; 99,70% de linhas no Docker; artifacts/ e docs/evidence/entrega3/ |
| Reprodutibilidade | Dockerfile multi-stage, Compose com runtime/tests/demo |
| Demonstração 3-5 min | Roteiro em DEMO.md; gravação e link do aluno ainda pendentes |
| Lições aprendidas | RETROSPECTIVE.md |
| PDF | Emitir versão definitiva após aprovação, release e link do vídeo acessível |

O vídeo não foi gravado até a preparação desta candidata. O PDF de revisão não deve ser submetido
como definitivo sem essa evidência obrigatória. A release v1.0.0 só será criada após a aprovação
humana do PR e o CI da main. Não se inventam links, aprovações ou resultados.

## Evidências visuais para o aluno

Os logs reais já atendem à alternativa screenshots/logs do enunciado. Se quiser complementar,
capture somente telas legíveis da versão final:

1. Terminal com o comando Docker, resumo `63 passed` e `Total coverage: 99.70%`.
2. GitHub Actions com `quality` verde e o commit correspondente.
3. Após publicação, página da release v1.0.0 com tag, commit e anexos.

Não são necessários prints da tela de Security desabilitada, de erros antigos do daemon ou de
configuração de branches para substituir o vídeo. A demonstração real de 3-5 minutos é obrigatória.

## Regenerar o relatório (autoria opcional)

O gerador usa `reportlab` (dependência de autoria, não do runtime). `gh` deve estar autenticado
para a captura pública. Sem link do vídeo, o comando abaixo gera apenas revisão:

```powershell
python scripts/capture_final_evidence.py
python scripts/build_final_report.py
```

Depois de fornecer vídeo real/duração e conferir acesso, homologar PR, integrar main e publicar a
release no commit aprovado. Capturar metadados finais em `artifacts/final/github.json`, passando
`--video-url`, `--video-seconds` e `--video-access-checked` apenas com os dados reais conferidos.
Executar o gerador com `--metadata artifacts/final/github.json --final --output output/pdf/ENTREGA_FINAL.pdf`.
O modo definitivo recusa pendências verificáveis. Anexar esse PDF à release; o de revisão não é
o documento de submissão. Links do PDF apontam a commits imutáveis, não a branches descartáveis.
