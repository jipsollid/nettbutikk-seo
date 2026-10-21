#!/usr/bin/env python3
"""Server-side SEO probe for a Shopify (or any) storefront.

Fetches pages the way a non-JavaScript crawler does and reports what is
actually in the HTML. Standard library only.

    python3 audit.py https://example.com --discover
    python3 audit.py https://example.com --urls /,/collections/all,/products/foo
    python3 audit.py https://example.com --discover --money "mmHg;inch;Buy 1, get 1 FREE;30-day"

--money takes the strings that carry the sale. The probe reports, per page,
whether each string is in the rendered-by-server HTML, only inside a <script>
(i.e. invisible to AI crawlers), or absent entirely. That column is usually
where the real finding is.
"""
import argparse, json, re, sys, urllib.request, urllib.error
from html import unescape  # 'html' alone would collide with the page-HTML variable
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
TIMEOUT = 20


def get(url, method="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", "replace") if method == "GET" else ""
            return r.status, body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", url
    except Exception as e:
        return 0, f"ERROR {e}", url


def strip_code(html):
    """Remove script/style/svg/template so text analysis sees what a reader sees."""
    return re.sub(r"<(script|style|noscript|svg|template)[^>]*>.*?</\1>", "",
                  html, flags=re.S | re.I)


def discover(base):
    """Pull URLs out of the sitemap index, falling back to the front page."""
    urls, status, body, _ = [], *get(urljoin(base, "/sitemap.xml"))
    if status != 200:
        return [base]
    children = re.findall(r"<loc>([^<]+)</loc>", body)
    for child in children:
        child = child.replace("&amp;", "&")
        if "agentic" in child:
            continue
        s, b, _ = get(child)
        if s == 200:
            urls += [u.replace("&amp;", "&") for u in re.findall(r"<loc>([^<]+)</loc>", b)]
    return [base] + urls


def one(url, money):
    status, html, final = get(url)
    row = {"url": url, "status": status}
    if status != 200 or not html:
        return row
    head = html[: html.find("</head>")] if "</head>" in html else html
    body = strip_code(html[html.find("</head>"):])

    def grab(pat, src=head):
        m = re.search(pat, src, re.I | re.S)
        return m.group(1).strip() if m else None

    # Decode entities before measuring: a raw "&ndash;" is 7 characters of
    # source but 1 character of title, and that overstates every length by 6.
    title = unescape(re.sub(r"\s+", " ", grab(r"<title>(.*?)</title>") or "")).strip()
    desc = grab(r'<meta name="description" content="([^"]*)"')
    desc = unescape(desc) if desc else desc
    row["title"] = title
    row["title_len"] = len(title)
    row["meta"] = desc
    row["meta_len"] = len(desc or "")
    row["canonical"] = grab(r'<link rel="canonical" href="([^"]*)"')
    row["robots_meta"] = grab(r'<meta name="robots" content="([^"]*)"')
    row["og_image"] = grab(r'<meta property="og:image" content="([^"]*)"')
    row["redirected_to"] = final if final.rstrip("/") != url.rstrip("/") else None

    ld_types, ld_bad = [], 0
    for block in re.findall(r"<script[^>]+ld\+json[^>]*>(.*?)</script>", html, re.S):
        try:
            obj = json.loads(block)
        except Exception:
            ld_bad += 1
            continue
        for o in (obj if isinstance(obj, list) else [obj]):
            if isinstance(o, dict) and o.get("@type"):
                ld_types.append(o["@type"])
                if "aggregateRating" in json.dumps(o):
                    ar = re.search(r'"ratingValue"\s*:\s*([\d.]+).*?"reviewCount"\s*:\s*(\d+)',
                                   json.dumps(o), re.S)
                    if ar:
                        row["aggregate_rating"] = f"{ar.group(1)} / {ar.group(2)} reviews"
    row["jsonld_types"] = sorted(set(ld_types))
    row["jsonld_invalid"] = ld_bad

    h = [(m.group(1).upper(), re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(2))).strip())
         for m in re.finditer(r"<(h[1-3])[^>]*>(.*?)</\1>", body, re.S | re.I)]
    row["h1"] = [t for lvl, t in h if lvl == "H1" and t]
    row["h1_count_incl_empty"] = sum(1 for lvl, _ in h if lvl == "H1")

    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))
    row["words"] = len(text.split())

    imgs = re.findall(r"<img\s[^>]*>", body, re.I)
    row["images"] = len(imgs)
    row["images_no_alt"] = sum(1 for i in imgs
                               if "alt=" not in i.lower() or re.search(r'alt="\s*"', i, re.I))

    host = urlparse(url).netloc
    links = re.findall(r'<a\s[^>]*href="([^"]+)"', body)
    internal = [l for l in links if l.startswith("/") or host in l]
    row["links_products"] = len({l.split("?")[0] for l in internal if "/products/" in l})
    row["links_collections"] = len({l.split("?")[0] for l in internal if "/collections/" in l})
    row["links_external"] = len({l for l in links if l.startswith("http") and host not in l})
    row["facet_urls"] = len({l for l in internal if "filter." in l or "sort_by=" in l})

    # The important column: can a non-JS crawler see the facts that sell?
    if money:
        seen, scripted, missing = [], [], []
        scripts = " ".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S | re.I))
        for s in money:
            if s.lower() in body.lower():
                seen.append(s)
            elif s.lower() in scripts.lower():
                scripted.append(s)
            else:
                missing.append(s)
        row["money_visible"] = seen
        row["money_js_only"] = scripted
        row["money_absent"] = missing
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--urls", help="comma-separated paths or absolute URLs")
    ap.add_argument("--discover", action="store_true", help="read sitemap.xml")
    ap.add_argument("--money", default="",
                    help="strings that carry the sale, separated by ';' (or ',' if none present)")
    ap.add_argument("--json", help="write full results here")
    a = ap.parse_args()

    base = a.base.rstrip("/")
    sep = ";" if ";" in a.money else ","
    money = [m.strip() for m in a.money.split(sep) if m.strip()]
    if a.urls:
        urls = [u if u.startswith("http") else urljoin(base + "/", u.lstrip("/"))
                for u in a.urls.split(",")]
    elif a.discover:
        urls = discover(base)
    else:
        urls = [base]

    rows = [one(u, money) for u in urls]

    print(f"{len(rows)} URL-ar henta som Googlebot, utan JavaScript\n")
    print("| url | st | title | meta | h1 | ord | img/u.alt | JSON-LD | facett |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r.get("status") != 200:
            print(f"| {r['url']} | **{r['status']}** | | | | | | | |")
            continue
        path = urlparse(r["url"]).path or "/"
        print(f"| {path} | {r['status']} | {r['title_len']} | "
              f"{r['meta_len'] or '**0**'} | {r['h1_count_incl_empty']} | {r['words']} | "
              f"{r['images']}/{r['images_no_alt']} | {','.join(r['jsonld_types']) or '—'} | "
              f"{r['facet_urls']} |")

    flags = []
    for r in rows:
        if r.get("status") != 200:
            continue
        p = urlparse(r["url"]).path or "/"
        if not r.get("meta"):
            flags.append(f"{p}: inga meta description")
        if r.get("title_len", 0) > 60:
            flags.append(f"{p}: tittel {r['title_len']} teikn – blir kutta")
        if r.get("images_no_alt"):
            flags.append(f"{p}: {r['images_no_alt']} bilete utan alt")
        if r.get("jsonld_invalid"):
            flags.append(f"{p}: {r['jsonld_invalid']} ugyldige JSON-LD-blokker")
        if r.get("aggregate_rating"):
            flags.append(f"{p}: AggregateRating {r['aggregate_rating']} – sjekk kvar tala kjem frå")
        if r.get("facet_urls"):
            flags.append(f"{p}: {r['facet_urls']} facett-URL-ar i HTML – crawl-felle")
        if r.get("money_js_only"):
            flags.append(f"{p}: **berre i JavaScript**: {', '.join(r['money_js_only'])}")
        if r.get("money_absent"):
            flags.append(f"{p}: finst ikkje: {', '.join(r['money_absent'])}")
    print("\n## Flagg\n")
    print("\n".join(f"- {f}" for f in flags) or "- ingen")

    if a.json:
        with open(a.json, "w") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)
        print(f"\nFulle data: {a.json}")


if __name__ == "__main__":
    main()
