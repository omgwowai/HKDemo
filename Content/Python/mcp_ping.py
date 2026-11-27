"""Health check for the Claude -> MCP -> UnrealMcpBridge -> UE Python chain.

Run via the `run_unreal_script` MCP tool with script_path="mcp_ping.py".
Read-only: touches nothing in the level or assets.
"""
import unreal

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()

info = {
    "engine_version": unreal.SystemLibrary.get_engine_version(),
    "project": unreal.SystemLibrary.get_game_name(),
    "project_dir": unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),
    "world": world.get_name() if world else None,
    "level_actor_count": len(actors),
    "args_echo": globals().get("mcp_args", {}),
}
for k, v in info.items():
    print(f"{k}: {v}")
mcp_result = info
