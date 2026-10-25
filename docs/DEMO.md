# Vídeo final - roteiro de 3 a 5 minutos

Felipe Amorim Monteiro - RA 22452139. Grave a tela com sua narração e dados fictícios.
Meta: aproximadamente quatro minutos, com aplicação e testes executados ao vivo.

## Preparação (antes de gravar)

Abra Docker Desktop, um terminal nesta pasta, o README no GitHub e http://localhost:8000/docs.
Prepare as imagens antes da gravação para não gastar o vídeo com downloads:

```powershell
docker compose build api tests demo
docker compose up -d --wait api
```

Use fonte grande, microfone ativo e feche telas com credenciais/dados pessoais.

## Roteiro de aproximadamente 4 minutos

| Tempo | O que mostrar | Narração sugerida |
|---|---|---|
| 0:00-0:30 | README e identificação | "Sou Felipe Amorim Monteiro, RA 22452139. O CampusFlow evita conflitos na reserva de salas de estudo por uma API local persistente em Docker." |
| 0:30-1:00 | Swagger: GET /rooms, Try it out, Execute | "Cada sala tem capacidade. A API aplica duração máxima, participantes e limite diário no calendário do campus." |
| 1:00-2:10 | Executar o comando demo abaixo | "Crio uma reserva e consulto seu ID. Outra no mesmo horário retorna 409. Consulto por usuário, cancelo e testo uma entrada inválida." |
| 2:10-3:00 | Executar o comando tests abaixo | "Os testes estão rodando agora: unitários, HTTP, SQLite, fusos e concorrência. 100% de passagem é diferente de cobertura de linhas. O gate é 90% de cobertura." |
| 3:00-3:35 | As-Built e diagrama | "O domínio é isolado do HTTP e do SQLite. A transação mantém verificação e gravação atômicas. O volume conserva os registros após reinício." |
| 3:35-4:10 | PR/release e retrospectiva | "A IA acelerou iterações, mas seus resultados exigiram testes e homologação humana. Aprendi sobre fusos, atomicidade e governança. A autorrevisão individual foi adaptada com autorização docente." |

Demonstração funcional:

```powershell
docker compose --profile demo run --rm demo
```

Testes ao vivo (mostre o resumo e coverage):

```powershell
docker compose --profile test run --rm --build tests
```

Se gravar antes da aprovação, diga que é candidata à homologação v1.0.0. Depois da publicação, mostre
a release v1.0.0. Não simule uma tag inexistente nem edite a saída para esconder falhas.

## Publicação do vídeo

Suba em YouTube não listado, Google Drive, Loom ou SharePoint. Libere acesso ao professor e confira
o link numa janela anônima/conta autorizada. Confirme duração entre 3 e 5 min, áudio legível e testes
visíveis. Envie o link aqui para incorporá-lo ao PDF e à release. Não envie senha ou token.

Após o uso, `docker compose down` encerra os contêineres sem apagar o volume.
