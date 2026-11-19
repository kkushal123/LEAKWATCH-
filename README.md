# LeakWatch: Secrets and Sensitive Data Leakage Monitor

> An AI-assisted agent that finds leaked secrets and personal data in repositories and team chats, filters out false alarms, and tells you exactly how to fix each leak.

## The problem
Developers accidentally commit API keys and passwords, and employees paste customer data into team chat. Exposed secrets can be exploited within minutes. Existing scanners drown teams in false positives, and teams often don't know what to do once a leak is found.

## What LeakWatch does
1. **Ingests** a repository history, a chat-channel export (JSON), or plain text files.
2. **Scans** with secret-detection patterns (AWS, GitHub, Slack, Stripe, Google keys, private keys, database URLs, JWTs, hardcoded passwords) and personal-data rules (credit cards with Luhn check, Aadhaar, PAN, SSN, phone numbers, emails).
3. **Judges** every hit with an LLM to decide whether it is a real secret or a test placeholder. A built-in heuristic is used if no API key is set.
4. **Assigns severity** from the secret type and how widely it has been exposed (for example, posted in #general or committed to git history ranks higher).
5. **Alerts the owner** for high and critical leaks.
6. **Generates a remediation checklist** (rotate, purge, notify) for each leak.
7. **Simulates remediation only after human approval.** Nothing real is changed.
8. **Outputs** a dashboard and a downloadable JSON leak report.

Optional extension: a **pre-commit hook** that blocks commits containing real secrets.

## Tech stack
Python, Flask, Anthropic Claude API , HTML/CSS/JavaScript dashboard.

## Quick start
```bash
git clone https://github.com/<your-username>/leakwatch.git
cd leakwatch
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...        

python app.py
```
The app opens in your browser. Click **Try with sample data** to see it work immediately, or upload your own files.

On Windows you can also double-click `run.bat`.

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Flask server and API |
| `scanner.py` | Detection rules and file parsers |
| `judge.py` | LLM judge with heuristic fallback |
| `remediation.py` | Checklists, owner alerts, simulated fixes |
| `precommit_hook.py` | Optional git pre-commit hook |
| `templates/index.html` | Dashboard |
| `samples.py` | Builds fake demo data at runtime (`python samples.py` writes it to `sample_data/`) |



## Safety by design
- Raw secrets are never sent to the browser. Only masked values are displayed.
- Remediation is simulated and requires explicit approval.
- All demo secrets in `samples.py` are fake and assembled at runtime so GitHub push protection is not triggered.

## Future work
Live Slack and GitHub integrations, real key-rotation connectors, scheduled scans, and team notifications by email.

## License
MIT
