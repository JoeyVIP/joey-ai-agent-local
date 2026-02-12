#!/usr/bin/env python3
"""
Rayter.tw WordPress REST API Content Extractor
Extracts all public content (pages, posts, products, categories, media) via REST API.
No authentication needed for public content.
"""

import json
import os
import sys
import time
import requests
from urllib.parse import urlparse, urljoin

BASE_URL = "https://rayter.tw"
WP_API = f"{BASE_URL}/wp-json/wp/v2"
WC_API = f"{BASE_URL}/wp-json/wc/store/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rayter-backup")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")
ELEMENTOR_DIR = os.path.join(OUTPUT_DIR, "elementor")

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": BASE_URL,
})


def fetch_all_pages(endpoint, params=None):
    """Fetch all pages from a paginated WP REST API endpoint."""
    if params is None:
        params = {}
    params["per_page"] = 100
    params["page"] = 1

    all_items = []
    while True:
        print(f"  Fetching {endpoint} page {params['page']}...")
        resp = SESSION.get(f"{WP_API}/{endpoint}", params=params, timeout=30)
        if resp.status_code == 400:
            # No more pages
            break
        resp.raise_for_status()
        items = resp.json()
        if not items:
            break
        all_items.extend(items)
        # Check if there are more pages
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if params["page"] >= total_pages:
            break
        params["page"] += 1
        time.sleep(0.3)

    return all_items


def fetch_wc_products():
    """Fetch WooCommerce products via Store API (public, no auth needed)."""
    all_products = []
    page = 1
    while True:
        print(f"  Fetching WC products page {page}...")
        resp = SESSION.get(f"{WC_API}/products", params={"per_page": 100, "page": page}, timeout=30)
        if resp.status_code != 200:
            print(f"  WC Store API returned {resp.status_code}, trying wp/v2/product...")
            break
        items = resp.json()
        if not items:
            break
        all_products.extend(items)
        page += 1
        time.sleep(0.3)
    return all_products


def fetch_wc_products_v2():
    """Fetch WooCommerce products via WP REST API (public posts)."""
    # WooCommerce products are custom post type 'product'
    all_products = []
    page = 1
    while True:
        print(f"  Fetching products (wp/v2) page {page}...")
        resp = SESSION.get(f"{WP_API}/product", params={"per_page": 100, "page": page, "status": "publish"}, timeout=30)
        if resp.status_code == 404:
            print("  product endpoint not found, trying 'products'...")
            resp = SESSION.get(f"{WP_API}/products", params={"per_page": 100, "page": page, "status": "publish"}, timeout=30)
        if resp.status_code != 200:
            print(f"  Products endpoint returned {resp.status_code}")
            break
        items = resp.json()
        if not items:
            break
        all_products.extend(items)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.3)
    return all_products


def fetch_wc_categories():
    """Fetch WooCommerce product categories."""
    # Try Store API first
    resp = SESSION.get(f"{WC_API}/products/categories", params={"per_page": 100}, timeout=30)
    if resp.status_code == 200:
        return resp.json()

    # Fallback to product_cat taxonomy
    resp = SESSION.get(f"{WP_API}/product_cat", params={"per_page": 100}, timeout=30)
    if resp.status_code == 200:
        return resp.json()

    print("  Could not fetch product categories")
    return []


def fetch_menus():
    """Fetch WordPress menus."""
    # Try menu endpoints
    menus = []
    for endpoint in ["menus", "menu-items", "navigation"]:
        resp = SESSION.get(f"{WP_API}/{endpoint}", params={"per_page": 100}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            menus.append({"endpoint": endpoint, "data": data})
            print(f"  Found menu data at {endpoint}: {len(data)} items")

    # Also try the menu-locations endpoint
    resp = SESSION.get(f"{BASE_URL}/wp-json/wp-api-menus/v2/menus", timeout=30)
    if resp.status_code == 200:
        menus.append({"endpoint": "wp-api-menus", "data": resp.json()})

    return menus


def fetch_site_settings():
    """Fetch general site settings."""
    settings = {}

    # Basic site info
    resp = SESSION.get(f"{BASE_URL}/wp-json", timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        settings["site_info"] = {
            "name": data.get("name"),
            "description": data.get("description"),
            "url": data.get("url"),
            "home": data.get("home"),
            "namespaces": data.get("namespaces"),
        }

    # Available post types
    resp = SESSION.get(f"{WP_API}/types", timeout=30)
    if resp.status_code == 200:
        settings["post_types"] = resp.json()

    # Available taxonomies
    resp = SESSION.get(f"{WP_API}/taxonomies", timeout=30)
    if resp.status_code == 200:
        settings["taxonomies"] = resp.json()

    return settings


def save_json(data, filename):
    """Save data as JSON file."""
    filepath = os.path.join(JSON_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {filepath} ({len(data) if isinstance(data, list) else 'object'})")


def extract_media_urls(media_items):
    """Extract download URLs from media items."""
    urls = []
    for item in media_items:
        source_url = item.get("source_url") or item.get("guid", {}).get("rendered")
        if source_url:
            urls.append({
                "id": item.get("id"),
                "url": source_url,
                "title": item.get("title", {}).get("rendered", ""),
                "mime_type": item.get("mime_type", ""),
                "alt_text": item.get("alt_text", ""),
            })
    return urls


def main():
    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(ELEMENTOR_DIR, exist_ok=True)

    print("=" * 60)
    print("Rayter.tw REST API Content Extraction")
    print("=" * 60)

    # 1. Site settings
    print("\n[1/8] Fetching site settings...")
    settings = fetch_site_settings()
    save_json(settings, "settings.json")

    # 2. Pages
    print("\n[2/8] Fetching pages...")
    pages = fetch_all_pages("pages")
    save_json(pages, "pages.json")
    print(f"  Total pages: {len(pages)}")

    # 3. Posts
    print("\n[3/8] Fetching posts...")
    posts = fetch_all_pages("posts")
    save_json(posts, "posts.json")
    print(f"  Total posts: {len(posts)}")

    # 4. Products (WooCommerce)
    print("\n[4/8] Fetching products...")
    products = fetch_wc_products()
    if not products:
        products = fetch_wc_products_v2()
    save_json(products, "products.json")
    print(f"  Total products: {len(products)}")

    # 5. Product categories
    print("\n[5/8] Fetching product categories...")
    categories = fetch_wc_categories()
    save_json(categories, "product_categories.json")
    print(f"  Total categories: {len(categories)}")

    # 6. Media
    print("\n[6/8] Fetching media...")
    media = fetch_all_pages("media")
    save_json(media, "media.json")
    media_urls = extract_media_urls(media)
    save_json(media_urls, "media_urls.json")
    print(f"  Total media items: {len(media)}")

    # 7. Menus
    print("\n[7/8] Fetching menus...")
    menus = fetch_menus()
    save_json(menus, "menus.json")

    # 8. Categories and Tags
    print("\n[8/8] Fetching categories and tags...")
    categories_wp = fetch_all_pages("categories")
    tags = fetch_all_pages("tags")
    save_json(categories_wp, "categories.json")
    save_json(tags, "tags.json")

    # Summary
    print("\n" + "=" * 60)
    print("Extraction Complete!")
    print("=" * 60)
    print(f"  Pages: {len(pages)}")
    print(f"  Posts: {len(posts)}")
    print(f"  Products: {len(products)}")
    print(f"  Media: {len(media)}")
    print(f"  Output: {JSON_DIR}")


if __name__ == "__main__":
    main()
