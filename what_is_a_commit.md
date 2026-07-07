# What is a Commit?

## Simple Definition

A commit is a SAVED SNAPSHOT of code changes with a message
explaining what was changed and why.

Like saving a Word document with a version name:
```
essay_draft1.docx           → commit: "initial draft"
essay_draft2.docx           → commit: "add introduction"
essay_final.docx            → commit: "fix grammar errors"
```

---

## What a Commit Contains

```
COMMIT:
sha:     abc123def456        ← unique ID (like a fingerprint)
author:  devin-ai-integration[bot]
message: "Add llms.txt compilation system for AI model"
pr_id:   3271196926          ← which PR this belongs to

CODE CHANGES (the patch):
+ import numpy as np         ← line ADDED (starts with +)
+ import pandas as pd        ← line ADDED
- old_function = None        ← line REMOVED (starts with -)
  existing_code              ← unchanged (starts with space)
```

---

## The Patch Column — Most Important

The patch column is the ACTUAL code the agent wrote.

```
Real patch from your dataset:

"  def process_data(df):
+     import numpy as np        ← ADDED: numpy import
+     import pandas as pd       ← ADDED: pandas import
+     result = np.mean(df)      ← ADDED: new code
-     old_calc = sum(df)/len(df)← REMOVED: old code
   return result               ← unchanged"
```

The paper's analysis ONLY looked at lines starting with +
Because those are what the AGENT actually wrote

```
+ import numpy as np    → agent added this → count it! ✅
- import old_lib        → agent removed this → skip ❌
  existing code         → not changed → skip ❌
```

---

## Commit vs Pull Request

```
PULL REQUEST:
→ The overall proposal
→ Contains MULTIPLE commits
→ One PR can have many commits inside it

Example PR: "Add data analysis feature"
  ├── Commit 1: "Add numpy import"
  ├── Commit 2: "Add data processing function"
  └── Commit 3: "Add unit tests"

COMMIT:
→ One specific saved change
→ Part of a larger PR
→ Has author, message, code diff
```

---

## In the AIDev Dataset

Stored in pr_commit_details table:

```
sha:                   abc123
pr_id:                 1002
author:                devin-ai-integration[bot]
filename:              analysis.py
additions:             3      ← 3 lines added
deletions:             0      ← 0 lines removed
patch:                 "+ import numpy as np
                        + import pandas as pd
                        + result = np.mean(data)"
```

This is the table your paper analysed!
711,923 rows → scanned every patch → found 29.5% import rate
