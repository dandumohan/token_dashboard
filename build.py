#!/usr/bin/env python3
"""
Builds both ways of publishing from the files in src/ :

  dist/          MULTI-FILE site (Netlify etc.)   dist/index.html            = main app
                                                  dist/mreports/index.html   = Mreports
                                                  dist/nursery/index.html    = Nursery Transactions
                 The main app loads Mreports / Nursery Transactions from their own URLs,
                 so you can fix one page and redeploy without touching the others.

  dist-single/   ONE-FILE version                 dist-single/Mindex_supabase.html
                 Both pages are copied inside the main app. Works offline from a pen drive / email
                 (it still needs internet for the Supabase data and the CDN libraries).

Usage:  python3 build.py          (Python 3.8+, standard library only)
"""
import json, re, shutil, datetime
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
BUILD = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def read(p): return Path(p).read_text(encoding="utf-8")
def write(p, s):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8", newline="")

config_js = read(ROOT / "config.js")
CONFIG_TAG = "<script>\n" + config_js.strip() + "\n</script>"

def stamp(html):
    """Copy config.js and the build time into a page."""
    assert "<!--@@CONFIG@@-->" in html, "page has no <!--@@CONFIG@@--> marker"
    return html.replace("<!--@@CONFIG@@-->", CONFIG_TAG).replace("@@BUILD@@", BUILD)

def js_string(s):
    """A JS string literal that is safe inside another page's <script>."""
    return json.dumps(s).replace("<", "\\u003c")

main = read(SRC / "main" / "Mindex_supabase.html")
mreports = read(SRC / "mreports" / "index.html")
nursery = read(SRC / "nursery" / "index.html")

# ---- A. multi-file site ----
out = ROOT / "dist"
if out.exists(): shutil.rmtree(out)
write(out / "index.html", stamp(main))
write(out / "mreports" / "index.html", stamp(mreports))
write(out / "nursery" / "index.html", stamp(nursery))

# ---- B. single file ----
single = stamp(main)
for marker, page in (("NURTXN_HTML", nursery), ("MREPORTS_HTML", mreports)):
    tag = "/*@@%s@@*/ null" % marker
    assert single.count(tag) == 1, "marker %s missing in the main app" % marker
    single = single.replace(tag, js_string(stamp(page)))
out2 = ROOT / "dist-single"
if out2.exists(): shutil.rmtree(out2)
write(out2 / "Mindex_supabase.html", single)

print("Built", BUILD)
print("  dist/                         multi-file site  (", sum(1 for _ in out.rglob("*.html")), "pages )")
print("  dist-single/Mindex_supabase.html  one file (", round(len(single) / 1024), "KB )")
