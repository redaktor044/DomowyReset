from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "theme" / "domowy-reset-v8.xml"
out = ROOT / "preview-v8.html"
css_out = ROOT / "preview-v8.css"

s = src.read_text(encoding="utf-8")

# Extract Blogger CSS using string boundaries, not a fragile regex.
skin_start = s.find("<b:skin")
if skin_start < 0:
    raise SystemExit("ERROR: could not find Blogger b:skin in V8")
skin_open_end = s.find(">", skin_start)
skin_end = s.find("</b:skin>", skin_open_end)
if skin_open_end < 0 or skin_end < 0:
    raise SystemExit("ERROR: malformed Blogger b:skin in V8")

css = s[skin_open_end + 1:skin_end]
css = re.sub(r"^\s*<!\[CDATA\[", "", css.strip())
css = re.sub(r"\]\]>\s*$", "", css).strip()
css = css.replace("\\:", ":").replace("\\;", ";")

# Extract body only.
body_start = s.find("<body")
body_open_end = s.find(">", body_start)
body_end = s.rfind("</body>")
if body_start < 0 or body_open_end < 0 or body_end < 0:
    raise SystemExit("ERROR: could not find body in V8")
body = s[body_open_end + 1:body_end]

# Static preview is the homepage. Remove Blogger conditionals and widgets.
body = re.sub(
    r"\s*<b:if\s+cond=['\"]data:blog\.pageType\s*!=\s*&quot;index&quot;['\"]\s*>.*?</b:if>\s*",
    "\n",
    body,
    flags=re.S | re.I,
)
body = re.sub(
    r"\s*<b:if\s+cond=['\"]data:blog\.pageType\s*==\s*&quot;index&quot;['\"]\s*>",
    "\n",
    body,
    flags=re.I,
)
body = re.sub(r"</b:if>", "", body, flags=re.I)
body = re.sub(r"<b:section\b[^>]*>", "", body, flags=re.I)
body = re.sub(r"</b:section>", "", body, flags=re.I)
body = re.sub(r"<b:widget\b[^>]*/>", "", body, flags=re.I)
body = re.sub(r"\bexpr:href=['\"]data:blog\.homepageUrl['\"]", 'href="/"', body)
body = re.sub(r"<data:[^>]+/>", "", body, flags=re.I)

# External CSS eliminates any chance of CSS being rendered as page text.
css_out.write_text(css + "\nhtml,body{margin:0;padding:0}\n", encoding="utf-8")

html = f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DOMOWY RESET — V8 Preview</title>
<link rel="stylesheet" href="preview-v8.css">
</head>
<body>
{body}
<div class="v8-badge">V8 PREVIEW</div>
<style>.v8-badge{{position:fixed;right:18px;bottom:18px;z-index:99999;padding:8px 12px;border-radius:999px;background:#20231e;color:#fffefa;font:700 10px/1 Arial,sans-serif;letter-spacing:.12em}}</style>
</body>
</html>'''

out.write_text(html, encoding="utf-8")

# Sanity checks.
if "<style" in css or "</style" in css:
    raise SystemExit("ERROR: CSS extraction produced HTML style tags")
if "<link rel=\"stylesheet\" href=\"preview-v8.css\">" not in html:
    raise SystemExit("ERROR: preview stylesheet link missing")
print(f"Preview created: {out}")
print(f"CSS created: {css_out}")
print("Preview validation: OK")
