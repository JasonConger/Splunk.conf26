#!/usr/bin/env python3
"""Check a Dashboard Studio definition before deploying it.

Accepts a .json definition or a .xml view with the JSON in <definition>.
Exits non-zero on errors; prints warnings for likely mistakes.

    python3 check_definition.py dashboards/platform_health.xml
"""
import json
import re
import sys

# Option names Studio silently ignores, with the name that works.
WRONG_OPTIONS = {
    "trendDisplayMode": "trendDisplay",
    "legendPlacement": "legendDisplay",
    "xAxisTitle": "xAxisTitleText",
    "yAxisTitle": "yAxisTitleText",
    "colors": "seriesColors",
}


def load(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".xml"):
        if not re.search(r'<dashboard[^>]*\bversion="2"', text):
            return None, ['<dashboard> is missing version="2" — Splunk will treat it as Simple XML']
        m = re.search(r"<!\[CDATA\[(.*)\]\]>", text, re.S)
        if not m:
            return None, ["no <definition><![CDATA[...]]> block found"]
        label = re.search(r"<label>(.*?)</label>", text, re.S)
        text = m.group(1)
        errors = []
        try:
            d = json.loads(text)
        except json.JSONDecodeError as e:
            return None, [f"definition is not valid JSON: {e}"]
        if label and d.get("title") and label.group(1).strip() != d["title"]:
            errors.append(f'<label> "{label.group(1).strip()}" differs from JSON title "{d["title"]}"')
        return d, errors
    try:
        return json.loads(text), []
    except json.JSONDecodeError as e:
        return None, [f"not valid JSON: {e}"]


def check(d):
    errors, warnings = [], []
    ds = d.get("dataSources", {})
    viz = d.get("visualizations", {})
    layout = d.get("layout", {})
    placed = {s.get("item") for s in layout.get("structure", [])}

    for vid, v in viz.items():
        vtype = v.get("type", "")
        if not vtype.startswith("splunk."):
            errors.append(f"{vid}: type '{vtype}' — use splunk.* types")
        for role, ref in (v.get("dataSources") or {}).items():
            if ref not in ds:
                errors.append(f"{vid}: dataSources.{role} -> '{ref}' does not exist")
        for opt in (v.get("options") or {}):
            if opt in WRONG_OPTIONS:
                errors.append(f"{vid}: option '{opt}' is ignored — use '{WRONG_OPTIONS[opt]}'")
            if opt.startswith("y2"):
                warnings.append(f"{vid}: '{opt}' — dual axes; consider two panels")
        if vid not in placed and vid not in layout.get("globalInputs", []):
            errors.append(f"{vid}: not in layout.structure — it will never render")
        if vtype == "splunk.table":
            warnings.append(f"{vid}: table — is a chart clearer?")

    for item in placed:
        if item not in viz and item not in d.get("inputs", {}):
            errors.append(f"layout.structure references '{item}', which does not exist")

    used = {ref for v in viz.values() for ref in (v.get("dataSources") or {}).values()}
    used |= {s.get("options", {}).get("extend") for s in ds.values()}
    for sid, s in ds.items():
        if sid not in used:
            warnings.append(f"{sid}: data source is never used")
        if s.get("type") == "ds.search" and not s.get("options", {}).get("query", "").strip():
            errors.append(f"{sid}: empty query")

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d, errors = load(sys.argv[1])
    warnings = []
    if d is not None:
        e, warnings = check(d)
        errors += e
    for w in warnings:
        print(f"WARN   {w}")
    for e in errors:
        print(f"ERROR  {e}")
    if not errors:
        n = len(d.get("visualizations", {}))
        print(f"OK     {n} panels, {len(d.get('dataSources', {}))} data sources")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
