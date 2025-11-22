import os, json, re
from .prompts import research_prompt, synthesis_prompt, chat_assistant_prompt
from .tools import run_web_search, ingest_local_pdf, call_openai_chat
DATA_FILE_PATH = "/mnt/data/AI Agent Building Assignment - Eightfold.pdf"

class CompanyResearchAgent:
    def __init__(self):
        self.local_doc_path = DATA_FILE_PATH if os.path.exists(DATA_FILE_PATH) else None

    async def handle_user_message(self, message, company=None, focus='overview', depth='standard'):
        msg_lower = (message or '').lower()
        if company or 'research' in msg_lower or 'account plan' in msg_lower:
            target = company or message
            result = await self.run_research(target, focus=focus, depth=depth)
            return f"I ran research and prepared an account plan. Summary: {result['account_plan_summary']}"
        prompt = chat_assistant_prompt(message)
        out = call_openai_chat(prompt)
        return out

    async def run_research(self, company, focus='overview', depth='standard'):
        search_results = run_web_search(company, focus=focus, top_k=5)
        findings = []
        for r in search_results:
            findings.append({"title": r['title'], "url": r['url'], "summary": r['snippet']})
        if self.local_doc_path:
            text = ingest_local_pdf(self.local_doc_path)
            findings.append({"title":"Uploaded Assignment PDF", "url": self.local_doc_path, "summary": text[:800]})
        conflicts = self._detect_conflicts(findings)
        prompt = synthesis_prompt(company, findings, conflicts, depth)
        plan_json = call_openai_chat(prompt, expect_json=True)
        summary_prompt = f"Summarize the following account plan into 3 concise bullets:\n{json.dumps(plan_json)}"
        summary = call_openai_chat(summary_prompt)
        return {"company": company, "findings": findings, "conflicts": conflicts, "account_plan": plan_json, "account_plan_summary": summary}

    def _detect_conflicts(self, findings):
        nums = {}
        for f in findings:
            matches = re.findall(r"\$?\d[\d,]+(?:\.\d+)?", f.get('summary',''))
            if matches:
                nums[f['title']] = matches
        if len(nums) > 1:
            return {"detected": True, "details": nums}
        return {"detected": False}
