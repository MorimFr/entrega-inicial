"""Gera o PDF consolidado da Entrega 2 a partir de fontes e logs reais.

Dependências de autoria (não da aplicação): reportlab, pillow; QA: pypdf e PyMuPDF.
Executar: python scripts/build_intermediate_report.py
"""

import json
import re
import textwrap
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence/entrega2"
OUTPUT = ROOT / "output/pdf/ENTREGA_INTERMEDIARIA.pdf"
REPO = "https://github.com/MorimFr/entrega-inicial"
BLUE = colors.HexColor("#17385B")
TEAL = colors.HexColor("#087F8C")


def read(path: Path) -> str:
    content = path.read_bytes()
    if content.startswith((b"\xff\xfe", b"\xfe\xff")):
        return content.decode("utf-16")
    return content.decode("utf-8-sig")


def configure_fonts() -> None:
    for base in [Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu")]:
        regular = base / ("arial.ttf" if base.name == "Fonts" else "DejaVuSans.ttf")
        bold = base / ("arialbd.ttf" if base.name == "Fonts" else "DejaVuSans-Bold.ttf")
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("Campus", str(regular)))
            pdfmetrics.registerFont(TTFont("Campus-Bold", str(bold)))
            pdfmetrics.registerFontFamily("Campus", normal="Campus", bold="Campus-Bold")
            return
    raise RuntimeError("Instale Arial ou DejaVuSans para renderizar acentos corretamente")


def inline(text: str) -> str:
    text = text.replace("—", "-").replace("–", "-").replace("‑", "-")
    rendered = escape(text)
    rendered = rendered.replace("&lt;br/&gt;", "<br/>")
    rendered = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        r'<link href="\2" color="#087F8C">\1</link>',
        rendered,
    )
    rendered = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", r"\1", rendered)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", rendered)
    rendered = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", rendered)
    rendered = rendered.replace("→", "-&gt;").replace("≥", "&gt;=")
    return rendered


class Architecture(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 490
        self.height = 166

    def draw(self):
        canvas = self.canv
        nodes = [
            (0, 110, "Cliente HTTP"),
            (168, 110, "FastAPI / schemas"),
            (336, 110, "Serviço / regras"),
            (336, 52, "Porta / transação"),
            (168, 0, "SQLite + volume"),
            (336, 0, "Memória / testes"),
            (0, 0, "Harness / CI"),
        ]
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(1.4)
        for x1, y1, x2, y2 in [
            (140, 128, 168, 128),
            (308, 128, 336, 128),
            (406, 110, 406, 88),
            (376, 52, 238, 36),
            (406, 52, 406, 36),
            (140, 18, 168, 18),
        ]:
            canvas.line(x1, y1, x2, y2)
        for x, y, label in nodes:
            canvas.setFillColor(colors.HexColor("#EAF2F6"))
            canvas.roundRect(x, y, 140, 36, 5, stroke=1, fill=1)
            canvas.setFillColor(BLUE)
            canvas.setFont("Campus", 9)
            canvas.drawCentredString(x + 70, y + 14, label)


def main() -> None:
    configure_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "BodyPT",
            fontName="Campus",
            fontSize=10,
            leading=14,
            spaceAfter=7,
            textColor=colors.HexColor("#263442"),
        )
    )
    styles.add(
        ParagraphStyle(
            "TitlePT",
            fontName="Campus-Bold",
            fontSize=30,
            leading=37,
            textColor=BLUE,
            spaceAfter=20,
        )
    )
    for level, size in [(1, 19), (2, 14), (3, 11)]:
        styles.add(
            ParagraphStyle(
                f"H{level}PT",
                fontName="Campus-Bold",
                fontSize=size,
                leading=size + 5,
                textColor=BLUE,
                spaceBefore=12,
                spaceAfter=9,
                keepWithNext=True,
            )
        )
    styles.add(
        ParagraphStyle(
            "CellPT",
            fontName="Campus",
            fontSize=8,
            leading=11,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            "CodePT",
            fontName="Courier",
            fontSize=8,
            leading=10.4,
            spaceBefore=7,
            spaceAfter=10,
            backColor=colors.HexColor("#F0F4F7"),
            borderPadding=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverPT",
            parent=styles["BodyPT"],
            fontSize=13,
            leading=20,
            alignment=TA_CENTER,
        )
    )
    story = []

    def para(text: str, style="BodyPT"):
        story.append(Paragraph(inline(text), styles[style]))

    def table(rows):
        count = len(rows[0])
        widths = {2: [132, 358], 3: [116, 170, 204], 4: [73, 139, 139, 139]}
        cells = [[Paragraph(inline(cell), styles["CellPT"]) for cell in row] for row in rows]
        element = Table(cells, colWidths=widths.get(count, [490 / count] * count), repeatRows=1)
        element.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEBF2")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B9C8D3")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.extend([element, Spacer(1, 10)])

    def code(text):
        wrapped = "\n".join(
            textwrap.fill(line.expandtabs(2), width=103, subsequent_indent="  ")
            if len(line) > 103
            else line.expandtabs(2)
            for line in text.splitlines()
        )
        story.append(Preformatted(wrapped, styles["CodePT"]))

    def markdown(path):
        lines = read(ROOT / path).splitlines()
        paragraph = []
        index = 0

        def flush():
            if paragraph:
                para(" ".join(paragraph))
                paragraph.clear()

        while index < len(lines):
            line = lines[index].strip()
            if line.startswith("```"):
                flush()
                block = []
                index += 1
                while index < len(lines) and not lines[index].strip().startswith("```"):
                    block.append(lines[index])
                    index += 1
                code("\n".join(block))
            elif line.startswith("|"):
                flush()
                rows = []
                while index < len(lines) and lines[index].strip().startswith("|"):
                    candidate = lines[index].strip()
                    if not re.match(r"^\|[\s:|\-]+\|$", candidate):
                        rows.append([cell.strip() for cell in candidate.strip("|").split("|")])
                    index += 1
                if rows:
                    # Corrige títulos com apenas quatro colunas de tabela neste relatório.
                    table(rows)
                continue
            elif line.startswith("#"):
                flush()
                level = min(3, len(line) - len(line.lstrip("#")))
                if index != 0:
                    para(line.lstrip("# "), f"H{level}PT")
            elif not line:
                flush()
            elif line.startswith("- ") or re.match(r"^\d+\. ", line):
                flush()
                para(line)
            else:
                paragraph.append(line)
            index += 1
        flush()

    snapshot = json.loads(read(EVIDENCE / "github.json"))
    pr = snapshot["pr"]
    published = pr["state"] == "MERGED"
    checks = pr.get("statusCheckRollup", [])
    success = next((item for item in checks if item.get("conclusion") == "SUCCESS"), None)
    ci_url = success["detailsUrl"].split("/job/")[0] if success else REPO + "/actions"

    story.append(Spacer(1, 80))
    para("CampusFlow", "TitlePT")
    para("Entrega 2 - Etapa intermediária", "H1PT")
    para("Publicação, refinamento, testes e análise técnico-ética do uso de IA")
    story.append(Spacer(1, 36))
    para("**Felipe Amorim Monteiro**<br/>RA 22452139", "CoverPT")
    para("14 de outubro de 2026", "CoverPT")
    story.append(Spacer(1, 32))
    para(f"Repositório público: [MorimFr/entrega-inicial]({REPO})")
    version_label = "Versão publicada" if published else "Versão candidata"
    para(f"{version_label}: [PR #24]({pr['url']}); implementação homologada f863ddb.")
    para(
        "**Estado:** versão aprovada e publicada na main."
        if published
        else "**Estado:** código e relatório preparados; aprovação e publicação na main pendentes."
    )
    para(
        "Equipe individual: autorrevisão na conta secundária, "
        "conforme autorização docente relatada pelo aluno."
    )
    story.append(PageBreak())

    para("1. Problema, escopo e ambiente", "H1PT")
    para(
        "CampusFlow resolve conflitos no agendamento de salas de estudo. "
        "A solução é uma API integrada "
        "que lista salas, cria/consulta/cancela reservas, calcula disponibilidade "
        "e consulta reservas "
        "por usuário. A versão final persiste em SQLite e conserva regras em transações locais."
    )
    table(
        [
            ["Regra", "Comportamento homologado"],
            ["RN-01 / RN-02", "Intervalos com offset, fim posterior e duração de até 2 horas."],
            ["RN-03", "Inteiro positivo estrito, limitado à capacidade da sala."],
            ["RN-04 / RN-05", "Conflitos rejeitados; intervalos adjacentes permitidos."],
            [
                "RN-06 / RN-08",
                "Até duas reservas ativas por usuário/dia do campus; canceladas liberam limites.",
            ],
            ["RN-07 / RN-09", "Segundo cancelamento é 409; recurso ausente é 404."],
            [
                "RN-10 / RN-11",
                "Listagem cronológica por usuário; transação conserva invariantes concorrentes.",
            ],
        ]
    )
    para("Arquitetura e fluxo de criação", "H2PT")
    story.append(Architecture())
    story.append(Spacer(1, 12))
    para(
        "HTTP valida o formato; serviço inicia transação, consulta "
        "sala/limite/conflitos e grava apenas "
        "se todas as regras passam. Exceção reverte a gravação. "
        "O domínio independe de FastAPI e SQL."
    )
    para("Instalação e execução", "H2PT")
    code(
        "docker compose up --build api\n# Swagger: http://localhost:8000/docs\n"
        "docker compose --profile test run --rm --build tests\n"
        '# Local: Python 3.12 + python -m pip install -e ".[dev]"\n'
        "python -m ruff check .\npython -m pytest"
    )
    para(
        "Docker usa imagem Python 3.12 fixada por digest e volume SQLite. "
        "Autenticação, interface web "
        "e implantação entre hosts ficam fora do escopo original. user_id não prova identidade; "
        "a API é um demonstrador acadêmico local, sem homologação para dados reais de produção."
    )
    story.append(PageBreak())

    para("2. Testes automatizados e execução", "H1PT")
    table(
        [
            ["Ambiente", "Passagem", "Cobertura", "Comprovação"],
            ["Windows / Python 3.14.7", "55/55 (100%)", "99,66%", "local.log; exit 0"],
            ["Docker / Python 3.12.15", "55/55 (100%)", "99,69%", "docker.log; exit 0"],
            [
                "GitHub Actions / Python 3.12.15",
                "55/55 (100%)",
                "99,69%",
                f"[workflow]({ci_url}); quality aprovado",
            ],
        ]
    )
    para(
        "Passagem mede testes aprovados sobre coletados; cobertura mede linhas exercitadas. "
        "A exigência de 100% de passagem está demonstrada. O gate de cobertura é 90%."
    )
    para("Log real do ambiente padronizado", "H2PT")
    docker_log = read(EVIDENCE / "docker.log")
    start = docker_log.find("============================= test session")
    code(docker_log[start:] if start >= 0 else docker_log[-4000:])
    story.append(PageBreak())
    para("CI e demonstração HTTP", "H1PT")
    para(
        f"[Execução verificada]({ci_url}) do commit f863ddb. Artefatos contêm stdout, "
        "coverage.xml e test-results.xml (JUnit). Logs completos ficam "
        "versionados em docs/evidence/entrega2/."
    )
    ci_lines = [
        line
        for line in read(EVIDENCE / "ci.log").splitlines()
        if any(
            term in line
            for term in [
                "All checks passed",
                "collected 55",
                "55 passed",
                "Total coverage",
                "platform linux",
            ]
        )
    ]
    code("\n".join(ci_lines))
    para("Fluxo funcional pelo HTTP e reinício", "H2PT")
    code(read(EVIDENCE / "demo.log"))
    code(read(EVIDENCE / "persistence.log"))
    para(
        "Os logs vieram de execução da aplicação em um projeto Compose "
        "de demonstração com dados fictícios. "
        "O contêiner foi recriado e o registro continuou cancelado. A instância foi encerrada, "
        "preservando o volume. Avisos de depreciação estão mantidos "
        "nos logs e não representam falhas."
    )
    story.append(PageBreak())

    para("3. Erros lógicos e re-especificação", "H1PT")
    markdown("docs/LOGICAL_ERRORS.md")
    story.append(PageBreak())
    para("4. Defesa das decisões de arquitetura", "H1PT")
    table(
        [
            ["ADR", "Decisão / benefício", "Trade-off"],
            ["001", "Domínio isolado e porta substituível", "mais componentes, menos acoplamento"],
            [
                "002",
                "FastAPI/Pydantic, Pytest/Ruff e gate 90%",
                "dependências e manutenção da suíte",
            ],
            [
                "003",
                "SQLite local + volume; memória para testes",
                "arquivo local não é banco distribuído",
            ],
            [
                "004",
                "UTC-03, tipos estritos e unidade de trabalho",
                "serializa escritores e fixa calendário institucional",
            ],
        ]
    )
    markdown("docs/adr/004-calendario-e-atomicidade.md")
    story.append(PageBreak())
    para("5. Governança e histórico iterativo", "H1PT")
    markdown("docs/GOVERNANCE.md")
    table(
        [
            ["PR", "Evidência e função"],
            [
                f"[#20]({REPO}/pull/20)",
                "Feature branch -> develop: SQLite, consultas, testes "
                "e documentação; aprovado e mergeado.",
            ],
            [f"[#22]({REPO}/pull/22)", "Sincronização da Entrega 1; aprovado e mergeado."],
            [
                f"[#24]({REPO}/pull/24)",
                "Release -> main: versão consolidada aprovada e mergeada."
                if published
                else "Release -> main: homologação; aprovação final pendente no snapshot.",
            ],
        ]
    )
    para(
        "A consulta de status está preservada em github.json. Issues de implementação encerradas "
        "referenciam PRs concluídos; #19/#25 acompanham a publicação/PDF. O histórico inclui "
        "teste antes da correção, implementação, documentação e evidências."
    )
    story.append(PageBreak())
    para("6. Comparação e análise ético-técnica de IA", "H1PT")
    markdown("docs/AI_ETHICS.md")
    story.append(PageBreak())
    para("7. Comunicação técnica e experiência", "H1PT")
    markdown("docs/EXPERIENCE_REPORT.md")
    story.append(PageBreak())
    para("8. Rastreabilidade da submissão", "H1PT")
    table(
        [
            ["Exigência do enunciado", "Onde está demonstrada"],
            [
                "Repositório público + solução",
                "Link na capa; API, SQLite, execução e fluxo HTTP na seção 1/2.",
            ],
            ["Nome completo + RA", "Capa; equipe individual e adaptação nas seções 5/6."],
            ["100% de passagem", "55/55 no Docker/local/CI, logs reais e links na seção 2."],
            ["Erros e re-especificação", "Seção 3; SPEC_CHANGELOG 0.4.0 e regressões preservadas."],
            ["README, arquitetura e ADRs", "README final, diagrama/fluxo, ADRs 001-004 e seção 4."],
            [
                "Comparação e quatro pilares éticos",
                "Seção 6: método, matriz, limites, dados, IP e revisão humana.",
            ],
            ["Relato de experiência", "Seção 7; desenvolvimento individual explicitado."],
            ["PRs e sprints", "Seção 5; PRs #20/#22/#24 e Issues no marco Sprint 2."],
        ]
    )
    para("Passo final de homologação", "H2PT")
    para(
        "O snapshot confirma o PR #24 mergeado na main. A versão publicada contém a solução e "
        "documentação; o aluno homologou a entrega na adaptação individual relatada."
        if published
        else "O conteúdo técnico está validado. O PR #24 requer aprovação humana do commit final e "
        "merge para atualizar a main. Após o merge, atualizar github.json e executar o gerador "
        "para emitir a versão de submissão. A autorização individual foi relatada pelo aluno."
    )
    para("Integridade e reprodução", "H2PT")
    para(
        "Fonte do relatório: scripts/build_intermediate_report.py e documentos versionados. "
        "Cada log original conserva o resultado observado. Prints são opcionais porque o enunciado "
        "aceita logs; nenhuma imagem simulada foi usada como prova. "
        "O PDF foi renderizado e revisado "
        "para legibilidade antes da entrega ao aluno."
    )

    def page(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(TEAL)
        canvas.line(52, 797, 543, 797)
        canvas.setFont("Campus", 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(52, 810, "CampusFlow | Entrega 2 | 14/10/2026")
        canvas.drawString(52, 31, "Felipe Amorim Monteiro - RA 22452139")
        canvas.drawRightString(543, 31, str(document.page))
        canvas.restoreState()

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=52,
        leftMargin=52,
        topMargin=59,
        bottomMargin=52,
        title="CampusFlow - Entrega intermediária",
        author="Felipe Amorim Monteiro",
        subject="SDD, testes e análise ético-técnica de IA",
    )
    document.build(story, onFirstPage=page, onLaterPages=page)
    print(OUTPUT)


if __name__ == "__main__":
    main()
