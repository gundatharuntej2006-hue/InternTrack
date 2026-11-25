"""Automated accessibility checks on the rendered template previews (KAN-49 / UA-6).

Run `python tools/ui_preview.py` first, then `python tools/a11y_check.py`.
Checks each page in tools/ui_preview_out/ against the UA-6 checklist items that
can be tested from HTML, plus colour contrast for the colours in static/css/app.css.
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "ui_preview_out"


def luminance(hex_colour):
    hex_colour = hex_colour.lstrip("#")
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# Text/background pairs actually used in app.css. 4.5:1 for text, 3:1 for borders/focus.
COLOUR_PAIRS = [
    ("Body text (--ink on white)", "#1f2937", "#ffffff", 4.5),
    ("Muted text (--muted on white)", "#4b5563", "#ffffff", 4.5),
    ("Muted text on panel (--muted on --panel)", "#4b5563", "#f5f7fa", 4.5),
    ("Links (--brand on white)", "#1b2b45", "#ffffff", 4.5),
    ("Top bar text (white on --brand)", "#ffffff", "#1b2b45", 4.5),
    ("Primary button (white on --brand)", "#ffffff", "#1b2b45", 4.5),
    ("Error text (--error on white)", "#b91c1c", "#ffffff", 4.5),
    ("Success marker (--ok on white)", "#166534", "#ffffff", 3.0),
    ("Input border (#6b7280 on white)", "#6b7280", "#ffffff", 3.0),
    ("Focus ring (--focus on white)", "#2563eb", "#ffffff", 3.0),
    ("Focus ring on top bar (white on --brand)", "#ffffff", "#1b2b45", 3.0),
]


def check_page(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    problems = []

    html = soup.find("html")
    if not html or not html.get("lang"):
        problems.append("missing <html lang>")
    if not soup.title or not soup.title.get_text(strip=True):
        problems.append("missing <title>")
    if not soup.find("meta", attrs={"name": "viewport"}):
        problems.append("missing viewport meta")

    main = soup.find("main")
    if not main:
        problems.append("missing <main> landmark")
    skip = soup.find("a", class_="skip")
    if not skip or skip.get("href") != "#main":
        problems.append("missing skip link to #main")

    h1s = soup.find_all("h1")
    if len(h1s) != 1:
        problems.append(f"expected one <h1>, found {len(h1s)}")
    last = 0
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        level = int(h.name[1])
        if last and level > last + 1:
            problems.append(f"heading level jumps h{last} -> h{level} ('{h.get_text(strip=True)[:40]}')")
        last = level

    ids = [t["id"] for t in soup.find_all(id=True)]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"duplicate ids: {', '.join(sorted(dupes))}")

    for field in soup.find_all(["input", "select", "textarea"]):
        if field.get("type") in ("hidden", "submit", "button"):
            continue
        fid = field.get("id")
        labelled = (
            (fid and soup.find("label", attrs={"for": fid}))
            or field.find_parent("label")
            or field.get("aria-label")
            or field.get("aria-labelledby")
        )
        if not labelled:
            problems.append(f"form field without label: name={field.get('name')}")
        if field.has_attr("aria-describedby"):
            for ref in field["aria-describedby"].split():
                if not soup.find(id=ref):
                    problems.append(f"aria-describedby points to missing id '{ref}'")

    for btn in soup.find_all("button"):
        if not (btn.get_text(strip=True) or btn.get("aria-label")):
            problems.append("button without text")
    for a in soup.find_all("a"):
        if not (a.get_text(strip=True) or a.get("aria-label")):
            problems.append(f"link without text: href={a.get('href')}")
        if a.get_text(strip=True).lower() in ("click here", "here", "more", "link"):
            problems.append(f"vague link text: '{a.get_text(strip=True)}'")
    for img in soup.find_all("img"):
        if not img.has_attr("alt"):
            problems.append(f"image without alt: {img.get('src')}")

    for table in soup.find_all("table"):
        if not table.find("th"):
            problems.append("table without header cells")
        elif not table.find("caption") and not table.get("aria-label") and not table.get("aria-labelledby"):
            problems.append("table without caption/aria-label")
        for th in table.find_all("th"):
            if not th.get("scope"):
                problems.append("table header without scope")
                break

    for fs in soup.find_all("fieldset"):
        if not fs.find("legend"):
            problems.append("fieldset without legend")

    summary = soup.find(class_="errorsummary")
    if summary and not (summary.get("role") == "alert" or summary.get("tabindex")):
        problems.append("error summary is not announced (role=alert or focus)")

    return problems


def main():
    pages = sorted(p for p in OUT.glob("*.html") if p.name != "index.html")
    if not pages:
        sys.exit("No previews found. Run: python tools/ui_preview.py")

    failed = 0
    print("== Page checks ==")
    for page in pages:
        problems = check_page(page)
        status = "PASS" if not problems else "FAIL"
        failed += bool(problems)
        print(f"{status}  {page.name}")
        for p in problems:
            print(f"      - {p}")

    print("\n== Colour contrast (WCAG 2.1 AA) ==")
    for name, fg, bg, need in COLOUR_PAIRS:
        ratio = contrast(fg, bg)
        ok = ratio >= need
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {ratio:5.2f}:1 (needs {need}:1)  {name}")

    print(f"\n{len(pages)} pages checked, {failed} failing item(s).")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
