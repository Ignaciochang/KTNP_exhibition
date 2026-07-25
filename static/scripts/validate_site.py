#!/usr/bin/env python3
"""Validate the generated Hugo site without external network access."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "public"
    html_files = list(root.rglob("*.html"))
    home = BeautifulSoup((root / "index.html").read_text(encoding="utf-8"), "html.parser")
    canonical = home.select_one('link[rel="canonical"]')
    base_path = urlparse(canonical["href"]).path if canonical else "/"
    broken: list[tuple[str, str]] = []
    external_runtime: list[tuple[str, str]] = []
    responsive_images = 0
    for page in html_files:
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for tag, attribute in (
            ("a", "href"),
            ("img", "src"),
            ("script", "src"),
            ("link", "href"),
        ):
            for node in soup.find_all(tag):
                value = node.get(attribute, "")
                if not value or value.startswith(("#", "mailto:", "tel:", "data:")):
                    continue
                if value.startswith(("http://", "https://")):
                    is_runtime = tag in ("script", "img") or (
                        tag == "link" and "stylesheet" in node.get("rel", [])
                    )
                    if is_runtime:
                        external_runtime.append((str(page.relative_to(root)), value))
                    continue
                clean = value.split("#", 1)[0].split("?", 1)[0]
                if clean.startswith(base_path):
                    clean = clean[len(base_path) :]
                target = root / clean.lstrip("/") if value.startswith("/") else page.parent / clean
                if clean.endswith("/") or not target.suffix:
                    target /= "index.html"
                if not target.exists():
                    broken.append((str(page.relative_to(root)), value))
        responsive_images += len(soup.select('img[srcset][loading="lazy"]'))

    search = json.loads((root / "index.json").read_text(encoding="utf-8"))
    posts = list((root / "posts").glob("*/index.html"))
    required = {
        name: (root / name).exists()
        for name in ("index.xml", "sitemap.xml", "robots.txt", "404.html", "index.json")
    }
    report = {
        "html_pages": len(html_files),
        "post_pages": len(posts),
        "search_records": len(search),
        "responsive_lazy_images": responsive_images,
        "broken_internal_refs": len(broken),
        "external_runtime_assets": len(external_runtime),
        **required,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if len(posts) != 31 or len(search) != 31 or broken or external_runtime or not all(required.values()):
        if broken:
            print("Broken references:", broken[:20])
        if external_runtime:
            print("External runtime assets:", external_runtime[:20])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
