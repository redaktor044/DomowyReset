from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
V7 = ROOT / "theme/domowy-reset-v7.xml"
V8 = ROOT / "theme/domowy-reset-v8.xml"

errors = []


def check_theme(path: Path, require_v8: bool = False):
    if not path.exists():
        errors.append(f"missing: {path}")
        return
    s = path.read_text(encoding="utf-8")

    # XML well-formedness catches broken Blogger markup before upload.
    try:
        ET.fromstring(s)
    except Exception as exc:
        errors.append(f"{path.name}: XML parse error: {exc}")

    if 'xmlns:b="http://www.google.com/2005/gml/b"' not in s:
        errors.append(f"{path.name}: missing Blogger b namespace")
    if 'xmlns:expr="http://www.google.com/2005/gml/expr"' not in s:
        errors.append(f"{path.name}: wrong/missing Blogger expr namespace")
    if "<b:skin><![CDATA[" not in s or "</b:skin>" not in s:
        errors.append(f"{path.name}: malformed b:skin")
    if "\\:" in s:
        errors.append(f"{path.name}: escaped CSS colon found")

    if require_v8:
        if '<div class="mast-center">' in s:
            errors.append("V8: mast-center still present")
        if '<nav class="mainnav mast-nav">' not in s:
            errors.append("V8: mast-nav missing")
        header_end = s.find("</header>")
        nav_pos = s.find('<nav class="mainnav mast-nav">')
        if nav_pos < 0 or header_end < 0 or nav_pos > header_end:
            errors.append("V8: mast-nav is not inside masthead")
        blog_pos = s.find('<section class="blog-area">')
        if blog_pos < 0:
            errors.append("V8: blog-area missing")
        else:
            guard_before = s.rfind("data:blog.pageType != &quot;index&quot;", 0, blog_pos)
            if guard_before < 0:
                errors.append("V8: blog-area is not guarded from homepage")

        for marker in ("class=\"hero\"", "class=\"category-row\"", "Najnowsze artykuły", "class=\"editorial-band\""):
            if marker not in s:
                errors.append(f"V8: missing homepage marker: {marker}")


check_theme(V7)
check_theme(V8, require_v8=True)

if errors:
    print("REPO VALIDATION: FAILED")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

print("REPO VALIDATION: OK")
print(" - V7 XML: OK")
print(" - V8 XML: OK")
print(" - Blogger namespaces: OK")
print(" - V8 masthead/nav: OK")
print(" - V8 homepage sections: OK")
print(" - V8 homepage blog gap guard: OK")
