# GERFEX ARCHITECTURE CLEANUP V1

## Confirmed Core

Gerfex
└── Queen
    ├── Judgement
    ├── Planner
    ├── Memory
    ├── Android
    ├── Skills
    └── Intelligence

## Active Entry Point

brain/queen_core.py

## Active Intelligence

brain/queen_intelligence.py

## Active Android Layer

brain/gerfex_android_unified.py
runtime/queue_runner.py

## Active Runtime

runtime/runtime_state.py
runtime/screen_reader_bridge.py

## Active Memory

memory/memory_manager.py
memory/memory.json

## Active Skills

skills/

## Remnants Detected

brain/brain_manager.py
brain/model_router.py

Reason:
Legacy DeepSeek-first architecture remnants.

Current project architecture:
Queen-first architecture.

Status:
Keep until merge plan executed.

## No Deletions Performed

Checkpoint protected.
