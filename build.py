#!/usr/bin/env python3
"""Build the DISTURB website into docs/ from content.py.

Run:    python3 build.py          (or: make site / make serve)
Deploy: git push                  (GitHub Actions builds and publishes docs/)

Standard library only — no dependencies.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import content as C

OUT = Path(__file__).parent / "docs"
OUT.mkdir(exist_ok=True)
YEAR = datetime.now().year

NAV = [
    ("Home", "index.html"),
    ("Research", "research.html"),
    ("Team", "team.html"),
    ("News", "news.html"),
    ("Publications", "publications.html"),
    ("Join us", "join.html"),
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
  font-family: "Lato", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  font-size: 17px; line-height: 1.65; color: var(--ink); background: var(--bg);
}
a { color: var(--red); text-decoration: none; }
a:hover { text-decoration: underline; }
img { max-width: 100%; height: auto; display: block; }
.container { max-width: 1160px; margin: 0 auto; padding: 0 1.25rem; }
.section { padding: 3.5rem 0; }
.section.alt { background: var(--panel); }
.kicker {
  color: var(--red); font-weight: 900; font-size: .8rem;
  letter-spacing: .14em; text-transform: uppercase; margin-bottom: .35rem;
}
h1, h2, h3 { color: var(--navy); line-height: 1.2; }
h2 { font-size: 1.9rem; font-weight: 900; margin-bottom: 1rem; }
h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: .4rem; }
.lead { font-size: 1.12rem; color: var(--muted); max-width: 52rem; }

/* header */
header.site { background: #fff; border-bottom: 1px solid var(--line); }
header.site .container { display: flex; align-items: center; gap: 1rem; padding-top: .7rem; padding-bottom: .7rem; }
.brand { display: flex; align-items: center; gap: .8rem; color: var(--navy); }
.brand:hover { text-decoration: none; }
.brand img { height: 52px; width: auto; }
.brand-word { font-weight: 900; font-size: 1.7rem; letter-spacing: .14em; line-height: 1; }
.brand-sub { font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-top: .25rem; }
.header-grant { margin-left: auto; text-align: right; font-size: .75rem; font-weight: 700;
  letter-spacing: .14em; text-transform: uppercase; color: var(--muted); line-height: 1.5; }
nav.site { background: var(--navy); position: sticky; top: 0; z-index: 50; }
nav.site ul { list-style: none; display: flex; flex-wrap: wrap; justify-content: flex-end; }
nav.site a { display: block; color: #cfd8e8; padding: .75rem .9rem; font-size: .9rem; letter-spacing: .03em; }
nav.site a:hover { color: #fff; text-decoration: none; }
nav.site a.active { color: #fff; box-shadow: inset 0 -3px 0 var(--red); }

/* hero */
.hero { position: relative; color: #fff; background: var(--navy) url("images/turbulence.jpg") center/cover; }
.hero::before { content: ""; position: absolute; inset: 0;
  background: linear-gradient(100deg, rgba(20,40,75,.96) 0%, rgba(20,40,75,.86) 50%, rgba(20,40,75,.35) 100%); }
.hero .container { position: relative; padding-top: 4.5rem; padding-bottom: 4.5rem; }
.hero h1 { color: #fff; font-size: clamp(2rem, 4.5vw, 3.1rem); font-weight: 900; max-width: 40rem; }
.hero p { font-size: 1.15rem; max-width: 40rem; margin-top: 1rem; color: #e3e9f4; }
.hero .motto { margin-top: 1.6rem; font-weight: 900; color: #fff; display: inline-block;
  border-left: 4px solid var(--red); padding-left: .8rem; }
.figures { background: var(--red); color: #fff; }
.figures .container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; padding-top: 1.1rem; padding-bottom: 1.1rem; text-align: center; }
.figures b { display: block; font-size: 1.6rem; font-weight: 900; line-height: 1.2; }
.figures span { font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; opacity: .9; }

/* grids & cards */
.grid { display: grid; gap: 1.25rem; }
.g2 { grid-template-columns: repeat(2, 1fr); }
.g3 { grid-template-columns: repeat(3, 1fr); }
.g4 { grid-template-columns: repeat(4, 1fr); }
.card { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 1.25rem; }
.alt .card { border-color: #dde3ec; }
.card p { color: var(--muted); font-size: .97rem; }
.apps { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin: 1.5rem 0 2rem; }
.apps figure { position: relative; border-radius: 6px; overflow: hidden; aspect-ratio: 4/3; }
.apps img { width: 100%; height: 100%; object-fit: cover; }
.apps figcaption { position: absolute; left: 0; right: 0; bottom: 0; padding: .3rem .6rem; font-size: .75rem;
  font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #fff;
  background: linear-gradient(transparent, rgba(0,0,0,.65)); }
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
  border-radius: 50%; background: var(--navy); color: #fff; font-weight: 900; font-size: .9rem; margin-bottom: .6rem; }
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
  color: var(--red); font-weight: 900; font-style: italic; }
.phases { display: grid; grid-template-columns: 22fr 27fr 24fr; gap: 4px; margin: 1rem 0 1.25rem; }
.phases div { color: #fff; padding: .55rem .8rem; font-size: .9rem; font-weight: 700; border-radius: 3px; }
.phases div:nth-child(1) { background: var(--blue); }
.phases div:nth-child(2) { background: var(--navy-2); }
.phases div:nth-child(3) { background: var(--red); }
.phases span { font-weight: 400; opacity: .9; }
table.wp { width: 100%; border-collapse: collapse; font-size: .97rem; }
table.wp td { padding: .5rem .4rem; border-top: 1px solid var(--line); vertical-align: top; }
table.wp td:first-child { font-weight: 900; color: var(--navy); width: 4rem; }
table.wp td:last-child { color: var(--muted); text-align: right; white-space: nowrap; }
.btn { display: inline-block; background: var(--red); color: #fff; padding: .6rem 1.1rem; border-radius: 4px; font-weight: 700; }
.btn:hover { text-decoration: none; background: #a50d26; }
.btn.ghost { background: transparent; color: var(--navy); border: 2px solid var(--navy); }

/* team */
.site-card { border-top: 4px solid var(--red); }
.site-card:nth-child(2) { border-top-color: var(--navy); }
.site-card:nth-child(3) { border-top-color: var(--blue); }
.site-card .pillar-name { font-size: .78rem; font-weight: 900; letter-spacing: .14em; text-transform: uppercase; color: var(--red); }
.pi { display: flex; gap: .9rem; align-items: center; margin: .9rem 0; }
.pi .ph { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.pi .ph.empty { background: var(--panel); display: flex; align-items: center; justify-content: center;
  color: var(--navy); font-weight: 900; font-size: 1.3rem; }
.pi b { display: block; font-size: 1.1rem; color: var(--navy); }
.pi span { font-size: .85rem; color: var(--muted); }
.members { list-style: none; font-size: .95rem; }
.members li { padding: .3rem 0; border-top: 1px solid var(--line); }

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
.motto-bar { background: var(--red); color: #fff; text-align: center; font-weight: 900; padding: .8rem; letter-spacing: .02em; }

@media (max-width: 900px) {
  .g3, .g4 { grid-template-columns: 1fr 1fr; }
  .synergy { grid-template-columns: 1fr; }
  .figures .container { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 640px) {
  body { font-size: 16px; }
  .g2, .g3, .g4 { grid-template-columns: 1fr; }
  .apps { grid-template-columns: 1fr 1fr; }
  .header-grant { display: none; }
  .brand img { height: 42px; }
  .brand-word { font-size: 1.4rem; }
  nav.site ul { justify-content: flex-start; overflow-x: auto; flex-wrap: nowrap; }
  nav.site a { padding: .7rem .65rem; white-space: nowrap; }
  .figures .container { grid-template-columns: repeat(2, 1fr); }
  .phases { grid-template-columns: 1fr; }
  .news-item { grid-template-columns: 1fr; gap: .2rem; }
  .funding { grid-template-columns: 1fr; }
  .section { padding: 2.5rem 0; }
}
"""

# ── Scaffolding ────────────────────────────────────────────────────────────────

def header_html(active: str) -> str:
    links = "".join(
        '<li><a href="{}"{}>{}</a></li>'.format(href, ' class="active"' if href == active else "", label)
        for label, href in NAV)
    return f"""
<header class="site"><div class="container">
  <a class="brand" href="index.html">
    <img src="images/logo.jpg" alt="DISTURB logo">
    <div><div class="brand-word">{C.PROJECT}</div><div class="brand-sub">{C.TAGLINE}</div></div>
  </a>
  <div class="header-grant">{C.GRANT}<br>{C.PERIOD} · GA {C.GA}</div>
</div></header>
<nav class="site"><div class="container"><ul>{links}</ul></div></nav>"""


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
<meta property="og:image" content="images/turbulence.jpg">
<link rel="icon" href="images/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
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
  <div class="kicker">{kicker}</div>
  <h2>{title}</h2>
  {inner}
</div></section>"""

# ── Page blocks ────────────────────────────────────────────────────────────────

def hero() -> str:
    figs = "".join(f"<div><b>{v}</b><span>{k}</span></div>" for v, k in C.KEY_FIGURES)
    return f"""
<section class="hero"><div class="container">
  <div class="kicker" style="color:#ff8a9a">{C.GRANT} · {C.PERIOD}</div>
  <h1>{C.HERO_TITLE}</h1>
  <p>{C.HERO_TEXT}</p>
  <div class="motto">{C.MOTTO}</div>
</div></section>
<div class="figures"><div class="container">{figs}</div></div>"""


def challenge_block(alt=False) -> str:
    apps = "".join(f'<figure><img src="images/{img}" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
                   for n, img in C.APPLICATIONS)
    cards = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in C.CHALLENGES)
    return section("The challenge", "Turbulence: a barrier to progress",
                   f'<p class="lead">{C.CHALLENGE_TEXT}</p><div class="apps">{apps}</div>'
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


def plan_block(alt=False) -> str:
    qs = "".join(f"<li>{q}</li>" for q in C.QUESTIONS)
    ph = "".join(f"<div>{n} <span>· {m}</span></div>" for n, m in C.PHASES)
    wp = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in C.WORK_PACKAGES)
    return section("Programme", "Scientific questions and six-year plan",
                   f'<div class="grid g2"><div><h3>Scientific questions</h3><ol class="questions">{qs}</ol></div>'
                   f'<div><h3>Six years, three phases</h3><div class="phases">{ph}</div>'
                   f'<table class="wp">{wp}</table><p style="margin-top:1rem;color:var(--muted)">{C.OUTPUTS_TEXT}</p>'
                   f'</div></div>', alt)


def initials(name: str) -> str:
    return "".join(w[0] for w in name.split()[:2])


def team_cards() -> str:
    out = ""
    for s in C.TEAM:
        pi = s["pi"]
        ph = (f'<img class="ph" src="images/{pi["photo"]}" alt="{pi["name"]}">' if pi.get("photo")
              else f'<div class="ph empty">{initials(pi["name"])}</div>')
        name = f'<a href="{pi["url"]}">{pi["name"]}</a>' if pi.get("url") else pi["name"]
        mem = "".join(f"<li>{m}</li>" for m in s["members"])
        site = f'<a href="{s["url"]}">{s["site"]}</a>' if s.get("url") else s["site"]
        out += (f'<div class="card site-card"><div class="pillar-name">{s["pillar"]}</div>'
                f'<div style="color:var(--muted);font-size:.92rem">{site}</div>'
                f'<div class="pi">{ph}<div><b>{name}</b><span>{pi["role"]}</span></div></div>'
                f'<ul class="members">{mem}</ul></div>')
    return f'<div class="grid g3">{out}</div>'


def news_list(items) -> str:
    if not items:
        return '<p class="empty-note">No news yet.</p>'
    return "".join(f'<div class="news-item"><time>{n["date"]}</time><div><h3>{n["title"]}</h3>'
                   f'<p>{n["text"]}</p></div></div>' for n in items)

# ── Pages ──────────────────────────────────────────────────────────────────────

def build_index():
    body = hero()
    body += section("The project", "Seeing turbulence through three lenses at once",
        f'<p class="lead">{C.CHALLENGE_TEXT}</p>'
        f'<p style="margin-top:1.5rem"><a class="btn" href="research.html">Explore the research</a> &nbsp; '
        f'<a class="btn ghost" href="join.html">Open positions</a></p>')
    body += twins_block(alt=True)
    body += flows_block()
    body += section("Consortium", "Three sites, three pillars", team_cards(), alt=True)
    body += section("Latest", "News", news_list(C.NEWS[:3]) +
                    '<p style="margin-top:1rem"><a href="news.html">All news →</a></p>')
    (OUT / "index.html").write_text(page("", "index.html", body))


def build_research():
    body = (challenge_block() + pillars_block(alt=True) + twins_block() +
            flows_block(alt=True) + plan_block())
    (OUT / "research.html").write_text(page("Research", "research.html", body))


def build_team():
    body = section("The team", "Experiment · Simulation · Modelling",
                   f'<p class="lead" style="margin-bottom:2rem">DISTURB brings together three groups, '
                   f'each leading one pillar: {C.SITES}.</p>' + team_cards())
    (OUT / "team.html").write_text(page("Team", "team.html", body))


def build_news():
    body = section("News", "Project news", news_list(C.NEWS))
    (OUT / "news.html").write_text(page("News", "news.html", body))


def build_publications():
    if C.PUBLICATIONS:
        items = ""
        for p in C.PUBLICATIONS:
            links = []
            if p.get("doi"):
                links.append(f'<a href="https://doi.org/{p["doi"]}">doi</a>')
            if p.get("open_access"):
                links.append(f'<a href="{p["open_access"]}">open access</a>')
            items += (f'<div class="pub"><div class="t">{p["title"]}</div>'
                      f'<div>{p["authors"]}</div><div class="m">{p["venue"]} ({p["year"]})'
                      f'{" · " + " · ".join(links) if links else ""}</div></div>')
    else:
        items = ('<p class="empty-note">Publications, open datasets and software will be listed '
                 'here as the project progresses.</p>')
    body = section("Outputs", "Publications, data and software", items)
    (OUT / "publications.html").write_text(page("Publications", "publications.html", body))


def build_join():
    if C.OPENINGS:
        rows = "".join(f'<div class="news-item"><time>{o.get("date","")}</time><div><h3>'
                       f'<a href="{o["url"]}">{o["title"]}</a></h3><p>{o["site"]}</p></div></div>'
                       for o in C.OPENINGS)
    else:
        rows = '<p class="empty-note">No positions are open yet — check back soon.</p>'
    figs = "".join(f'<div class="card" style="text-align:center"><h3 style="font-size:2rem">{v}</h3>'
                   f'<p>{k}</p></div>' for v, k in C.KEY_FIGURES[2:])
    body = section("Join us", "Open positions",
                   f'<p class="lead" style="margin-bottom:1.5rem">{C.OPENINGS_TEXT}</p>'
                   f'<div class="grid g3" style="margin-bottom:2rem">{figs}</div>{rows}')
    (OUT / "join.html").write_text(page("Join us", "join.html", body))


def main():
    (OUT / "style.css").write_text(STYLE)
    (OUT / ".nojekyll").write_text("")
    build_index(); build_research(); build_team(); build_news()
    build_publications(); build_join()
    print(f"Built site into {OUT}/")


if __name__ == "__main__":
    main()
