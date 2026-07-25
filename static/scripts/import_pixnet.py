#!/usr/bin/env python3
"""Convert the read-only PIXNET backup into Hugo page bundles."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def clean_body(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and lines[0].startswith("- "):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines).strip() + "\n"


def description_from(body: str, limit: int = 115) -> str:
    plain = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
    plain = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", plain)
    plain = re.sub(r"[*_#>`~]", "", plain)
    plain = " ".join(plain.split())
    return plain[:limit].rstrip("，。,. ") + ("…" if len(plain) > limit else "")


def remove_first_image(body: str) -> str:
    """The first image is rendered as the page hero; avoid showing it twice."""
    return re.sub(r"(?m)^!\[[^\]]*\]\([^)]*\)\s*\n?", "", body, count=1).lstrip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", type=Path, default=Path("pixnet_backup"))
    parser.add_argument("--site", type=Path, default=Path("static"))
    args = parser.parse_args()
    source = args.backup / "articles"
    target = args.site / "content" / "posts"
    target.mkdir(parents=True, exist_ok=True)
    imported = 0
    copied_images = 0
    for article_dir in sorted(source.iterdir()):
        if not article_dir.is_dir():
            continue
        metadata = json.loads((article_dir / "metadata.json").read_text(encoding="utf-8"))
        body = clean_body((article_dir / "article.md").read_text(encoding="utf-8"))
        description = description_from(body)
        body = remove_first_image(body)
        bundle = target / str(metadata["id"])
        bundle.mkdir(exist_ok=True)
        images_source = article_dir / "images"
        images_target = bundle / "images"
        if images_target.exists():
            shutil.rmtree(images_target)
        if images_source.exists():
            shutil.copytree(images_source, images_target)
            copied_images += sum(1 for item in images_target.iterdir() if item.is_file())
        front_matter = "\n".join(
            [
                "---",
                f"title: {quoted(metadata['title'])}",
                f"date: {quoted(metadata['published'])}",
                f"slug: {quoted(str(metadata['id']))}",
                f"description: {quoted(description)}",
                f"pixnet_id: {quoted(str(metadata['id']))}",
                f"original_url: {quoted(metadata['url'])}",
                "draft: false",
                "---",
                "",
            ]
        )
        (bundle / "index.md").write_text(front_matter + body, encoding="utf-8")
        imported += 1
    print(f"Imported {imported} posts and {copied_images} images into {target}")


if __name__ == "__main__":
    main()
