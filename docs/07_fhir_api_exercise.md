# 07 — Hands-on exercise: a real FHIR API

> This is the only part of the kit that touches a real system: the **public HAPI FHIR R4 test server** (`https://hapi.fhir.org/baseR4`). It is a demo server run by the HAPI FHIR open-source project. Anyone can read what is sent to it, and it is cleared from time to time. **Only synthetic data was used:** a made-up patient called "Demo Testpatient" with a fake identifier and a fake phone number.

## Why this exercise is in the kit

Medivane's own API is fictional, so I cannot call it. FHIR is real, and it is the standard a UK hospital integration team would most likely ask for in phase 2, when assessment outcomes go into the EPR (see [03_solution_design.md](03_solution_design.md), section 9). Before that conversation, an implementation specialist should be able to read a FHIR resource, run a search and understand the error messages.

## FHIR in five lines

- **FHIR** (Fast Healthcare Interoperability Resources) is a standard from HL7 for exchanging health data over normal REST APIs, in JSON or XML.
- Data comes in **resources**: `Patient`, `Observation` (a measurement), `QuestionnaireResponse` (answers to a form), `Encounter` and about 140 more.
- Each resource has a URL: `GET [base]/Patient/123` reads it, `POST [base]/Patient` creates it, `PUT` updates it.
- **Searches** use query parameters: `GET [base]/Observation?subject=Patient/123&code=...` returns a `Bundle` of matches.
- **Codes** come from shared code systems, for example **LOINC** `8867-4` = heart rate, so two systems agree on what a number means.

## What I ran, and what came back

All calls were run on **17 November 2026, 17:42–17:56 UTC**, from a browser, against the public server: the first run (rows 0–11), two extra checks after something unexpected happened (rows 12–13), and a full re-run of the collection. The raw responses are saved unchanged in [api-exercise/responses/](../api-exercise/responses/) (I removed only the long HTML copy of error messages and, where noted, fields that were not needed). Server: HAPI FHIR Server `8.13.10-SNAPSHOT`, FHIR version `4.0.1`.

| # | Request | Status | Result |
|---|---|---|---|
| 0 | `GET /metadata?_summary=true` | **200** | Server says it speaks FHIR 4.0.1 |
| 1 | `POST /Patient` (synthetic patient) | **201** | Created `Patient/829749`, version 1 |
| 2 | `GET /Patient/829749` | **200** | Same patient back, `ETag: W/"1"` |
| 3 | `POST /Observation` (heart rate 72/min for that patient) | **201** | Created `Observation/829750` |
| 4 | `GET /Observation/829750` | **200** | Same observation back |
| 5 | `GET /Observation?subject=Patient/829749&code=http://loinc.org\|8867-4` | **200** | `Bundle`, `total: 1` — only our observation |
| 6 | `GET /Observation?code=http://loinc.org\|8867-4&_summary=count` | **200** | `total: 23555` heart-rate observations on the whole server (count only, no records downloaded) |
| 7 | `GET /Patient?_tag=...\|portfolio-demo&_summary=count` | **200** | `total: 1` — our tag finds only our patient |
| 8 | `PUT /Patient/829749` with `If-Match: W/"1"` | **200** | Updated; now version 2, `ETag: W/"2"` |
| 9 | The same `PUT` again with `If-Match: W/"1"` | **409** | Refused: version 1 is no longer current |
| 10 | `GET /Patient/this-id-does-not-exist-12345` | **404** | `OperationOutcome`: resource not known |
| 11 | `POST /Observation` with `status: "not-a-real-status"` | **400** | `OperationOutcome`: unknown status code |
| 12 | Row 1 again, exactly the same body | **412** | Refused: "duplicating existing resource: Patient/829749" |
| 13 | Row 7 again after 2 more test patients existed | **200** | `total: 1` from cache; with `Cache-Control: no-cache` the answer was `total: 3` |
| — | Full re-run of the collection with a new identifier | 201, 200, 201, 200, 200, 200, **409** | Same behaviour as the first run: `Patient/829760`, `Observation/829761` ([14_full_rerun_summary.json](../api-exercise/responses/14_full_rerun_summary.json)) |

The IDs above were assigned by the server. Because the server is cleared from time to time, they may no longer exist when you read this; run the collection to get your own.

### 1. Create a test patient

Request body (synthetic):

```json
{
  "resourceType": "Patient",
  "meta": { "tag": [{ "system": "https://github.com/kubabiros595-png/implementation-discovery-kit", "code": "portfolio-demo" }] },
  "identifier": [{ "system": "https://example.org/fhir/sid/northbridge-demo-mrn", "value": "NBH-DEMO-0001" }],
  "active": true,
  "name": [{ "use": "official", "family": "Testpatient", "given": ["Demo"] }],
  "gender": "unknown",
  "birthDate": "1980-01-01"
}
```

Real response: `201 Created`, header `Location: https://hapi.fhir.org/baseR4/Patient/829749/_history/1`. The body is the same resource with three fields added by the server:

```json
"id": "829749",
"meta": {
  "lastUpdated": "2026-11-17T12:43:13.084-05:00",
  "source": "#HjmBKUbCI4Nhu1za",
  "versionId": "1",
  "tag": [ ... same tag ... ]
}
```

**What it shows:** the server owns the ID and the version number. A client should store the ID it gets back, not invent one.

### 2–4. Read the patient, create and read an observation

The observation links to the patient by reference (`"subject": {"reference": "Patient/829749"}`) and uses a LOINC code and a UCUM unit:

```json
"code": { "coding": [{ "system": "http://loinc.org", "code": "8867-4", "display": "Heart rate" }] },
"valueQuantity": { "value": 72, "unit": "beats/minute", "system": "http://unitsofmeasure.org", "code": "/min" }
```

Real response: `201 Created`, `Observation/829750`, version 1. Reading it back returned `200` with the same content.

### 5. Search observations for that patient

```
GET /Observation?subject=Patient/829749&code=http://loinc.org|8867-4
```

Real response (shortened; full file: [05_search_observations_for_patient.json](../api-exercise/responses/05_search_observations_for_patient.json)):

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 1,
  "entry": [{
    "fullUrl": "https://hapi.fhir.org/baseR4/Observation/829750",
    "resource": { "resourceType": "Observation", "id": "829750", "status": "final", "...": "..." },
    "search": { "mode": "match" }
  }]
}
```

**What it shows:** a search always returns a `Bundle`, even with one match or none. Code that expects a single resource will break.

### 6–7. Counting without downloading other people's data

`_summary=count` returned only `"total": 23555` for heart rate across the whole server. I used it on purpose: the public server holds test records sent by many other people, and I did not want to download or show any of them. Tagging my own resources (`meta.tag`) and searching by `_tag` found exactly 1 patient: mine.

### 8–9. Safe updates with versions

The first `PUT` with `If-Match: W/"1"` returned `200` and version 2. Sending exactly the same request again returned:

```json
{
  "resourceType": "OperationOutcome",
  "issue": [{
    "severity": "error",
    "code": "processing",
    "diagnostics": "HAPI-0550: HAPI-0989: Trying to update Patient/829749/_history/1 but this is not the current version"
  }]
}
```

Status **409 Conflict**. **What it shows:** `If-Match` stops two systems from silently overwriting each other's changes. In a hospital this matters: the EPR and a vendor can both touch the same record.

### 12–13. Two things I did not expect

I found both while re-running the collection to check it works for someone else.

**A duplicate is refused (412).** Sending the same patient again returned `412 Precondition Failed` with `"HAPI-2840: Can not create resource duplicating existing resource: Patient/829749"`. The same body with a different identifier value was accepted (`201`, `Patient/829759`). This server is set up to block exact duplicates; another server might quietly create a second copy. **Lesson for the implementation:** decide with the hospital's integration team how a retry of the same assessment is handled. A webhook delivered twice (Medivane sends "at least once") must not create two records, so the receiver must check the `event_id` first, or use a conditional create (`If-None-Exist`), whatever the server does.

**Search results can be cached.** After two more test patients existed, the tag search still said `total: 1`. The same search with the header `Cache-Control: no-cache` said `total: 3`, and listing the IDs showed all three. **Lesson:** right after writing something, read it back by its ID, not by a search; or ask for a fresh search. Otherwise a test can "fail" when nothing is wrong, or pass when something is.

### 10–11. Errors

- `404` for an unknown ID: `"HAPI-2001: Resource Patient/this-id-does-not-exist-12345 is not known"`.
- `400` for an invalid status: `"... Invalid attribute value \"not-a-real-status\": Unknown ObservationStatus code 'not-a-real-status'"`.

Both come back as an `OperationOutcome` resource, not as plain text. A webhook receiver or integration engine should log the `diagnostics` field, because that is what support teams need first.

## Where FHIR would appear in the Northbridge implementation

| Moment | FHIR use | Phase |
|---|---|---|
| Assessment completed | Northbridge's integration engine receives the outcome and writes a `QuestionnaireResponse` (answers) plus a resource for the urgency outcome, linked to the patient in the EPR | Phase 2 |
| Before an assessment | The app backend could read age and sex from the EPR (`GET Patient/...`) instead of asking again | Phase 2, only if the DPIA allows it |
| Which profile | UK hospitals often expect national UK profiles of FHIR resources. Which ones Northbridge's engine needs is an open question for the integration team | Phase 2 discovery |
| Safety | `If-Match` on updates, `OperationOutcome` logging, and never retrying a `400` without a fix | Phase 2 build |

Phase 1 does **not** use FHIR: outcomes stay in Medivane and in the advice-line task list (decision D6).

## Try it yourself

1. Import [api-exercise/fhir_exercise.postman_collection.json](../api-exercise/fhir_exercise.postman_collection.json) into Postman, or into Hoppscotch (Hoppscotch imports Postman collections).
2. Run requests 00–05 in order. Request 01 sets a new `{{runId}}` (so the server does not refuse a duplicate), creates the patient and saves its ID into `{{patientId}}`; request 03 saves `{{observationId}}`. Search requests send `Cache-Control: no-cache`.
   In Hoppscotch, Postman's scripts may not run after import: type any new value into `runId` and copy the IDs into `patientId` and `observationId` yourself.
3. Run 08 twice and watch the second one fail with 409.
4. Never put real names, NHS numbers or real phone numbers into a public test server.

## Limits of this exercise

- One public test server, one afternoon, about 40 calls. It shows how FHIR behaves, not how a hospital's integration engine behaves (security, profiles, validation rules and authentication all differ).
- The public server has **no authentication**. A real FHIR endpoint would use OAuth 2.0 (often the SMART on FHIR profile), which I did not test here.
- I did not test FHIR Subscriptions (FHIR's own version of webhooks), because they would need a public endpoint to receive the calls.
