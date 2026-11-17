# 01 — Discovery workshop pack

> **Fictional case.** Medivane, Northbridge Health, their hospitals, people and every number here are invented for a portfolio exercise. Not medical or legal advice.

## Context in three lines

- **Medivane** (fictional vendor) sells an AI symptom assessment and triage product for adults. Partners use it through a REST API and a web console for clinicians.
- **Northbridge Health** (fictional) runs 5 hospitals in England. It wants the product in its patient app and on its nurse-led patient advice line.
- This pack is what the Medivane implementation specialist prepares before the first workshop, and what comes out of it.

| Hospital (fictional) | Role in the project |
|---|---|
| Northbridge General | Pilot site 1, largest advice-line team |
| Harrowfield Hospital | Pilot site 2 |
| St Aldric's, Kelsey Vale, Marston Quay | Phase 2 rollout, not in this pilot |

## 1. Workshop agenda (90 minutes, video call)

**Goal:** leave the room with agreed goals, the clinical path, the integration shape and a list of open questions, each with an owner and a date.

**Who should attend:** Northbridge digital lead (chair), app product owner, advice-line nurse lead, Clinical Safety Officer, Information Governance (IG) lead, integration lead, IT security, and someone from the app agency. From Medivane: implementation specialist (runs the session), solutions engineer, clinical lead.

**Send 3 working days before:** this agenda, the question list (section 2), the product's API overview and the standard security pack.

| Time | Block | What happens | Output |
|---|---|---|---|
| 0–10 | Intros and goal of the session | Each person says their role and one thing that would make this project a success for them | List of personal success criteria |
| 10–25 | Business goals | Why now, what problem, how it is measured today | 2–3 measurable goals, current baseline |
| 25–45 | Clinical path | Walk one patient through today's journey, then the new one, on a shared screen | Current and future journey, who acts on each outcome |
| 45–65 | Integrations and identity | Where the product plugs in, who builds what, SSO, webhooks | Draft integration diagram, owner per piece |
| 65–80 | Data, privacy and security | What data moves, where it is stored, for how long, who is controller | Data flow draft, list of documents IG needs |
| 80–88 | Success and next steps | Go-live criteria, pilot scope, dates | Decisions list and action list |
| 88–90 | Close | Read back decisions and actions | Everyone agrees, notes go out within 24 hours |

**Rules I set at the start:** we decide scope, not solutions in detail; any question we cannot answer in 3 minutes goes on the open-questions list with an owner; no promises on dates until the action list is closed.

## 2. Discovery questions (25)

Grouped by topic. Bold questions are the ones I must get answered in the room; the rest can be answered in writing afterwards.

### Business goals (4)
1. **What problem are you solving first: advice-line waiting times, A&E attendances that could be handled elsewhere, or patient experience?**
2. How do you measure that problem today, and what are the current numbers?
3. Who signs off the business case, and what result after 3 months would make them extend to all 5 hospitals?
4. What has been tried before, and why did it stop?

### Clinical path (5)
5. **What happens today, step by step, when a patient calls the advice line with a new symptom?**
6. **For each outcome level (call 999, urgent, same day, within 3 days, self-care), who acts on it and how fast?**
7. Which patient groups must be excluded (age, pregnancy, specific conditions), and what should they see instead?
8. Can a nurse change the outcome, and should the reason be recorded?
9. Who is your Clinical Safety Officer, and when can we hold the first hazard workshop?

### Integrations (5)
10. **Which systems need to talk to the product: the patient app, the advice-line tools, the EPR, an integration engine?**
11. Who builds the app side: an in-house team or an agency, and what capacity do they have in the next 3 months?
12. Do you have a backend that the app already uses, or does the app call third parties directly?
13. Can you receive webhooks from the internet (public HTTPS endpoint, firewall rules, certificate management)?
14. Does any outcome need to land in the EPR in phase 1, and if so in which format (FHIR, HL7 v2, PDF)?

### Data and data protection (5)
15. **Who is the data controller for assessment data, and do you see Medivane as a processor?**
16. Which patient identifiers do you want to send, if any? Could a pseudonymous reference work?
17. How long must assessment records be kept, and where should the official record live?
18. Must all data stay in the UK, or is the EU acceptable?
19. Which documents will your IG team need from us (DPIA input, data processing agreement, subprocessor list)?

### Security (3)
20. **What identity provider do staff use, and do you support SAML 2.0 or OpenID Connect?**
21. What security assurance do you need before go-live (security questionnaire, penetration test summary, certifications)?
22. Who is the security contact for incidents, and what is your expected notification time?

### Success and operations (3)
23. **What must be true on go-live day for you to say "go"?**
24. Who supports users on day one: your service desk, the app agency, or us, and how should tickets reach Medivane?
25. How often do you want to review results after go-live, and with whom?

## 3. Workshop notes (fictional)

*Workshop held in week 1 of the project. 11 attendees. Notes written by the Medivane implementation specialist and sent the same day.*

**Business goals**
- The advice line takes about 9,500 calls a month across the 5 hospitals. At peak times about 3 in 10 callers hang up before a nurse answers. Median call length is 14 minutes. (Northbridge figures, not yet checked by us; the nurse lead will send the monthly report.)
- Main goal for the board: shorter calls and fewer abandoned calls. A&E attendances are a "nice to have" and will not be used to judge the pilot, because too many other things change A&E numbers.
- The digital lead wants patients to be able to get advice in the app outside phone hours (the line runs 8:00–22:00).

**Clinical path**
- Today a nurse follows a paper-based protocol and types notes into the advice-line task list. Urgent cases get a callback from a senior nurse.
- Nurse lead: "Nurses will not accept a black box." They need to see why the product chose an outcome, and they must be able to change it.
- The Clinical Safety Officer wants every "call 999" outcome to show on screen at once, not only after the assessment ends. Medivane confirmed this is how the API works: the emergency outcome is returned in the response to the answer that triggered it.
- Exclusions agreed: under 16s, and pregnancy-related symptoms (the product's pregnancy pathways are not validated yet, per Medivane's clinical lead). These patients see a screen with the advice-line number and 999.

**Integrations**
- The patient app is built by an external agency. It has a backend for login and appointments. The app will call Medivane only through this backend, so no API secret sits on a phone.
- EPR write-back was raised. Agreed it is **out of phase 1**: the integration team is busy with another project until next quarter. Phase 1 stores outcomes in Medivane and in the advice-line task list.
- The integration lead can expose a public HTTPS webhook endpoint through the existing API gateway. Firewall changes take about 2 weeks to approve.

**Data and security**
- IG lead sees Northbridge as controller and Medivane as processor, to be confirmed by legal on both sides.
- Northbridge prefers not to send NHS numbers or names to Medivane. Agreed to test a pseudonymous patient reference created by the app backend.
- Data must stay in the UK. Medivane hosts production in UK data centres (fictional statement from the solutions engineer; to be backed by the subprocessor list).
- Staff sign in with the organisation-wide identity provider. SAML 2.0 is supported; OIDC "probably".

**Success**
- Go-live is a "go" only if: the safety case is signed, the DPIA is approved, UAT has no open critical or high defects, and nurses at both pilot sites are trained.

## 4. Decisions

| # | Decision | Agreed by |
|---|---|---|
| D1 | Pilot at Northbridge General and Harrowfield; other 3 hospitals in phase 2 after the 3-month review | Digital lead |
| D2 | Channels in phase 1: patient app and advice line (clinician console). No web chat, no telephony integration | Digital lead, nurse lead |
| D3 | Adults 16 and over only; pregnancy-related symptoms excluded, with a clear "where to go instead" screen | Clinical Safety Officer, Medivane clinical lead |
| D4 | The app calls Medivane only through the Northbridge app backend; no secrets in the app | Integration lead, IT security |
| D5 | No names or NHS numbers sent to Medivane in phase 1; pseudonymous patient reference only | IG lead |
| D6 | EPR write-back is out of phase 1; to be scoped for phase 2 (FHIR is the likely format) | Digital lead |
| D7 | Nurses can change the urgency level; a reason is required and logged | Nurse lead, Clinical Safety Officer |
| D8 | Staff SSO through SAML 2.0 with the Northbridge identity provider | IT security |
| D9 | Success is judged on call length, abandoned calls, app completion and nurse agreement; A&E numbers are tracked but not used to judge the pilot | Digital lead |
| D10 | Weekly 30-minute status call; monthly steering; formal review after 3 months live | Both sides |

## 5. Open questions and actions

| # | Action | Owner | Due |
|---|---|---|---|
| A1 | Send monthly advice-line report (calls, abandoned calls, call length) for the last 6 months, as the baseline | Northbridge nurse lead | Week 2 |
| A2 | Send manufacturer clinical safety case and hazard log | Medivane clinical lead | Week 1 |
| A3 | Confirm controller/processor roles and start the data processing agreement | Both legal teams | Week 3 |
| A4 | Send subprocessor list and hosting locations in writing | Medivane solutions engineer | Week 1 |
| A5 | Confirm app agency capacity: named developers and dates | Northbridge digital lead | Week 2 |
| A6 | Raise firewall change for the webhook endpoint | Northbridge integration lead | Week 2 |
| A7 | Confirm whether OIDC is supported, or go with SAML | Northbridge IT security | Week 2 |
| A8 | Draft the data flow diagram for the DPIA | Medivane implementation specialist | Week 2 |
| A9 | Book two hazard workshops | Northbridge Clinical Safety Officer | Week 3 |
| A10 | Find 3 nurses to join UAT | Northbridge nurse lead | Week 4 |

**Note on legal and regulatory points:** everything about controller/processor roles, UK GDPR, medical device status and clinical safety standards in this pack is a working assumption, to be checked with both legal teams and the Clinical Safety Officer. It is not legal advice.
