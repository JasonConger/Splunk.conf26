# Starter kit

Copy what you need into the root of your project — the directory you run your
agent from. Nothing here contains a secret; credentials come from environment
variables or OAuth.

## What's in it

| File | What it's for | Guide section |
|---|---|---|
| [`.mcp.json.oauth.example`](.mcp.json.oauth.example) | Connect the Splunk MCP server with browser sign-in. No secret in the file. | [6](../README.md#6-connecting-the-splunk-mcp-server) |
| [`.mcp.json.token.example`](.mcp.json.token.example) | Connect with an encrypted MCP token read from `${SPLUNK_MCP_TOKEN}`. | [6](../README.md#6-connecting-the-splunk-mcp-server) |
| [`.claude/settings.json`](.claude/settings.json) | Permission rules: ask before REST writes and packaging, deny deletes, deny reading `.env` and token files, deny printing the environment. | [7](../README.md#7-api-access-and-security) |
| [`.claude/skills/studio-dashboards/`](.claude/skills/studio-dashboards/SKILL.md) | A seed skill for authoring Dashboard Studio JSON, plus `check_definition.py`. | [4](../README.md#write-your-own) |
| [`CLAUDE.md.template`](CLAUDE.md.template) | Blank data dictionary. Rename to `CLAUDE.md`. | [3](../README.md#3-know-before-you-start) |
| [`examples/CLAUDE.md.example`](examples/CLAUDE.md.example) | The same, filled in for a real (anonymised) dataset. | [3](../README.md#3-know-before-you-start) |
| [`prompts/analyse.md`](prompts/analyse.md) | Step 1 prompt: findings before panels. | [8](../README.md#8-writing-a-good-dashboard-prompt) |
| [`prompts/build-dashboard.md`](prompts/build-dashboard.md) | Step 2 prompt: findings into a dashboard, validated, deployed on request. | [8](../README.md#8-writing-a-good-dashboard-prompt) |
| [`examples/platform_health.json`](examples/platform_health.json) | A valid Studio definition on `index=_internal` — deployable to any instance. | [9](../README.md#9-debugging) |
| [`examples/savedsearches.conf`](examples/savedsearches.conf) | A summary-index rollup and an alert, valid keys only, with the invalid ones listed. | [9](../README.md#9-debugging) |
| [`splunk/ai_sandbox/`](splunk/ai_sandbox/) | A sandbox app that passes AppInspect Cloud checks, with the platform health dashboard installed. | [7](../README.md#7-api-access-and-security) |
| [`splunk/ai_agent_role.md`](splunk/ai_agent_role.md) | A least-privilege role for the agent, and the inheritance trap to avoid. | [7](../README.md#7-api-access-and-security) |
| [`scripts/splunk-rest.sh`](scripts/splunk-rest.sh) | `check`, `create-dashboard`, `get-dashboard`, `list-dashboards`, `delete-dashboard` (typed confirmation). | [7](../README.md#7-api-access-and-security) |
| [`scripts/package-app.sh`](scripts/package-app.sh) | Package an app directory as `.spl` and run AppInspect. | [9](../README.md#9-debugging) |
| [`.gitignore`](.gitignore) | Keeps `.env`, token files and build output out of git. | [7](../README.md#7-api-access-and-security) |

## Try the whole path in ten minutes

Every step works on any Splunk instance, before you point anything at your own
data.

1. **Sandbox and role.** Package and upload the sandbox app, then create the
   role and service user from [`splunk/ai_agent_role.md`](splunk/ai_agent_role.md).

   ```bash
   ./scripts/package-app.sh splunk/ai_sandbox
   ```

   Upload `dist/ai_sandbox-0.1.0.spl` under **Apps → Manage Apps → Install app
   from file**. Open **AI Sandbox → Platform health** — it should show data.

2. **Connect.** Copy one `.mcp.json.*.example` to `.mcp.json`, set the
   environment variables, start Claude Code, run `/mcp`.

3. **Ask.** "Which indexes can you see?" — the answer should match the role.

4. **Deploy over REST** (if port 8089 is open to you):

   ```bash
   export SPLUNK_HOST='https://<your-stack>.splunkcloud.com:8089'
   export SPLUNK_TOKEN='<REST token for svc_ai_agent>'
   export SPLUNK_APP='ai_sandbox'
   ./scripts/splunk-rest.sh check
   ./scripts/splunk-rest.sh create-dashboard "Platform health copy" examples/platform_health.json
   ```

5. **Now your data.** Fill in `CLAUDE.md`, then run the two prompts.
