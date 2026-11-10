# Changelog

The camilore.com website has no version number. Entries are dated.

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
