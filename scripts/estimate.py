"""Totals for data/effort_estimate.csv. Three-point estimate:
expected = (low + 4 x likely + high) / 6 (PERT). Standard library only."""
import csv
rows = list(csv.DictReader(open("data/effort_estimate.csv")))
tot = {}
for r in rows:
    l, m, h = float(r["low_pd"]), float(r["likely_pd"]), float(r["high_pd"])
    e = (l + 4 * m + h) / 6
    t = tot.setdefault(r["side"], [0, 0, 0, 0])
    t[0] += l; t[1] += m; t[2] += h; t[3] += e
for side, (l, m, h, e) in tot.items():
    print(f"{side:12} low {l:5.0f}  likely {m:5.0f}  high {h:5.0f}  expected {e:5.1f}")
L = sum(v[0] for v in tot.values()); M = sum(v[1] for v in tot.values()); H = sum(v[2] for v in tot.values()); E = sum(v[3] for v in tot.values())
print(f"{'Total':12} low {L:5.0f}  likely {M:5.0f}  high {H:5.0f}  expected {E:5.1f}")
