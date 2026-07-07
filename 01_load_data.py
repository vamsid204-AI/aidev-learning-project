"""
SCRIPT 01 — Load and Understand the Dataset
============================================
This script loads our sample AIDev data and shows
you what each column means, with real examples.

Run from the project root:
    python analysis/01_load_data.py
"""

import pandas as pd
from pathlib import Path

# ── Load the data ──────────────────────────────────────────
data_path = Path("data/sample_prs.csv")
df = pd.read_csv(data_path)

print("=" * 60)
print("STEP 1: WHAT DOES THE DATASET LOOK LIKE?")
print("=" * 60)
print(f"\nTotal rows (PRs): {len(df)}")
print(f"Columns: {list(df.columns)}")

# ── Show what each column means ────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: WHAT DOES EACH COLUMN MEAN?")
print("=" * 60)

column_explanations = {
    "pr_id":      "Unique ID number for this PR",
    "title":      "What the agent called its change",
    "agent":      "Which AI wrote this PR",
    "state":      "merged=accepted ✅  closed=rejected ❌",
    "created_at": "When agent opened the PR",
    "closed_at":  "When PR was accepted or rejected",
    "merged_at":  "When accepted (NULL if rejected)",
    "repo_name":  "Which GitHub project",
    "repo_stars": "How popular the project is",
    "filename":   "Which file was changed",
    "patch":      "ACTUAL code the agent wrote (+ = added)"
}

for col, explanation in column_explanations.items():
    print(f"\n  {col}:")
    print(f"  → {explanation}")
    sample = df[col].dropna().iloc[0]
    if col == "patch":
        print(f"  → Example: (see below)")
    else:
        print(f"  → Example: '{sample}'")

# ── Show one complete PR ────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: ONE COMPLETE REAL PR EXPLAINED")
print("=" * 60)

pr = df[df["pr_id"] == 1002].iloc[0]

print(f"""
PR ID:      {pr['pr_id']}
Title:      {pr['title']}
Agent:      {pr['agent']}
State:      {pr['state']}
Created:    {pr['created_at']}
Merged:     {pr['merged_at']}
Repository: {pr['repo_name']} ({pr['repo_stars']} stars)
File:       {pr['filename']}

What the agent actually wrote (patch):
{pr['patch']}

Reading the patch:
→ Lines starting with + = agent ADDED this code
→ Lines starting with - = agent REMOVED code
→ Lines with space     = code that already existed
""")

# ── Show accepted vs rejected ──────────────────────────────
print("=" * 60)
print("STEP 4: ACCEPTED vs REJECTED PRs")
print("=" * 60)

accepted = df[df["state"] == "merged"]
rejected = df[df["state"] == "closed"]

print(f"\nTotal PRs: {len(df)}")
print(f"Accepted (merged): {len(accepted)} "
      f"({len(accepted)/len(df)*100:.1f}%)")
print(f"Rejected (closed): {len(rejected)} "
      f"({len(rejected)/len(df)*100:.1f}%)")

print("\nAccepted PR examples:")
for _, row in accepted.head(3).iterrows():
    print(f"  ✅ PR {row['pr_id']}: '{row['title']}' "
          f"by {row['agent']}")

print("\nRejected PR examples:")
for _, row in rejected.head(3).iterrows():
    print(f"  ❌ PR {row['pr_id']}: '{row['title']}' "
          f"by {row['agent']}")

# ── Show agents ────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: WHICH AGENTS ARE IN THE DATA?")
print("=" * 60)

agent_counts = df["agent"].value_counts()
print()
for agent, count in agent_counts.items():
    bar = "█" * count
    print(f"  {agent:<25} {count:>2} PRs  {bar}")

print("\nThis mirrors the real AIDev dataset:")
print("  OpenAI Codex   → 411,621 PRs")
print("  Devin          →  24,893 PRs")
print("  GitHub Copilot →  16,531 PRs")
print("  Cursor         →   1,981 PRs")
print("  Claude Code    →   1,509 PRs")
