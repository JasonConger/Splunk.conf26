#!/usr/bin/env bash
# Package a Splunk app directory into an installable .spl, then vet it.
#
#   ./package-app.sh ../splunk/ai_sandbox
#
# Produces dist/<app>-<version>.spl. Upload it via Apps > Manage Apps >
# Install app from file (Splunk Cloud: private app upload, vetted on install).

set -euo pipefail

src="${1:?path to app directory}"
app="$(basename "$src")"
version="$(awk -F' *= *' '/^\[id\]/{f=1} f&&$1=="version"{print $2; exit}' "$src/default/app.conf")"
out="dist/${app}-${version:-0.0.0}.spl"
mkdir -p dist

# COPYFILE_DISABLE stops macOS adding ._ resource files, which fail AppInspect.
COPYFILE_DISABLE=1 tar -czf "$out" \
  --exclude='.DS_Store' --exclude='local' --exclude='*.pyc' --exclude='__pycache__' \
  -C "$(dirname "$src")" "$app"
echo "Packaged $out"

if command -v splunk-appinspect >/dev/null; then
  splunk-appinspect inspect "$out" --mode precert --included-tags cloud
else
  echo "Install AppInspect to vet before upload: pip install splunk-appinspect"
fi
