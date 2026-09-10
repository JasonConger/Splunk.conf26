# Starter prompt:

Here is the exact prompt I used to build a Splunk add-on with `ucc-gen`

> using the documentation located at https://splunk.github.io/addonfactory-ucc-generator/ create a Splunk add-on for me

:bulb: Note: The model I used was `Claude Sonnet 5 (High)`

<details>
<summary>And here is the output from the prompt</summary>

  ---

  User: using the documentation located at https://splunk.github.io/addonfactory-ucc-generator/ create a Splunk add-on for me
  GitHub Copilot: Updated todo list
  
  Fetched https://splunk.github.io/addonfactory-ucc-generator/
  
  Fetched 3 resources
  Analyzing your answers...
  
  Execution complete: Set up UCC and generate add-on
  
  Ran terminal command:  { echo '>>> 1. python3 --version'; python3 --version; echo '>>> 2. python3 -m venv .venv'; python3 -m venv .venv; echo '>>> 3. source .venv/bin/activate && pip install --upgrade pip'; source .venv/bin/activate && pip install --upgrade pip; echo '>>> 4. source .venv/bin/activate && pip install splunk-add-on-ucc-framework'; source .venv/bin/activate && pip install splunk-add-on-ucc-framework; echo '>>> 5. source .venv/bin/activate && ucc-gen --version'; source .venv/bin/activate && ucc-gen --version; echo '>>> 6. source .venv/bin/activate && ucc-gen init --addon-name "splunk_conf26_demo" --addon-display-name "Splunk .conf26 Demo" --addon-input-name test_input --overwrite'; source .venv/bin/activate && ucc-gen init --addon-name "splunk_conf26_demo" --addon-display-name "Splunk .conf26 Demo" --addon-input-name test_input --overwrite; echo '>>> 7. find splunk_conf26_demo -maxdepth 2 -print'; find /Users/jconger/Dev/Splunk.conf26/splunk_conf26_demo -maxdepth 2 -print; } 2>&1

  Ran terminal command:  cat '/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_KdIXtpendiEb5ZvQ4ejZG7L2__vscode-1789006368636/content.txt'

  Ran terminal command:  f='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_KdIXtpendiEb5ZvQ4ejZG7L2__vscode-1789006368636/content.txt'; wc -l "$f"; sed -n '1,240p' "$f"

  Ran terminal command:  f='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_KdIXtpendiEb5ZvQ4ejZG7L2__vscode-1789006368636/content.txt'; sed -n '1,100p' "$f"

  Ran terminal command:  f='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_KdIXtpendiEb5ZvQ4ejZG7L2__vscode-1789006368636/content.txt'; tail -80 "$f"

  Execution complete: Build the generated add-on
  
  Ran terminal command:  source .venv/bin/activate && ucc-gen build --source splunk_conf26_demo/package --ta-version 1.0.0; exit_code=$?; printf '\n=== ucc-gen exit code: %s ===\n' "$exit_code"; if [[ -d /Users/jconger/Dev/Splunk.conf26/output ]]; then printf '\n=== output directory (max depth 2) ===\n'; find /Users/jconger/Dev/Splunk.conf26/output -maxdepth 2 -print; else printf '\n=== output directory not created ===\n'; fi; exit "$exit_code"
  
  Ran terminal command:  cat '/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_0BSDPn3iyh8ewUJM9QJrd3jE__vscode-1789006368642/content.txt'
  
  Ran terminal command:  content='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_0KRW7WZKspVPTGQCKFZvrJX__vscode-1789006368643/content.txt'; wc -c "$content"; head -c 18000 "$content"
  
  Ran terminal command:  content='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_0KRW7WZKxSpVPTGQCKFZvrJX__vscode-1789006368643/content.txt'; printf '%s\n' '=== captured output size ==='; wc -c "$content"; printf '%s\n' '=== captured output ==='; cat "$content"
  
  Ran terminal command:  content='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_9fLxCnPuRE3oVGOzZnebnDuP__vscode-1789006368645/content.txt'; wc -l "$content"; sed -n '1,160p' "$content"
  
  Ran terminal command:  content='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_kA7dr4PBaKldJlPrn3fSewZu__vscode-1789006368646/content.txt'; if [[ -f "$content" ]]; then wc -l "$content"; sed -n '1,100p' "$content"; else find '/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e' -name content.txt -print; fi
  
  Ran terminal command:  content='/Users/jconger/Library/Application Support/Code/User/workspaceStorage/3fa49c788d1b9c086999e3f117843def/GitHub.copilot-chat/chat-session-resources/f1e2ada7-a9ef-454d-86c0-da7065b2b91e/call_0BSDPn3iyh8ewUJM9QJrd3jE__vscode-1789006368642/content.txt'; wc -l "$content"; sed -n '1,120p' "$content"
  
  Ran terminal command:  source .venv/bin/activate && ucc-gen build --source splunk_conf26_demo/package --ta-version 1.0.0 2>&1; exit_code=$?; printf '\n=== ucc-gen exit code: %s ===\n' "$exit_code"; if [[ -d output ]]; then printf '\n=== output directory (max depth 2) ===\n'; find output -maxdepth 2 -print; else printf '\n=== output directory not created ===\n'; fi; exit 0
  
  Build succeeded. Now packaging it into an installable archive and updating `.gitignore` to exclude generated build artifacts and the virtual environment. 
  
  Execution complete: Package the built add-on
  
  Ran terminal command:  source .venv/bin/activate && ucc-gen package --path output/splunk_conf26_demo
  
  Created 4 todos
  
  Now update `.gitignore` to exclude build outputs and the venv, and confirm the generated add-on structure. 
  
  Read , lines 1 to 30
  
  Good — `.venv` and `*.tar.gz` are already ignored. Let's also ignore the UCC `output` build folder specifically. 
  
  Replacing 3 lines with 4 lines in 
  
  Created and built a UCC-based Splunk add-on:
  
  - **Source add-on**: `splunk_conf26_demo` — contains `globalConfig.json`, `package/` (with `app.manifest`, `bin/`, `lib/`)
  - **Built add-on**: `splunk_conf26_demo` — full installable app with generated `.conf` files, UI, and the `test_input` modular input
  - **Package**: `splunk_conf26_demo-1.0.0.tar.gz` — installable archive, ready to upload to Splunk
  - Python venv (`.venv`) created with `splunk-add-on-ucc-framework` 5.52.0 installed
  - Updated `.gitignore` to exclude `output`, `.tar.gz` packages, and `.venv`
  
  To customize inputs/fields, edit `globalConfig.json`, then rebuild with:
  ```
  source .venv/bin/activate
  ucc-gen build --source splunk_conf26_demo/package --ta-version 1.0.0
  ucc-gen package --path output/splunk_conf26_demo
  ```
  
  Install the `.tar.gz` in your Splunk instance via **Manage Apps → Install app from file**.
  
  Completed: *Set up UCC and generate add-on* (1/4)
  
  Made changes.
  
  ---
</details>

:clock1: Total time to build the add-on from scratch - **2:49**
