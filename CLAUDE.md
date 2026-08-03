# CLAUDE.md — fathomm.org

Static site for **fathomm.org**. **No build step, no framework.** Every file is served as-is.

## Design system
Deep-navy / sky-blue minimalist theme, applied site-wide:
- Background `linear-gradient(135deg,#000a14,#001428)`; accent `#0ea5e9` (hover `#38bdf8`); text `#eaf2f8`, muted `#93a7b8`.
- Typeface: **Inter** everywhere (Google Fonts). Logotype: 🌊 + `Fathomm` wordmark.
- Nav (all pages): brand · **Ocean Voyages** (`/ocean`) · **Global Clinics** (`/atlas`) · **Join Waitlist** (CTA → `/#waitlist`). No other nav links.
- The atlas keeps its light-theme CSS but is repainted by a `DARK MINIMALIST RESKIN` override block at the end of its `<style>` (grade colors A–E kept; map uses CARTO `dark_all` tiles).

## Layout
- `index.html` — homepage: medical tourism around the world + the AI trip-setup business model + waitlist → `/`.
- `ocean/index.html` — Ocean Voyages: the original "Dive deeper" landing → `/ocean`.
- `atlas/index.html` — Global Clinics: the trust-scored atlas (full parallax page) → `/atlas`.

## Waitlist
`index.html` has a `#waitlist` form. Paste your form endpoint into the `WAITLIST_ENDPOINT`
constant in the page's `<script>` (Formspree / Tally / Google Form POST URL). Until it is set,
the form validates the email and shows a friendly message without sending anywhere.
- `embeds/fathomm-map.html` — embeddable map widget (iframe) → `/embeds/fathomm-map.html`.
- `data/clinics.json` / `clinics.csv` — clinic dataset (115 providers, 20 countries, trust-scored 0–100).
- `tools/build_data.py` — regenerates `data/clinics.{json,csv}` from source.
- `tools/inject.py` — injects `data/clinics.json` into the two HTML files (from `tools/*_template.html`).
- `CNAME` (`fathomm.org`), `.nojekyll` — GitHub Pages custom domain + path serving.

The atlas page and widget are **self-contained**: clinic data is inlined, no runtime fetch.

## Deploy
Push to `origin/main` (GitHub Pages serves it). Live URLs:
`https://fathomm.org/atlas` and `https://fathomm.org/embeds/fathomm-map.html`.

## Update clinic data
```
python3 tools/build_data.py    # rewrites data/clinics.json + .csv
python3 tools/inject.py        # rebuilds atlas/index.html + embeds/fathomm-map.html
```
Commit the regenerated `data/*` and both HTML files together.

## Conventions
- Keep it dependency-light: only Leaflet (cdnjs), Google Fonts, and CARTO tiles load at runtime.
- Trust Score = evidence 30 · accreditation 25 · transparency 15 · track record 15 · safety 15.
  It is a decision aid, not medical advice; keep experimental/discredited labels intact.
