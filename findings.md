# My Dissertation Replication Findings

## Paper Replicated
"A Study of Library Usage in Agent-Authored Pull Requests"
Lukas Twist & Jie M. Zhang — King's College London
MSR 2026 Mining Challenge

---

## My Results vs Paper Results

| Finding | Paper Reports | My Replication | Match? |
|---|---|---|---|
| Library import rate | 29.5% | 29.48% | ✅ |
| New dependency rate | 1.3% | 1.29% | ✅ |
| Version pinning rate | 75.0% | 75.0% | ✅ |

All three headline numbers match within 0.1% ✅

---

## What Each Number Means

### 29.5% — Library Import Rate

Out of 26,760 agent PRs analysed:
- 7,888 PRs imported at least one library
- The agent wrote lines like `import numpy as np`
- Found by scanning + lines in pr_commit_details patch column

**By language:**
| Language | Import Rate |
|---|---|
| C# | 45.5% — highest |
| TypeScript | 40.0% |
| Python | 37.8% |
| Go | 12.6% — lowest |

### 1.3% — New Dependency Rate

Out of 26,760 agent PRs:
- Only 345 PRs added a brand new library to requirements.txt
- Agents are conservative — mostly use existing libraries
- Found by scanning + lines in requirements.txt/package.json

**By language:**
| Language | New Dep Rate |
|---|---|
| C# | 6.1% |
| Python | 2.8% |
| Go | 0.2% |
| TypeScript | 0.1% |

### 75.0% — Version Pinning Rate

Of the 345 PRs that added new dependencies:
- 258 specified an exact version number (e.g. requests==2.31.0)
- 87 did NOT specify a version (just wrote the name)
- Agents are 8x better than chatbots (which only do 9%)

---

## My Original Contributions

### 1. Rust Analysis (paper excluded Rust)

The paper only covered 4 languages. I computed Rust:

| Metric | Rust Result |
|---|---|
| Total Rust PRs | 1,079 |
| Standard library usage | 0% ← unusual! |
| New dependencies | 1 PR out of 1,079 |
| Version pinning | 100% (of that 1 PR) |

**Finding:** Rust agents show completely different behaviour.
They never use Rust's standard library (via `use std::`)
and almost never add new dependencies.

This could be because:
- Rust's internal workspace crates look like external ones
- Rust's `use` syntax differs from `import`
- Rust developers rarely add new crates in individual PRs

### 2. Hallucination Check (notebook 05)

The paper's conclusion explicitly called for this as future work:
> "Do agents reproduce known LLM failure modes,
>  such as hallucinating library names?"

I built notebook 05 to check whether new dependencies
actually exist on real package registries (PyPI, npm, etc.)

**Method:**
- Take each new dependency from the output JSON files
- Query the real registry API
- Flag any that return 404 (not found)

---

## Dataset Used

**AIDev-pop (100+ star repositories)**
- Downloaded from: https://huggingface.co/datasets/hao-li/AIDev
- Pinned version: commit eee0408a277826d88fc0ca5fa07d2fc325c96af1
- Files: pull_request.parquet, repository.parquet, pr_commit_details.parquet
- Size: 33,596 PRs, 2,807 repos, 711,923 commit rows

**After filtering to 4 languages:**
- 26,760 PRs (matches paper exactly ✅)

---

## How to Run the Analysis

```bash
# 1. Clone the original paper's code
git clone https://github.com/itsluketwist/agent-library-usage
cd agent-library-usage

# 2. Set up environment
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e .

# 3. Run notebooks in order
jupyter lab
# Then run 01 → 02 → 03 → 04 → 05
```

---

## Key Connections to AIDev Paper

The AIDev paper (Ashkan's paper) found:
- Agents are accepted 38-65% vs human 76.8% (Finding #2)
- Agents are 10-13x faster than humans (Finding #5)

My paper adds:
- When agents write code, 29.5% uses a library
- They rarely add new ones (1.3%)
- When they do, 75% include a version number
- This is responsible dependency management
- But the 25% without versions could contribute to rejections
