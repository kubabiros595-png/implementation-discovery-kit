"""Generates the fictional QBR usage data (deterministic, seed fixed).
Everything here is invented for a portfolio case."""
import csv, random
random.seed(11)
rows = []
hospitals = ["Northbridge General", "Harrowfield"]
for week in range(1, 14):
    for h in hospitals:
        scale = 1.0 if h == "Northbridge General" else 0.62
        ramp = min(1.0, 0.45 + 0.07 * week)          # adoption ramps up over the first weeks
        for ch in ["patient_app", "advice_line"]:
            if ch == "patient_app":
                started = int(random.gauss(560, 25) * scale * ramp)
                # weeks 1-7: drop-off at the medicines question; fixed in release of week 8
                comp_rate = random.uniform(0.66, 0.71) if week < 8 else random.uniform(0.79, 0.83)
                reviewed = 0
                overrides = 0
                aht = ""
            else:
                started = int(random.gauss(610, 20) * scale * min(1.0, 0.7 + 0.03 * week))
                comp_rate = random.uniform(0.93, 0.96)
                reviewed = None
                aht = round(random.uniform(12.7, 13.3) - (0.2 * week), 1)
            completed = int(started * comp_rate)
            if ch == "advice_line":
                reviewed = completed               # every advice-line outcome is seen by a nurse
                overrides = int(completed * random.uniform(0.06, 0.09))
            mix = [0.03, 0.12, 0.27, 0.30, 0.28] if ch == "patient_app" else [0.05, 0.18, 0.33, 0.27, 0.17]
            counts = [int(completed * m) for m in mix]
            counts[4] += completed - sum(counts)
            red_flags = counts[0]
            # webhook incident: hospital rotated its TLS certificate without telling Medivane in week 6
            late = 0
            if week == 6:
                late = int(red_flags * 0.55)
            else:
                late = 1 if random.random() < 0.25 and red_flags else 0
            api_calls = completed * 9 + (started - completed) * 4
            errors_5xx = int(api_calls * random.uniform(0.0003, 0.0011))
            if week == 10 and h == "Northbridge General":
                errors_5xx += 60                    # 38-minute partial outage on the vendor side (both channels)
            rows.append(dict(week=week, hospital=h, channel=ch,
                assessments_started=started, assessments_completed=completed,
                outcome_emergency_now=counts[0], outcome_urgent_4h=counts[1], outcome_same_day=counts[2],
                outcome_within_3_days=counts[3], outcome_self_care=counts[4],
                red_flag_alerts=red_flags, red_flag_alerts_over_60s=late,
                nurse_reviewed=reviewed, nurse_urgency_changed=overrides,
                api_calls=api_calls, api_5xx_errors=errors_5xx,
                median_call_minutes=aht))
with open("data/qbr_weekly_usage.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
