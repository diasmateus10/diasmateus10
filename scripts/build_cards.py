#!/usr/bin/env python3
"""
Gera os dois cartoes SVG do perfil do GitHub.

Edite apenas o bloco DATA abaixo e rode:
    python scripts/build_cards.py

Saida: signature-card.svg e ledger-card.svg na raiz do repositorio.
"""

from pathlib import Path
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# DATA — unica parte que voce edita
# --------------------------------------------------------------------------
DATA = {
    "name": "Mateus Dias",
    "role": "Revenue Intelligence Architect",
    "place": "São Paulo, Brasil",
    # O caminho que um dado percorre ate virar decisao. Maximo 5 etapas.
    "pipeline": [
        "TOTVS, SQL Server, Supabase, ComexStat",
        "Power Query and SQL modeling",
        "Fabric / Power BI semantic model",
        "DAX agent orchestrated in n8n",
        "Answer delivered inside Teams",
    ],
    # Linhas do cartao-ficha. Rotulo curto, valor sem pontuacao decorativa.
    "years": "4+ years",
    "ledger": [
        ("Role", "Senior Market Intelligence Analyst, M.Cassab"),
        ("Markets", "Brazil, China, Argentina, Colombia, Paraguay"),
        ("Sectors", "Animal health, pharmaceutical, chemical"),
        ("Domain", "Sales, inventory, supply chain, pricing"),
        ("BI", "Power BI Premium, Fabric, DAX, Power Query"),
        ("Data", "SQL Server, Supabase, Python, TOTVS extracts"),
        ("AI", "n8n multi-agent, LLM pipelines, Claude Code"),
        ("Audience", "Directors, shareholders, ops leadership"),
    ],
}

# --------------------------------------------------------------------------
# Tokens visuais — ficha de razao / livro-caixa, nao terminal generico
# --------------------------------------------------------------------------
INK = "#0E1A24"        # fundo, azul-tinta profundo
RULE = "#22394A"       # linhas da ficha
PAPER = "#E9E4D8"      # texto principal, papel quente
MUTED = "#8AA0AD"      # texto secundario
AMBER = "#DFA33F"      # acento, commodity
SIGNAL = "#57ABC6"     # acento de dado

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SERIF = "Iowan Old Style, Palatino Linotype, Georgia, serif"

W, H = 480, 362
R = 10


def _shell(title: str) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{R}" '
        f'fill="{INK}" stroke="{RULE}"/>'
        f'<title>{escape(title)}</title>'
    )


def signature_card() -> str:
    d = DATA
    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="{escape(d["name"])}, {escape(d["role"])}">'
    )
    p.append(_shell(f'{d["name"]} — {d["role"]}'))

    # marcacoes de margem, como furos de fichario
    for i in range(6):
        y = 40 + i * 48
        p.append(f'<rect x="0" y="{y}" width="4" height="18" fill="{RULE}"/>')

    p.append(
        f'<text x="34" y="62" font-family="{SERIF}" font-size="34" '
        f'fill="{PAPER}">{escape(d["name"])}</text>'
    )
    p.append(
        f'<text x="36" y="86" font-family="{MONO}" font-size="12.5" '
        f'letter-spacing="0.6" fill="{AMBER}">{escape(d["role"])}</text>'
    )
    p.append(f'<line x1="34" y1="104" x2="{W - 30}" y2="104" stroke="{RULE}"/>')
    p.append(
        f'<text x="34" y="126" font-family="{MONO}" font-size="11" '
        f'fill="{MUTED}">how a business question gets answered</text>'
    )

    top = 150
    step = 30
    n = len(d["pipeline"])
    p.append(
        f'<line x1="41" y1="{top - 6}" x2="41" y2="{top + (n - 1) * step + 6}" '
        f'stroke="{RULE}" stroke-width="2"/>'
    )
    for i, label in enumerate(d["pipeline"]):
        y = top + i * step
        last = i == n - 1
        fill = AMBER if last else SIGNAL
        p.append(f'<circle cx="41" cy="{y - 4}" r="3.5" fill="{fill}"/>')
        p.append(
            f'<text x="58" y="{y}" font-family="{MONO}" font-size="12.5" '
            f'fill="{PAPER if last else MUTED}">{escape(label)}</text>'
        )

    p.append(
        f'<text x="34" y="{H - 24}" font-family="{MONO}" font-size="11" '
        f'fill="{MUTED}">{escape(d["place"])}</text>'
    )
    p.append(
        f'<text x="{W - 30}" y="{H - 24}" text-anchor="end" font-family="{MONO}" '
        f'font-size="11" fill="{MUTED}">{escape(d["years"])} in market intelligence</text>'
    )
    p.append("</svg>")
    return "\n".join(p)


def ledger_card() -> str:
    d = DATA
    rows = d["ledger"]
    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Experience and stack summary">'
    )
    p.append(_shell("Experience and stack"))

    head_y = 46
    p.append(
        f'<text x="26" y="{head_y - 16}" font-family="{MONO}" font-size="11" '
        f'letter-spacing="0.8" fill="{AMBER}">what I do and what I do it with</text>'
    )
    p.append(f'<line x1="18" y1="{head_y}" x2="{W - 18}" y2="{head_y}" stroke="{RULE}"/>')

    # coluna do numero da linha, como planilha
    row_h = 34
    bottom = head_y + row_h * len(rows)
    p.append(f'<line x1="46" y1="{head_y}" x2="46" y2="{bottom}" stroke="{RULE}"/>')
    p.append(f'<line x1="152" y1="{head_y}" x2="152" y2="{bottom}" stroke="{RULE}"/>')
    for i, (label, value) in enumerate(rows):
        y = head_y + row_h * (i + 1)
        baseline = y - 12
        p.append(
            f'<line x1="18" y1="{y}" x2="{W - 18}" y2="{y}" stroke="{RULE}" '
            f'stroke-opacity="0.6"/>'
        )
        p.append(
            f'<text x="26" y="{baseline}" font-family="{MONO}" font-size="11" '
            f'fill="{RULE if i else SIGNAL}">{i + 1:02d}</text>'
        )
        p.append(
            f'<text x="58" y="{baseline}" font-family="{MONO}" font-size="12" '
            f'fill="{SIGNAL}">{escape(label)}</text>'
        )
        p.append(
            f'<text x="164" y="{baseline}" font-family="{MONO}" font-size="11.5" '
            f'fill="{PAPER}">{escape(value)}</text>'
        )

    p.append("</svg>")
    return "\n".join(p)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    (root / "signature-card.svg").write_text(signature_card(), encoding="utf-8")
    (root / "ledger-card.svg").write_text(ledger_card(), encoding="utf-8")
    print("wrote signature-card.svg and ledger-card.svg")


if __name__ == "__main__":
    main()
