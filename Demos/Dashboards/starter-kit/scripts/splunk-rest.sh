#!/usr/bin/env bash
# Minimal Splunk REST helper for AI-built dashboards.
#
#   export SPLUNK_HOST='https://<your-stack>.splunkcloud.com:8089'
#   export SPLUNK_TOKEN='<REST token — NOT your MCP token>'
#   export SPLUNK_APP='ai_sandbox'          # write into a sandbox app, not search
#
#   ./splunk-rest.sh check
#   ./splunk-rest.sh create-dashboard "Energy Review" dashboards/energy.json
#   ./splunk-rest.sh get-dashboard energy_review
#   ./splunk-rest.sh list-dashboards
#   ./splunk-rest.sh delete-dashboard energy_review
#
# Token: Splunk Web > Settings > Tokens > New Token. Give it a short expiry.
# Splunk Cloud: port 8089 must be allowlisted for your IP (ACS search-api).

set -euo pipefail

: "${SPLUNK_HOST:?export SPLUNK_HOST=https://<your-stack>:8089 first}"
: "${SPLUNK_TOKEN:?export SPLUNK_TOKEN first — never hard-code it here}"
APP="${SPLUNK_APP:-ai_sandbox}"
USER_NS="${SPLUNK_USER:-nobody}"

api() {
  curl -sS --fail-with-body -H "Authorization: Bearer ${SPLUNK_TOKEN}" "$@"
}

slugify() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '_' \
    | sed -e 's/^_//' -e 's/_*$//'
}

case "${1:-}" in
  check)
    api "${SPLUNK_HOST}/services/server/info?output_mode=json" \
      | python3 -c 'import json,sys; d=json.load(sys.stdin)["entry"][0]["content"]; print("OK  Splunk", d["version"])'
    api "${SPLUNK_HOST}/services/authentication/current-context?output_mode=json" \
      | python3 -c 'import json,sys; c=json.load(sys.stdin)["entry"][0]["content"]; print("    as", c["username"], "| roles", ",".join(c["roles"]))'
    ;;

  create-dashboard)
    title="${2:?title}"; deffile="${3:?path to Dashboard Studio JSON}"
    name="$(slugify "$title")"
    python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$deffile" \
      || { echo "definition is not valid JSON" >&2; exit 1; }
    # Dashboard Studio views are a version="2" XML wrapper around the JSON.
    payload="$(python3 - "$title" "$deffile" <<'PY'
import html, json, sys
title, path = sys.argv[1], sys.argv[2]
definition = json.dumps(json.load(open(path)), separators=(",", ":"))
print('<dashboard version="2" theme="light"><label>%s</label><definition><![CDATA[%s]]></definition></dashboard>'
      % (html.escape(title), definition))
PY
)"
    api -X POST "${SPLUNK_HOST}/servicesNS/${USER_NS}/${APP}/data/ui/views?output_mode=json" \
      --data-urlencode "name=${name}" --data-urlencode "eai:data=${payload}" > /dev/null
    echo "Created ${name} in app ${APP}"
    ;;

  get-dashboard)
    api "${SPLUNK_HOST}/servicesNS/${USER_NS}/${APP}/data/ui/views/${2:?name}?output_mode=json" \
      | python3 -c 'import json,sys; e=json.load(sys.stdin)["entry"][0]; print("EXISTS", e["name"], "| updated", e["updated"])'
    ;;

  list-dashboards)
    api "${SPLUNK_HOST}/servicesNS/${USER_NS}/${APP}/data/ui/views?output_mode=json&count=0&search=eai:acl.app=${APP}" \
      | python3 -c 'import json,sys; [print(e["name"]) for e in json.load(sys.stdin)["entry"]]'
    ;;

  delete-dashboard)
    name="${2:?name}"
    read -r -p "Delete ${name} from ${APP}? Type the name to confirm: " ok
    [[ "$ok" == "$name" ]] || { echo "Aborted."; exit 1; }
    api -X DELETE "${SPLUNK_HOST}/servicesNS/${USER_NS}/${APP}/data/ui/views/${name}?output_mode=json" > /dev/null
    echo "Deleted ${name}"
    ;;

  *) sed -n '2,16p' "$0"; exit 1 ;;
esac
