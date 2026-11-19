"""Minimal BibTeX → dict parser for the Publications tab (one entry per cell)."""

from __future__ import annotations

import re

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303",
           "c": "\u0327", "v": "\u030c", "=": "\u0304", ".": "\u0307", "u": "\u0306", "H": "\u030b"}
SPECIAL = {r"\ss": "ß", r"\o": "ø", r"\O": "Ø", r"\aa": "å", r"\AA": "Å", r"\ae": "æ",
           r"\l": "ł", r"\L": "Ł", r"\&": "&amp;", "--": "–", "~": " "}


def detex(s: str) -> str:
    import unicodedata
    s = re.sub(r"\{?\\([`'^\"~=.uvcH])\s*\{?\\?([A-Za-z])\}?\}?",
               lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENTS[m.group(1)]), s)
    for k, v in SPECIAL.items():
        s = s.replace(k + "{}", v).replace("{" + k + "}", v).replace(k, v) if k.startswith("\\") else s.replace(k, v)
    s = re.sub(r"\\(emph|textit|textbf|mathrm)\{([^{}]*)\}", r"\2", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def parse(text: str) -> dict | None:
    m = re.match(r"\s*@(\w+)\s*\{\s*([^,\s]*)\s*,", text)
    if not m:
        return None
    out = {"type": m.group(1).lower(), "key": m.group(2)}
    i, n = m.end(), len(text)
    while i < n:
        fm = re.compile(r"\s*([\w-]+)\s*=\s*").match(text, i)
        if not fm:
            break
        name, i = fm.group(1).lower(), fm.end()
        if i < n and text[i] in "{\"":
            close = "}" if text[i] == "{" else '"'
            depth, j = 0, i
            while j < n:
                c = text[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                if (close == "}" and depth == 0 and c == "}") or (close == '"' and c == '"' and j > i and depth == 0):
                    break
                j += 1
            val, i = text[i + 1:j], j + 1
        else:
            vm = re.compile(r"[^,}\s]+").match(text, i)
            val, i = (vm.group(), vm.end()) if vm else ("", i)
        out[name] = val
        cm = re.compile(r"\s*,?").match(text, i)
        i = cm.end()
    return out


def _initials(first: str) -> str:
    parts = re.split(r"(\s+|-)", first.strip())
    return "".join(p if p.strip() in ("", "-") else (p[0] + "." if not p.endswith(".") else p) for p in parts).replace(".", ". ").replace(".  ", ". ").replace(". -", ".-").strip()


def authors(field: str) -> str:
    names = [a.strip() for a in re.split(r"\s+and\s+", field) if a.strip()]
    out = []
    for a in names:
        a = detex(a)
        if a.lower() == "others":
            out.append("et al."); continue
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
        else:
            bits = a.split()
            last, first = bits[-1], " ".join(bits[:-1])
        out.append(f"{_initials(first)} {last}".strip())
    if len(out) <= 2:
        return " and ".join(out)
    return ", ".join(out[:-1]) + " and " + out[-1]
