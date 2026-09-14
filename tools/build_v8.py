from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src_path = ROOT / "theme" / "domowy-reset-v7.xml"
out_path = ROOT / "theme" / "domowy-reset-v8.xml"

s = src_path.read_text(encoding="utf-8")

# 1) Blogger namespace must be the GML namespace.
s = s.replace(
    'xmlns:expr="http://www.google.com/1999/xhtml"',
    'xmlns:expr="http://www.google.com/2005/gml/expr"',
)

# 2) Remove the old centered masthead message completely.
s = re.sub(r'<div class="mast-center">.*?</div>', '', s, count=1, flags=re.S)

# 3) Move the primary navigation inside the masthead.
nav_match = re.search(r'<nav class="mainnav">.*?</nav>', s, flags=re.S)
if nav_match:
    nav = nav_match.group(0)
    nav = nav.replace(
        '<nav class="mainnav">',
        '<nav class="mainnav mast-nav">',
        1,
    )
    s = s[:nav_match.start()] + s[nav_match.end():]
    action_match = re.search(r'<div class="mast-actions">.*?</div>', s, flags=re.S)
    if action_match:
        s = s[:action_match.start()] + nav + s[action_match.start():]

# 4) Blog1/sidebar must NOT create an empty homepage column.
# Wrap the complete blog-area in a non-index Blogger conditional.
if '<section class="blog-area">' in s:
    start = s.index('<section class="blog-area">')
    end = s.index('</section>', start) + len('</section>')
    block = s[start:end]
    if 'data:blog.pageType != &quot;index&quot;' not in s[start:end + 120]:
        wrapped = (
            '<b:if cond=\'data:blog.pageType != &quot;index&quot;\'>\n'
            + block
            + '\n</b:if>'
        )
        s = s[:start] + wrapped + s[end:]

# 5) V8 editorial CSS overrides.
css = r'''
    .mast-center{display:none!important}
    .masthead{grid-template-columns:auto minmax(0,1fr) auto!important;align-items:end!important;gap:34px!important}
    .mast-nav{border:0!important;background:transparent!important;min-width:0!important}
    .mast-nav .wrap{width:auto!important;min-height:0!important;justify-content:flex-end!important;gap:24px!important;overflow:visible!important}
    .mast-nav a{padding:8px 0 7px!important;font-size:12px!important}
    .mast-nav a:after{bottom:1px!important}
    .hero{padding:30px 0 22px}
    .category-row{padding:26px 0 30px}
    @media(max-width:1100px){
      .masthead{grid-template-columns:1fr auto!important;align-items:center!important}
      .mast-nav{grid-column:1/-1;grid-row:2}
      .mast-nav .wrap{justify-content:flex-start!important;overflow:auto!important}
    }
    @media(max-width:700px){
      .masthead{padding:22px 0 16px}
      .mast-nav{margin-top:4px}
      .mast-nav .wrap{gap:18px!important}
    }
'''

if '</b:skin>' not in s:
    raise SystemExit('ERROR: V7 has no Blogger b:skin closing tag')
s = s.replace('</b:skin>', css + '\n  </b:skin>', 1)

# Hard validation before writing anything.
checks = {
    'correct Blogger expr namespace': 'xmlns:expr="http://www.google.com/2005/gml/expr"' in s,
    'mast-center removed': '<div class="mast-center">' not in s,
    'mast-nav exists': '<nav class="mainnav mast-nav">' in s,
    'blog area guarded': "data:blog.pageType != &quot;index&quot;" in s and '<section class="blog-area">' in s,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('ERROR: V8 validation failed: ' + ', '.join(failed))

out_path.write_text(s, encoding="utf-8")
print(f"V8 created: {out_path}")
print("V8 validation: OK")
