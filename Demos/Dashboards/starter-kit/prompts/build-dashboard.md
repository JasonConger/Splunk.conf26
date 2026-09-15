# Step 2 — Build the dashboard

Run in the same session as step 1, so the findings and validated SPL are
already in context.

## Template

```text
Turn those findings into a <Dashboard Studio / React> dashboard for
<audience>, who will look at it <on a wall screen / weekly / during incidents>.

Panels — no more than <N>:
1. <headline numbers: which KPIs>
2. <the key picture: which chart, which finding it shows>
3. <...>
Finish with a short ranked list of what to change.

Design:
- Charts over tables. A table only where the reader needs exact values.
- One idea per panel, titled with the finding, not the metric
  ("Surplus exists only 10:00–15:00", not "Hourly solar").
- <theme, colour or brand constraints>. No dual axes.
- Absolute time range: <start> to <end>.

Before you write the definition:
- Run every panel search through the MCP and show me its row count and
  runtime. Anything that returns 0 rows or runs > 10s gets fixed first.

Deliver:
- Save the definition to dashboards/<name>.json.
- Do not deploy. Show me the panel list, then wait for me to say "deploy".
- On "deploy": scripts/splunk-rest.sh create-dashboard "<Title>" dashboards/<name>.json
  into app <ai_sandbox>, then confirm it exists with get-dashboard.
```

## Why each part is there

| Part | Without it |
|---|---|
| Audience and viewing distance | Dense, document-style panels |
| Panel cap | Every finding becomes a panel |
| "Charts over tables" | Tables — the model's default for anything tabular |
| Finding-as-title | Panels that make the reader work out the point |
| Validate before building | Panels that render "No results found" in front of your audience |
| Save, then wait for "deploy" | An unreviewed write to a shared instance |
