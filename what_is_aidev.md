# What is the AIDev Dataset?

## One Line Definition

> AIDev is a database of 456,535 real pull requests
> written by AI agents on real GitHub projects,
> collected between December 2024 and June 2025.

---

## AIDev vs AIDev-pop

```
AIDEV (Full):                    AIDEV-POP (Popular only):
─────────────────────────        ──────────────────────────────
456,535 PRs                      7,122 PRs
61,453 repositories              856 repositories
ANY star count (even 0)          500+ GitHub stars ONLY
NO code diffs included           HAS code diffs (patch column)
Good for: scale overview         Good for: deep analysis
Bad for:  code analysis          Bad for:  nothing - it's better!

YOUR PROJECT used:
33,596 PRs (100+ stars threshold)
Filtered to 26,760 (4 languages)
→ Matched paper exactly ✅
```

---

## Why the Star Filter Matters

```
WITHOUT FILTER (AIDev Full):
"my-test-project"    0 stars  ← throwaway, nobody uses it
"hello-world-123"    2 stars  ← student learning project
"random-experiment"  5 stars  ← abandoned after 1 week
→ Agent PR merged because owner forgot to close it
→ Tells us NOTHING about real quality

WITH FILTER (AIDev-pop 500+ stars):
"freenet/freenet-core"   2,391 stars ← serious project
"coleam00/mcp-crawl4ai"  1,447 stars ← real users depend on it
"JonasKruckenberg/k23"     515 stars ← maintained by team
→ Agent PR accepted/rejected by REAL developers
→ Results are MEANINGFUL
```

---

## The Nine Tables

```
TABLE               WHAT IT STORES                  USED IN YOUR PAPER?
────────────────    ─────────────────────────────   ───────────────────
pull_request        Each PR (title, state, dates)   ✅ YES
repository          Each repo (name, stars, lang)   ✅ YES
user                Each developer (name, company)  No
pr_comments         Feedback comments on PRs        No
pr_reviews          Formal review decisions         No
pr_commits          Commit metadata                 No
pr_commit_details   ACTUAL CODE DIFFS               ✅ YES (main one!)
pr_timeline         Full event history              No
issue               Original bug/feature requests  No
related_issue       Links PRs to issues             No
```

---

## The Five AI Agents

```
Agent              Company        How Identified in Dataset
─────────────────  ─────────────  ──────────────────────────────
OpenAI Codex       OpenAI         branch starts with "codex/"
Devin              Cognition AI   author = "devin-ai-integration[bot]"
GitHub Copilot     Microsoft      branch starts with "copilot/"
Cursor             Anysphere      branch starts with "cursor/"
Claude Code        Anthropic      body contains "Co-Authored-By: Claude"
```

---

## The Three Numbers Your Paper Found

```
From scanning the patch column of pr_commit_details:

29.5% → PRs that imported any library
         (lines starting with "+" containing "import")

 1.3% → PRs that added brand new dependencies
         (lines starting with "+" in requirements.txt)

75.0% → New dependencies that specified a version
         (lines containing "==" like "numpy==1.26.4")
```

---

## Internal vs External Library

```
INTERNAL (built-in, comes with language):
import os           ← Python built-in
import sys          ← Python built-in
import fmt          ← Go built-in
→ No installation needed
→ Made by language creators
→ Counted SEPARATELY in paper

EXTERNAL (must install separately):
import numpy        ← must pip install numpy
import react        ← must npm install react
import testify      ← must go get testify
→ Published by other developers
→ Listed in requirements.txt/package.json
→ These are what the 29.5% and 1.3% count
```

---

## New Dependency vs Hallucinated Library

```
NEW DEPENDENCY (real):
Agent adds to requirements.txt:
+ requests==2.31.0
→ requests EXISTS on PyPI ✅
→ Has existed since 2011 ✅
→ Just NEW to this project ✅
→ This is what the 1.3% measures

HALLUCINATED (invented):
Agent adds to requirements.txt:
+ super_fast_json_parser
→ Does NOT exist on PyPI ❌
→ Agent made up the name ❌
→ Would crash on installation ❌
→ This is what notebook 05 checks!
```
