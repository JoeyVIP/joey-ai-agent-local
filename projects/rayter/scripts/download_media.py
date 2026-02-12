#!/usr/bin/env python3
"""
Rayter.tw Media Downloader
Downloads all media files from rayter.tw using URLs from the REST API backup.
"""

import json
import os
import sys
import time
import hashlib
from urllib.parse import urlparse, unquote
import requests

BASE_URL = "https://rayter.tw"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rayter-backup")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")
MEDIA_DIR = os.path.join(OUTPUT_DIR, "wp-content", "uploads")

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": BASE_URL + "/",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
})


def load_media_urls():
    """Load media URLs from JSON backup."""
    filepath = os.path.join(JSON_DIR, "media_urls.json")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def url_to_filepath(url):
    """Convert a media URL to a local file path preserving WP upload structure."""
    parsed = urlparse(url)
    path = unquote(parsed.path)

    # Extract path after /wp-content/uploads/
    if "/wp-content/uploads/" in path:
        relative = path.split("/wp-content/uploads/")[1]
    else:
        # Fallback: use the filename
        relative = os.path.basename(path)

    return os.path.join(MEDIA_DIR, relative)


def download_file(url, filepath):
    """Download a single file with retry logic."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Skip if already downloaded
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return "skipped"

    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30, stream=True)
            if resp.status_code == 200:
                content_type = resp.headers.get("Content-Type", "")
                # Verify it's not an HTML error page
                if "text/html" in content_type and not url.endswith(".html") and not url.endswith(".svg"):
                    # Check first bytes
                    content = resp.content
                    if b"<!DOCTYPE" in content[:100] or b"<html" in content[:100]:
                        return "html_error"
                    with open(filepath, "wb") as f:
                        f.write(content)
                    return "ok"

                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return "ok"
            elif resp.status_code == 404:
                return "404"
            else:
                if attempt < 2:
                    time.sleep(1)
                    continue
                return f"error_{resp.status_code}"
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            return f"exception: {str(e)}"

    return "failed"


def main():
    media_items = load_media_urls()
    print(f"Total media items to download: {len(media_items)}")
    print(f"Output directory: {MEDIA_DIR}")
    print()

    stats = {"ok": 0, "skipped": 0, "404": 0, "html_error": 0, "error": 0}
    failed_items = []

    for i, item in enumerate(media_items, 1):
        url = item["url"]
        filepath = url_to_filepath(url)
        filename = os.path.basename(filepath)

        status = download_file(url, filepath)

        if status == "ok":
            stats["ok"] += 1
            size = os.path.getsize(filepath)
            print(f"  [{i}/{len(media_items)}] OK ({size:,} bytes) {filename}")
        elif status == "skipped":
            stats["skipped"] += 1
            print(f"  [{i}/{len(media_items)}] SKIP (exists) {filename}")
        elif status == "404":
            stats["404"] += 1
            print(f"  [{i}/{len(media_items)}] 404 {filename}")
            failed_items.append({"url": url, "status": "404"})
        elif status == "html_error":
            stats["html_error"] += 1
            print(f"  [{i}/{len(media_items)}] HTML_ERR {filename}")
            failed_items.append({"url": url, "status": "html_error"})
        else:
            stats["error"] += 1
            print(f"  [{i}/{len(media_items)}] {status} {filename}")
            failed_items.append({"url": url, "status": status})

        # Rate limit
        if status == "ok":
            time.sleep(0.1)

    # Summary
    print()
    print("=" * 60)
    print("Download Complete!")
    print("=" * 60)
    print(f"  Downloaded: {stats['ok']}")
    print(f"  Skipped (exists): {stats['skipped']}")
    print(f"  Not found (404): {stats['404']}")
    print(f"  HTML errors: {stats['html_error']}")
    print(f"  Other errors: {stats['error']}")
    print(f"  Total: {len(media_items)}")

    if failed_items:
        failed_path = os.path.join(JSON_DIR, "media_download_failures.json")
        with open(failed_path, "w", encoding="utf-8") as f:
            json.dump(failed_items, f, ensure_ascii=False, indent=2)
        print(f"\n  Failed items saved to: {failed_path}")


if __name__ == "__main__":
    main()
