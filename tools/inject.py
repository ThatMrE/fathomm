#!/usr/bin/env python3
"""
Regenerate the deployable atlas page + embed widget from the templates and
the current clinic dataset. No build tooling required beyond Python 3.

Pipeline:
    python tools/build_data.py     # (re)creates data/clinics.{json,csv} from source
    python tools/inject.py         # injects data/clinics.json into the two HTML files

Run from the repository root.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "clinics.json")
PLACEHOLDER = "/*__CLINIC_DATA__*/"

TARGETS = [
    ("tools/atlas_template.html",  "atlas/index.html"),
    ("tools/widget_template.html", "embeds/fathomm-map.html"),
]

def main():
    if not os.path.exists(DATA):
        sys.exit("data/clinics.json not found — run `python tools/build_data.py` first.")
    data = open(DATA, encoding="utf-8").read()
    # sanity check the JSON parses before we inject it
    n = len(json.loads(data)["clinics"])
    for tpl_rel, out_rel in TARGETS:
        tpl_path = os.path.join(ROOT, tpl_rel)
        out_path = os.path.join(ROOT, out_rel)
        tpl = open(tpl_path, encoding="utf-8").read()
        if PLACEHOLDER not in tpl:
            sys.exit(f"placeholder {PLACEHOLDER} missing from {tpl_rel}")
        open(out_path, "w", encoding="utf-8").write(tpl.replace(PLACEHOLDER, data))
        print(f"wrote {out_rel:28s} ({n} clinics, {os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    main()
