from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src_path = ROOT / 'theme' / 'domowy-reset-v7.xml'
out_path = ROOT / 'theme' / 'domowy-reset-v8.xml'

s = src_path.read_text(encoding='utf-8')
s = s.replace('xmlns:expr="http://www.google.com/1999/xhtml"', 'xmlns:expr="http://www.google.com/2005/gml/expr"')

# Remove the centered masthead copy.
s = re.sub(r'<div class="mast-center">.*?</div>', '', s, flags=re.S)

# Move primary navigation into the masthead, between brand and actions.
nav = re.search(r'<nav class="mainnav">.*?</nav>', s, flags=re.S)
if nav:
    nav_html = nav.group(0).replace('<nav class="mainnav">', '<nav class="mainnav mast-nav">', 1)
    s = s[:nav.start()] + s[nav.end():]
    actions = re.search(r'<div class="mast-actions">.*?</div>', s, flags=re.S)
    if actions:
        s = s[:actions.start()] + nav_html + s[actions.start():]

# Keep the homepage editorial hierarchy: HERO -> CATEGORIES -> LATEST -> EDITORIAL.
# The source V7 already has this order; normalize the category block if needed.

# Critical Blogger fix: Blog1/sidebar belongs on post/archive pages, not the homepage.
# On the homepage this block creates a large empty column when there are no posts.
blog = re.search(r'\s*<section class="blog-area">.*?</section>\s*', s, flags=re.S)
if blog:
    blog_html = blog.group(0).strip()
    wrapped = "\n    <b:if cond='data:blog.pageType != &quot;index&quot;'>\n" + blog_html + "\n    </b:if>\n"
    s = s[:blog.start()] + wrapped + s[blog.end():]

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
