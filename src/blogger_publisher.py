import json
import os
from typing import Any, Dict, Optional

import requests

BLOGGER_API = "https://www.googleapis.com/blogger/v3"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


def get_access_token() -> str:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
    refresh_token = os.environ["GOOGLE_REFRESH_TOKEN"]

    response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def blogger_request(
    method: str,
    path: str,
    *,
    access_token: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    response = requests.request(
        method,
        f"{BLOGGER_API}/{path.lstrip('/')}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=payload,
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(
            f"Blogger API error {response.status_code}: {response.text}"
        )
    return response.json() if response.text else {}


def create_post(
    *,
    blog_id: str,
    title: str,
    content: str,
    labels: Optional[list[str]] = None,
    is_draft: bool = True,
) -> Dict[str, Any]:
    token = get_access_token()
    post = {"title": title, "content": content}
    if labels:
        post["labels"] = labels

    path = f"blogs/{blog_id}/posts"
    if is_draft:
        path += "?isDraft=true"

    return blogger_request(
        "POST",
        path,
        access_token=token,
        payload=post,
    )


def main() -> None:
    blog_id = os.environ["BLOGGER_BLOG_ID"]
    title = os.environ.get("POST_TITLE", "DOMOWY RESET — test publikacji")
    content = os.environ.get(
        "POST_CONTENT",
        "<p>Test publikacji przez Blogger API v3.</p>",
    )
    labels_raw = os.environ.get("POST_LABELS", "DOMOWY RESET")
    labels = [x.strip() for x in labels_raw.split(",") if x.strip()]
    is_draft = os.environ.get("PUBLISH_AS_DRAFT", "true").lower() == "true"

    result = create_post(
        blog_id=blog_id,
        title=title,
        content=content,
        labels=labels,
        is_draft=is_draft,
    )
    print(json.dumps({
        "id": result.get("id"),
        "url": result.get("url"),
        "status": "draft" if is_draft else "published",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
