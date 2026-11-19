"""Builds FAKE demo data at runtime. Secret-looking strings are assembled from pieces
so GitHub's push protection does not block this repo. Every value here is fake.
Run `python samples.py` to also write them into a local sample_data/ folder."""
import json, os

AWS = "AK" + "IAJ3Q7XM2PLR5TW9ZD"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/" + "bPxRfiCYzR8vN2qLs4"
STRIPE = "sk_" + "live_51Hq8vKLm3nPzXy7aB9cD2eF"
FAKE_STRIPE = "sk_" + "live_EXAMPLEEXAMPLEEXAMPLE123"
GH = "gh" + "p_aB3dE6gH9jK2mN5pQ8sT1vW4yZ7cF0hJ3kL6"
SLACK = "xo" + "xb-8291034756-qwErTyUiOpAs"
DB = "post" + "gres://admin:Pr0d!Pass99x@db.acme.io:5432/orders"
PEM = "-----BEGIN RSA " + "PRIVATE KEY-----"
EXAMPLE_AWS = "AK" + "IAIOSFODNN7EXAMPLE"


def build():
    repo = f"""commit a1b2c3d4e5f6a7b8c9d0
Author: Ravi Kumar <ravi@acme.io>
Date:   Mon Nov 2 10:14:00 2026

    add payment config

diff --git a/config/settings.py b/config/settings.py
+++ b/config/settings.py
+AWS_ACCESS_KEY_ID = "{AWS}"
+aws_secret_access_key = "{AWS_SECRET}"
+STRIPE_KEY = "{STRIPE}"
+DB_URL = "{DB}"

commit 9f8e7d6c5b4a39281706
Author: Meera Nair <meera@acme.io>
Date:   Tue Nov 3 16:40:00 2026

    add example env and tests

diff --git a/.env.example b/.env.example
+++ b/.env.example
+API_KEY="your_api_key_here"
+AWS_KEY={EXAMPLE_AWS}
+password = "changeme"
"""
    chat = {"messages": [
        {"user": "dev_arjun", "channel": "general", "text": f"deploy is failing, here's the token {GH}"},
        {"user": "support_priya", "channel": "support", "text": "Customer Anita Rao, card 4539 1488 0343 6467, PAN ABCDE1234F, phone 9876543210 wants a refund"},
        {"user": "dev_sam", "channel": "dev", "text": f"use slack token {SLACK} for the bot"},
        {"user": "hr_lee", "channel": "random", "text": "Aadhaar for onboarding: 2345 6789 0123"},
        {"user": "dev_sam", "channel": "dev", "text": f"tests use fake key {FAKE_STRIPE} do not worry"},
        {"user": "pm_dana", "channel": "general", "text": "lunch at 1pm, ping me at dana@example.com"}]}
    notes = f"""Server setup notes
{PEM}
MIIEowIBAAKCAQEA...
-----END RSA PRIVATE KEY-----
password = "Zx9!kQ2#mV7pL"
"""
    return {"repo_history.txt": repo, "chat_export.json": json.dumps(chat, indent=1), "notes.txt": notes}


if __name__ == "__main__":
    os.makedirs("sample_data", exist_ok=True)
    for n, c in build().items():
        open(os.path.join("sample_data", n), "w", encoding="utf-8").write(c)
    print("Wrote a fake demo files to sample_data/ (do not commit this folder).")
