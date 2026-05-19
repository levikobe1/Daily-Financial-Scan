להחליף את כל `generator.py` בקוד הבא. התיקון המרכזי: בריחת סוגריים בתוך `f"""..."""` כדי ש־Python לא ינסה לפרש קוד JavaScript. 

```python
import os
import json
import time
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
OUTPUT_FILE = "index.html"

PROMPT = """
Find the most important economic and macroeconomic news from the last 24 hours (today) specifically from these sources: Reuters, Bloomberg, Yahoo Finance, TheMarker, and Globes.

STRICT INSTRUCTIONS:
1. DEDUPLICATION: If multiple sources report on the exact same event, compile them into ONE single item.
2. DEEP LINKS REQUIRED: For each item, specify a 'sources' array of objects with 'name' and exact deep article 'url'.
3. Hebrew Language: All text fields must be written in high-quality, professional financial Hebrew.
4. Format: Respond strictly with a JSON array conforming to this schema:
[{
    "id": "unique_string",
    "title": "Main news headline in Hebrew",
    "summary": "Clear, concise summary in Hebrew",
    "importance": "High" or "Medium" or "Low",
    "scope": "global" or "local",
    "implication_global": "Implications worldwide in Hebrew",
    "implication_local": "Implications in Israel in Hebrew",
    "publish_time": "DD/MM/YYYY HH:MM",
    "category": "e.g., מט\\"ח, ריבית, נדל\\"ן, מאקרו",
    "sources": [{"name": "Globes", "url": "https://www.globes.co.il/news/article.aspx?did=1001479834"}]
}]
"""


def fetch_real_news_from_gemini():
    print("מתחבר ל-Gemini API ומבצע סריקה חיה ברשת...")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                text_response = result["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_response)

            print(f"שגיאת שרת ({response.status_code}). מנסה שוב...")

        except Exception as e:
            print(f"שגיאה בניסיון {attempt + 1}: {e}")

        time.sleep(2)

    return None


def generate_html(news_data):
    print("מייצר את קובץ ה-HTML הסטטי המעודכן...")

    now_str = datetime.now().strftime("%d/%m/%Y ב-%H:%M")
    js_news_array = json.dumps(news_data, ensure_ascii=False)
    current_year = datetime.now().year

    html_content = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>הבוקר הכלכלי - עדכון יומי</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;500;600;700;800&family=Rubik:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body {{
            font-family: 'Assistant', sans-serif;
            background-color: #0b0f19;
        }}

        h1, h2, h3, h4, .font-heading {{
            font-family: 'Rubik', sans-serif;
        }}
    </style>
</head>

<body class="text-slate-100 min-h-screen flex flex-col selection:bg-blue-500/30">

    <header class="border-b border-slate-800/60 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="bg-gradient-to-tr from-blue-600 to-indigo-600 p-2.5 rounded-xl text-white shadow-md">
                    <i data-lucide="trending-up" class="w-5 h-5"></i>
                </div>
                <div>
                    <h1 class="text-md sm:text-lg font-bold bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">הבוקר הכלכלי</h1>
                    <p class="text-[11px] text-slate-400">איסוף חכם, סינון וניתוח משמעויות מקרו-כלכליות</p>
                </div>
            </div>

            <div class="flex items-center gap-4">
                <div class="bg-slate-900/60 px-3 py-1.5 rounded-full border border-slate-800/80 text-xs text-slate-300">
                    עדכון הבא: מחר ב-08:00
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col gap-8">

        <div class="border-b border-slate-800/60 pb-5">
            <span class="text-xs font-bold text-blue-500 tracking-widest uppercase">סקירת מנהלים יומית</span>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-100 mt-1">גיליון הבוקר הכלכלי</h2>
            <p class="text-xs text-slate-400 mt-1.5 flex items-center gap-1.5">
                <i data-lucide="calendar" class="w-3.5 h-3.5 text-slate-500"></i>
                עודכן בתאריך: <strong class="text-slate-200">{now_str}</strong>
            </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-4 justify-between items-center bg-slate-900/20 border border-slate-800/40 p-4 rounded-2xl">
            <div class="relative w-full sm:w-72">
                <i data-lucide="search" class="w-3.5 h-3.5 text-slate-500 absolute right-3 top-1/2 -translate-y-1/2"></i>
                <input
                    type="text"
                    id="searchInput"
                    oninput="filterNews()"
                    placeholder="חיפוש חופשי בכותרות ובתקצירים..."
                    class="w-full bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 pl-4 pr-9 text-xs focus:outline-none focus:border-blue-500 text-slate-200"
                >
            </div>

            <div class="flex gap-2 w-full sm:w-auto">
                <select id="scopeFilter" onchange="filterNews()" class="bg-slate-950/60 border border-slate-800/60 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none flex-1 sm:flex-none">
                    <option value="all">כל הזירות</option>
                    <option value="global">גלובלי בלבד</option>
                    <option value="local">ישראל בלבד</option>
                </select>

                <select id="importanceFilter" onchange="filterNews()" class="bg-slate-950/60 border border-slate-800/60 text-xs text-slate-300 rounded-xl px-3 py-2 focus:outline-none flex-1 sm:flex-none">
                    <option value="all">כל רמות החשיבות</option>
                    <option value="High">חשיבות עליונה</option>
                    <option value="Medium">חשיבות בינונית</option>
                    <option value="Low">חשיבות נמוכה</option>
                </select>
            </div>
        </div>

        <div id="newsFeed" class="flex flex-col gap-6"></div>

    </main>

    <footer class="border-t border-slate-900 bg-slate-950/40 py-6 text-center text-xs text-slate-500">
        <p>מערכת הבוקר הכלכלי © {current_year}. הופק אוטומטית באמצעות Gemini.</p>
    </footer>

    <script>
        const newsData = {js_news_array};

        function renderNews(newsArray) {{
            const container = document.getElementById("newsFeed");
            container.innerHTML = "";

            if (!Array.isArray(newsArray) || newsArray.length === 0) {{
                container.innerHTML = `
                    <div class="text-center py-12 text-slate-500 border border-slate-800/40 rounded-2xl bg-slate-900/10">
                        <p class="text-xs">לא נמצאו ידיעות מתאימות לפילטרים.</p>
                    </div>
                `;
                return;
            }}

            newsArray.forEach(item => {{
                const importance = item.importance || "Medium";

                const badgeColor =
                    importance === "High"
                        ? "bg-red-500/10 text-red-400 border border-red-500/20"
                        : importance === "Low"
                            ? "bg-slate-500/10 text-slate-400 border border-slate-500/20"
                            : "bg-amber-500/10 text-amber-400 border border-amber-500/20";

                const badgeText =
                    importance === "High"
                        ? "חשיבות עליונה"
                        : importance === "Low"
                            ? "חשיבות נמוכה"
                            : "בינונית";

                const scopeBadge = item.scope === "global"
                    ? `<span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[10px] px-2 py-0.5 rounded-lg font-bold">גלובלי</span>`
                    : `<span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] px-2 py-0.5 rounded-lg font-bold">ישראל</span>`;

                const safeSources = Array.isArray(item.sources) ? item.sources : [];

                const sourcesHtml = safeSources.map(src => {{
                    const srcName = src.name || "מקור";
                    const srcUrl = src.url || "#";

                    return `
                        <a href="${{srcUrl}}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 bg-slate-800/50 hover:bg-slate-800 text-slate-300 border border-slate-700/50 text-[10px] px-2.5 py-0.5 rounded-md transition-all">
                            <i data-lucide="external-link" class="w-2.5 h-2.5 text-slate-400"></i>
                            ${{srcName}}
                        </a>
                    `;
                }}).join("");

                const primaryLink = safeSources[0]?.url || "#";

                const card = document.createElement("div");
                card.className = "bg-slate-900/20 border border-slate-800/40 rounded-2xl p-6 hover:border-slate-800 hover:bg-slate-900/30 transition-all flex flex-col gap-4 group";

                card.innerHTML = `
                    <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/40 pb-3">
                        <div class="flex flex-wrap items-center gap-2">
                            ${{scopeBadge}}
                            <span class="text-[10px] px-2 py-0.5 rounded-lg font-bold ${{badgeColor}}">${{badgeText}}</span>
                            <span class="text-[10px] text-slate-500 font-semibold bg-slate-800/20 px-2 py-0.5 rounded-lg">${{item.category || "כללי"}}</span>
                            <div class="flex flex-wrap items-center gap-1.5 ms-2 border-r border-slate-800 pr-3.5">
                                <span class="text-[10px] text-slate-500">מקורות:</span>
                                ${{sourcesHtml}}
                            </div>
                        </div>

                        <div class="flex items-center gap-1 text-[10px] text-slate-500 font-mono">
                            <i data-lucide="clock" class="w-3 h-3"></i>
                            <span>${{item.publish_time || ""}}</span>
                        </div>
                    </div>

                    <div>
                        <a href="${{primaryLink}}" target="_blank" rel="noopener" class="inline-block group-hover:text-blue-400 transition-colors">
                            <h4 class="text-base sm:text-md font-bold text-slate-100 leading-snug flex items-center gap-2">
                                <span>${{item.title || "ללא כותרת"}}</span>
                                <i data-lucide="external-link" class="w-4 h-4 opacity-0 group-hover:opacity-100 text-blue-500 transition-all"></i>
                            </h4>
                        </a>

                        <p class="text-xs sm:text-sm text-slate-400 leading-relaxed mt-2.5">${{item.summary || ""}}</p>
                    </div>

                    <div class="bg-slate-950/40 border border-slate-800/50 rounded-xl p-4 flex flex-col gap-3">
                        <div class="text-[11px] font-bold text-slate-300 flex items-center gap-1.5 border-b border-slate-900/80 pb-2">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-blue-400"></i>
                            משמעויות והשפעות:
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="border-r-2 border-blue-500/40 p-2 rounded-l">
                                <span class="text-[10px] font-bold text-blue-400 block mb-1">🌍 גלובלי:</span>
                                <p class="text-xs text-slate-300 leading-relaxed">${{item.implication_global || ""}}</p>
                            </div>

                            <div class="border-r-2 border-emerald-500/40 p-2 rounded-l">
                                <span class="text-[10px] font-bold text-emerald-400 block mb-1">🇮🇱 ישראל:</span>
                                <p class="text-xs text-slate-300 leading-relaxed">${{item.implication_local || ""}}</p>
                            </div>
                        </div>
                    </div>
                `;

                container.appendChild(card);
            }});

            lucide.createIcons();
        }}

        function filterNews() {{
            const searchQuery = document.getElementById("searchInput").value.toLowerCase();
            const scopeVal = document.getElementById("scopeFilter").value;
            const importanceVal = document.getElementById("importanceFilter").value;

            const filtered = newsData.filter(item => {{
                const title = (item.title || "").toLowerCase();
                const summary = (item.summary || "").toLowerCase();

                const matchesSearch =
                    title.includes(searchQuery) ||
                    summary.includes(searchQuery);

                const matchesScope =
                    scopeVal === "all" ||
                    item.scope === scopeVal;

                const matchesImportance =
                    importanceVal === "all" ||
                    item.importance === importanceVal;

                return matchesSearch && matchesScope && matchesImportance;
            }});

            renderNews(filtered);
        }}

        window.onload = function() {{
            renderNews(newsData);
        }};
    </script>
</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"קובץ ה-HTML {OUTPUT_FILE} עודכן בהצלחה!")


if __name__ == "__main__":
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("אנא הגדר את מפתח ה-Gemini API שלך בסקריפט או כמשתנה סביבה.")
    else:
        news_data = fetch_real_news_from_gemini()

        if news_data:
            generate_html(news_data)
        else:
            print("שגיאה בקבלת נתונים מה-API. הקובץ לא עודכן.")
```
