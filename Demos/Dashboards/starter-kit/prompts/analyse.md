# Step 1 — Analyse

Run in a fresh Claude Code session, in the directory that holds your
`CLAUDE.md` and `.mcp.json`. Analysis first, dashboard second: a dashboard
built before you know the findings ends up as a wall of tables.

## Template

```text
Use the Splunk MCP server to analyse <subject> in <index / rollup>,
<absolute start date> to <absolute end date>.

Context: <who will use this and what decision it supports>.

Answer these questions:
1. <the question — phrase it as the decision, not the metric>
2. <second question>
3. <anything you suspect but haven't confirmed>

Constraints:
- Use the summary rollups in CLAUDE.md; tell me before any raw scan.
- Treat the broken fields listed in CLAUDE.md as unusable.
- For every number you report, show the SPL that produced it.

Output: a short findings report, ranked by impact, with the evidence for
each finding. Flag anything surprising you weren't asked about.
Don't build a dashboard yet.
```

## Worked example

```text
Use the Splunk MCP server to run an energy efficiency, usage and anomaly
analysis on household energy data: index=energy, 1 January to 20 June 2026.
Look at appliance energy, weather, solar production and grid import/export.

Two things I specifically want:

Where am I losing energy? Not the total — the shape. When do I generate,
when do I use it, and what does that mismatch cost me.

An optimal timetable. Work out the best hours to run the dryer, the washer
and the electric heating on solar, based on when surplus actually exists
rather than when I currently run them.

Use the summary rollups in CLAUDE.md. Show the SPL behind every number.
Rank the findings by impact. Don't build the dashboard yet.
```

## What a good run looks like

- First tool call within seconds, and it goes to the summary rollups.
- Every headline number carries the search that produced it.
- At least one finding you didn't ask for — the analysis looked, not just
  answered.

If it starts a multi-minute raw scan, stop it and point it back at CLAUDE.md.
