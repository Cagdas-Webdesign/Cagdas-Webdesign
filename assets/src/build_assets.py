"""Generate the profile README's SVG assets.

    python3 assets/src/build_assets.py

Layout model. GitHub wraps every README image in a link, so a <picture> can only
switch between its dark and light source (GitHub handles that itself); it cannot
switch layouts by screen width. The hero is therefore one wide image designed to
stay legible when scaled down, and everything else is a fixed-width card
(256 px) shown at its natural size: three per row on a desktop profile, one per
row on a phone, never scaled.

Content and palette live here once, so a fact changes in one place and every
variant stays in step. Standard library only. An SVG loaded as an image cannot
fetch web fonts, so text uses system font stacks; widths are budgeted
conservatively and checked, and small labels use monospace, whose width is
predictable on every platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent

SANS = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#0a1020",
        "panel": "#0f182c",
        "line": "#1f2b44",
        "line2": "#2b3a58",
        "text": "#e8eef8",
        "text2": "#9aa8bf",
        "muted": "#64748e",
        "cyan": "#22d3ee",
        "blue": "#3b82f6",
        "blue2": "#60a5fa",
        "green": "#34d399",
        "chip": "#0a1222",
        "glow": 0.18,
    },
    "light": {
        "bg": "#f6f8fc",
        "panel": "#f8fafd",
        "line": "#d9e0ec",
        "line2": "#c3cede",
        "text": "#0b1324",
        "text2": "#475569",
        "muted": "#64748b",
        "cyan": "#0891b2",
        "blue": "#2563eb",
        "blue2": "#2563eb",
        "green": "#059669",
        "chip": "#ffffff",
        "glow": 0.10,
    },
}

# Estimated em widths, deliberately generous for wide fallback fonts.
EM = {"mono": 0.61, "sans": 0.56, "sans-bold": 0.6, "caps-bold": 0.76}


def check(text: str, size: float, kind: str, avail: float, where: str) -> None:
    width = (len(text) - text.count(" ") * 0.6) * size * EM[kind]
    if width > avail:
        raise SystemExit(f"[{where}] '{text}' needs ~{width:.0f}px, has {avail:.0f}px")


def t(x, y, text, size, fill, family=SANS, weight=400, anchor="start", spacing=0):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(text)}</text>'
    )


def svg(w, h, title, desc, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
        f"{body}\n</svg>\n"
    )


# ---------------------------------------------------------------------------
# Hero — one image, sized so name and role stay legible at phone width
# ---------------------------------------------------------------------------
NAME = "ÇAĞDAŞ UÇAR"
ROLE = "Full-Stack Development · Python Backends · AI/RAG Systems"
PIPELINE = ["query", "embed", "retrieve", "generate", "verify", "cite"]
HERO_DESC = (
    f"Çağdaş Uçar — {ROLE}. Illustration: a query point linked to its nearest neighbours in a "
    "vector space, and a six-stage pipeline: query, embed, retrieve, generate, verify, cite."
)

# Fixed constellation (normalized 0..1); the first point is the query.
POINTS = [
    (0.52, 0.48), (0.30, 0.30), (0.70, 0.26), (0.40, 0.70), (0.64, 0.66), (0.12, 0.52),
    (0.88, 0.50), (0.22, 0.10), (0.80, 0.86), (0.08, 0.84), (0.94, 0.14), (0.48, 0.92),
    (0.58, 0.08), (0.30, 0.52), (0.76, 0.44), (0.18, 0.72), (0.90, 0.72), (0.40, 0.14),
]
NEIGHBOURS = [13, 4, 14]  # nearest to the query: drawn as retrieved


def constellation(c, x0, y0, w, h, k=1.0):
    def pt(i):
        return x0 + POINTS[i][0] * w, y0 + POINTS[i][1] * h

    qx, qy = pt(0)
    out = []
    for i in range(1, len(POINTS)):
        for j in range(i + 1, len(POINTS)):
            (ax, ay), (bx, by) = pt(i), pt(j)
            if ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 < 0.27 * max(w, h):
                out.append(
                    f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{c["line2"]}" stroke-width="{k:.2f}" opacity="0.75"/>'
                )
    for n in NEIGHBOURS:
        nx, ny = pt(n)
        out.append(
            f'<line x1="{qx:.1f}" y1="{qy:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{c["cyan"]}" stroke-width="{1.6 * k:.2f}" stroke-dasharray="{4 * k:.1f} {4 * k:.1f}"/>'
        )
    for i in range(1, len(POINTS)):
        px, py = pt(i)
        hit = i in NEIGHBOURS
        out.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{(5 if hit else 3.2) * k:.1f}" fill="{c["cyan"] if hit else c["bg"]}" stroke="{c["cyan"] if hit else c["muted"]}" stroke-width="{1.4 * k:.2f}"/>'
        )
    out.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="{16 * k:.1f}" fill="{c["blue"]}" opacity="0.2"/>')
    out.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="{7 * k:.1f}" fill="{c["blue2"]}"/>')
    return "".join(out)


def pipeline(c, x0, x1, y, size, r):
    n = len(PIPELINE)
    step = (x1 - x0) / (n - 1)
    out = [
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["line2"]}" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y}" x2="{x1 - step:.1f}" y2="{y}" stroke="url(#flow)" stroke-width="2"/>',
    ]
    for i, label in enumerate(PIPELINE):
        x = x0 + i * step
        last = i == n - 1
        stroke = c["green"] if last else c["cyan"] if i else c["blue2"]
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{c["bg"]}" stroke="{stroke}" stroke-width="2"/>')
        if last:
            k = r * 0.5
            out.append(
                f'<path d="M{x - k:.1f} {y:.1f} l{k * 0.7:.1f} {k * 0.7:.1f} l{k * 1.3:.1f} {-k * 1.4:.1f}" fill="none" stroke="{c["green"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r * 0.35:.1f}" fill="{stroke}"/>')
        anchor = "start" if i == 0 else "end" if last else "middle"
        lx = x - r if i == 0 else x + r if last else x
        out.append(t(f"{lx:.1f}", y + r + size + 8, label, size, c["green"] if last else c["text2"], MONO, 500, anchor))
    return "".join(out)


def hero(c):
    w, h = 640, 410
    roles = ("Full-Stack Development", "Python Backends · AI/RAG Systems")
    check(NAME, 60, "caps-bold", 576, "hero name")
    for r in roles:
        check(r, 26, "sans", 576, "hero role")
    body = [
        "<defs>"
        f'<linearGradient id="flow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["blue2"]}"/><stop offset="1" stop-color="{c["cyan"]}"/></linearGradient>'
        f'<radialGradient id="glow" cx="0.85" cy="0.18" r="0.7"><stop offset="0" stop-color="{c["cyan"]}" stop-opacity="{c["glow"]}"/><stop offset="1" stop-color="{c["cyan"]}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{c["line2"]}" opacity="0.55"/></pattern>'
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="18" fill="{c["bg"]}"/>',
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#glow)"/>',
        f'<rect x="400" y="1" width="239" height="170" fill="url(#dots)" opacity="0.6"/>',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="{c["line"]}"/>',
        constellation(c, 432, 26, 172, 118),
        f'<rect x="36" y="42" width="12" height="12" rx="2.5" fill="{c["cyan"]}"/>',
        t(58, 54, "ENGINEERING SHOWCASE", 16, c["cyan"], MONO, 600, spacing=2.5),
        t(32, 204, NAME, 60, c["text"], SANS, 800, spacing=1),
    ]
    for i, r in enumerate(roles):
        body.append(t(36, 248 + i * 34, r, 26, c["text2"], SANS, 500))
    body.append(pipeline(c, 46, 594, 346, 16.5, 9.5))
    return svg(w, h, "Çağdaş Uçar — Engineering Showcase", HERO_DESC, "".join(body))


# ---------------------------------------------------------------------------
# Cards — fixed 256 px wide, shown at natural size
# ---------------------------------------------------------------------------
CW = 256


def card_frame(c, h, tone):
    return (
        f'<rect x="0.5" y="0.5" width="{CW - 1}" height="{h - 1}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>'
        f'<rect x="18" y="0.5" width="34" height="3" rx="1.5" fill="{tone}"/>'
    )


@dataclass
class Metric:
    slug: str
    value: str
    label: str
    scope: str
    tone: str  # green = a verified pass state, blue = documentation
    desc: str


METRICS = [
    Metric("tests", "2,855", "passing tests", "documented · backend v1.3.0", "green",
           "2,855 passing tests, as documented for portfolio-rag-backend v1.3.0."),
    Metric("acceptance", "24/24", "evaluation questions passed", "release v1.2.0-accepted", "green",
           "24 of 24 evaluation questions passed in the live release acceptance of v1.2.0 "
           "(tag v1.2.0-accepted). This is not a result for v1.3.0."),
    Metric("adrs", "8", "architecture decision records", "docs/adr · ADR 0001–0008", "blue",
           "8 architecture decision records in docs/adr of portfolio-rag-backend."),
]


def metric_card(c, m: Metric):
    h, pad = 148, 18
    check(m.label, 15, "sans", CW - pad, "metric label")
    check(m.scope, 12, "mono", CW - 2 * pad - 16, "metric scope")
    tone = c[m.tone]
    body = [
        card_frame(c, h, tone),
        t(pad - 1, 66, m.value, 46, c["text"], SANS, 750, spacing=-0.5),
        t(pad, 94, m.label, 15, c["text"], SANS, 500),
        f'<circle cx="{pad + 4}" cy="{h - pad - 4}" r="4" fill="{tone}"/>',
        t(pad + 15, h - pad, m.scope, 12, c["text2"], MONO, 500),
    ]
    return svg(CW, h, f"{m.value} {m.label}", m.desc, "".join(body))


@dataclass
class Step:
    slug: str
    title: str
    lines: tuple[str, ...]
    chip: str
    tone: str = "blue2"
    optional: bool = False


QUERY_STEPS = [
    Step("embed", "Embed the query", ("Normalized question → vector", "same model as the corpus"), "Mistral · mistral-embed"),
    Step("retrieve", "Retrieve evidence", ("Top-k 7, public by construction", "No match → fixed reply, no LLM"), "Cloudflare Vectorize"),
    Step("context", "Build context", ("IDs → text from bundled corpus", "Ranked, deduped, token-bounded"), "in-process · no provider", "muted"),
    Step("generate", "Generate answer", ("From retrieved passages only", "Instructions stay system-only"), "Workers AI · gpt-oss-120b", "cyan"),
    Step("verify", "Verify grounding", ("Checks answer vs cited passages", "default: the generator itself"), "optional: Groq gpt-oss-20b", "cyan", True),
    Step("cite", "Publish citations", ("Only sources retrieved for", "this request are returned"), "backend-owned · verified", "green"),
]
INGEST_STEPS = [
    Step("author", "Author knowledge", ("Markdown + YAML frontmatter", "versioned, reviewed in git"), "knowledge/*.md", "muted"),
    Step("validate", "Validate", ("Schema version and metadata", "visibility: public | internal"), "strict · reports all errors", "muted"),
    Step("chunk", "Chunk", ("Structure-aware, deterministic", "SHA-256 fingerprint per chunk"), "no model in the loop", "muted"),
    Step("plan", "Plan changes", ("Create / re-embed / delete", "unchanged chunks cost nothing"), "incremental · dry-run", "muted"),
    Step("embed", "Embed", ("Title + heading path + text", "versioned embedding space"), "Mistral · mistral-embed"),
    Step("index", "Index", ("Vectors and metadata, no text", "upserts first, then deletes"), "Cloudflare Vectorize"),
]


def step_card(c, s: Step, n: int, total: int, flow: str):
    h, pad = 164, 16
    tone = c[s.tone]
    check(s.title, 17, "sans-bold", CW - 2 * pad - 34, f"title {s.title}")
    for line in s.lines:
        check(line, 12, "mono", CW - 2 * pad, f"line {s.title}")
    check(s.chip, 12, "mono", CW - 2 * pad - 30, f"chip {s.title}")
    out = [
        card_frame(c, h, tone),
        f'<rect x="{pad}" y="20" width="24" height="24" rx="6" fill="none" stroke="{tone}" stroke-width="1.5"/>',
        t(pad + 12, 37, str(n), 13, tone, MONO, 700, "middle"),
        t(pad + 34, 38.5, s.title, 17, c["text"], SANS, 650),
    ]
    for i, line in enumerate(s.lines):
        out.append(t(pad, 72 + i * 19, line, 12, c["text2"], MONO, 400))
    cy = h - pad - 28
    chip_w = len(s.chip) * 12 * 0.61 + 30
    dash = ' stroke-dasharray="5 4"' if s.optional else ""
    out.append(
        f'<rect x="{pad}" y="{cy}" width="{chip_w:.1f}" height="28" rx="14" fill="{c["chip"]}" stroke="{tone}" stroke-opacity="0.8"{dash}/>'
    )
    out.append(f'<circle cx="{pad + 14}" cy="{cy + 14}" r="3.5" fill="{tone}"/>')
    out.append(t(pad + 24, cy + 18.2, s.chip, 12, c["text"], MONO, 500))
    desc = f"{flow}, step {n} of {total}: {s.title}. {' '.join(s.lines)}. Provider or property: {s.chip}."
    return svg(CW, h, f"{n}. {s.title}", desc, "".join(out))


def main() -> None:
    for old in OUT.glob("*.svg"):
        old.unlink()
    count = 0
    for theme, c in THEMES.items():
        files = {f"hero-{theme}.svg": hero(c)}
        for m in METRICS:
            files[f"proof-{m.slug}-{theme}.svg"] = metric_card(c, m)
        for i, s in enumerate(QUERY_STEPS, 1):
            files[f"query-{i}-{s.slug}-{theme}.svg"] = step_card(c, s, i, len(QUERY_STEPS), "Query flow")
        for i, s in enumerate(INGEST_STEPS, 1):
            files[f"ingest-{i}-{s.slug}-{theme}.svg"] = step_card(c, s, i, len(INGEST_STEPS), "Offline indexing")
        for name, content in files.items():
            (OUT / name).write_text(content, encoding="utf-8")
            count += 1
    print(f"wrote {count} files to {OUT}")


if __name__ == "__main__":
    main()
