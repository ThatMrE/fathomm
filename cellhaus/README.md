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

The `#apply` form uses **Netlify Forms** (`data-netlify="true"`, form name
`apply`). Submissions appear in the Netlify dashboard under *Forms* with no
extra setup. JavaScript shows an inline success panel; if JS is disabled the
native POST still works. Replace `hello@haus.fund` with the real inbox before
going live.
