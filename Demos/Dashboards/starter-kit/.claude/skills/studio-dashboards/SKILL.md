---
name: studio-dashboards
description: Author Splunk Dashboard Studio dashboards — the version 2 JSON definition (dataSources, visualizations, layout) inside a <dashboard version="2"> XML file. Use when asked to build, create, convert to, or fix a "Dashboard Studio" dashboard, "dashboard JSON", a splunk.singlevalue / splunk.line / splunk.column panel, or to turn analysis findings into a Splunk dashboard.
---

# Dashboard Studio dashboards

A starter skill. Extend it with every mistake you see an agent make — that is
what a skill is for.

## Workflow

1. **Validate searches first.** Run every panel search through the Splunk MCP
   server with the dashboard's time range. Report row count and runtime. Fix
   anything that returns 0 rows or runs longer than ~10s before writing JSON.
2. **Write the definition** to a file, following the rules below.
3. **Check it:** `python3 .claude/skills/studio-dashboards/scripts/check_definition.py <file>`
4. **Show the panel list and stop.** Deploy only when the user says so.

## File format

A dashboard stored in an app (`default/data/ui/views/<name>.xml`) or sent over
REST (`eai:data`) is a version 2 XML wrapper around the JSON:

```xml
<dashboard version="2" theme="light">
  <label>Platform health</label>
  <description>One line on what the dashboard answers.</description>
  <definition><![CDATA[
{ "title": "Platform health", "dataSources": {}, "visualizations": {}, "layout": {} }
  ]]></definition>
</dashboard>
```

`version="2"` is what makes it Studio. Without it Splunk treats the file as
Simple XML. Keep `<label>` and the JSON `title` identical.

## Definition skeleton

```json
{
  "title": "…",
  "description": "…",
  "inputs": {},
  "defaults": {},
  "dataSources": {
    "ds_errors": {
      "type": "ds.search",
      "name": "Errors",
      "options": {
        "query": "index=_internal log_level=ERROR | stats count",
        "queryParameters": { "earliest": "-24h", "latest": "now" }
      }
    }
  },
  "visualizations": {
    "viz_errors": {
      "type": "splunk.singlevalue",
      "title": "Errors, last 24h",
      "dataSources": { "primary": "ds_errors" },
      "options": { "unit": "", "trendDisplay": "off", "sparklineDisplay": "off" }
    }
  },
  "layout": {
    "type": "absolute",
    "options": { "width": 1440, "height": 900, "display": "auto" },
    "structure": [
      { "item": "viz_errors", "type": "block", "position": { "x": 20, "y": 20, "w": 340, "h": 160 } }
    ],
    "globalInputs": []
  }
}
```

- IDs are free-form but unique. Use descriptive ones: `ds_errors`, `viz_errors_by_hour`.
- Every `layout.structure[].item` must exist in `visualizations`; every
  `dataSources.primary` must exist in `dataSources`.
- **Historical analysis: absolute times** (`"2026-01-01T00:00:00"`). Live
  monitoring: relative (`"-24h"`, `"now"`).
- Several panels over the same base search: one `ds.search` plus `ds.chain`
  sources (`"extend": "ds_base"`, `"query": "| stats …"`) — one search job
  instead of many.

## Visualization types and options

Use `splunk.*` types. The legacy `viz.*` names are wrong.

| Type | Use for | Options worth knowing |
|---|---|---|
| `splunk.singlevalue` | One headline number | `unit`, `unitPosition` (`before`/`after`), `underLabel`, `numberPrecision`, `majorFontSize`, `majorColor`, `trendDisplay` (`percent`/`absolute`/`off`), `sparklineDisplay` (`off`/`before`/`after`) |
| `splunk.line` | Change over time or an ordered axis | `xAxisTitleText`, `yAxisTitleText`, `legendDisplay` (`right`/`left`/`top`/`bottom`/`off`), `seriesColors`, `seriesColorsByField`, `nullValueDisplay` (`gaps`/`zero`/`connect`), `lineWidth`, `markerDisplay` |
| `splunk.column` | Comparing categories or buckets | Axis and legend options as above, `stackMode` (`auto`/`stacked`/`stacked100`), `dataValuesDisplay` (`off`/`all`/`minmax`) |
| `splunk.bar` | Ranked categories with long labels | As column. `xAxisLabelRotation` is not supported. |
| `splunk.markdown` | Titles, context, the "so what" | `markdown` (required), `fontSize` (`extraSmall`…`extraLarge`), `fontColor`, `backgroundColor` |
| `splunk.table` | Only when the reader needs exact values | Keep it short — `count` |

Colours: `seriesColorsByField` (`{"ERROR":"#C2323C"}`) keeps a series the same
colour across panels; `seriesColors` assigns by order.

## Design rules

- **Charts over tables.** A dashboard of tables is a report.
- **Title each panel with its finding**, not its metric:
  "Errors doubled after 06:00", not "Errors by hour".
- **One idea per panel.** Cap the panel count the user gave you.
- **No dual axes** (`y2`). Two measures with different units get two panels.
- **Lead with a markdown block** saying what the dashboard answers.
- **Encode meaning in colour sparingly**: one alert colour, used only for bad.

## Mistakes to catch

| Wrong | Right |
|---|---|
| `"type": "viz.line"` | `"type": "splunk.line"` |
| `"trendDisplayMode": "off"` | `"trendDisplay": "off"` |
| Relative range on historical data | Absolute `earliest` / `latest` |
| `<dashboard>` with no `version="2"` | `<dashboard version="2">` |
| A search that was never run | Validate via MCP first — row count, runtime |
| Panel in `visualizations` but not in `layout.structure` | Add it, or it never renders |

Studio silently ignores unknown options. A wrong name doesn't error — it just
doesn't do anything, which is why the checker looks for known-wrong names.
