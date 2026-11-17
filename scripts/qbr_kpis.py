"""Computes the 5 QBR KPIs from data/qbr_weekly_usage.csv.
Run: python3 scripts/qbr_kpis.py  (standard library only)
Writes data/qbr_kpi_summary.csv. All data is fictional."""
import csv
from collections import defaultdict

BASELINE_CALL_MINUTES = 14.0   # fictional pre-go-live median, from the discovery workshop
MONTHS = {"M1": range(1, 5), "M2": range(5, 9), "M3": range(9, 14)}

rows = list(csv.DictReader(open("data/qbr_weekly_usage.csv")))
for r in rows:
    for k, v in r.items():
        if k not in ("hospital", "channel") and v != "":
            r[k] = float(v)

def pick(month=None, channel=None, hospital=None):
    return [r for r in rows
            if (month is None or int(r["week"]) in MONTHS[month])
            and (channel is None or r["channel"] == channel)
            and (hospital is None or r["hospital"] == hospital)]

def s(rs, k): return sum(r[k] for r in rs)
def pct(a, b): return round(100 * a / b, 1) if b else None

out = []
def add(kpi, scope, month, value, unit, num="", den=""):
    out.append(dict(kpi=kpi, scope=scope, month=month, value=value, unit=unit, numerator=num, denominator=den))

for m in MONTHS:
    for ch in ("patient_app", "advice_line"):
        rs = pick(m, ch)
        add("1 Completion rate", ch, m, pct(s(rs, "assessments_completed"), s(rs, "assessments_started")), "%",
            int(s(rs, "assessments_completed")), int(s(rs, "assessments_started")))
    rs = pick(m, "advice_line")
    add("2 Nurse agreement rate", "advice_line", m,
        pct(s(rs, "nurse_reviewed") - s(rs, "nurse_urgency_changed"), s(rs, "nurse_reviewed")), "%",
        int(s(rs, "nurse_reviewed") - s(rs, "nurse_urgency_changed")), int(s(rs, "nurse_reviewed")))
    rs = pick(m)
    add("3 Red-flag alerts delivered within 60 s", "all", m,
        pct(s(rs, "red_flag_alerts") - s(rs, "red_flag_alerts_over_60s"), s(rs, "red_flag_alerts")), "%",
        int(s(rs, "red_flag_alerts") - s(rs, "red_flag_alerts_over_60s")), int(s(rs, "red_flag_alerts")))
    add("4 API success rate (non-5xx)", "all", m,
        round(100 - 100 * s(rs, "api_5xx_errors") / s(rs, "api_calls"), 2), "%",
        int(s(rs, "api_calls") - s(rs, "api_5xx_errors")), int(s(rs, "api_calls")))
    rs = pick(m, "advice_line")
    vals = [r["median_call_minutes"] for r in rs]
    add("5 Advice-line call length (mean of weekly medians)", "advice_line", m,
        round(sum(vals) / len(vals), 1), "min", "", f"baseline {BASELINE_CALL_MINUTES}")

with open("data/qbr_kpi_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for o in out: print(o)

# Extra facts quoted in the QBR one-pager
tot = pick()
print("\nTotal started", int(s(tot, "assessments_started")), "completed", int(s(tot, "assessments_completed")))
print("Red-flag alerts total", int(s(tot, "red_flag_alerts")))
w6 = [r for r in tot if r["week"] == 6]
print("Week 6 red flags", int(s(w6, "red_flag_alerts")), "late", int(s(w6, "red_flag_alerts_over_60s")))
w10 = [r for r in tot if r["week"] == 10]
print("Week 10 5xx", int(s(w10, "api_5xx_errors")), "of", int(s(w10, "api_calls")))
for h in ("Northbridge General", "Harrowfield"):
    for m in MONTHS:
        rs = pick(m, "patient_app", h)
        print(h, m, "app completion", pct(s(rs, "assessments_completed"), s(rs, "assessments_started")))
m3 = pick("M3")
print("M3 weekly avg completed:", round(s(m3, "assessments_completed") / 5))
app_m3 = pick("M3", "patient_app"); 
print("M3 app self-care share", pct(s(app_m3, "outcome_self_care"), s(app_m3, "assessments_completed")))
print("M3 app weekly avg started", round(s(app_m3,'assessments_started')/5))
