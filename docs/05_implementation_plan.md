# 05 — Implementation plan

> **Fictional case.** Weeks are counted from kickoff (week 1). Names, roles and dates are invented. Regulatory sign-offs are assumptions to be checked with legal and clinical safety teams.

## 1. Phases at a glance

| Phase | Weeks | Goal | Ends with |
|---|---|---|---|
| 0. Mobilise | 1–2 | Same picture of goals and scope on both sides | Discovery notes, decisions and actions sent; sandbox access |
| 1. Design and approvals start | 2–6 | Agree how it fits together; start the slow approvals early | Solution design signed off (M2) |
| 2. Build | 6–12 | App backend, screens, webhook receiver, SSO, callback queue | End-to-end flow works in sandbox (M3) |
| 3. Test | 12–16 | Prove it works and is safe | UAT passed, no open critical/high defects (M4) |
| 4. Readiness | 16–19 | Sign-offs, training, production set-up | Go / no-go decision (M5) |
| 5. Go-live and hypercare | 20–23 | Live at 2 hospitals, close watch | Hypercare exit (M6) |
| 6. Handover | 24 | Customer success takes over | Handover note, first monthly report (M7) |

The slow items (clinical safety case and DPIA) start in week 2 and run alongside the build, because they are the most likely reason for a late go-live (risks R02 and R03).

## 2. Work plan

| Weeks | Task | Owner | Depends on |
|---|---|---|---|
| 1 | Kickoff, discovery workshop, notes within 24 h | Medivane implementation specialist | — |
| 1 | Send manufacturer safety case, security pack, subprocessor list | Medivane clinical lead / solutions engineer | — |
| 1–2 | Sandbox API clients and console accounts | Medivane implementation specialist | Signed order |
| 2 | Baseline report for the advice line (6 months) | Northbridge nurse lead | — |
| 2 | Confirm app agency developers and dates | Northbridge digital lead | — |
| 2 | Raise firewall change for webhook endpoint | Northbridge integration lead | — |
| 2–3 | Data flow diagram for the DPIA | Medivane implementation specialist | Discovery decisions |
| 2–17 | DPIA and data processing agreement | Northbridge IG lead + both legal teams | Data flow diagram |
| 2–18 | Deployment clinical safety case and hazard log | Northbridge Clinical Safety Officer | Manufacturer safety case |
| 3–4 | Solution design review and sign-off | Both, chaired by Northbridge digital lead | Discovery |
| 4, 9 | Hazard workshops 1 and 2 | Northbridge Clinical Safety Officer + Medivane clinical lead | Solution design |
| 6–11 | App backend endpoints | App agency | Sandbox clients |
| 6–12 | App screens for assessments | App agency | Backend endpoints |
| 7–9 | Webhook receiver | App agency | Firewall change |
| 7–9 | SSO set-up and test | Northbridge IT + Medivane | IdP details |
| 8–11 | Callback queue in the advice-line task list | Northbridge integration lead | Webhook receiver |
| 6–11 | Integration support sessions, twice a week | Medivane solutions engineer | — |
| 12–13 | System integration test (40 clinical scenarios + failure tests) | Medivane implementation specialist + app agency | M3 |
| 14 | UAT round 1 (6 nurses, 2 half-days) | Northbridge nurse lead | System test passed |
| 14 | Accessibility audit of new app screens | App agency | Screens complete |
| 15 | Fix defects from round 1 | App agency / Medivane | UAT round 1 |
| 16 | UAT round 2 | Northbridge nurse lead | Fixes released |
| 17 | Train-the-trainer (2 sessions) | Medivane implementation specialist | UAT round 2 |
| 17–19 | Nurse training at both pilot sites (about 40 nurses) | Northbridge nurse lead | Train-the-trainer |
| 18 | Production API clients, secrets, webhook endpoint, SSO | Medivane + Northbridge integration lead | Approvals in progress |
| 19 | Go / no-go meeting | Northbridge digital lead (decides) | Checklist below |
| 20 | Go-live at both pilot sites | Both | Go decision |
| 20–23 | Hypercare: daily checks in week 20, then twice a week | Medivane implementation specialist | Go-live |
| 24 | Handover to customer success manager | Medivane implementation specialist | Hypercare exit |

## 3. Milestones

| # | Milestone | Week | How we know it is done |
|---|---|---|---|
| M1 | Discovery closed | 2 | All 10 actions from the workshop have an answer or a new date |
| M2 | Solution design signed off | 4 | Signed by the digital lead, integration lead, IT security and Clinical Safety Officer |
| M3 | End-to-end in sandbox | 12 | A test patient goes app → backend → API → webhook → callback queue, and a nurse completes an assessment in the console with SSO |
| M4 | UAT passed | 16 | Both rounds done; no open critical or high defects |
| M5 | Go decision | 19 | Every go-live checklist item is green, or has a signed exception |
| M6 | Hypercare exit | 23 | Exit criteria below met for 2 weeks in a row |
| M7 | Handover | 24 | Handover note accepted by the customer success manager and Northbridge digital lead |

## 4. Go-live checklist

Every line needs evidence, not a "yes". The Northbridge digital lead makes the call; any item not green needs a written exception signed by its owner.

| # | Item | Owner | Evidence |
|---|---|---|---|
| **Safety and approvals** ||||
| G1 | Deployment clinical safety case signed | Northbridge Clinical Safety Officer | Signed document, version number |
| G2 | DPIA approved; data processing agreement signed | Northbridge IG lead | Approval email; signed agreement |
| G3 | Security assurance accepted | Northbridge IT security | Sign-off on security pack |
| **Function** ||||
| G4 | "Call 999" shown at once in the app in all red-flag test scenarios | Northbridge app product owner | UAT results, 100% of red-flag scenarios |
| G5 | Exclusion screens shown for under 16 and pregnancy-related symptoms | Northbridge app product owner | UAT results |
| G6 | Nurse can change urgency, reason is required, change is logged | Northbridge nurse lead | UAT results + log export |
| G7 | No open critical or high defects | Medivane implementation specialist | Defect list |
| G8 | New app screens pass the accessibility audit (WCAG 2.2 AA) or have a dated fix plan | App agency | Audit report |
| **Technical** ||||
| G9 | Production API clients live; secrets stored in the backend's secret store | Northbridge integration lead | Screenshot of secret store entry (no values) |
| G10 | Webhook signature check on; duplicate events ignored; test event received in production | Northbridge integration lead | Receiver log |
| G11 | Failed-delivery alerts reach both on-call contacts | Medivane support lead | Test alert email received |
| G12 | Webhook endpoint's certificate expiry date is on the change calendar | Northbridge integration lead | Calendar entry |
| G13 | SSO works for all pilot nurses; a disabled user cannot sign in | Northbridge IT | Test log |
| G14 | Fallback message (advice-line number + 999) shown when the API is unreachable | App agency | Test with API blocked |
| **People and operations** ||||
| G15 | At least 90% of pilot-site nurses trained | Northbridge nurse lead | Training register |
| G16 | Paper protocol for outages printed and at every advice-line desk | Northbridge nurse lead | Photo or checklist |
| G17 | Support route agreed: Northbridge service desk → Medivane support, with P1 phone number | Both | Support runbook |
| G18 | Reporting: baseline numbers agreed and first weekly report scheduled | Medivane implementation specialist | Baseline table, calendar invite |

## 5. Hypercare exit criteria

Hypercare ends when, for 2 weeks in a row:

- no open P1 or P2 tickets;
- at least 98% of red-flag alerts delivered to the webhook within 60 seconds;
- app completion rate stable or rising;
- nurses changing the urgency level in less than 12% of assessments (above that, the nurse lead and Medivane clinical lead review the cases first).

## 6. Meetings

| Meeting | When | Who | Output |
|---|---|---|---|
| Status call | Weekly, 30 min | Project leads both sides | Updated plan, risks 12+, decisions needed |
| Steering | Monthly, 45 min | Digital lead, Medivane account lead, implementation specialist | Decisions on change requests and dates |
| Hypercare stand-up | Daily in week 20, then twice a week | Implementation specialist, integration lead, nurse lead | Ticket list, fixes |
| 3-month review (QBR) | 3 months after go-live | Digital lead, nurse lead, Medivane CSM + implementation specialist | See [06_qbr_month3.md](06_qbr_month3.md) |
