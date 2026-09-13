# DOMOWY RESET — Blogger Publisher

Automatyzacja publikowania artykułów do Blogger API v3.

## Architektura

- `src/blogger_publisher.py` — klient Blogger API v3
- `scripts/oauth_local.py` — jednorazowa autoryzacja OAuth na komputerze
- `.github/workflows/publish.yml` — publikacja przez GitHub Actions
- `content/` — gotowe artykuły do publikacji

## Wymagane sekrety GitHub Actions

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- `BLOGGER_BLOG_ID`

## Ważne

Nie commituj plików z hasłami, tokenami ani `client_secret.json`.
