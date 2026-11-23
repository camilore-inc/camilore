# Changelog

The camilore.com website has no version number. Entries are dated.

## 2026-11-23 — Search engines notified on every push

- Google Search Console and Bing Webmaster Tools set up (owner contact@camilore.com, verified through the
  camilore.com domain, sitemap submitted).
- IndexNow: after each push to `main`, a GitHub Actions workflow waits for the
  Pages deploy and sends the changed sitemap pages to Bing and the other
  IndexNow engines (`scripts/indexnow.py`, key file at the root).

## 2026-11-22 — Real English and Spanish pages; search and sharing metadata

- **Every language has its own address:** French at `/` and `/privacy.html`,
  English at `/en/`, Spanish at `/es/`. The text is in the HTML, so search
  engines index all three languages (before, only French was indexed and the
  other languages existed only after JavaScript ran). The FR/EN/ES switcher is
  made of real links; a visitor's choice is remembered, and there is no
  automatic browser-language switch.
- **Built by `python3 scripts/build_pages.py`** from the French root pages
  (the templates) and the text in `scripts/content/home.json` and
  `privacy.json`. Edit those, then run the script; it also writes
  `sitemap.xml`, `robots.txt` and the redirects, and checks the result.
- **Search and sharing:** clearer titles and descriptions in each language,
  hreflang links between languages, `sitemap.xml` and `robots.txt`, a
  1200×630 sharing image (`assets/images/brand/camilore-og-1200x630.png`, from
  `scripts/og-card.html`), and Schema.org Organization data (Camilore Inc.,
  Québec, contact, Jax Max Delta as its brand) with the same identifier that
  jaxmaxdelta.com now uses for its publisher.
- **Duplicates removed:** `index_light.html` and `privacy_light.html` were exact
  copies of the pages; they now redirect to them (`noindex`), and nothing links
  to them.
- Fixes: the French "À propos" text in the HTML matched the current wording
  only after JavaScript ran (it still mentioned personal finance); the English
  vision quote opened with a closing quote mark; accessibility labels are now
  translated.

## 2026-11-09 — old JMD privacy page removed; JMD card uses the master icon and headline

- `jaxmaxdelta/privacy.html` is deleted. The approved Jax Max Delta Privacy
  Policy is only at jaxmaxdelta.com/{en,fr,es}/privacy.html; the old address
  now returns 404 instead of redirecting.
- Home (`index.html`, `index_light.html`): the Jax Max Delta card shows the app's
  1024 px master icon and the site's headline, "Your Race Engineer. Your Pit
  Wall. Your Race Memory." (FR/ES equivalents), replacing "Your Pit Wall. In
  Your Hand. / Your Race Engineer. In Your Ear."

## 2026-11 — JMD subsite redirected to jaxmaxdelta.com; JMD wording aligned with app 1.29.0; JMD privacy and support routed to jaxmaxdelta.com.

- `jaxmaxdelta/index.html`, `support.html` and `privacy.html` are now redirect
  pages (meta refresh, canonical link, `noindex`, visible fallback link) to
  `https://jaxmaxdelta.com/{en|fr|es}/`, `…/support.html` and `…/privacy.html`.
  The visitor's saved site language is kept; English otherwise.
- Home (`index.html`, `index_light.html`): Jax Max Delta card uses the approved
  wording ("Your Pit Wall. In Your Hand. / Your Race Engineer. In Your Ear."),
  is presented as a Camilore Inc. product, links to jaxmaxdelta.com and routes
  JMD support to support@jaxmaxdelta.com. EN/FR/ES.
- Corporate privacy policy (`privacy.html`, `privacy_light.html`): scoped to the
  corporate website; section 3 now points to the Jax Max Delta Privacy Policy on
  jaxmaxdelta.com and to support@jaxmaxdelta.com. Last updated 2026-11-09.
- Legal name "Camilore Inc." in titles and copyright lines; canonical and Open
  Graph metadata added.
- Fixed a JavaScript syntax error (curly quotes used as string delimiters in the
  French translations) that stopped the language switcher on the home and
  privacy pages.
