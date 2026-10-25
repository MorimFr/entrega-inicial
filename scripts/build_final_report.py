"""PDF da Entrega 3 a partir de XMLs/logs reais e snapshot público do GitHub.

Autoria: pip install reportlab. Não é dependência da aplicação/runtime.
O modo --final recusa publicação sem vídeo, release no commit homologado e CI da main.
"""

import argparse
import json
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from build_intermediate_report import Architecture, configure_fonts, inline, read
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence/entrega3"
REPO = "https://github.com/MorimFr/entrega-inicial"
RELEASE = f"{REPO}/releases/tag/v1.0.0"
BLUE = colors.HexColor("#17385B")
TEAL = colors.HexColor("#087F8C")


def pending(snapshot: dict) -> list[str]:
    """Critérios verificáveis; não assume aprovação/publicação a partir do nome de arquivo."""
    reasons = []
    pr, main = snapshot["pr"], snapshot["main"]
    if pr["state"] != "MERGED" or (pr.get("mergeCommit") or {}).get("oid") != main["sha"]:
        reasons.append("PR final ainda não integrado ao commit atual da main")
    if not any(review["state"] == "APPROVED" for review in pr.get("reviews", [])):
        reasons.append("homologação humana do PR ainda não registrada")
    checks = snapshot["protection"]["required_status_checks"]["contexts"]
    if not main["protected"] or "quality" not in checks:
        reasons.append("proteção da main/quality não confirmada")
    if not any(
        run["headSha"] == main["sha"]
        and run["headBranch"] == "main"
        and run["conclusion"] == "success"
        for run in snapshot["runs"]
    ):
        reasons.append("CI aprovado do commit final da main ainda não confirmado")
    release = snapshot.get("release")
    if not release or release["isDraft"] or snapshot.get("tag_commit") != main["sha"]:
        reasons.append("release v1.0.0 publicada no commit aprovado ainda não confirmada")
    if snapshot["open_prs"]:
        reasons.append("existem Pull Requests abertos")
    video = snapshot["video"]
    if not video["url"] or not video["seconds"] or not 180 <= video["seconds"] <= 300:
        reasons.append("vídeo real de 3-5 minutos ainda não informado")
    if not video["access_checked"]:
        reasons.append("acesso do professor ao vídeo ainda não conferido")
    return reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=EVIDENCE / "github.json")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "output/pdf/ENTREGA_FINAL_REVISAO.pdf"
    )
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    snapshot = json.loads(args.metadata.read_text(encoding="utf-8-sig"))
    source_ref = snapshot["main"]["sha"] if args.final else snapshot["pr"]["headRefOid"]
    blob = f"{REPO}/blob/{source_ref}"
    reasons = pending(snapshot)
    junit = ET.parse(EVIDENCE / "junit.xml").getroot().find("testsuite")
    assert junit is not None
    total = int(junit.attrib["tests"])
    failed = sum(int(junit.attrib[key]) for key in ("failures", "errors", "skipped"))
    if failed:
        raise RuntimeError("A evidência não demonstra aprovação integral dos testes")
    if args.final and reasons:
        raise RuntimeError("PDF definitivo bloqueado: " + "; ".join(reasons))
    coverage = ET.parse(EVIDENCE / "coverage.xml").getroot()
    covered, valid = int(coverage.attrib["lines-covered"]), int(coverage.attrib["lines-valid"])
    percent = f"{100 * covered / valid:.2f}".replace(".", ",")
    if covered / valid < 0.9:
        raise RuntimeError("Cobertura abaixo do critério mínimo de 90%")
    configure_fonts()
    styles = getSampleStyleSheet()
    for name, size, leading in [("BodyPT", 10, 14), ("CellPT", 8.5, 11.5)]:
        styles.add(
            ParagraphStyle(
                name,
                fontName="Campus",
                fontSize=size,
                leading=leading,
                spaceAfter=7 if name == "BodyPT" else 0,
                textColor=BLUE,
            )
        )
    styles.add(
        ParagraphStyle(
            "TitlePT",
            fontName="Campus-Bold",
            fontSize=30,
            leading=36,
            spaceAfter=18,
            textColor=BLUE,
        )
    )
    styles.add(
        ParagraphStyle(
            "HeadingPT",
            fontName="Campus-Bold",
            fontSize=18,
            leading=24,
            spaceAfter=14,
            textColor=BLUE,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "CodePT",
            fontName="Courier",
            fontSize=8,
            leading=11,
            spaceAfter=12,
            backColor=colors.HexColor("#EEF4F7"),
            borderPadding=7,
        )
    )
    story = []

    def para(text: str, style: str = "BodyPT") -> None:
        story.append(Paragraph(inline(text), styles[style]))

    def heading(text: str, new_page: bool = True) -> None:
        if new_page:
            story.append(PageBreak())
        para(text, "HeadingPT")

    def table(rows: list[list[str]], widths: list[int]) -> None:
        rendered = [[Paragraph(inline(cell), styles["CellPT"]) for cell in row] for row in rows]
        grid = Table(rendered, colWidths=widths, repeatRows=1, hAlign="LEFT")
        grid.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DFEDF2")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B5CAD6")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.extend([grid, Spacer(1, 14)])

    def code(text: str) -> None:
        wrapped = "\n".join(
            textwrap.fill(line, 87, subsequent_indent="  ", replace_whitespace=False)
            if line
            else ""
            for line in text.splitlines()
        )
        story.append(Preformatted(wrapped, styles["CodePT"]))

    para("CampusFlow", "TitlePT")
    para("Entrega 3 - Conclusão do projeto", "HeadingPT")
    para("Solução final, As-Built, testes homologados e release versionada.")
    para("**Felipe Amorim Monteiro - RA 22452139**<br/>Equipe individual. CEUB.")
    para(f"Snapshot de governança: {snapshot['captured_at']}.")
    status = "DEFINITIVO PARA SUBMISSÃO" if args.final else "REVISÃO - NÃO SUBMETER AINDA"
    para(f"**Estado: {status}**")
    table(
        [
            ["Indicador", "Resultado observado"],
            ["Harness Docker", f"{total}/{total} aprovados (100%); 0 falhas/erros/ignorados"],
            ["Cobertura de linhas", f"{percent}% ({covered}/{valid}); mínimo 90%"],
            ["Aplicação empacotada", "API HTTP, SQLite persistente, runtime sem root e sem pytest"],
            [
                "Vídeo",
                "Informado e acesso conferido"
                if snapshot["video"]["access_checked"]
                else "Pendente de gravação/link acessível ao professor",
            ],
            [
                "Release",
                "Publicada e vinculada ao commit da main"
                if args.final
                else "Publicação estável depende de homologação; consultar pendências",
            ],
        ],
        [150, 341],
    )
    para(
        f"[Repositório público]({REPO})<br/>[PR final #{snapshot['pr']['number']}]"
        f"({snapshot['pr']['url']})<br/>[Release v1.0.0]({RELEASE})"
        + (" - URL prevista; verificar publicação antes de submeter." if not args.final else "")
    )
    para(
        "**Resumo executivo.** O CampusFlow resolve conflitos de reserva de salas compartilhadas "
        "com validação de capacidade, duração, fuso e limite diário. A solução entrega API local "
        "persistente e testes em ambiente padronizado. Não promete autenticação institucional nem "
        "segurança para exposição pública; esses itens estão fora do escopo aprovado."
    )

    heading("1. Solução entregue e As-Built")
    story.extend([Architecture(), Spacer(1, 15)])
    para(
        "O adaptador HTTP valida o formato e chama o serviço. As regras não são duplicadas nas "
        "rotas; domínio e porta de repositório permitem testes em memória e SQLite. Criação e "
        "cancelamento mantêm consultas e gravação na mesma fronteira transacional. SQLite usa "
        "BEGIN IMMEDIATE no mesmo arquivo local."
    )
    table(
        [
            ["Contrato", "Entrega definitiva"],
            ["GET /health e /rooms", "Liveness e catálogo: sala-a (4), sala-b (8)"],
            [
                "POST /reservations",
                "201 + reserva; 404 sala ausente; 409 conflito/limite; 422 inválido",
            ],
            ["GET /reservations/{id}", "Reserva com estado; 404 se inexistente"],
            [
                "GET /reservations?user_id=...",
                "Filtro opcional active/cancelled e ordenação por instante/ID",
            ],
            ["DELETE /reservations/{id}", "200 cancelled; segundo cancelamento 409; ausente 404"],
            [
                "GET /rooms/{id}/availability",
                "Consulta de ausência de conflito; ISO com offset obrigatório",
            ],
        ],
        [193, 298],
    )
    para(
        "Regras: intervalo semiaberto com fuso, duração até duas horas, inteiro positivo até a "
        "capacidade, adjacência permitida, no máximo duas reservas ativas por usuário na data do "
        "campus UTC-03. Canceladas não ocupam horário nem limite. "
        "Datas numéricas/epoch são rejeitadas."
    )
    para(
        f"[As-Built 1.0.0]({blob}/docs/SPECIFICATION.md) e "
        f"[snapshot OpenAPI]({blob}/docs/openapi.json): RF-01 a RF-08, "
        "RN-01 a RN-11, RNF-01 a RNF-07. CI confere o snapshot contra a API."
    )

    heading("2. Relatório dos testes aprovados")
    para(
        f"Fonte automática: junit.xml, execução {junit.attrib['timestamp']}; tempo registrado "
        f"no JUnit: {junit.attrib['time']} s. Linux, Python 3.12.15, pytest 8.4.1."
    )
    counts = Counter(case.attrib["classname"].split(".")[1] for case in junit.findall("testcase"))
    table(
        [["Camada", "Casos", "Resultado"]]
        + [[name, str(count), "Todos aprovados"] for name, count in sorted(counts.items())]
        + [["Total", str(total), "100% de passagem"]],
        [240, 70, 181],
    )
    para(
        "Abrangência: criação/consulta/cancelamento, 404, duração exata de 2 h e excesso, "
        "capacidade, tipos inválidos, conflito/adjacência, limite diário, offsets diferentes, "
        "recriação de repositório, rollback e concorrência entre threads/instâncias SQLite."
    )
    log = read(EVIDENCE / "docker.log")
    code("\n".join(log.splitlines()[-21:]))
    para(
        "O aviso de depreciação Starlette/AnyIO foi preservado no log completo. Não houve testes "
        "ignorados ou desativados para satisfazer o gate. Execução complementar no host Python "
        "3.14.7: 63 aprovados e 99,67%; a referência homologada é o Docker Python 3.12."
    )
    para(
        f"[Log integral]({blob}/docs/evidence/entrega3/docker.log), "
        f"[JUnit]({blob}/docs/evidence/entrega3/junit.xml) e "
        "artefatos do workflow identificado na seção de governança."
    )

    heading("3. Cobertura e demonstração HTTP")
    rows = [["Módulo", "Linhas cobertas / total", "Cobertura"]]
    for module in coverage.findall(".//class"):
        lines = module.findall("./lines/line")
        hits = sum(int(line.attrib["hits"]) > 0 for line in lines)
        rows.append(
            [
                module.attrib["filename"],
                f"{hits}/{len(lines)}",
                f"{100 * hits / len(lines):.2f}%".replace(".", ","),
            ]
        )
    rows.append(["TOTAL", f"{covered}/{valid}", f"{percent}%"])
    table(rows, [242, 150, 99])
    para(
        "Cobertura de linhas, não de branches. A única linha não executada é o retorno defensivo "
        "None em repository.py:100. Não se remove tratamento válido para inflar a métrica. "
        "100% de passagem e cobertura são medidas distintas; nenhuma garante ausência de defeitos."
    )
    demo = read(EVIDENCE / "demo.log")
    lines = [line for line in demo.splitlines() if " -> HTTP " in line or "DEMO_OK:" in line]
    code("\n".join(lines).replace("7cd6d067-36d5-4447-af39-519f93874bc9", "{id}"))
    para(
        "Trecho da demo HTTP real; identificador substituído por {id} apenas para legibilidade. "
        "O log original preserva o valor integral. Após force-recreate, a consulta retornou 200 "
        "com o estado cancelled preservado (PERSISTENCE_OK). Runtime: uid 999 e pytest ausente."
    )

    heading("4. Instalação, execução e empacotamento")
    para(
        "Pré-requisito: Docker Engine/Desktop iniciado e Compose disponível. Clone o repositório; "
        "após publicação use a tag v1.0.0. Antes disso, a branch de revisão não é release estável."
    )
    code(
        f"git clone {REPO}.git\ncd entrega-inicial\n"
        "git checkout v1.0.0\ndocker compose up --build -d --wait api"
    )
    para(
        "Abra http://localhost:8000/docs. A API publica só em 127.0.0.1. Não são necessárias "
        "credenciais nem Python local. Para mudar porta, crie .env com CAMPUSFLOW_PORT=8001. "
        "O Compose fixa CAMPUSFLOW_DATABASE_PATH=/app/data/campusflow.db em volume nomeado."
    )
    code(
        "docker compose --profile demo run --rm demo\n"
        "docker compose --profile test run --rm --build tests\n"
        "docker compose down"
    )
    para(
        "O harness executa Ruff + Pytest e retorna código não zero em falhas. Exporta "
        "artifacts/test-output.log, junit.xml, coverage.xml e htmlcov/index.html para o host. "
        "down encerra contêineres sem excluir o banco; não use --volumes para conservar reservas."
    )
    table(
        [
            ["Decisão", "Justificativa e trade-off"],
            [
                "ADR-001/002",
                "Camadas/porta substituível; FastAPI + Ruff/Pytest; "
                "mais interfaces, maior isolamento",
            ],
            [
                "ADR-003",
                "SQLite local dispensa servidor; serializa escritores e não atende multi-host",
            ],
            ["ADR-004", "UTC-03 comum e transação atômica evitam limites contornados/corridas"],
            [
                "ADR-005",
                "Versão única; runtime mínimo sem root; harness separado; "
                "publicação após homologação",
            ],
        ],
        [125, 366],
    )
    para(
        "Base Python fixada por digest e dependências diretas fixadas. Manifests instalados foram "
        "registrados; não se afirma reprodução bit a bit de transitivas/build tools. Limites: "
        "user_id não autentica identidade, catálogo fixo, "
        "sem política de antecedência ou frontend próprio."
    )

    heading("5. Governança, release e rastreabilidade")
    pr = snapshot["pr"]
    para(
        f"[PR #{pr['number']}]({pr['url']}): {pr['state']}; "
        f"rascunho: {'sim' if pr['isDraft'] else 'não'}. "
        f"Branch {pr['headRefName']} para {pr['baseRefName']}."
    )
    code(
        f"HEAD da candidata: {pr['headRefOid']}\nmain no snapshot: {snapshot['main']['sha']}\n"
        f"Tag v1.0.0: {snapshot.get('tag_commit') or 'ainda não publicada'}"
    )
    para(
        "Main protegida com PR obrigatório, uma aprovação, descarte de aprovações antigas, "
        "aprovação do último push, check quality estrito e aplicação aos administradores. "
        "A tag estável será vinculada ao commit aprovado, sem mover tags publicadas."
    )
    relevant_runs = [
        run
        for run in snapshot["runs"]
        if run["headSha"] in {pr["headRefOid"], snapshot["main"]["sha"]}
    ]
    for run in relevant_runs[:4]:
        para(
            f"[Workflow {run['databaseId']}]({run['url']}): {run['headBranch']}, "
            f"{run['status']}/{run['conclusion'] or 'em andamento'}, SHA {run['headSha'][:12]}."
        )
    para(
        "MorimFr e SrMorim são contas do mesmo aluno. O professor autorizou a adaptação "
        "individual segundo relato do aluno. Os PRs evidenciam autorrevisão humana, não uma "
        "revisão independente entre integrantes. Não foram criadas aprovações pelo agente."
    )
    para(
        f"[Issue #26]({REPO}/issues/26) organiza os critérios de encerramento. "
        f"Histórico: [PR #10]({REPO}/pull/10), [#11]({REPO}/pull/11), "
        f"[#20]({REPO}/pull/20), [#22]({REPO}/pull/22) e [#24]({REPO}/pull/24)."
    )
    para(
        "Higienização: removidos arquivos operacionais temporários da etapa anterior, sem "
        "apagar o histórico. Bancos, .env, bytecode e relatórios regeneráveis são ignorados. "
        "Inspeção básica não encontrou credenciais nos arquivos versionados; "
        "não equivale a pentest."
    )

    heading("6. Retrospectiva e vídeo de demonstração")
    para(
        "A evolução foi de API em memória para persistência SQLite, calendário do campus, "
        "atomicidade, contratos conferidos e empacotamento. A suíte cresceu de 26 para 55 e 63 "
        "casos, preservando regressões em vez de desativar testes."
    )
    para(
        "**Eficácia da IA.** Codex auxiliou decomposição, implementação, inspeção e documentação. "
        "O ganho observado foi a capacidade de iterar mais hipóteses e validações. Não foi medido "
        "tempo de referência manual; não há percentual de produtividade causal a apresentar."
    )
    para(
        "**Dificuldades e lições.** Validação restrita ao HTTP, coerção de tipos, "
        "offsets diferentes, "
        "ordenação textual e janela de corrida mostraram que código plausível pode contrariar "
        "o contrato. Testes, transações e re-especificação corrigiram os defeitos. Squashes em "
        "branches duradouras ensinaram a preservar ancestralidade na promoção de releases."
    )
    para(
        "**Governança e segurança.** A aprovação humana não é delegada ao agente. "
        "O escopo é local: "
        "não expor dados reais numa API sem autenticação. Contexto enviado à IA não deve conter "
        "segredos. Código gerado requer revisão de dependências, licenças e correção. Cobertura "
        "alta não substitui homologação ou uma especificação adequada."
    )
    video = snapshot["video"]
    if video["url"]:
        para(
            f"**Vídeo:** [demonstração funcional]({video['url']}). "
            f"Duração informada: {video['seconds']} segundos. Acesso conferido: "
            f"{'sim' if video['access_checked'] else 'não'}."
        )
    else:
        para(
            "**VÍDEO PENDENTE.** O aluno informou que ainda não gravou. É necessário gravar "
            "3-5 minutos com tela, narração, fluxo de uso e execução dos testes em tempo real, "
            "publicar link acessível ao professor e incorporá-lo antes de submeter."
        )
    table(
        [
            ["Tempo sugerido", "Conteúdo da gravação real"],
            ["0:00-1:00", "Identificação, problema resolvido, Swagger GET /rooms"],
            ["1:00-2:10", "Demo ao vivo: criação, consulta, conflito, filtro e cancelamento"],
            ["2:10-3:00", "Harness ao vivo e resultado/cobertura"],
            ["3:00-4:10", "As-Built, PR/release e lições aprendidas"],
        ],
        [120, 371],
    )
    para(
        f"[Roteiro e comandos]({blob}/docs/DEMO.md). "
        "Vídeo deve ter áudio legível e resultados visíveis; não simular saída ou tag inexistente."
    )

    heading("7. Checklist de encerramento")
    table(
        [
            ["Item exigido no PDF", "Referência / estado"],
            ["Release oficial v1.0.0", "Capa e seção 5; depende de publicação no commit aprovado"],
            ["Nome e RA", "Capa e rodapé: Felipe Amorim Monteiro, 22452139"],
            ["100% de passagem e coverage", "Seções 2/3; logs e XML reais anexados no repositório"],
            ["Link do vídeo 3-5 minutos", "Seção 6; gravação real e acesso são obrigatórios"],
            ["Resumo executivo e lições", "Capa e seção 6; contexto individual explícito"],
        ],
        [190, 301],
    )
    if not args.final:
        para("**Pendências verificadas no snapshot:**")
        for reason in reasons:
            para("- " + reason + ".")
        para(
            "Este documento é material de revisão. Não deve ser submetido como encerramento "
            "definitivo enquanto essas pendências existirem. "
            "O gerador recusa --final nessas condições."
        )
    else:
        para(
            "Snapshot confirma PR integrado, CI aprovado da main, proteção, "
            "ausência de PRs abertos "
            "e release no mesmo commit. Link/duração e acesso do vídeo foram informados/conferidos "
            "pelo aluno. Este PDF é a versão de submissão da Entrega 3."
        )
    para(
        "**Integridade.** Relatório gerado por scripts/build_final_report.py a partir de XMLs/logs "
        "e snapshot público coletado por capture_final_evidence.py. Nenhum print sintético é usado "
        "como prova. O enunciado aceita screenshots/logs; os logs reais já documentam os testes."
    )

    def page(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(TEAL)
        canvas.line(52, 797, 543, 797)
        canvas.setFont("Campus", 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(
            52,
            810,
            "CampusFlow | Entrega 3 | "
            + ("Definitivo" if args.final else "Revisão - não submeter"),
        )
        canvas.drawString(52, 31, "Felipe Amorim Monteiro - RA 22452139")
        canvas.drawRightString(543, 31, str(document.page))
        canvas.restoreState()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(args.output),
        pagesize=A4,
        leftMargin=52,
        rightMargin=52,
        topMargin=59,
        bottomMargin=52,
        title="CampusFlow - Entrega 3",
        author="Felipe Amorim Monteiro",
        subject="Encerramento, testes e release",
    )
    doc.build(story, onFirstPage=page, onLaterPages=page)
    print(f"PDF_OK: {args.output}")


if __name__ == "__main__":
    main()
