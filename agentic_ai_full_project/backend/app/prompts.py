import json

def research_prompt(company, focus, sources):
    bullets = '\n'.join([f"- {s['title']}: {s['url']}" for s in sources])
    return f"Research {company} focusing on {focus}. Use these sources:\n{bullets}\nSummarize top findings and list any conflicts."

def synthesis_prompt(company, findings, conflicts, depth):
    findings_summary = '\n'.join([f"- {f['title']}: {f.get('summary','')[:300]}" for f in findings])
    return f"""
You are a research assistant. Create a structured account plan JSON for {company}.
Depth: {depth}
Findings:
{findings_summary}
Conflicts: {json.dumps(conflicts)}

Return ONLY valid JSON matching this schema keys:
company, date, executive_summary, key_contacts (list of objects), market_overview, product_summary,
financial_highlights (object), swot (object), recommended_actions (list), sources (list of {title,url,date}).
If a fact is unverified, mark it in sources with a note.
"""

def chat_assistant_prompt(user_message):
    return f"You are a helpful research assistant. User: {user_message}\nReply concisely with helpful next steps."