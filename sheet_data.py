"""Read the DISTURB Google Sheet (tabs: Team, Publications, Positions).

Each tab is fetched as CSV by its name, so only the standard library is needed.
The sheet must be shared "Anyone with the link → Viewer".

Rows come back as dicts keyed by the header row, lower-cased and stripped
(e.g. "Photo URL" → "photo url"). Blank rows are dropped.

Override the sheet with the SHEET_ID environment variable (e.g. a test copy).
"""

from __future__ import annotations

import csv
import io
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SHEET_ID = os.environ.get("SHEET_ID") or "1160bdymzk7c3r4y803dXJmIrAQQnHDXTPIVhS06giGU"


def _url(tab: str) -> str:
    q = urllib.parse.urlencode({"tqx": "out:csv", "sheet": tab})
    return f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?{q}"


def tab(name: str) -> list[dict] | None:
    """Rows of one tab, or None if the sheet/tab cannot be read."""
    try:
        req = urllib.request.Request(_url(name), headers={"User-Agent": "disturb-site-build"})
        with urllib.request.urlopen(req, timeout=60) as r:
            ctype = r.headers.get("Content-Type", "")
            text = r.read().decode("utf-8")
    except urllib.error.URLError as e:
        print(f"WARNING: could not fetch sheet tab '{name}': {e}", file=sys.stderr)
        return None
    if "csv" not in ctype or text.lstrip().startswith("<"):
        print(f"WARNING: sheet tab '{name}' is not readable — is the sheet shared "
              f"'Anyone with the link can view'?", file=sys.stderr)
        return None
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return []
    head = [h.strip().lower() for h in rows[0]]
    out = []
    for r in rows[1:]:
        d = {h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(head) if h}
        if any(d.values()):
            out.append(d)
    return out
