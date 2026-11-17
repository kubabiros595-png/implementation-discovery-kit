# 02 — RFP response (fictional)

> **Fictional case.** Northbridge Health's RFP and Medivane's answers are invented. Statements about Medivane's product, hosting and certifications are part of the fiction. Regulatory points are assumptions to be checked with legal and clinical safety teams, not legal advice.

## How to read this response

Each answer starts with a status, so the evaluation panel can scan it:

| Status | Meaning |
|---|---|
| **Yes** | Available today, in the standard product, at no extra cost |
| **Partly** | Available with a limit, which the answer names |
| **Depends** | We cannot answer until we know something about your set-up; the answer says what |
| **No** | Not available. If it is on the roadmap we say so, without a date we cannot keep |

Rule we follow: **we do not promise dates, numbers or features that depend on things we do not control.** Where an answer depends on Northbridge's systems or people, we say so.

## Questions and answers

### Integration

**Q1. Describe how your product integrates with our patient app.**
**Yes.** The app's backend calls our REST API (JSON over HTTPS). The flow is: start an assessment, send answers one at a time, get the next question or the outcome back in each response. Your app draws the screens; we send question text, answer options and the outcome. A full sequence diagram is in [03_solution_design.md](03_solution_design.md). We do not offer an SDK for mobile apps, because the app should not call us directly.

**Q2. Can outcomes be written to our electronic patient record (EPR)?**
**Depends.** We can export each completed assessment as FHIR R4 resources (a QuestionnaireResponse for the answers and a summary of the outcome). Whether this lands in your EPR depends on your integration engine accepting FHIR R4 and on which UK profiles it expects. We have not seen your engine's specification yet. We suggest this as phase 2, and we will estimate it after a 1-hour session with your integration team.

**Q3. Do you support webhooks?**
**Yes.** We send events for `assessment.completed`, `assessment.red_flag` and `assessment.abandoned`. Each request is signed (HMAC-SHA256 with a shared secret and a timestamp) so you can check it came from us. If your endpoint does not answer with a 2xx status, we retry 6 times over about an hour, then email both on-call contacts. Delivery is "at least once", so your receiver must ignore duplicate event IDs.

**Q4. What are your API limits?**
**Yes.** 50 requests per second per API client. Your pilot volume (around 2,000 assessments a week across both channels, about 9 calls each) needs well under 1 request per second on average. If you expect peaks we do not know about (for example a public health campaign), tell us and we will check them with our platform team.

### Identity and SSO

**Q5. Do you support single sign-on for staff?**
**Partly.** SAML 2.0 is supported today. OpenID Connect is supported for some identity providers; we need to test yours in our sandbox before we can say yes. Automatic user provisioning (SCIM) is **not** available yet: user accounts are created on first SSO sign-in, and removing access is done by disabling the user in your identity provider plus a monthly access review we run with you.

**Q6. How does the API authenticate your system and ours?**
**Yes.** OAuth 2.0 client credentials. Each environment (sandbox, production) and each channel (app, advice line) gets its own client, so access can be revoked separately. Tokens last 15 minutes. Secrets are shown once and can be rotated without downtime (two secrets can be active during a rotation). IP allow-listing is available on request.

### Data hosting and data protection

**Q7. Where is data hosted? Does any data leave the UK?**
**Yes — UK only** for production data, in two UK data centres (fictional). Our EU region is not used for your account. Two subprocessors outside the hosting provider see support tickets only, not assessment data; the full list is attached to the security pack. Your legal team should check this list against your own requirements; we are not giving legal advice.

**Q8. What patient data do you need?**
**Yes.** The minimum is age, sex at birth (for clinical logic) and the answers to the questions. Names, NHS numbers, addresses and contact details are **not** needed. We recommend that your backend sends a pseudonymous reference so you can link our record to your own. If you choose to send identifiers, your DPIA must cover it.

**Q9. Who is the data controller, and what documents will you provide?**
**Depends.** Our working assumption is that Northbridge is the controller and Medivane is a processor under UK GDPR. This must be confirmed by both legal teams, because it depends on how the product is used and who decides the purpose. We provide: a data processing agreement template, DPIA input (data flow, retention, security measures), the subprocessor list and our records of processing.

**Q10. How long do you keep data?**
**Partly.** Default retention is 30 days in our system, after which assessments are deleted, and the official record lives with you. Your clinical and legal teams must decide whether that fits your records policy. If you need us to keep data longer, it can be configured, but that changes the DPIA.

### Clinical safety and regulation

**Q11. Is the product a medical device, and what safety documents do you provide?**
**Partly.** In this fictional case, Medivane states the product is registered as a medical device in the UK, and we provide a manufacturer clinical safety case and hazard log. You will still need your own deployment safety case, signed by your Clinical Safety Officer, because it depends on how you use the product. Our working assumption is that the UK clinical risk management standards for health IT apply: DCB0129 to us as the manufacturer and DCB0160 to you as the deploying organisation. Please check our registration status with the regulator yourself; we cannot do that check for you. This is not regulatory advice.

**Q12. Which patients is the product for?**
**Partly.** Adults aged 16 and over, in English. It is not designed for children, and pregnancy-related pathways are not part of the product you would deploy. The product does not replace emergency services: a "call 999" outcome is shown at once, mid-assessment.

### Accessibility

**Q13. Is the product accessible?**
**Depends.** Our clinician console was audited against WCAG 2.2 AA (fictional; summary report available). For the patient app, **your app draws the screens**, so accessibility depends mostly on the app. We help by keeping question text short and plain (tested at a reading age of about 11) and by sending text alternatives for any images. Your app agency's audit must cover the new screens.

### Support

**Q14. What support do you offer, and what are the response times?**
**Yes.**

| Priority | Example | Hours | First response | Updates |
|---|---|---|---|---|
| P1 | API down or red-flag alerts not delivered | 24/7 | 30 minutes | Every hour |
| P2 | Feature broken for some users | Mon–Fri 8:00–18:00 UK | 4 working hours | Daily |
| P3 | Question or minor bug | Mon–Fri 8:00–18:00 UK | 1 working day | Weekly |

Monthly API availability target: 99.9%, measured on our side. A named implementation specialist leads the project, and a customer success manager takes over 4 weeks after go-live.

### Timeline

**Q15. How long will implementation take?**
**Depends.** Our estimate for the 2-hospital pilot is **about 20 weeks from kickoff to go-live**, with 4 weeks of hypercare after that. Most of the time sits on your side, and three things decide whether 20 weeks holds:

1. Your app agency's capacity to build the backend and app screens (about 35 working days on their side, see [04_scope_risks_estimate.md](04_scope_risks_estimate.md)).
2. When your Clinical Safety Officer can sign the deployment safety case.
3. When your IG team approves the DPIA.

If these are not confirmed by week 2, we will re-plan with you rather than keep a date we cannot meet. EPR write-back is not part of this estimate.
