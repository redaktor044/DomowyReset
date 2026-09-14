from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src_path = ROOT / 'theme' / 'domowy-reset-v7.xml'
out_path = ROOT / 'theme' / 'domowy-reset-v8.xml'

s = src_path.read_text(encoding='utf-8')
s = s.replace('xmlns:expr="http://www.google.com/1999/xhtml"', 'xmlns:expr="http://www.google.com/2005/gml/expr"')

# Remove the centered masthead copy.
s = re.sub(r'<div class="mast-center">.*?</div>', '', s, flags=re.S)

# Move the primary navigation into the masthead, between brand and actions.
nav = re.search(r'<nav class="mainnav">.*?</nav>', s, flags=re.S)
if nav:
    nav_html = nav.group(0).replace('<nav class="mainnav">', '<nav class="mainnav mast-nav">')
    s = s[:nav.start()] + s[nav.end():]
    actions = re.search(r'<div class="mast-actions">.*?</div>', s, flags=re.S)
    if actions:
        s = s[:actions.start()] + nav_html + s[actions.start():]

# Keep homepage editorial sections clean: the live Blog widget/sidebar belongs
# on article/archive pages, otherwise an empty Blog1 column creates a huge gap.
blog = re.search(r'<section class="blog-area">.*?</section>', s, flags=re.S)
if blog and '<b:if cond=' not in blog.group(0):
    blog_html = blog.group(0)
    replacement = '<b:if cond=\'data:blog.pageType != &quot;index&quot;\'>\n      ' + blog_html + '\n    </b:if>'
    s = s[:blog.start()] + replacement + s[blog.end():]

# V8 editorial CSS overrides.
css = r'''
    .mast-center{display:none!important}
    .masthead{grid-template-columns:auto minmax(0,1fr) auto!important;align-items:end!important;gap:34px!important}
    .mast-nav{border:0!important;background:transparent!important;min-width:0}
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
s = s.replace('</b:skin>', css + '\n  </b:skin>')

out_path.write_text(s, encoding='utf-8')
print(f'V8 created: {out_path}')
