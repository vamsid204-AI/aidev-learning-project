# AIDev Learning Project 🤖

A beginner-friendly project to understand the AIDev dataset
and GitHub concepts (commits, issues, pull requests, reviews).

**Based on:**
> "A Study of Library Usage in Agent-Authored Pull Requests"
> Lukas Twist & Jie M. Zhang — King's College London
> MSR 2026 Mining Challenge

**Student:** Vamsi | Edinburgh Napier University | MSc Dissertation

---

## What This Project Teaches

### GitHub Concepts
| Concept | What It Is | Real Example |
|---|---|---|
| Repository | A project folder on GitHub | This project |
| Commit | A saved change with a message | "Add PR analyser script" |
| Issue | A task or question to solve | "Add acceptance rate chart" |
| Pull Request | Proposed code changes | Merging a new feature branch |
| Review | Feedback on a pull request | "Looks good, please add tests" |
| Comment | A note on code or PR | "Why did you use this library?" |
| Branch | A separate version to work on | `feature/add-chart` |
| Merge | Combining a branch into main | Accepting a pull request |

### AIDev Dataset Concepts
| Concept | Meaning | Your Data |
|---|---|---|
| AIDev Full | All 456,535 agent PRs | Any GitHub repo |
| AIDev-pop | Popular repos only | 500+ stars filter |
| pr_commit_details | Actual code changes | patch column |
| patch column | Lines agent added/removed | + means added |
| New dependency | New library added to project | requirements.txt |
| Version pinning | Specifying exact version | requests==2.31.0 |

---

## Project Structure

```
aidev-learning-project/
│
├── README.md              ← You are here
│
├── data/
│   └── sample_prs.csv     ← Mini version of AIDev dataset
│
├── concepts/
│   ├── what_is_a_pr.md    ← Pull request explained
│   ├── what_is_a_commit.md← Commit explained
│   └── what_is_aidev.md   ← AIDev dataset explained
│
├── analysis/
│   ├── 01_load_data.py    ← Load and show the dataset
│   ├── 02_acceptance_rate.py ← Calculate acceptance rates
│   ├── 03_library_check.py← Check library imports in patches
│   └── 04_version_check.py← Check version pinning
│
└── results/
    └── findings.md        ← What we found
```

---

## The Three Headline Numbers

These came from YOUR replication of the paper:

```
29.5%  of PRs imported at least one library
 1.3%  of PRs added a brand new dependency
75.0%  of new dependencies specified a version number
```

---

## Quick Links

- Paper: https://arxiv.org/pdf/2512.11589
- Code:  https://github.com/itsluketwist/agent-library-usage
- Data:  https://huggingface.co/datasets/hao-li/AIDev
- My dissertation replication results: see results/findings.md
