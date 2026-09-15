# A least-privilege role for an AI agent

The agent acts with whatever the token's role allows. Instructions in
`CLAUDE.md` and permission rules reduce mistakes; **the role is the boundary.**
Give the agent its own service user with this role, never your admin account.

## The trap: inheriting `user`

The obvious move is a new role that inherits `user` and lists a few indexes.
It doesn't scope anything.

- Importing a role imports **its allowed indexes too**, and the two lists are
  combined.
- On a stock Splunk Cloud stack the `user` role has `srchIndexesAllowed = *` —
  every non-internal index.

So `importRoles = user` plus `srchIndexesAllowed = energy` can still search
everything. **Don't inherit.** Enable each capability explicitly.

Check your own stack:

```spl
| rest /services/authorization/roles splunk_server=local
| table title imported_roles srchIndexesAllowed srchIndexesDefault
```

## The role

| Setting | Value | Why |
|---|---|---|
| Inherit | **nothing** | See above |
| Indexes allowed | `energy`, `summary` — only what this work needs | The agent can only reason about, and leak, what it can read |
| Default index | `energy` | |
| Capability `search` | enabled | Run searches |
| Capability `mcp_tool_execute` | enabled | Use MCP tools |
| Capability `get_metadata` | enabled | Hosts, sources, sourcetypes |
| Capability `edit_own_objects` | enabled | Create its own dashboards and searches |
| Capability `schedule_search` | *only if* it will schedule rollups or alerts | |
| Search job quota | 3 | Stops a runaway loop from starving other users |
| Max search time | 300 s | |
| App write access | `ai_sandbox` only, via the app's `default.meta` | Everything it creates lands in one reviewable place |

Start with this set. If a tool call fails with a permission error, add the one
capability it needs — don't jump to a broader role.

### Do not grant

| Capability / role | Why not |
|---|---|
| Role `can_delete`, `delete_by_keyword` | Irreversible data deletion |
| `admin_all_objects` | Edit or delete anyone's content |
| `mcp_tool_admin` | Enable, disable and register MCP tools for everyone |
| `edit_tokens_all`, `edit_tokens_own` | Mint more credentials |
| `edit_roles`, `edit_user` | Escalate its own access |
| `install_apps` | Ship code to the search head |
| Role `mcp_user`, `power`, `sc_admin` | Bundles several of the above |

## Create it

### Splunk Web (simplest, and the way on Splunk Cloud)

**Settings → Roles → New Role**

1. **Inheritance:** leave everything unticked.
2. **Capabilities:** tick the capabilities in the table above.
3. **Indexes:** tick only the indexes this work needs; set the default.
4. **Resources:** search job limit 3, max search time 300s.

Then **Settings → Users → New User** `svc_ai_agent` with only this role.

### REST (admin token required)

```bash
curl -sS -H "Authorization: Bearer ${SPLUNK_ADMIN_TOKEN}" \
  "${SPLUNK_HOST}/services/authorization/roles" \
  -d name=ai_agent \
  -d capabilities=search \
  -d capabilities=mcp_tool_execute \
  -d capabilities=get_metadata \
  -d capabilities=edit_own_objects \
  -d srchIndexesAllowed=energy \
  -d srchIndexesAllowed=summary \
  -d srchIndexesDefault=energy \
  -d srchJobsQuota=3 \
  -d srchMaxTime=300
```

Run this yourself, not through the agent — it's an access-control change.

### authorize.conf (Splunk Enterprise)

```ini
[role_ai_agent]
# No importRoles — inheriting 'user' would grant every index.
srchIndexesAllowed = energy;summary
srchIndexesDefault = energy
srchJobsQuota = 3
srchMaxTime = 300
search = enabled
mcp_tool_execute = enabled
get_metadata = enabled
edit_own_objects = enabled
```

Each capability is its own line: `<capability> = enabled`. A single
`capabilities = a;b;c` line is **not** valid and is silently ignored.

## Tokens for the service user

- **OAuth:** the service user signs in through the browser; nothing to mint.
- **MCP token:** an admin creates an encrypted token for `svc_ai_agent` in the
  Splunk MCP Server app (needs `edit_tokens_all` + `mcp_tool_admin` on the
  admin's role).
- **REST token:** Settings → Tokens → New Token, user `svc_ai_agent`,
  **short expiry**.

## Verify

Connect the agent with the service user's credentials and ask:

```text
Which indexes can you search? Run: | eventcount summarize=false index=* | dedup index | table index
```

The answer should be exactly the indexes you granted. Anything more means an
inherited role is still in play.
