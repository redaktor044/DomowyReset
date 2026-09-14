from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'theme' / 'domowy-reset-v8.xml'
out = ROOT / 'preview-v8.html'

s = src.read_text(encoding='utf-8')

# Convert Blogger skin into normal browser CSS.
m = re.search(r'<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>', s, flags=re.S)
css = m.group(1) if m else ''
s = re.sub(r'<b:skin><!\[CDATA\[.*?\]\]></b:skin>', '<style>\n' + css + '\n</style>', s, flags=re.S)

# Preview is the homepage, so remove Blogger's non-index-only content.
s = re.sub(r"\s*<b:if cond='data:blog\.pageType != &quot;index&quot;'>.*?</b:if>\s*", '\n', s, flags=re.S)

# Unwrap homepage conditional and remove Blogger-only section/widget markup.
s = re.sub(r"\s*<b:if cond='data:blog\.pageType == &quot;index&quot;'>", '\n', s)
s = s.replace('</b:if>', '')
s = re.sub(r'<b:section[^>]*>', '', s)
s = re.sub(r'</b:section>', '', s)
s = re.sub(r'<b:widget[^>]*/>', '', s)

# Replace Blogger expressions with static preview values.
s = s.replace('expr:href="data:blog.homepageUrl"', 'href="/"')
s = s.replace('<data:blog.pageTitle/>', 'DOMOWY RESET')
s = re.sub(r'\s+xmlns:[^=]+="[^"]+"', '', s)
s = re.sub(r'\s+b:[^=]+="[^"]+"', '', s)
s = re.sub(r'\s+expr:[^=]+="[^"]+"', '', s)
s = re.sub(r'<data:[^>]+/>', '', s)

# Mark this as a local visual preview.
s = s.replace('</head>', '<style>body:before{content:"V8 PREVIEW";position:fixed;right:18px;bottom:18px;z-index:9999;padding:8px 12px;border-radius:999px;background:#20231e;color:#fffefa;font:700 10px/1 DM Sans,Arial,sans-serif;letter-spacing:.12em}</style></head>')

out.write_text(s, encoding='utf-8')
print(f'Preview created: {out}')
