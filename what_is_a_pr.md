# What is a Pull Request (PR)?

## Simple Definition

A Pull Request is a PROPOSAL to add code changes to a project.

Think of it like submitting an essay to a teacher:
```
YOU write an essay          → AI agent writes code
YOU submit it               → Agent opens a Pull Request
TEACHER reviews it          → Human developer reviews it
TEACHER accepts it          → PR gets MERGED ✅
TEACHER rejects it          → PR gets CLOSED ❌
```

---

## The Life of a Pull Request

```
STEP 1: CREATE (opened)
Agent writes code on a separate branch
Agent submits it as a Pull Request
State = OPEN

STEP 2: REVIEW
Human developer reads the changes
They can:
→ Leave COMMENTS (questions, suggestions)
→ Submit a REVIEW (approve or request changes)
→ Ask for more changes

STEP 3: OUTCOME
Either:
→ MERGED   = accepted, code added to project ✅
             merged_at column has a date
→ CLOSED   = rejected, code not used ❌
             merged_at column is NULL

STEP 4: DONE
Issue that triggered PR gets closed automatically
```

---

## In the AIDev Dataset

Each PR is one row in the pull_request table:

```
pr_id:      1001
title:      "Fix login bug"
agent:      Claude_Code
state:      merged
created_at: 2025-03-15 09:00
merged_at:  2025-03-15 11:00  ← has a date = ACCEPTED ✅
closed_at:  2025-03-15 11:00
```

vs a rejected PR:

```
pr_id:      1005
title:      "Fix payment error"
agent:      GitHub_Copilot
state:      closed
created_at: 2025-03-01 09:00
merged_at:  NULL              ← no date = REJECTED ❌
closed_at:  2025-03-05 17:00
```

---

## Turnaround Time

How long the PR took = closed_at - created_at

```
PR 1001 (Claude Code, accepted):
closed_at:  2025-03-15 11:00
created_at: 2025-03-15 09:00
Turnaround: 2 hours

PR 1005 (Copilot, rejected):
closed_at:  2025-03-05 17:00
created_at: 2025-03-01 09:00
Turnaround: 4 days 8 hours
```

Key finding from the paper:
- Agents are FASTER than humans at completing PRs
- But LESS LIKELY to be accepted
