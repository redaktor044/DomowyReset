from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / 'theme' / 'domowy-reset-v8.xml'
out = ROOT / 'preview-v8.html'

s = src.read_text(encoding='utf-8')

m = re.search(r'<b:skin\\b[^>]*>\\s*<!\\[CDATA\\[(.*?)\\]\\]>\\s*</b:skin>', s, flags=re.S | re.I)
if not m:
    raise SystemExit('ERROR: could not find Blogger b:skin in V8')
css = m.group(1).strip()
css = css.replace(r'\\:', ':').replace(r'\\;', ';')

b = re.search(r'<body\\b[^>]*>(.*?)</body>', s, flags=re.S | re.I)
if not b:
    raise SystemExit('ERROR: could not find body in V8')
body = b.group(1)

body = re.sub(r"\\s*<b:if\\s+cond=['\"]data:blog\\.pageType\\s*!=\\s*&quot;index&quot;['\"]\\s*>.*?</b:if>\\s*", '\\n', body, flags=re.S | re.I)
body = re.sub(r"\\s*<b:if\\s+cond=['\"]data:blog\\.pageType\\s*==\\s*&quot;index&quot;['\"]\\s*>", '\\n', body, flags=re.I)
body = re.sub(r'</b:if>', '', body, flags=re.I)
body = re.sub(r'<b:section\\b[^>]*>', '', body, flags=re.I)
body = re.sub(r'</b:section>', '', body, flags=re.I)
body = re.sub(r'<b:widget\\b[^>]*/>', '', body, flags=re.I)
body = re.sub(r'\\bexpr:href=["\']data:blog\\.homepageUrl["\']', 'href="/"', body)
body = re.sub(r'<data:[^>]+/>', '', body, flags=re.I)

html = f'''<!doctype html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>DOMOWY RESET — V8 Preview</title>\n<style>\n{css}\nhtml,body{{margin:0;padding:0}}\n</style>\n</head>\n<body>\n{body}\n<div style="position:fixed;right:18px;bottom:18px;z-index:99999;padding:8px 12px;border-radius:999px;background:#20231e;color:#fffefa;font:700 10px/1 Arial,sans-serif;letter-spacing:.12em">V8 PREVIEW</div>\n</body>\n</html>'''

out.write_text(html, encoding='utf-8')
print(f'Preview created: {out}')
