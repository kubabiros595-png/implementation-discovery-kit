# 04 — Scope, risks and effort estimate

> **Fictional case.** All names, numbers and estimates are invented for a portfolio exercise. Regulatory items are assumptions to be checked with legal and clinical safety teams.

## 1. Scope

### In scope (phase 1 pilot)

| # | Item |
|---|---|
| S1 | Two pilot hospitals: Northbridge General and Harrowfield |
| S2 | Patient app: assessment screens built by the app agency on top of the Medivane API, through the app backend |
| S3 | Advice line: nurses use the Medivane clinician console during calls, with SSO (SAML 2.0) |
| S4 | Webhooks for red-flag, completed and abandoned assessments, received by the app backend |
| S5 | Callback task in the advice-line task list for urgent and red-flag outcomes from the app |
| S6 | Adults 16+, English only, the standard Medivane pathways minus pregnancy-related ones |
| S7 | Sandbox and production environments; 2 API clients per environment (app, advice line) |
| S8 | Clinical safety support, DPIA input, test plan, train-the-trainer, go-live and 4 weeks of hypercare |
| S9 | Monthly usage report and a review after 3 months live |

### Out of scope (phase 1)

| Item | Why | Where it goes |
|---|---|---|
| EPR write-back (FHIR or other) | Integration team busy until next quarter (decision D6) | Phase 2, separate estimate |
| The other 3 hospitals | Pilot first (D1) | Phase 2 after the 3-month review |
| Languages other than English | Not available in the product today | Product roadmap, no date |
| Children under 16, pregnancy pathways | Not validated for this use (D3) | Not planned |
| Telephony integration (screen pop, call recording link) | Not needed to prove value; adds a third party | Possible later change request |
| Changing question wording | Questions are part of the validated product | Not possible; feedback goes to Medivane's clinical team |
| Building or hosting the app backend | Northbridge and its agency own it | Northbridge |
| Automatic user provisioning (SCIM) | Not available in the product yet | Roadmap |

**Change rule:** anything new goes on a change request list with a short estimate. Steering decides each month: phase 1, phase 2, or no.

## 2. Risk register (10 risks)

Likelihood (L) and impact (I) on a 1–5 scale; score = L × I. 12 or more is reviewed every week, below 12 every month. Source: [data/risk_register.csv](../data/risk_register.csv).

| ID | Risk | L | I | Score | Owner | Plan | Early warning sign |
|---|---|---|---|---|---|---|---|
| R02 | The clinical safety case is not signed off in time | 3 | 5 | **15** | Northbridge Clinical Safety Officer | Start the hazard log in week 2; book two hazard workshops early; Medivane sends its manufacturer safety case in week 1 | Hazard workshop not booked by week 4 |
| R03 | The DPIA raises questions that change the data flow late | 3 | 4 | **12** | Northbridge IG lead | Share the data flow diagram in week 2; keep the patient reference pseudonymous; agree retention before build starts | IG asks for a change after week 8 |
| R04 | The app agency has less capacity than planned | 3 | 4 | **12** | Northbridge digital lead | Confirm named developers and dates before kickoff; Medivane gives sample code and two review sessions a week | Backend endpoints not in sandbox by week 8 |
| R05 | Webhook alerts fail without anyone noticing (expired certificate or firewall change) | 3 | 4 | **12** | Northbridge integration lead | Monitoring on failed deliveries; Medivane retries for one hour then emails both on-call contacts; certificate expiry on the change calendar | Delivery failures above 1% in a day |
| R07 | Patients drop out of the assessment in the app | 4 | 3 | **12** | Northbridge app product owner | Track drop-off per question from week 1; fix the worst question first; plain-language review of question text | App completion below 75% after 4 weeks |
| R08 | Scope creep: requests for EPR write-back or extra languages during phase 1 | 4 | 3 | **12** | Medivane implementation specialist | Change requests go to a list for phase 2 with an estimate; steering decides | New requirement raised in a status meeting without a change request |
| R01 | A patient with a red-flag symptom is not told to call 999 because the app shows the outcome late or not at all | 2 | 5 | **10** | Northbridge app product owner + Medivane clinical lead | The emergency outcome comes back in the same API response as the answer that triggered it, and the app must show it before anything else; tested in every UAT round; the webhook is only a second channel for the hospital | Any UAT script where the emergency screen is not the first thing shown |
| R09 | The product is used for people it was not designed for (under 16, pregnancy) | 2 | 5 | **10** | Medivane clinical lead | Age check before the first question; clear exclusion screen with where to go instead; covered in the safety case | Number of people stopped at the age check rises week on week |
| R06 | Nurses do not trust the outcome and redo the assessment by hand, which makes calls longer | 3 | 3 | **9** | Advice-line nurse lead | Involve 3 nurses in UAT; show the reasoning summary; nurses can change the urgency with a reason; review changes every 2 weeks | Nurse urgency changes above 12% in a week |
| R10 | Vendor-side outage during peak hours | 2 | 4 | **8** | Medivane support lead | Status page + alerts to Northbridge; app shows a fallback message with the advice-line number and 999; advice line keeps its paper protocol for outages | Error rate above 1% for 5 minutes |

**Why R01 scores 10 and not higher:** its impact is the worst possible (5), but the design removes most of the likelihood: the warning does not depend on the webhook. It stays on the weekly list anyway, because of its impact.

## 3. Effort estimate (person-days)

### Method

- Each task has three numbers: **low** (everything goes well), **likely**, and **high** (the assumption breaks).
- Expected value = (low + 4 × likely + high) / 6. This weights the likely case but lets the high case pull the number up, because in projects things more often take longer than shorter.
- Every task has the one assumption that, if wrong, moves it most. When an assumption breaks, we re-estimate that line, not the whole plan.
- Totals are calculated by [scripts/estimate.py](../scripts/estimate.py) from [data/effort_estimate.csv](../data/effort_estimate.csv).

### Totals

| Side | Low | Likely | High | Expected |
|---|---|---|---|---|
| Medivane | 34 | 47 | 64 | **47.7** |
| Northbridge (incl. app agency) | 68 | 92 | 138 | **95.7** |
| **Total** | 102 | 139 | 202 | **143.3** |

**What this tells the client:** two thirds of the work is on the hospital side. The single biggest item is the app agency's build (backend, screens and webhook receiver: 35 likely days). If the agency cannot start in week 6, the date moves, whatever Medivane does. That is why it is risk R04 and action A5 in the [discovery pack](01_discovery_workshop.md).

### Line items

| ID | Task | Side | Low | Likely | High | Assumption |
|---|---|---|---|---|---|---|
| E01 | Kickoff + discovery workshop + write-up | Medivane | 3 | 4 | 5 | One 90-minute workshop plus two follow-up calls are enough to close the open questions |
| E02 | Weekly status + steering (20 weeks) | Medivane | 8 | 10 | 12 | 30 minutes a week plus one steering meeting a month |
| E03 | Project management + internal sign-offs | Northbridge | 10 | 12 | 16 | One part-time project manager across 5 hospitals |
| E04 | Environments + API clients + secrets set-up | Medivane | 1 | 2 | 3 | Sandbox and production clients use the standard set-up process |
| E05 | Backend service (BFF) that calls the Medivane API | Northbridge | 10 | 14 | 20 | The app agency already has a backend; it adds endpoints and does not build a new service |
| E06 | Patient app screens for the assessment flow | Northbridge | 12 | 16 | 24 | Uses Medivane's question JSON; no custom question wording; English only |
| E07 | Webhook receiver + signature check + retries | Northbridge | 3 | 5 | 8 | Receiver runs inside the same backend; uses the sample code from the Medivane docs |
| E08 | Integration support + code review sessions | Medivane | 5 | 7 | 10 | Two sessions a week during build (weeks 6–11) |
| E09 | Advice-line callback queue for urgent outcomes | Northbridge | 4 | 6 | 9 | Built in the advice line's existing task list; no telephony (CTI) integration |
| E10 | SSO for the clinician console (SAML or OIDC) | Northbridge | 2 | 3 | 5 | The hospital identity team has set up SAML apps before |
| E11 | SSO configuration + test on the vendor side | Medivane | 1 | 2 | 3 | Standard SAML/OIDC set-up; no custom claims mapping |
| E12 | Clinical safety case + hazard log (deployment side) | Northbridge | 6 | 8 | 12 | The Clinical Safety Officer is available about 1 day a week; Medivane supplies its manufacturer safety case |
| E13 | Clinical safety support + hazard workshops | Medivane | 3 | 4 | 6 | Medivane clinical lead joins two hazard workshops and answers questions in writing |
| E14 | DPIA + data processing agreement | Northbridge | 4 | 6 | 10 | Legal and IG review in parallel with the build; no new legal-basis questions appear |
| E15 | DPIA input + security questionnaire answers | Medivane | 2 | 3 | 4 | Standard security pack is accepted; one round of follow-up questions |
| E16 | Test plan + test scripts (incl. 40 clinical test scenarios) | Medivane | 3 | 4 | 6 | Medivane reuses its validated scenario library and adapts 10 scenarios |
| E17 | End-to-end + user acceptance testing | Northbridge | 8 | 10 | 15 | Two test rounds; 6 nurses for 2 half-days each |
| E18 | Accessibility check of app screens (WCAG 2.2 AA) | Northbridge | 2 | 3 | 5 | The app agency runs its usual audit; no testing with assistive-technology users in scope |
| E19 | Train-the-trainer for advice-line nurses + guide | Medivane | 2 | 3 | 4 | Two sessions; Northbridge nurse leads train the rest |
| E20 | Nurse training rollout (pilot hospitals) | Northbridge | 3 | 4 | 6 | About 40 nurses; 1-hour sessions in groups of 8 |
| E21 | Go-live readiness review + cutover | Medivane | 2 | 2 | 3 | Pilot go-live at 2 hospitals on the same day |
| E22 | Hypercare (first 4 weeks) | Medivane | 4 | 6 | 8 | Daily check in week 1, then twice a week |
| E23 | Hypercare (first 4 weeks) | Northbridge | 4 | 5 | 8 | On-call developer from the app agency during week 1 |

**Not in the estimate:** EPR write-back, phase 2 hospitals, Northbridge's own internal approvals beyond the project manager's time, and any penetration test Northbridge commissions itself.
