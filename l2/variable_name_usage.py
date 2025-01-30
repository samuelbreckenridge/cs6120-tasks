import json
import sys
from collections import Counter

def variable_usage(bril: dict) -> Counter[str]:
    """Return a Counter object for a bril program's variable name usage (includes both dest and args usage)"""
    all_instrs = []
    for func in bril["functions"]:
        all_instrs.extend(func["instrs"])
    cnt = Counter()
    for instr in all_instrs:
        if dest := instr.get("dest"):
            cnt[dest] += 1
        if args := instr.get("args"):
            for arg in args:
                cnt[arg] += 1
    return cnt

if __name__ == "__main__":
    bril_json = json.loads(sys.stdin.read())
    vu = variable_usage(bril_json)
    print(f"Unique variable names: {len(vu)}")
    print(f"Total variable uses: {vu.total()}")
    print(f"Top 10 variables names by usage: {vu.most_common(10)}")

