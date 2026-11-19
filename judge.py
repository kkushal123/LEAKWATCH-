"""Decide whether each hit is a real leak or a test placeholder.
Uses Claude if ANTHROPIC_API_KEY is set; otherwise a built-in heuristic."""
import json, os, re
from scanner import entropy

PLACEHOLDER = re.compile(r"(?i)example|sample|dummy|changeme|placeholder|your[_-]|<.*>|xxxx|fake|test|todo|1234|abcd|redacted|\$\{|process\.env|os\.environ")


def heuristic(f):
    ctx = f["line"] + " " + f["raw"]
    if PLACEHOLDER.search(ctx) and f["kind"] == "secret":
        return {"verdict": "placeholder", "confidence": 0.8, "reason": "Contains placeholder/test wording."}
    if f["type"] == "Hardcoded Password":
        val = re.search(r"['\"]([^'\"]+)['\"]", f["raw"])
        if val and entropy(val.group(1)) < 2.2:
            return {"verdict": "placeholder", "confidence": 0.6, "reason": "Low-entropy value, likely a dummy."}
    if f["type"] == "Email Address" and re.search(r"@(example|test)\.", f["raw"]):
        return {"verdict": "placeholder", "confidence": 0.9, "reason": "Reserved example domain."}
    return {"verdict": "real", "confidence": 0.7, "reason": "Matches a known format with no placeholder signals."}


def llm_judge(findings):
    import anthropic
    client = anthropic.Anthropic()
    items = [{"id": i, "type": f["type"], "line": f["line"], "file": f["file"]} for i, f in enumerate(findings)]
    prompt = ("You are a security triage assistant. For each item decide whether the matched text is a REAL "
              "leaked secret/personal data or a TEST PLACEHOLDER/dummy/example. Reply ONLY with a JSON list of "
              '{"id":int,"verdict":"real"|"placeholder","confidence":0-1,"reason":"short"}.\n' + json.dumps(items))
    msg = client.messages.create(model=os.getenv("LEAKWATCH_MODEL", "claude-sonnet-4-6"), max_tokens=4000,
                                 messages=[{"role": "user", "content": prompt}])
    text = re.sub(r"```json|```", "", msg.content[0].text).strip()
    return {d["id"]: d for d in json.loads(text)}


def judge_all(findings):
    llm = {}
    if os.getenv("ANTHROPIC_API_KEY") and findings:
        try:
            for s in range(0, len(findings), 40):
                chunk = findings[s:s + 40]
                for k, v in llm_judge(chunk).items(): llm[s + k] = v
        except Exception as e:
            print("LLM judge has failed, using heuristic:", e)
    for i, f in enumerate(findings):
        j = llm.get(i) or heuristic(f)
        f["verdict"], f["confidence"], f["reason"] = j["verdict"], j["confidence"], j["reason"]
        f["judged_by"] = "llm" if i in llm else "heuristic"
    return findings
