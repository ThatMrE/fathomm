#!/usr/bin/env python3
"""Inline data/directory.json into atlas/index.html's #directory section
(between the FULL DIRECTORY markers), using tools/directory_template.html.
Idempotent. Run after tools/build_directory.py.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = json.load(open(f"{ROOT}/data/directory.json"))
KEYS = ['name','city','country','region','specialty','website','accreditation','status','trust_score','tier','lat','lng','defunct']
trimmed = [{k: c.get(k) for k in KEYS} for c in data]
for c in trimmed:
    if not c.get('defunct'): c.pop('defunct', None)
    if c.get('trust_score') is None: c.pop('trust_score', None)
    if c.get('tier') is None: c.pop('tier', None)
    if not c.get('accreditation'): c.pop('accreditation', None)
    if not c.get('website'): c.pop('website', None)
    if c.get('lat') is None: c.pop('lat', None)
    if c.get('lng') is None: c.pop('lng', None)
blob = json.dumps(trimmed, ensure_ascii=False, separators=(',',':'))

section = open(f"{ROOT}/tools/directory_template.html", encoding='utf-8').read().replace('__DIR_DATA__', blob)

atlas_path = f"{ROOT}/atlas/index.html"
html = open(atlas_path, encoding='utf-8').read()
START = '<!-- ===================== FULL DIRECTORY'
END = '<!-- =================== END FULL DIRECTORY =================== -->'
if START in html and END in html:
    html = html[:html.index(START)] + section + html[html.index(END)+len(END):]
    mode = 'replaced'
else:
    idx = html.find('<footer')
    if idx == -1: sys.exit('ERROR: no <footer> in atlas')
    html = html[:idx] + section + '\n\n' + html[idx:]
    mode = 'inserted'
open(atlas_path, 'w', encoding='utf-8').write(html)
print(f"{mode}; entries={len(trimmed)}; blob_bytes={len(blob)}")
