def judge(prompt, context=None):

    text = (prompt or "").lower().strip()

    if (
        ("أخبار" in text or "اخبار" in text or "خبر" in text or "ai news" in text)
        and
        ("تابع" in text or "أهم" in text or "اهم" in text or "افتح" in text or "لخص" in text)
    ):
        return {
            "intent": "task_router",
            "needs_tool": True,
            "advice": "نفذ مهمة أخبار مركبة",
            "owner_approval_required": False
        }

    if text.startswith("افتح 1") or text.startswith("افتح 2") or text.startswith("افتح 3"):
        return {
            "intent": "open_source",
            "needs_tool": True,
            "advice": "افتح نتيجة محفوظة",
            "owner_approval_required": False
        }

    if text.startswith("لخص 1") or text.startswith("لخص 2") or text.startswith("لخص 3"):
        return {
            "intent": "summarize_source",
            "needs_tool": True,
            "advice": "لخص نتيجة محفوظة",
            "owner_approval_required": False
        }

    if any(x in text for x in [
        "ابحث",
        "أخبار",
        "اخبار",
        "search",
        "news"
    ]):
        return {
            "intent": "search",
            "needs_tool": True,
            "advice": "استخدم محرك بحث Gerfex",
            "owner_approval_required": False
        }

    if any(x in text for x in [
        "افتح التطبيق",
        "افتح كروم",
        "كروم",
        "chrome",

        "افتح يوتيوب",
        "يوتيوب",
        "youtube",

        "افتح الإعدادات",
        "افتح اعدادات",
        "الإعدادات",
        "اعدادات",
        "settings",

        "افتح الملفات",
        "الملفات",
        "files",

        "اقرأ الشاشة",
        "اقرا الشاشة",
        "dump ui",

        "ارجع",
        "رجوع",
        "back",

        "الرئيسية",
        "home"
    ]):
        return {
            "intent": "android_action",
            "needs_tool": True,
            "advice": "تنفيذ أمر أندرويد مباشر",
            "owner_approval_required": False
        }

    return {
        "intent": "chat",
        "needs_tool": False,
        "advice": "رد عادي",
        "owner_approval_required": False
    }
