#!/usr/bin/env python3
"""Build the DISTURB website into docs/ from content.py.

Run:    python3 build.py          (or: make site / make serve)
Deploy: git push                  (GitHub Actions builds and publishes docs/)

Standard library only — no dependencies.
"""

from __future__ import annotations

from datetime import datetime
import re
from pathlib import Path

import content as C
import sheet_data
import bibtex

OUT = Path(__file__).parent / "docs"
OUT.mkdir(exist_ok=True)
YEAR = datetime.now().year

NAV = [
    ("Home", "index.html"),
    ("Team", "team.html"),
    ("Publications", "publications.html"),
    ("Positions", "positions.html"),
]

# ── Styles ─────────────────────────────────────────────────────────────────────
STYLE = """
:root {
  --navy: #14284b; --navy-2: #1f3a66; --red: #c8102e; --blue: #6f8fc6;
  --ink: #1a1f2b; --muted: #5a6273; --line: #e3e7ee; --panel: #eef2f7; --bg: #ffffff;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  font-size: 17px; line-height: 1.65; color: var(--ink); background: var(--bg);
}
a { color: var(--red); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; height: auto; display: block; }
.container { max-width: 1160px; margin: 0 auto; padding: 0 1.25rem; }
.section { padding: 3.5rem 0; }
.section.alt { background: var(--panel); }
.kicker {
  color: var(--red); font-weight: 800; font-size: .8rem;
  letter-spacing: .14em; text-transform: uppercase; margin-bottom: .35rem;
}
h1, h2, h3 { color: var(--navy); line-height: 1.2; }
h2 { font-size: 1.9rem; font-weight: 800; margin-bottom: 1rem; }
h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: .4rem; }
.lead { font-size: 1.12rem; color: var(--muted); max-width: 52rem; }

/* nav (all pages) */
nav.site { background: var(--navy); position: sticky; top: 0; z-index: 50; }
nav.site .container { display: flex; align-items: center; gap: 1rem; }
.nav-brand { display: flex; align-items: center; gap: .6rem; color: #fff; font-weight: 800;
  letter-spacing: .04em; font-size: 1.05rem; padding: .45rem 0; flex-shrink: 0; }
.nav-brand:hover { text-decoration: none; }
.nav-brand img { height: 30px; width: auto; border-radius: 2px; }
nav.site ul { list-style: none; display: flex; margin-left: auto; }
nav.site a.lnk { display: block; color: #cfd8e8; padding: .85rem .9rem; font-size: .92rem; font-weight: 600; letter-spacing: .02em; }
nav.site a.lnk:hover { color: #fff; text-decoration: none; }
nav.site a.lnk.active { color: #fff; box-shadow: inset 0 -3px 0 var(--red); }

/* brand strip (inner pages) */
.brandbar { background: #fff; border-bottom: 1px solid var(--line); }
.brandbar .container { display: flex; align-items: center; gap: 1.5rem; padding-top: 1rem; padding-bottom: 1rem; }
.brandbar img { height: 72px; width: auto; }
.grant { margin-left: auto; text-align: right; font-size: .78rem; font-weight: 700;
  letter-spacing: .16em; text-transform: uppercase; color: var(--muted); line-height: 1.6; }
.grant b { color: var(--navy); font-weight: 800; }

/* home hero: the animated logo */
.hero { background: #fff; border-bottom: 1px solid var(--line); }
.hero .container { display: flex; align-items: center; gap: 1.5rem 2.5rem; flex-wrap: wrap;
  padding-top: 1.4rem; padding-bottom: 1.4rem; }
.hero-logo { width: min(100%, 420px); flex-shrink: 0; }
.hero-logo img { width: 100%; height: auto; }
.hero-meta { margin-left: auto; text-align: right; }
.partners { display: flex; align-items: center; justify-content: flex-end; flex-wrap: wrap; gap: .8rem 1.3rem; }
.partners img { height: 38px; width: auto; }
.partners img.eu { height: 56px; }
.partners img.sq { height: 40px; }
.partners img.ct { height: 26px; }
.hero-meta .motto { color: var(--red); font-weight: 800; font-size: 1.05rem; line-height: 1.3; margin-top: .9rem; }
.hero-meta .grant { font-size: .74rem; margin: .8rem 0 0; text-align: inherit; }
@media (max-width: 1100px) { .hero-meta { margin-left: 0; text-align: left; } .partners { justify-content: flex-start; } }
.intro { background: var(--navy); color: #e3e9f4; }
.intro .container { padding-top: 3rem; padding-bottom: 3rem; }
.intro h1 { color: #fff; font-size: clamp(1.7rem, 3.6vw, 2.5rem); font-weight: 800; max-width: 46rem; }
.intro p { font-size: 1.12rem; max-width: 50rem; margin-top: .9rem; }
.intro h1::after { content: ""; display: block; width: 4rem; height: 4px; background: var(--red); margin-top: 1rem; }

/* grids & cards */
.grid { display: grid; gap: 1.25rem; }
.g2 { grid-template-columns: repeat(2, 1fr); }
.g3 { grid-template-columns: repeat(3, 1fr); }
.g4 { grid-template-columns: repeat(4, 1fr); }
.card { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 1.25rem; }
.alt .card { border-color: #dde3ec; }
.card p { color: var(--muted); font-size: .97rem; }
.pillar { display: flex; flex-direction: column; overflow: hidden; padding: 0; }
.pillar img { aspect-ratio: 16/10; object-fit: cover; width: 100%; background: #000; }
.pillar .body { padding: 1.1rem 1.25rem 1.3rem; }
.pillar h3::before { content: ""; display: inline-block; width: 1.6rem; margin-right: .5rem; vertical-align: middle;
  border-top: 4px solid var(--red); }
.pillar.dashed h3::before { border-top: 4px dashed var(--navy); }
.pillar.dotted h3::before { border-top: 4px dotted var(--blue); }
.limits { list-style: none; margin-top: .8rem; font-size: .9rem; color: var(--muted); }
.limits li { padding: .25rem 0; border-top: 1px solid var(--line); }
.limits b { color: var(--red); font-weight: 700; }
.twin-badge { display: inline-flex; align-items: center; justify-content: center; width: 3rem; height: 3rem;
  border-radius: 50%; background: var(--navy); color: #fff; font-weight: 800; font-size: .9rem; margin-bottom: .6rem; }
.twin:nth-child(2) .twin-badge { background: var(--navy-2); }
.twin:nth-child(3) .twin-badge { background: var(--red); }
.twin .mode { font-size: .85rem; color: var(--muted); font-style: italic; margin-bottom: .4rem; }
.synergy { display: grid; grid-template-columns: 1fr 1.1fr; gap: 2rem; align-items: center; margin-bottom: 2rem; }
.synergy img { border-radius: 8px; border: 1px solid var(--line); background: #fff; }
.flow img { border-radius: 6px; aspect-ratio: 8/3; object-fit: cover; width: 100%; margin-bottom: .8rem; }
.flow h3 span { color: var(--red); font-weight: 400; font-size: .95rem; }
.questions { list-style: none; counter-reset: q; }
.questions li { counter-increment: q; padding: .7rem 0 .7rem 2.6rem; position: relative; border-top: 1px solid var(--line); font-size: 1.05rem; }
.questions li::before { content: counter(q, lower-roman); position: absolute; left: 0; top: .65rem;
  color: var(--red); font-weight: 800; font-style: italic; }
.phases { display: grid; grid-template-columns: 22fr 27fr 24fr; gap: 4px; margin: 1rem 0 1.25rem; }
.phases div { color: #fff; padding: .55rem .8rem; font-size: .9rem; font-weight: 700; border-radius: 3px; }
.phases div:nth-child(1) { background: var(--blue); }
.phases div:nth-child(2) { background: var(--navy-2); }
.phases div:nth-child(3) { background: var(--red); }
.phases span { font-weight: 400; opacity: .9; }
table.wp { width: 100%; border-collapse: collapse; font-size: .97rem; }
table.wp td { padding: .5rem .4rem; border-top: 1px solid var(--line); vertical-align: top; }
table.wp td:first-child { font-weight: 800; color: var(--navy); width: 4rem; }
table.wp td:last-child { color: var(--muted); text-align: right; white-space: nowrap; }
.btn { display: inline-block; background: var(--red); color: #fff; padding: .6rem 1.1rem; border-radius: 4px; font-weight: 700; }
.btn:hover { text-decoration: none; background: #a50d26; }
.btn.ghost { background: transparent; color: var(--navy); border: 2px solid var(--navy); }

/* team */
.site-card { border-top: 4px solid var(--navy); }
.pi { display: flex; gap: .9rem; align-items: center; margin: .9rem 0; }
.pi .ph { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.pi .ph.empty { background: var(--panel); display: flex; align-items: center; justify-content: center;
  color: var(--navy); font-weight: 800; font-size: 1.3rem; }
.pi b { display: block; font-size: 1.1rem; color: var(--navy); }
.pi span { font-size: .85rem; color: var(--muted); }
.members { list-style: none; font-size: .95rem; }
.members li { padding: .3rem 0; border-top: 1px solid var(--line); }
.members li span { color: var(--muted); font-size: .88rem; }
.people { list-style: none; margin-top: 2.5rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0 1.25rem; }
.people li { padding: .7rem 0; border-top: 1px solid var(--line); }
.people b { display: block; color: var(--navy); font-weight: 700; }
.people span { color: var(--muted); font-size: .9rem; }
@media (max-width: 900px) { .people { grid-template-columns: 1fr 1fr; } }
@media (max-width: 640px) { .people { grid-template-columns: 1fr; } }

/* news & pubs */
.news-item { display: grid; grid-template-columns: 7rem 1fr; gap: 1rem; padding: 1.2rem 0; border-top: 1px solid var(--line); }
.news-item time { color: var(--red); font-weight: 700; font-size: .9rem; }
.pub { padding: .9rem 0; border-top: 1px solid var(--line); }
.pub .t { font-weight: 700; color: var(--navy); }
.pub .m { color: var(--muted); font-size: .95rem; }
.empty-note { color: var(--muted); font-style: italic; padding: 1rem 0; }

/* footer */
footer.site { background: var(--navy); color: #c9d3e5; font-size: .85rem; margin-top: 0; }
footer.site .container { padding-top: 2rem; padding-bottom: 2rem; }
.funding { display: grid; grid-template-columns: auto 1fr; gap: 1.5rem; align-items: center;
  background: #fff; color: var(--muted); border-radius: 6px; padding: 1rem 1.25rem; }
.funding img { height: 64px; width: auto; }
.funding p { font-size: .8rem; line-height: 1.5; }
.foot-row { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem; margin-top: 1.25rem; }
footer.site a { color: #fff; }
.motto-bar { background: var(--red); color: #fff; text-align: center; font-weight: 800; padding: .8rem; letter-spacing: .02em; }

@media (max-width: 900px) {
  .g3, .g4 { grid-template-columns: 1fr 1fr; }
  .synergy { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  body { font-size: 16px; }
  .g2, .g3, .g4 { grid-template-columns: 1fr; }
  }
"""

import hashlib
CSS_VER = hashlib.md5(STYLE.encode()).hexdigest()[:8]  # cache-buster: changes whenever the CSS does

# ── Scaffolding ────────────────────────────────────────────────────────────────

def header_html(active: str) -> str:
    links = "".join(
        '<li><a class="lnk{}" href="{}">{}</a></li>'.format(" active" if href == active else "", href, label)
        for label, href in NAV)
    nav = (f'<nav class="site"><div class="container">'
           f'<a class="nav-brand" href="index.html"><img src="images/logo_mark.png" alt="">{C.PROJECT}</a>'
           f'<ul>{links}</ul></div></nav>')
    if active == "index.html":
        return nav  # the home hero carries the full logo
    return nav + f"""
<div class="brandbar"><div class="container">
  <a href="index.html"><img src="images/logo_lockup.png" alt="{C.PROJECT} — {C.TAGLINE}"></a>
  <div class="grant top"><b>{C.GRANT}</b><br>{C.PERIOD} · GA {C.GA}</div>
</div></div>"""


def footer_html() -> str:
    return f"""
<div class="motto-bar">{C.MOTTO}</div>
<footer class="site"><div class="container">
  <div class="funding">
    <img src="images/eu_erc.png" alt="Funded by the European Union — European Research Council">
    <p>{C.EU_DISCLAIMER}</p>
  </div>
  <div class="foot-row">
    <span>{C.SITES}</span>
    <span>© {YEAR} {C.PROJECT} consortium</span>
  </div>
</div></footer>"""


def page(title: str, active: str, body: str, description: str = "") -> str:
    full = f"{title} · {C.PROJECT}" if title else f"{C.PROJECT} · {C.TAGLINE}"
    desc = description or C.HERO_TEXT
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="images/logo_lockup.png">
<link rel="icon" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={CSS_VER}">
</head>
<body>
{header_html(active)}
<main>
{body}
</main>
{footer_html()}
</body>
</html>
"""


def section(kicker: str, title: str, inner: str, alt: bool = False, id_: str = "") -> str:
    idattr = f' id="{id_}"' if id_ else ""
    return f"""
<section class="section{' alt' if alt else ''}"{idattr}><div class="container">
  {f'<div class="kicker">{kicker}</div>' if kicker else ''}
  <h2>{title}</h2>
  {inner}
</div></section>"""

# ── Page blocks ────────────────────────────────────────────────────────────────

# Logo strip in the Home banner: EU/ERC first, then the three institutions.
# EU rules: the EU emblem must be at least as large as any other logo shown.
PARTNER_LOGOS = [
    ("Funded by the European Union — European Research Council", "logo_eu_erc.png", "eu", "https://erc.europa.eu/"),
    ("CNRS", "logo_cnrs.png", "sq", "https://www.cnrs.fr/"),
    ("Institut Pprime", "logo_pprime.png", "sq", "https://pprime.fr/"),
    ("Sapienza Università di Roma", "logo_sapienza.png", "", "https://www.uniroma1.it/"),
    ("Caltech", "logo_caltech.png", "ct", "https://www.caltech.edu/"),
]


def hero() -> str:
    alt = f"{C.PROJECT} — {C.TAGLINE}"
    partners = "".join(
        f'<a href="{url}" title="{name}"><img class="{cls}" src="images/{img}" alt="{name}" '
        f'height="{ {"eu": 56, "sq": 40, "ct": 26}.get(cls, 38) }"></a>'
        for name, img, cls, url in PARTNER_LOGOS)
    return f"""
<section class="hero"><div class="container">
  <picture class="hero-logo">
    <source srcset="images/logo_lockup.png" media="(prefers-reduced-motion: reduce)">
    <img src="images/logo_anim.webp" width="824" height="191" alt="{alt}">
  </picture>
  <div class="hero-meta">
    <div class="partners">{partners}</div>
    <div class="grant">{C.GRANT} · {C.PERIOD} · GA {C.GA}</div>
  </div>
</div></section>
<section class="intro"><div class="container">
  <h1>{C.HERO_TITLE}</h1>
  <p>{C.HERO_TEXT}</p>
</div></section>"""


def challenge_block(alt=False) -> str:
    cards = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in C.CHALLENGES)
    return section("The challenge", "Turbulence: a barrier to progress",
                   f'<p class="lead" style="margin-bottom:2rem">{C.CHALLENGE_TEXT}</p>'
                   f'<div class="grid g4">{cards}</div>', alt)


def pillars_block(alt=False) -> str:
    cards = ""
    for p in C.PILLARS:
        lim = "".join(f"<li><b>{k}</b> · {v}</li>" for k, v in p["limits"])
        cards += (f'<div class="card pillar {p["style"]}"><img src="images/{p["image"]}" alt="{p["name"]}" loading="lazy">'
                  f'<div class="body"><h3>{p["name"]}</h3><p>{p["text"]}</p><ul class="limits">{lim}</ul></div></div>')
    return section("State of the art, and its blind spots",
                   "Three pillars, each with extraordinary progress and its own uncertainty",
                   f'<div class="grid g3">{cards}</div>', alt)


def twins_block(alt=False) -> str:
    cards = "".join(f'<div class="card twin"><div class="twin-badge">{b}</div><h3>{n}</h3>'
                    f'<div class="mode">{m}</div><p>{d}</p></div>' for b, n, m, d in C.TWINS)
    return section("Pillar synergy", "The DISTURB answer: a hierarchy of three digital twins",
                   f'<div class="synergy"><p class="lead">{C.SYNERGY_TEXT}</p>'
                   f'<img src="images/dt.jpg" alt="Data assimilation: twin estimate tracking the true flow, '
                   f'with uncertainty shrinking at assimilated measurements"></div>'
                   f'<div class="grid g3">{cards}</div>', alt)


def flows_block(alt=False) -> str:
    cards = "".join(f'<div class="flow"><img src="images/{img}" alt="{n}" loading="lazy">'
                    f'<h3>{n} <span>· {k}</span></h3><p>{d}</p></div>' for n, k, img, d in C.FLOWS)
    return section("Proving grounds", "Three canonical flows, in water and in air",
                   f'<div class="grid g3">{cards}</div>', alt)




# ── Sheet helpers ──────────────────────────────────────────────────────────────

def g(row: dict, *keys: str) -> str:
    """First non-empty value among the given column names (lower-case)."""
    for k in keys:
        v = row.get(k, "")
        if v:
            return v
    return ""


def img_src(v: str) -> str:
    return v if v.startswith(("http://", "https://")) else f"images/{v}"


def initials(name: str) -> str:
    return "".join(w[0] for w in name.split()[:2] if w)


def link(text: str, url: str) -> str:
    return f'<a href="{url}">{text}</a>' if url else text


def not_connected(what: str) -> str:
    return (f'<p class="empty-note">{what} will appear here once the project spreadsheet is '
            f'connected.</p>')

# ── Team ───────────────────────────────────────────────────────────────────────

def _is_pi(row: dict) -> bool:
    role = g(row, "role", "position", "title").lower()
    return bool(re.search(r"\bpi\b|principal investigator", role))


def _last(r: dict) -> str:
    return (g(r, "last") or g(r, "name").split()[-1]).lower()


def team_from_sheet(rows: list[dict]) -> str:
    """PIs first, in the sheet's row order; everyone else below, A–Z by last name."""
    rows = [r for r in rows if g(r, "name") and g(r, "show", "visible").lower() not in ("no", "n", "false", "0", "hide")]
    pis = [r for r in rows if _is_pi(r)]
    others = sorted((r for r in rows if not _is_pi(r)), key=lambda r: (_last(r), g(r, "first").lower()))

    cards = ""
    for p in pis:
        name = g(p, "name"); photo = g(p, "photo", "image", "photo url")
        ph = (f'<img class="ph" src="{img_src(photo)}" alt="{name}">' if photo
              else f'<div class="ph empty">{initials(name)}</div>')
        email = g(p, "email")
        mail = f' · <a href="mailto:{email}">email</a>' if email else ""
        cards += (f'<div class="card site-card">'
                  f'<div class="pi">{ph}<div><b>{link(name, g(p, "url", "website", "link"))}</b>'
                  f'<span>{g(p, "role", "position", "title")}{mail}</span></div></div>'
                  f'<div style="color:var(--muted);font-size:.92rem">{g(p, "institution", "affiliation", "site")}</div></div>')
    out = f'<div class="grid g3">{cards}</div>'

    if others:
        items = "".join(
            f'<li><b>{link(g(r, "name"), g(r, "url", "website", "link"))}</b>'
            f'<span>{" · ".join(x for x in (g(r, "role", "position", "title"), g(r, "institution", "affiliation", "site")) if x)}</span></li>'
            for r in others)
        out += f'<ul class="people">{items}</ul>'
    return out


def team_from_content() -> str:
    """Fallback (sheet not reachable): the poster team from content.py."""
    rows = []
    for s in C.TEAM:
        rows.append(dict(name=s["pi"]["name"], role="PI", institution=s["site"],
                         url=s["pi"].get("url", ""), photo=s["pi"].get("photo", "")))
        rows += [dict(name=m, institution=s["site"]) for m in s["members"]]
    return team_from_sheet(rows)


# ── Map the sheet's columns onto the fields the pages use ─────────────────────

def norm_team(rows):
    if rows is None:
        return None
    out = []
    for r in rows:
        r = dict(r)
        r.setdefault("name", " ".join(x for x in (r.get("first", ""), r.get("last", "")) if x))
        r["url"] = g(r, "url", "homepage", "website")
        out.append(r)
    return out  # order is decided in team_from_sheet


def norm_pubs(rows):
    if rows is None:
        return None
    out = []
    for r in rows:
        b = bibtex.parse(r.get("citation", "")) if r.get("citation") else None
        if not b:
            if g(r, "title"):
                out.append(r)
            continue
        bits = [bibtex.detex(g(b, "journal", "booktitle", "school", "publisher", "howpublished"))]
        if b.get("volume"):
            bits.append(b["volume"] + (f"({b['number']})" if b.get("number") else ""))
        if b.get("pages"):
            bits.append(bibtex.detex(b["pages"]))
        out.append(dict(title=bibtex.detex(b.get("title", "")), authors=bibtex.authors(b.get("author", "")),
                        venue=", ".join(x for x in bits if x), year=b.get("year", ""),
                        doi=b.get("doi", ""), url=r.get("link") or b.get("url", "")))
    return out


def norm_positions(rows):
    if rows is None:
        return None
    out = []
    for r in rows:
        r = dict(r)
        r["title"] = g(r, "title", "position")
        r["site"] = g(r, "site", "location", "institution")
        c = r.get("contact", "")
        if c.startswith(("http://", "https://")):
            r.setdefault("url", c)
            r["contact_html"] = f'<a href="{c}">details and application</a>'
        elif "@" in c:
            r["contact_html"] = f'Contact: <a href="mailto:{c}">{c}</a>'
        elif c:
            r["contact_html"] = f"Contact: {c}"
        out.append(r)
    return out

# ── Pages ──────────────────────────────────────────────────────────────────────

def build_index():
    body = (hero() + challenge_block() + pillars_block(alt=True) + twins_block() +
            flows_block(alt=True))
    (OUT / "index.html").write_text(page("", "index.html", body))


def build_team(rows):
    inner = team_from_sheet(rows) if rows else team_from_content()
    body = section("", "The team", inner)
    (OUT / "team.html").write_text(page("Team", "team.html", body))


def _year(r) -> int:
    m = re.search(r"\d{4}", g(r, "year", "date"))
    return int(m.group()) if m else 0


def build_publications(rows):
    if rows is None:
        inner = not_connected("Publications")
    elif not [r for r in rows if g(r, "title")]:
        inner = ('<p class="empty-note">Publications, open datasets and software will be listed '
                 'here as the project progresses.</p>')
    else:
        rows = sorted((r for r in rows if g(r, "title")), key=_year, reverse=True)
        inner, cur = "", None
        for r in rows:
            y = _year(r)
            if y != cur:
                inner += f'<h3 style="margin-top:1.8rem">{y or "Forthcoming"}</h3>'
                cur = y
            doi = g(r, "doi")
            doi = re.sub(r"^(https?://(dx\.)?doi\.org/)", "", doi)
            links = []
            if doi:
                links.append(f'<a href="https://doi.org/{doi}">doi</a>')
            for k, label in (("url", "link"), ("link", "link"), ("pdf", "pdf"),
                             ("open access", "open access"), ("data", "data"), ("code", "code")):
                if r.get(k) and not (label == "link" and any("link" in l for l in links)):
                    links.append(f'<a href="{r[k]}">{label}</a>')
            venue = g(r, "venue", "journal", "conference", "booktitle")
            meta = " · ".join(x for x in (venue, g(r, "type")) if x)
            inner += (f'<div class="pub"><div class="t">{g(r, "title")}</div>'
                      f'<div>{g(r, "authors", "author")}</div>'
                      f'<div class="m">{meta}{" · " if meta and links else ""}{" · ".join(links)}</div></div>')
    body = section("Outputs", "Publications, data and software", inner)
    (OUT / "publications.html").write_text(page("Publications", "publications.html", body))


CLOSED = ("closed", "filled", "no", "past", "expired")


def build_positions(rows):
    if rows is None:
        listing = not_connected("Open positions")
    else:
        rows = [r for r in rows if g(r, "title", "position")]
        open_ = [r for r in rows if g(r, "status", "open").lower() not in CLOSED]
        closed = [r for r in rows if r not in open_]

        def item(r):
            when = g(r, "deadline", "date", "start")
            meta = " · ".join(x for x in (g(r, "type", "level"), g(r, "site", "institution", "location")) if x)
            desc = g(r, "description", "details", "summary")
            contact = r.get("contact_html", "")
            return (f'<div class="news-item"><time>{when}</time><div>'
                    f'<h3>{link(g(r, "title", "position"), g(r, "url", "link", "apply"))}</h3>'
                    f'<p style="color:var(--muted)">{meta}</p>'
                    f'{f"<p>{desc}</p>" if desc else ""}{f"<p>{contact}</p>" if contact else ""}</div></div>')

        listing = ("".join(item(r) for r in open_) if open_ else
                   '<p class="empty-note">No positions are open yet — check back soon.</p>')
        if closed:
            listing += ('<h3 style="margin-top:2.5rem">Filled or closed</h3>' +
                        "".join(item(r) for r in closed))
    body = section("Join us", "Positions available",
                   listing)
    (OUT / "positions.html").write_text(page("Positions", "positions.html", body))


def main():
    (OUT / "style.css").write_text(STYLE)
    (OUT / ".nojekyll").write_text("")
    for old in ("research.html", "news.html", "join.html"):
        (OUT / old).unlink(missing_ok=True)
    team = norm_team(sheet_data.tab("Team"))
    pubs = norm_pubs(sheet_data.tab("Publications"))
    pos = norm_positions(sheet_data.tab("Positions"))
    build_index()
    build_team(team)
    build_publications(pubs)
    build_positions(pos)
    print(f"Built site into {OUT}/")


if __name__ == "__main__":
    main()
