"""Sorting, searching and blend algorithms: quick sort, binary search, greedy, DP, backtracking."""

def quicksort(a, key):
    if len(a) < 2: return a
    p = key(a[len(a) // 2])
    return (quicksort([x for x in a if key(x) < p], key) + [x for x in a if key(x) == p]
            + quicksort([x for x in a if key(x) > p], key))

def binsearch_ge(a, t, key):      # first index with key >= t (a sorted ascending)
    lo, hi = 0, len(a)
    while lo < hi:
        m = (lo + hi) // 2
        if key(a[m]) < t: lo = m + 1
        else: hi = m
    return lo


def greedy_blend(batches, qty, target):   # fractional knapsack by quality-per-cost
    left, mix = qty, []
    for b in quicksort(batches, lambda b: -b["quality"] / max(b["cost"], 1e-9)):
        t = min(left, b["qty"])
        if t > 0: mix.append({"name": b["name"], "qty": round(t, 2)}); left -= t
        if left <= 0: break
    used = {m["name"]: m["qty"] for m in mix}
    tot = sum(used.values()) or 1
    q = sum(b["quality"] * used.get(b["name"], 0) for b in batches) / tot
    c = sum(b["cost"] * used.get(b["name"], 0) for b in batches)
    return {"mix": mix, "quality": round(q, 1), "cost": round(c, 2),
            "meets_target": q >= target and left <= 0}

def dp_knapsack(items, cap):      # 0/1 knapsack: best total quality within cap kg
    n = len(items)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    for i, it in enumerate(items, 1):
        wt = int(it["qty"])
        for c in range(cap + 1):
            dp[i][c] = dp[i - 1][c]
            if wt <= c: dp[i][c] = max(dp[i][c], dp[i - 1][c - wt] + it["quality"])
    c, pick = cap, []
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            pick.append(items[i - 1]["name"]); c -= int(items[i - 1]["qty"])
    return {"best_total_quality": dp[n][cap], "batches": pick[::-1]}

def backtrack_blend(items, need, lim):   # hard limits; prune batches that violate them
    def ok(b): return b["moisture"] <= lim["moisture"] and b["broken"] <= lim["broken"] and b["purity"] >= lim["purity"]
    def go(i, chosen, qty):
        if qty >= need: return True
        if i == len(items): return False
        b = items[i]
        if ok(b):
            chosen.append(b["name"])
            if go(i + 1, chosen, qty + b["qty"]): return True
            chosen.pop()
        return go(i + 1, chosen, qty)
    chosen = []
    return {"found": go(0, chosen, 0), "batches": chosen}
