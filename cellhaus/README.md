# CellHaus — website

A single self-contained static page for **CellHaus**, the cell & gene therapy
residency in Kobe, Japan (Haus Fund · Global Residency Node 02, launching
September 2026).

- **No build step, no framework.** Everything is inline in `index.html`
  (only Google Fonts loads at runtime).
- Content is drawn from the CellHaus program briefing and pitch deck, modelled
  on the public Mirai Tech City "apply" flow. Confidential fund financials
  (LP economics, portfolio metrics, SAFE carry) are intentionally **not**
  published here.

## Deploy to Netlify

**Option A — drag & drop:** upload the `cellhaus/` folder at
[app.netlify.com/drop](https://app.netlify.com/drop).

**Option B — connect the repo:** point Netlify at this repository. The root
`netlify.toml` sets `publish = "cellhaus"` and no build command, so Netlify
serves `cellhaus/index.html` as-is.

## Application form

The `#apply` section embeds the **Airtable application form**
(`airtable.com/app9STfjol4NHGEWj/pag6vvU75E9mWLH49/form`) via an iframe, with a
direct "Open the application form" link as a fallback. Submissions land in the
linked Airtable base — no Netlify Forms setup required. Replace
`hello@haus.fund` with the real inbox before going live.
