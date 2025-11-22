import os, json, re
from PyPDF2 import PdfReader

def run_web_search(query, focus='overview', top_k=5):
    qslug = query.lower().replace(' ', '') if query else 'unknown'
    return [
        {"title": f"{query} - Official", "url": f"https://{qslug}.example.com", "snippet": f"Official site snippet for {query}."},
        {"title": f"News: {query}", "url": f"https://news.example.com/{qslug}", "snippet": f"Recent news mentioning revenue $12,345 for {query}."}
    ][:top_k]

def ingest_local_pdf(path):
    if not os.path.exists(path):
        return None
    try:
        reader = PdfReader(path)
        texts = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                texts.append(t)
        return '\\n\\n'.join(texts)
    except Exception as e:
        return f"(Failed to extract PDF: {e})"

def call_openai_chat(prompt, expect_json=False):
    import os, json
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        if expect_json:
            return {
                "company": "DemoCo",
                "date": "2025-11-22",
                "executive_summary": "Demo executive summary.",
                "key_contacts": [],
                "market_overview": "Demo market overview.",
                "product_summary": "Demo product summary.",
                "financial_highlights": {},
                "swot": {},
                "recommended_actions": [],
                "sources": []
            }
        return "(stub) This is a demo response because OPENAI_API_KEY is not set."
    try:
        import openai
        openai.api_key = key
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{"role":"system","content":"You are a helpful company research assistant."},{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=800,
        )
        text = resp['choices'][0]['message']['content']
        if expect_json:
            try:
                return json.loads(text)
            except Exception:
                return {"note":"failed_to_parse_json","raw":text}
        return text
    except Exception as e:
        return f"(openai call failed: {e})"
