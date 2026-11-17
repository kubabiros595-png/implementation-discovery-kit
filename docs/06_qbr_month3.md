# 06 — Quarterly business review, 3 months after go-live

> **Fictional case.** Every number comes from the invented dataset [data/qbr_weekly_usage.csv](../data/qbr_weekly_usage.csv) (2 hospitals × 2 channels × 13 weeks) and is calculated by [scripts/qbr_kpis.py](../scripts/qbr_kpis.py). Results: [data/qbr_kpi_summary.csv](../data/qbr_kpi_summary.csv). Not medical advice; the KPIs describe how the service runs, not clinical outcomes.

## Part A — the one-page review

**Northbridge Health × Medivane — pilot review, weeks 1–13 live**
Pilot sites: Northbridge General, Harrowfield. Month 1 = weeks 1–4, month 2 = weeks 5–8, month 3 = weeks 9–13.

### Headline

18,376 assessments completed in 13 weeks. In month 3 the median advice-line call took **10.8 minutes against a 14.0-minute baseline**, and app completion rose from **68.7% to 81.0%** after one screen fix. One webhook incident in week 6 delayed hospital alerts; patients were not affected, because the "call 999" message never depends on the webhook.

### KPIs

Targets were agreed with Northbridge at the go / no-go meeting (checklist item G18).


| KPI | Month 1 | Month 2 | Month 3 | Target | Status |
|---|---|---|---|---|---|
| 1a. App completion rate | 68.7% | 71.6% | **81.0%** | ≥ 75% | Met in month 3 |
| 1b. Advice-line completion rate | 93.9% | 94.2% | **94.4%** | ≥ 90% | Met |
| 2. Nurse agreement rate | 92.6% | 92.8% | **92.4%** | ≥ 88% | Met; review the changes |
| 3. Red-flag alerts delivered within 60 s | 98.4% | **85.7%** | 97.9% | ≥ 98% | Missed in months 2 and 3 |
| 4. API success rate (non-5xx) | 99.95% | 99.95% | **99.79%** | ≥ 99.9% | Missed in month 3 (week-10 outage) |
| 5. Advice-line call length (mean of weekly medians) | 12.4 min | 11.7 min | **10.8 min** | ≤ 11.0 min | Met in month 3 |

### What works

- **Calls are shorter.** 10.8 minutes in month 3, down from 14.0, at both sites (Harrowfield: 13.1 min in week 1, 10.4 in week 13). Caveat: this is the weekly median from Northbridge's call system, and other changes in the advice line may also play a part.
- **Nurses mostly agree with the outcome.** About 92–93% of advice-line outcomes were accepted without a change, every month.
- **The app screen fix worked.** In weeks 1–7 many patients stopped at the "medicines you take" question, which was a free-text box in the app. In week 8 the app agency switched to the structured picker the API already supports, with an "I'm not sure" option. Completion went from 67.6% in week 7 to 80.1% in week 9.

### What does not work yet

- **Week 6 webhook incident.** Northbridge renewed the certificate on its API gateway with an incomplete chain. Our webhook calls failed for most of a weekend; retries ran out and the alert email went to a shared mailbox nobody watched at weekends. 29 of 56 red-flag alerts that week arrived later than 60 seconds. Every one of those patients saw "call 999" on screen at the time; what was late was the hospital's follow-up task.
- **Red-flag alerts are still below target in month 3 (97.9%).** 7 of 327 were late. These are single late deliveries, not an outage; we have not found a pattern yet.
- **Week 10 outage on our side.** A 38-minute partial outage at Medivane caused 120 failed requests at Northbridge General. The app showed the fallback message as designed. Monthly availability was 99.91%, just inside the 99.9% target, but the error rate for the month is below what we want.
- **What we cannot see:** abandoned calls, the board's main goal, are measured by Northbridge's telephone system. We have not seen that data, so we make no claim about it.

### Recommendations

| # | Recommendation | Owner | By |
|---|---|---|---|
| 1 | Send failed-webhook alerts to the on-call phone, not a shared mailbox; add certificate checks to the change process | Northbridge integration lead | 2 weeks |
| 2 | Investigate the 7 late red-flag alerts in month 3, one by one | Medivane support lead | 2 weeks |
| 3 | Share the outage report for week 10 and the fix | Medivane support lead | Done in week 11; walk through it at this meeting |
| 4 | Review the 347 cases in month 3 where nurses changed the urgency, grouped by symptom, with both clinical leads | Medivane clinical lead + Northbridge nurse lead | Next month |
| 5 | Share abandoned-call figures for the 6 months before and the 3 months after go-live | Northbridge nurse lead | Before the phase 2 decision |
| 6 | Decide on phase 2 (3 more hospitals) once items 1, 2 and 5 are closed | Northbridge digital lead | Next steering |

### One expansion opportunity (for the sales team)

**What we heard:** in week 11, the Emergency Department lead at Northbridge General asked whether nurses at the urgent treatment centre front desk could use the clinician console to stream walk-in patients.

**Why it may be real:** the request came from the client, not from us; the advice-line nurses' agreement rate (92%+) is the evidence the ED lead quoted.

**What we do not know:** whether the product is validated for face-to-face streaming, whether this fits the current contract, and who would own the safety case. A CSM should not answer those.

**What I did:** logged it for the account executive with the contact, the quote and the open questions. I told the ED lead that the right people would come back to her, and I promised nothing.

## Part B — KPI definitions

| # | KPI | Formula | Source columns | Why it matters | Watch out |
|---|---|---|---|---|---|
| 1 | Completion rate (per channel) | completed ÷ started | `assessments_completed`, `assessments_started` | An assessment that is not finished gives the patient no advice | A patient who stops after a "call 999" screen counts as completed, because the outcome was given |
| 2 | Nurse agreement rate | (reviewed − urgency changed) ÷ reviewed, advice line only | `nurse_reviewed`, `nurse_urgency_changed` | Shows whether nurses trust the outcome | High is not always good: it could also mean nurses stop checking. Review the changes, not only the rate |
| 3 | Red-flag alerts within 60 s | (red-flag alerts − alerts over 60 s) ÷ red-flag alerts | `red_flag_alerts`, `red_flag_alerts_over_60s` | The hospital's follow-up depends on it | The patient's on-screen warning is not measured here; it does not depend on the webhook |
| 4 | API success rate | 1 − (5xx errors ÷ API calls) | `api_5xx_errors`, `api_calls` | Shows reliability as Northbridge feels it | Not the same as contract availability, which is measured in minutes |
| 5 | Advice-line call length | Mean of the weekly median call length | `median_call_minutes` (from Northbridge's call system) | The board's first goal | A mean of medians is a rough summary, not a true monthly median |

## Part C — numbers behind the KPIs

| KPI | Month | Value | Numerator | Denominator |
|---|---|---|---|---|
| 1a App completion | M1 / M2 / M3 | 68.7% / 71.6% / 81.0% | 1,544 / 2,376 / 3,665 | 2,246 / 3,320 / 4,527 |
| 1b Advice-line completion | M1 / M2 / M3 | 93.9% / 94.2% / 94.4% | 2,896 / 3,326 / 4,569 | 3,083 / 3,529 / 4,841 |
| 2 Nurse agreement | M1 / M2 / M3 | 92.6% / 92.8% / 92.4% | 2,681 / 3,085 / 4,222 | 2,896 / 3,326 / 4,569 |
| 3 Red-flag alerts ≤ 60 s | M1 / M2 / M3 | 98.4% / 85.7% / 97.9% | 179 / 197 / 320 | 182 / 230 / 327 |
| 4 API success | M1 / M2 / M3 | 99.95% / 99.95% / 99.79% | 43,493 / 55,877 / 78,478 | 43,516 / 55,906 / 78,642 |
| 5 Call length | M1 / M2 / M3 | 12.4 / 11.7 / 10.8 min | — | baseline 14.0 min |

Month 3 has 5 weeks, so its totals are larger than months 1 and 2; compare the rates, not the totals.

## How to rerun the numbers

```bash
python3 scripts/make_qbr_data.py   # recreates the fictional dataset (fixed seed)
python3 scripts/qbr_kpis.py        # prints the KPIs and writes data/qbr_kpi_summary.csv
```
