import json
import time
from pathlib import Path

BASE = Path(__file__).parent

SUPPORTED_MODELS = {
    "gerfex": {
        "role": "origin",
        "enabled": True,
        "type": "local_identity_runtime"
    },
    "queen": {
        "role": "learning_advisor",
        "enabled": True,
        "type": "internal_reasoning_rules"
    },
    "deepseek": {
        "role": "assistant_model",
        "enabled": False,
        "type": "external_helper_placeholder"
    },
    "gpt": {
        "role": "assistant_model",
        "enabled": False,
        "type": "external_helper_placeholder"
    },
    "gemini": {
        "role": "assistant_model",
        "enabled": False,
        "type": "external_helper_placeholder"
    }
}

ACTIVE_HELPER_MODEL = "deepseek"

def load_json(name, default):
    path = BASE / name
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def identity():
    return load_json("identity.json", {})

def memory():
    return load_json("memory.json", {})

def model_status():
    return {
        "ok": True,
        "origin": "Gerfex",
        "core_brain": "Queen",
        "active_helper_model": ACTIVE_HELPER_MODEL,
        "models": SUPPORTED_MODELS,
        "rule": "Gerfex is the origin. Queen is Gerfex core brain. External models are helper tools only."
    }

def decide(prompt, selected_model="Gerfex"):
    text = (prompt or "").strip().lower()
    ident = identity()

    needs_helper = False
    reason = "local_rules_first"

    if any(x in text for x in ["حلل", "اشرح", "فكر", "اكتب", "صمم", "برمج", "analyze", "explain"]):
        needs_helper = True
        reason = "complex_reasoning_or_generation"

    return {
        "ok": True,
        "origin": ident.get("name", "Gerfex"),
        "core_brain": "Queen",
        "selected_model": selected_model,
        "helper_model": ACTIVE_HELPER_MODEL,
        "needs_helper_model": needs_helper,
        "reason": reason,
        "rule": "External models advise only when Queen asks. They do not own identity or execution."
    }

def answer_identity(prompt):
    text = (prompt or "").strip().lower()
    ident = identity()
    mem = memory()

    name = ident.get("name", "Gerfex")
    system_type = ident.get("system_type", "Personal Sovereign AI")
    owner = ident.get("owner", "Mashel")
    rules = ident.get("core_rules", [])
    notes = mem.get("project_notes", [])

    if "من انت" in text or "من أنت" in text:
        return f"أنا {name}، {system_type}. Queen هي عقلي الداخلي، والنماذج الخارجية أدوات مساعدة فقط عند الحاجة."

    if "هدفك" in text or "ما هو هدفك" in text or "ماهو هدفك" in text:
        return f"هدفي أن أساعد {owner} كذكاء شخصي سيادي: أفهم الأوامر، أستخدم ذاكرتي، أتحكم بالأدوات والهاتف، وأستدعي النماذج المساعدة فقط عند الحاجة."

    if "سيدك" in text or "مالكك" in text or "صاحبك" in text or "من صاحبك" in text:
        return f"صاحب القرار النهائي هو {owner}. Queen هي عقلي الداخلي، وليست سيدًا مستقلًا، والنماذج الخارجية أدوات فقط."

    if "كوين" in text or "queen" in text:
        return "Queen مستشار تعلم محدود داخل Gerfex. وظيفتها مناقشة الأفكار والتعلم داخل جلسة التعلم فقط. لا تملك صلاحية التنفيذ أو اتخاذ القرار النهائي."

    if "قدراتك" in text or "وش تقدر" in text or "ماذا تستطيع" in text:
        return "قدراتي الحالية: الدردشة الأساسية، قراءة هويتي وذاكرتي، البحث عبر المتصفح، فتح التطبيقات والروابط عبر Android queue، وتهيئة المسار لاستدعاء النماذج المساعدة لاحقًا."

    if "قواعدك" in text or "القواعد" in text:
        if rules:
            return "قواعدي الأساسية:\n" + "\n".join(f"- {r}" for r in rules)
        return "قاعدتي الأساسية: Gerfex هو الأصل، Queen هي العقل الداخلي، والنماذج الخارجية أدوات مساعدة فقط."

    if "ذاكرتك" in text or "ماذا تتذكر" in text:
        if notes:
            return "من ذاكرتي الحالية:\n" + "\n".join(f"- {n}" for n in notes)
        return "لدي ذاكرة مخصصة، لكن لا توجد ملاحظات مشروع ظاهرة في هذا الملف حاليًا."

    return None

def ask_helper_model(prompt, selected_model="Gerfex"):
    decision = decide(prompt, selected_model)
    if not decision["needs_helper_model"]:
        return {
            "ok": False,
            "reason": "helper_not_needed",
            "decision": decision
        }

    helper = decision["helper_model"]
    if not SUPPORTED_MODELS.get(helper, {}).get("enabled"):
        return {
            "ok": False,
            "reason": "helper_model_not_connected_yet",
            "helper_model": helper,
            "decision": decision,
            "fallback": "Queen will answer with local rules until helper models are connected."
        }

    return {
        "ok": False,
        "reason": "real_external_call_not_implemented_yet",
        "helper_model": helper,
        "decision": decision
    }

def think(prompt, selected_model="Gerfex"):
    started = time.time()

    direct = answer_identity(prompt)
    decision = decide(prompt, selected_model)

    if direct:
        reply = direct
    else:
        helper = ask_helper_model(prompt, selected_model)
        if helper.get("ok"):
            reply = helper.get("reply", "")
        elif helper.get("reason") == "helper_model_not_connected_yet":
            reply = "أفهم طلبك، لكن النموذج المساعد غير موصول بعد. سأتعامل معه محليًا قدر الإمكان."
        else:
            reply = f"Gerfex فهم رسالتك: {prompt}"

    return {
        "ok": True,
        "reply": reply,
        "origin": "Gerfex",
        "core_brain": "Queen",
        "selected_model": selected_model,
        "decision": decision,
        "model_status": model_status(),
        "latency": round(time.time() - started, 3)
    }

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) or "من انت"
    print(json.dumps(think(prompt), ensure_ascii=False, indent=2))
