#!/usr/bin/env python3
"""Build camilore.com's French, English and Spanish pages as real, separate URLs.

Each page exists once per language, with its text already in the HTML:

    /                    /en/                    /es/
    /privacy.html        /en/privacy.html        /es/privacy.html

Search engines index every language (one URL per language, linked with
hreflang), and nothing depends on JavaScript. The French pages at the root are
also the templates: elements carry data-i18n / data-i18n-aria keys, and the text
for each language lives in scripts/content/<page>.json. Edit the JSON (or the
markup of the root page), then run:

    python3 scripts/build_pages.py

It rewrites all six pages, sitemap.xml and the duplicate-page redirects, then
checks the result. Standard library only.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://camilore.com"
LANGS = ("fr", "en", "es")
LOCALES = {"fr": "fr_CA", "en": "en_CA", "es": "es_ES"}
PAGES = {"home": "index.html", "privacy": "privacy.html"}
ORG_ID = f"{BASE}/#organization"
JMD = "https://jaxmaxdelta.com"


def path_of(page: str, lang: str) -> str:
    """Public path of a page in a language ('/', '/en/privacy.html', ...)."""
    prefix = "/" if lang == "fr" else f"/{lang}/"
    return prefix if page == "home" else f"{prefix}{PAGES[page]}"


def file_of(page: str, lang: str) -> Path:
    folder = ROOT if lang == "fr" else ROOT / lang
    return folder / PAGES[page]


def attr(value: str) -> str:
    return html.escape(value, quote=True)


def head(page: str, lang: str, meta: dict) -> str:
    url = BASE + path_of(page, lang)
    title, desc = attr(meta["title"]), attr(meta["description"])
    lines = [
        f"<title>{title}</title>",
        f'<meta name="description" content="{desc}" />',
        f'<link rel="canonical" href="{url}" />',
        *(f'<link rel="alternate" hreflang="{code}" href="{BASE}{path_of(page, code)}" />' for code in LANGS),
        f'<link rel="alternate" hreflang="x-default" href="{BASE}{path_of(page, "fr")}" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="Camilore Inc." />',
        f'<meta property="og:locale" content="{LOCALES[lang]}" />',
        *(f'<meta property="og:locale:alternate" content="{LOCALES[code]}" />' for code in LANGS if code != lang),
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:title" content="{title}" />',
        f'<meta property="og:description" content="{desc}" />',
        f'<meta property="og:image" content="{BASE}/assets/images/brand/camilore-og-1200x630.png" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        '<meta property="og:image:alt" content="Camilore Inc." />',
        '<meta name="twitter:card" content="summary_large_image" />',
    ]
    if page == "home":
        lines.append(f'<script type="application/ld+json">{json.dumps(organization(lang, meta), ensure_ascii=False)}</script>')
    return "<!-- seo:start -->\n  " + "\n  ".join(lines) + "\n  <!-- seo:end -->"


def organization(lang: str, meta: dict) -> dict:
    """Schema.org Organization; the same @id is the publisher on jaxmaxdelta.com."""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": ORG_ID,
        "name": "Camilore",
        "legalName": "Camilore Inc.",
        "url": f"{BASE}/",
        "logo": f"{BASE}/apple-touch-icon.png",
        "description": meta["description"],
        "email": "contact@camilore.com",
        "address": {"@type": "PostalAddress", "addressRegion": "QC", "addressCountry": "CA"},
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "customer support", "email": "contact@camilore.com",
             "availableLanguage": ["French", "English", "Spanish"]},
        ],
        "brand": {"@type": "Brand", "name": "Jax Max Delta", "url": f"{JMD}/{lang}/"},
        "inLanguage": lang,
    }


PREFS = """<!-- prefs:start -->
  <script>
    // Remember the language a visitor picks. Only an explicit earlier choice
    // moves a visitor off the French root; there is no browser-language
    // redirect, so every language URL serves exactly the language it promises.
    (function () {
      var links = document.querySelectorAll('[data-lang-link]');
      links.forEach(function (a) { a.addEventListener('click', function () {
        try { localStorage.setItem('camilore-lang', a.getAttribute('data-lang-link')); } catch (e) {}
      }); });
      var here = document.documentElement.lang, saved = '';
      try { saved = localStorage.getItem('camilore-lang') || ''; } catch (e) {}
      if (here === 'fr' && (saved === 'en' || saved === 'es') && !/[?&]lang=fr\\b/.test(location.search)) {
        var target = document.querySelector('[data-lang-link="' + saved + '"]');
        if (target) location.replace(target.getAttribute('href') + location.hash);
      }
    })();
  </script>
  <!-- prefs:end -->"""


def render(template: str, page: str, lang: str, content: dict) -> str:
    text, aria, meta = content["text"], content["aria"], content["meta"]
    out = re.sub(r'<html lang="\w+"', f'<html lang="{lang}"', template, count=1)
    out = re.sub(r"<!-- seo:start -->[\s\S]*?<!-- seo:end -->", lambda _: head(page, lang, meta), out, count=1)
    out = re.sub(r"<!-- prefs:start -->[\s\S]*?<!-- prefs:end -->", lambda _: PREFS, out, count=1)

    def fill(match: re.Match) -> str:
        tag, before, key, after = match.groups()
        if key not in text:
            raise SystemExit(f"{page}/{lang}: no text for data-i18n={key!r}")
        return f'<{tag}{before}data-i18n="{key}"{after}>{text[key]}</{tag}>'

    out = re.sub(r'<(\w+)([^>]*?)data-i18n="(\w+)"([^>]*)>[\s\S]*?</\1>', fill, out)

    def label(match: re.Match) -> str:
        key = match.group(1)
        if key not in aria:
            raise SystemExit(f"{page}/{lang}: no label for data-i18n-aria={key!r}")
        return f'data-i18n-aria="{key}" aria-label="{attr(aria[key])}"'

    out = re.sub(r'data-i18n-aria="(\w+)"(?: aria-label="[^"]*")?', label, out)
    out = re.sub(r'data-href="(\w+)" href="[^"]*"', lambda m: f'data-href="{m[1]}" href="{path_of(m[1], lang)}"', out)
    out = re.sub(r'href="[^"]*" data-jmd-path=""', f'href="{JMD}/{lang}/" data-jmd-path=""', out)

    def switch(match: re.Match) -> str:
        code = match.group(1)
        # The French link says ?lang=fr so it wins over a saved English/Spanish choice.
        href = path_of(page, code) + ("?lang=fr" if code == "fr" else "")
        current = ' aria-current="page"' if code == lang else ""
        cls = "lang-btn active" if code == lang else "lang-btn"
        return f'<a class="{cls}" data-lang-link="{code}" hreflang="{code}" lang="{code}" href="{href}"{current}>'

    return re.sub(r'<a class="lang-btn[^"]*" data-lang-link="(\w+)"[^>]*>', switch, out)


REDIRECT = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Camilore Inc.</title>
  <meta name="robots" content="noindex, follow" />
  <meta http-equiv="refresh" content="0; url={target}" />
  <link rel="canonical" href="{BASE}{target}" />
  <script>window.location.replace('{target}' + window.location.hash);</script>
</head>
<body>
  <p><a href="{target}">Camilore Inc.</a></p>
</body>
</html>
"""


def sitemap() -> str:
    urls = []
    for page in PAGES:
        alts = "\n".join(
            f'    <xhtml:link rel="alternate" hreflang="{code}" href="{BASE}{path_of(page, code)}"/>' for code in LANGS
        ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{path_of(page, "fr")}"/>'
        urls += [f"  <url>\n    <loc>{BASE}{path_of(page, lang)}</loc>\n{alts}\n  </url>" for lang in LANGS]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def check() -> None:
    problems = []
    for page in PAGES:
        for lang in LANGS:
            source = file_of(page, lang).read_text(encoding="utf-8")
            label = file_of(page, lang).relative_to(ROOT)
            if f'<html lang="{lang}"' not in source:
                problems.append(f"{label}: wrong html lang")
            if len(re.findall(r"<h1\b", source)) != 1:
                problems.append(f"{label}: needs exactly one <h1>")
            if f'<link rel="canonical" href="{BASE}{path_of(page, lang)}" />' not in source:
                problems.append(f"{label}: wrong canonical")
            if re.search(r'aria-label="[^"]*"', source) is None or "_light" in source or "<button" in source:
                problems.append(f"{label}: labels, duplicate links or JS-only language buttons remain")
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source):
                json.loads(block)
            for target in re.findall(r'(?:href|src)="(/[^"#?]*)', source):
                local = ROOT / target.lstrip("/")
                if not (local.is_file() or (local / "index.html").is_file()):
                    problems.append(f"{label}: missing local target {target}")
    if problems:
        raise SystemExit("Build check failed:\n- " + "\n- ".join(problems))


def main() -> None:
    for page, name in PAGES.items():
        template = (ROOT / name).read_text(encoding="utf-8")
        content = json.loads((ROOT / "scripts" / "content" / f"{page}.json").read_text(encoding="utf-8"))
        for lang in LANGS:
            target = file_of(page, lang)
            target.parent.mkdir(exist_ok=True)
            target.write_text(render(template, page, lang, content[lang]), encoding="utf-8")
    # The old *_light.html copies duplicated the pages; they now point to them.
    for old, page in (("index_light.html", "home"), ("privacy_light.html", "privacy")):
        target = path_of(page, "fr")
        (ROOT / old).write_text(REDIRECT.format(target=target, BASE=BASE), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    check()
    print(f"Built {len(PAGES) * len(LANGS)} pages, sitemap.xml, robots.txt and 2 redirects; checks passed.")


if __name__ == "__main__":
    main()
