# GERFEX MERGE PLAN V1

Confirmed Active Core:
- queen_core.py
- queen_intelligence.py
- queen_judgement.py
- gerfex_android_unified.py
- memory_manager.py
- planner_core.py

Legacy Components:
- brain_manager.py
- model_router.py

Findings:

brain_manager.py:
- Still executed by queen_core.py
- Still reports DeepSeek as primary brain
- Must be converted to Queen architecture

model_router.py:
- No active runtime usage detected
- Functionality already replaced by Queen local routing

Next Phase:
1. Convert brain_manager.py to Queen-first architecture
2. Remove DeepSeek-first terminology
3. Keep compatibility layer
4. No file deletions
5. Re-test Queen runtime

Status:
READY FOR QUEEN ARCHITECTURE CONVERSION
