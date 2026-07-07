"""
SCRIPT 03 — Check Library Imports in Patches
==============================================
This is the CORE of the Twist & Zhang paper.
We scan the patch column looking for import statements
in lines starting with "+" (lines the agent ADDED).

This is exactly what src/extractors/python.py does
in the real project at:
https://github.com/itsluketwist/agent-library-usage

Run: python analysis/03_library_check.py
"""

import pandas as pd
import re
from pathlib import Path

df = pd.read_csv(Path("data/sample_prs.csv"))

# ── Define what counts as standard vs external ─────────────
PYTHON_STANDARD_LIBS = {
    "os", "sys", "json", "re", "math", "time",
    "datetime", "pathlib", "collections", "itertools",
    "typing", "unittest", "logging", "subprocess",
    "io", "abc", "copy", "functools", "random"
}

def extract_imports_from_patch(patch_text, filename):
    """
    Scan a code diff (patch) for library imports.

    ONLY looks at lines starting with + because:
    + = agent ADDED this line
    - = agent REMOVED (skip)
    space = unchanged (skip)

    This is the exact same logic as the paper's extractors.
    """
    if not isinstance(patch_text, str):
        return [], []

    # Only process Python files for this demo
    if not filename.endswith('.py'):
        return [], []

    standard_libs = []
    external_libs = []

    for line in patch_text.split('\n'):
        # Only look at lines the agent ADDED
        if not line.startswith('+'):
            continue

        # Remove the + sign
        code = line[1:].strip()

        # Skip empty lines and comments
        if not code or code.startswith('#'):
            continue

        # Check for: import numpy
        if code.startswith('import '):
            parts = code.split()
            if len(parts) >= 2:
                lib = parts[1].split('.')[0]
                if lib in PYTHON_STANDARD_LIBS:
                    standard_libs.append(lib)
                else:
                    external_libs.append(lib)

        # Check for: from numpy import array
        elif code.startswith('from '):
            parts = code.split()
            if len(parts) >= 2:
                lib = parts[1].split('.')[0]
                if lib in PYTHON_STANDARD_LIBS:
                    standard_libs.append(lib)
                else:
                    external_libs.append(lib)

    return standard_libs, external_libs


# ── Run the analysis ────────────────────────────────────────
print("=" * 60)
print("LIBRARY IMPORT DETECTION")
print("RQ1 from Twist & Zhang paper")
print("=" * 60)

print("""
What we're doing:
→ Reading the 'patch' column of each row
→ Looking at lines starting with +
→ Checking if those lines contain import statements
→ Classifying: is it standard (built-in) or external?

This is EXACTLY what the paper's code does on
711,923 real rows of pr_commit_details
""")

results = []
for _, row in df.iterrows():
    std_libs, ext_libs = extract_imports_from_patch(
        row['patch'], row['filename']
    )
    results.append({
        'pr_id': row['pr_id'],
        'filename': row['filename'],
        'agent': row['agent'],
        'state': row['state'],
        'standard_libs': std_libs,
        'external_libs': ext_libs,
        'has_any_import': len(std_libs) + len(ext_libs) > 0,
        'has_external': len(ext_libs) > 0
    })

results_df = pd.DataFrame(results)

# ── Show what we found in each file ────────────────────────
print("WHAT WE FOUND IN EACH FILE:")
print()
for _, row in results_df.iterrows():
    if row['filename'].endswith('.py'):
        print(f"PR {row['pr_id']:4d} | {row['filename']:<25}")
        if row['standard_libs']:
            print(f"         Standard libs: {row['standard_libs']}")
        if row['external_libs']:
            print(f"         External libs: {row['external_libs']} ← counts toward 29.5%")
        if not row['standard_libs'] and not row['external_libs']:
            print(f"         No imports found")
        print()

# ── Calculate the percentage ────────────────────────────────
python_rows = results_df[
    results_df['filename'].str.endswith('.py', na=False)
]

# Get unique PRs
pr_results = python_rows.groupby('pr_id').agg({
    'has_external': 'any',
    'agent': 'first',
    'state': 'first'
}).reset_index()

total_prs = len(df['pr_id'].unique())
prs_with_external = pr_results['has_external'].sum()
pct = prs_with_external / total_prs * 100

print("=" * 60)
print("THE CALCULATION")
print("=" * 60)
print(f"""
Total unique PRs:              {total_prs}
PRs with external library:     {prs_with_external}
Percentage:                    {pct:.1f}%

Paper reports:                 29.5%

Our small sample is different because we only have
{len(df)} rows vs the paper's 711,923 rows

The METHOD is identical - the paper just had more data
""")

# ── Show the patch scanning process ────────────────────────
print("=" * 60)
print("HOW THE PATCH SCANNING WORKS")
print("=" * 60)

example_patch = """+ import numpy as np
+ import os
+ # import old_library
+ result = numpy.mean(data)
- old_result = sum(data)"""

print(f"\nExample patch:\n{example_patch}")
print("""
Scanning rules:
Line 1: "+ import numpy as np"  → starts with + ✅ → numpy = external ✅
Line 2: "+ import os"           → starts with + ✅ → os = standard library
Line 3: "+ # import old_library"→ starts with + ✅ → but it's a COMMENT → skip
Line 4: "+ result = ..."        → starts with + ✅ → not an import → skip
Line 5: "- old_result = ..."    → starts with - ❌ → REMOVED code → skip

Result: 1 external library found (numpy)
→ This PR counts toward the 29.5%
""")
