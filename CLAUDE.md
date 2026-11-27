# HKDemo

Unreal Engine 5.8 project (source engine at `E:/UnrealEngine`, association
`{4B303DEF-4E44-1DE5-A177-09B23BCA8A5A}`). Remote: https://github.com/omgwowai/HKDemo

## Driving the editor from Claude (MCP)

Claude operates the running UE editor through one MCP tool, `run_unreal_script`.
The chain is:

```
Claude Code ──stdio──> mcp_server/ (Python, .mcp.json "unreal")
            ──WebSocket 127.0.0.1:8777──> Plugins/UnrealMcpBridge (editor plugin)
            ──> UE embedded Python runs Content/Python/<script>.py
```

- Any UE editor task: use the `driving-unreal-via-mcp` skill
  (`.claude/skills/driving-unreal-via-mcp/`). Introspect the `unreal` API before
  writing real scripts; never guess signatures.
- Scripts must live under `Content/Python/`. Args arrive as global `mcp_args`;
  set `mcp_result` (JSON-serializable) to return data.
- Health check: `run_unreal_script(script_path="mcp_ping.py")`.
- If the tool returns `Unreal editor not connected on 127.0.0.1:8777`, the
  editor isn't running (or the plugin failed to load). Ask the user to open
  `HKDemo.uproject`; don't retry blindly.
- Port / scripts root are configurable in Project Settings → Plugins →
  Unreal MCP Bridge (`UUnrealMcpBridgeSettings`).

## First-time setup on a new machine

1. Install the MCP server venv:
   ```
   cd mcp_server
   py -3 -m venv .venv
   .venv/Scripts/python.exe -m pip install -e ".[dev]"
   ```
   `.mcp.json` points at `E:/HKDemo/mcp_server/.venv/Scripts/python.exe`;
   adjust the path if the repo is cloned elsewhere.
2. Build the editor target (compiles `UnrealMcpBridge`):
   ```
   E:\UnrealEngine\Engine\Build\BatchFiles\Build.bat HKDemoEditor Win64 Development -Project=E:\HKDemo\HKDemo.uproject -WaitMutex
   ```
3. Install **Ultra Dynamic Sky** into `Content/UltraDynamicSky` from your own
   Fab library. It is a paid asset and is deliberately not in this public repo
   (see `.gitignore`).
4. Open `HKDemo.uproject`, then start Claude Code in this folder and approve
   the `unreal` MCP server.

## Repo conventions

- Not tracked: `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`,
  IDE files, `.venv/`, `.claude/settings.local.json`, `Content/UltraDynamicSky/`.
- `Content/Python/_explore.py` is the skill's scratch introspection script;
  it is ignored. Give real scripts descriptive names and commit them.
