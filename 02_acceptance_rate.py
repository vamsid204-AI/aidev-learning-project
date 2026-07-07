"""
SCRIPT 02 — Calculate Acceptance Rates
========================================
This shows which agents get their PRs accepted most often.
Connects to Finding #2 from the AIDev paper:
"Agents lag humans in PR acceptance rates"

Run: python analysis/02_acceptance_rate.py
"""

import pandas as pd
from pathlib import Path

df = pd.read_csv(Path("data/sample_prs.csv"))

# Only look at one row per PR (not per file)
pr_df = df.drop_duplicates(subset="pr_id")

print("=" * 60)
print("ACCEPTANCE RATE BY AGENT")
print("Finding #2 from AIDev paper")
print("=" * 60)

print("""
What is acceptance rate?
→ Out of all PRs an agent submitted
→ What % were actually merged (accepted)?

How calculated:
→ Count PRs where merged_at is NOT null = accepted
→ Divide by total PRs from that agent
→ Multiply by 100
""")

# ── Calculate per agent ────────────────────────────────────
results = []
for agent in pr_df["agent"].unique():
    agent_prs = pr_df[pr_df["agent"] == agent]
    total = len(agent_prs)
    accepted = len(agent_prs[agent_prs["state"] == "merged"])
    rate = accepted / total * 100
    results.append({
        "agent": agent,
        "total": total,
        "accepted": accepted,
        "rate": rate
    })

results_df = pd.DataFrame(results).sort_values(
    "rate", ascending=False
)

print("Results from our sample data:")
print()
for _, row in results_df.iterrows():
    bar_full = "█" * int(row["rate"] / 10)
    bar_empty = "░" * (10 - int(row["rate"] / 10))
    print(f"  {row['agent']:<25} "
          f"{row['accepted']}/{row['total']} PRs  "
          f"{row['rate']:>5.1f}%  "
          f"{bar_full}{bar_empty}")

# ── Compare to real paper numbers ─────────────────────────
print("\n" + "=" * 60)
print("COMPARING TO REAL PAPER NUMBERS")
print("=" * 60)

print("""
REAL AIDev Paper findings (Table 5):

Agent           Real Acceptance Rate
─────────────   ────────────────────
Human           76.8%  ← baseline
OpenAI Codex    65.3%  ← 11% below human
Devin           48.9%  ← 27% below human
Cursor          51.4%  ← 25% below human
Claude Code     52.5%  ← 24% below human
GitHub Copilot  38.2%  ← 38% below human ← WORST

Key finding:
ALL agents are accepted LESS OFTEN than humans
Even the best agent (Codex) is 11% below human

Why?
→ Agents pass lab benchmarks (SWE-bench: 70%+)
→ But real developers trust them less
→ Real PRs need style, conventions, maintainability
→ Not just "does the code run?"
""")

# ── Calculate turnaround time ──────────────────────────────
print("=" * 60)
print("TURNAROUND TIME")
print("=" * 60)

print("""
Turnaround time = closed_at - created_at

This measures HOW LONG until a decision was made
(accepted OR rejected)
""")

pr_df = pr_df.copy()
pr_df["created_dt"] = pd.to_datetime(pr_df["created_at"])
pr_df["closed_dt"] = pd.to_datetime(pr_df["closed_at"])
pr_df["turnaround_hours"] = (
    pr_df["closed_dt"] - pr_df["created_dt"]
).dt.total_seconds() / 3600

for _, row in pr_df.iterrows():
    status = "✅ ACCEPTED" if row["state"] == "merged" else "❌ REJECTED"
    hours = row["turnaround_hours"]
    if hours < 24:
        time_str = f"{hours:.1f} hours"
    else:
        time_str = f"{hours/24:.1f} days"
    print(f"  PR {row['pr_id']:4d} | {row['agent']:<25} | "
          f"{status} | {time_str}")

print("""
Real paper findings (Table 5):
→ OpenAI Codex accepted in 0.3 hours (18 minutes!)
→ Human accepted in 3.9 hours
→ GitHub Copilot accepted in 17.2 hours (SLOWEST)
→ Codex is 13x faster than humans to get merged
""")
