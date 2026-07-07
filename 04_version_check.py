"""
SCRIPT 04 — Check Version Pinning
====================================
This checks: when agents add new dependencies,
do they specify a version number?

This is RQ2 from the Twist & Zhang paper:
→ 1.3% of PRs add new dependencies
→ Of those, 75% specify a version number

Run: python analysis/04_version_check.py
"""

import pandas as pd
from pathlib import Path

df = pd.read_csv(Path("data/sample_prs.csv"))

# ── Explain the concept first ──────────────────────────────
print("=" * 60)
print("VERSION PINNING CHECK")
print("RQ2 from Twist & Zhang paper")
print("=" * 60)

print("""
WHAT IS VERSION PINNING?

When adding a new library to requirements.txt:

WITHOUT version (RISKY ❌):
    requests
    pandas
    → Installs whatever latest version is available
    → Code might break if library updates

WITH version (SAFE ✅):
    requests==2.31.0
    pandas==2.2.2
    → Always installs exactly this version
    → Code behaves consistently forever

The paper found:
→ Agents: 75% specify version  ← good!
→ Chatbots: only 9% specify    ← bad!
→ Agents are 8x better than chatbots
""")

# ── Find requirements.txt changes ─────────────────────────
req_rows = df[
    df['filename'].isin(['requirements.txt', 'package.json',
                         'go.mod', 'pyproject.toml'])
].copy()

print("=" * 60)
print("SCANNING REQUIREMENTS.TXT CHANGES")
print("=" * 60)
print()

new_deps_found = []

for _, row in req_rows.iterrows():
    patch = row['patch']
    if not isinstance(patch, str):
        continue

    print(f"PR {row['pr_id']} | {row['filename']} | {row['agent']}")
    print(f"Patch content:")

    for line in patch.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            dep_line = line[1:].strip()
            if not dep_line or dep_line.startswith('#'):
                continue

            # Check for version specifiers
            has_version = any(
                op in dep_line
                for op in ['==', '>=', '<=', '~=', '!=', '>']
            )

            status = "✅ HAS version" if has_version else "❌ NO version"
            print(f"  {line}  →  {dep_line:<30} {status}")

            new_deps_found.append({
                'pr_id': row['pr_id'],
                'agent': row['agent'],
                'library': dep_line.split('==')[0].split('>=')[0].strip(),
                'full_entry': dep_line,
                'has_version': has_version
            })
    print()

# ── Calculate the numbers ──────────────────────────────────
print("=" * 60)
print("THE CALCULATIONS")
print("=" * 60)

total_prs = len(df['pr_id'].unique())
prs_with_new_dep = len(req_rows['pr_id'].unique())
pct_new_dep = prs_with_new_dep / total_prs * 100

print(f"""
NUMBER 1 — New Dependency Rate (1.3%):
  Total unique PRs:             {total_prs}
  PRs touching requirements:    {prs_with_new_dep}
  Percentage:                   {pct_new_dep:.1f}%
  Paper says:                   1.3%
""")

if new_deps_found:
    deps_df = pd.DataFrame(new_deps_found)
    total_deps = len(deps_df)
    versioned = deps_df['has_version'].sum()
    pct_versioned = versioned / total_deps * 100

    print(f"""NUMBER 2 — Version Pinning Rate (75%):
  Total new dependency lines:   {total_deps}
  Lines WITH version number:    {versioned}
  Percentage:                   {pct_versioned:.1f}%
  Paper says:                   75.0%

  Individual results:""")

    for _, row in deps_df.iterrows():
        status = "✅" if row['has_version'] else "❌"
        print(f"    {status} PR {row['pr_id']:4d} | "
              f"{row['agent']:<25} | {row['full_entry']}")

# ── Show language breakdown ────────────────────────────────
print(f"""
REAL PAPER BREAKDOWN BY LANGUAGE:

Language    New dep PRs    Version rate
──────────  ───────────    ────────────
TypeScript  9   (0.1%)     100% ← perfect always
Go          16  (0.2%)     100% ← perfect always
Python      200 (2.8%)     82.5%
C#          120 (6.1%)     46.9% ← weakest
──────────  ───────────    ────────────
Overall     345 (1.3%)     75.0%

The numbers mean:
→ TypeScript agents ALWAYS pin versions ✅
→ C# agents only pin versions HALF the time ⚠️
→ Overall still 8x better than chatbots (9%)
""")

# ── Chatbot vs agent comparison ────────────────────────────
print("=" * 60)
print("CHATBOT vs AGENT COMPARISON")
print("=" * 60)
print("""
CHATBOT (e.g. asking ChatGPT):
User: "how do I make an HTTP request in Python?"
ChatGPT: "pip install requests" ← no version ❌

AGENT (e.g. Devin, Claude Code):
Agent reads requirements.txt
Sees project already pins versions like: flask==2.3.0
Agent adds:  requests==2.31.0  ← matches project style ✅

WHY agents are better:
→ Agent sees the REAL project files
→ Agent copies the versioning pattern already there
→ Chatbot answers in isolation with no context
→ Context = better version discipline
""")
