# GERFEX FINAL MERGE PLAN V1

## Goal

Organize Gerfex before planting Queen as its internal brain.

Gerfex remains the sovereign system.
Queen becomes the internal reasoning brain.
External models remain tools only.

## Completed discovery

- GERFEX_CAPABILITY_MAP_V1.json
- GERFEX_DUPLICATE_AND_IMPORTANT_CAPABILITIES_V1.md
- GERFEX_FINAL_CAPABILITY_MATRIX_V1.md
- GERFEX_AUDIT_COMMANDS_V1.md
- GERFEX_AUDIT_TOP_FILES_V1.md
- GERFEX_AUDIT_DECISION_V1.md
- GERFEX_CORE_REVIEW_FULL_V1.md

## Main source checkpoint

Use this as the trusted working base:

gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339

Reason:
This checkpoint proves the working chain:

HUD -> Backend -> Queen -> Android Queue -> Queue Runner -> YouTube

## Core capabilities and selected sources

### Android command center

Source:
gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/agent/gerfex_android_unified.py

Role:
- queue_action
- open_app
- open_url
- search_google
- tap
- swipe
- type_text
- press_back
- press_home
- press_recent
- press_enter
- wait
- dump_ui
- screenshot

### Android executor / queue runner

Source:
gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/runtime/queue_runner.py

Role:
- process android_queue.txt
- execute open_url
- execute open_app
- execute tap/swipe/type/key/wait/dump_ui/screenshot
- uses rish/Shizuku

### Stable action executor

Source:
gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/packages/gerfex_stable_core_api_package_v1/core/action_executor_v1.py

Role:
Keep as reference/merge source for:
- open_url
- open_settings
- tap
- swipe
- type_text
- press_back
- press_home
- press_enter
- wait
- dump_ui
- open_chrome
- open_youtube_results

### Intent / goal core

Sources:
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/agent/gerfex_goal_loop_core.py
- goal_engine.py

Role:
- detect_intent
- detect_goal_type
- build_plan
- execute_goal idea
- recovery idea

Important:
Do not copy old goal_engine.py as final core.
Extract useful ideas into:
- goal_planner.py
- goal_executor.py
- recovery_manager.py

### Screen reading

Source:
gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/runtime/screen_reader_bridge.py

Role:
- read_screen

### Skills

Sources:
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/runtime/skill_executor.py
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/packages/gerfex_stable_core_api_package_v1/skill_registry_v1.py
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/packages/gerfex_stable_core_api_package_v1/skills/youtube_skill_v2.py

Role:
- run_skill
- list_skills
- youtube_search_open_first

### Memory

Do not use old memory files directly as final.

Old sources reviewed:
- archive/legacy_scripts_v1/gervex.py
- archive/legacy_scripts_v1/memory_context.py

Decision:
Create clean memory_manager.py with:
- load_json
- save_json
- load_memory
- save_memory
- append_memory_note
- log_action

### Recovery

Old source reviewed:
- goal_engine.py

Decision:
Create recovery_manager.py with:
- log_recovery
- should_retry
- wait_and_retry idea

### Queen

Sources:
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/agent/queen_core.py
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/agent/queen_judgement.py
- gerfex_checkpoint_hud_youtube_success_clean_v1_20260530_215339/gerfex_official_runtime_v1/agent/gerfex_brain_unified.py

Decision:
Do not make Queen the system root.
Queen goes inside Gerfex as:
brain/queen_brain.py
brain/queen_judgement.py

Gerfex official entry point must be:
core/gerfex_core.py

## Final folder target

gerfex_unified_core_v1/

Expected structure:

core/
brain/
android/
runtime/
skills/
goals/
memory/
recovery/
ui_bridge/
archive_reference/

## Archive rule

Do not delete old files.
Copy important references into:
archive_reference/

## Final rule

After this plan, do not start another broad audit unless a test fails.
