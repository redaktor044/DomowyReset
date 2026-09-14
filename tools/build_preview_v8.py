from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'theme' / 'domowy-reset-v8.xml'
out = ROOT / 'preview-v8.html'

s = src.read_text(encoding='utf-8')

# Extract the Blogger skin and render it as ordinary browser CSS.
m = re.search(r'<b:skin><!\[CDATA\[(.*?)\]\]></b:skin>', s, flags=re.S)
if not m:
    raise SystemExit('ERROR: could not find Blogger b:skin in V8')
css = m.group(1).strip()

# V8 generator may leave XML-escaped characters in generated override CSS.
# They must be real CSS punctuation in a normal HTML preview.
css = css.replace(r'\:', ':').replace(r'\;', ';')

# Extract only the body. This prevents Blogger-only head/XML markup from leaking into preview.
b = re.search(r'<body>(.*?)</body>', s, flags=re.S)
if not b:
    raise SystemExit('ERROR: could not find body in V8')
body = b.group(1)

# Preview is always the homepage.
body = re.sub(r"\s*<b:if cond='data:blog\.pageType != &quot;index&quot;'>.*?</b:if>\s*", '\n', body, flags=re.S)
body = re.sub(r"\s*<b:if cond='data:blog\.pageType == &quot;index&quot;'>", '\n', body)
body = body.replace('</b:if>', '')

# Remove Blogger section/widget wrappers while preserving their inner markup.
body = re.sub(r'<b:section[^>]*>', '', body)
body = re.sub(r'</b:section>', '', body)
body = re.sub(r'<b:widget[^>]*/>', '', body)

# Replace Blogger expressions/data tags with static preview values.
body = body.replace('expr:href="data:blog.homepageUrl"', 'href="/"')
body = re.sub(r'<data:[^>]+/>', '', body)

# Build a clean standalone HTML preview.
html = '''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DOMOWY RESET — V8 Preview</title>
<style>
%s
/* Preview safety */
html,body{margin:0;padding:0}
</style>
</head>
<body>
%s
<div style="position:fixed;right:18px;bottom:18px;z-index:99999;padding:8px 12px;border-radius:999px;background:#20231e;color:#fffefa;font:700 10px/1 Arial,sans-serif;letter-spacing:.12em">V8 PREVIEW</div>
</body>
</html>
''' % (css, body)

out.write_text(html, encoding='utf-8')
print(f'Preview created: {out}')
