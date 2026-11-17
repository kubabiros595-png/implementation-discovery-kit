# Jak to działa: Implementation Discovery Kit

Notatka dla mnie, prostym językiem. Medivane, Northbridge Health i wszystkie liczby są wymyślone. Prawdziwy jest tylko publiczny serwer testowy FHIR. To nie jest porada prawna ani medyczna.

## O co chodzi w jednym zdaniu

Wdrożenie to nie tylko budowa: zanim ktokolwiek napisze kod, trzeba zrozumieć klienta, odpowiedzieć uczciwie na jego pytania, ustalić zakres, ryzyka i plan, a po starcie pokazać liczbami, co działa, a co nie.

## Kolejność dokumentów i po co każdy

| Krok | Dokument | Po co | Pytanie, na które odpowiada |
|---|---|---|---|
| 1 | Warsztat discovery (`docs/01`) | Zrozumieć cel, ścieżkę pacjenta, systemy, dane | „Co klient naprawdę chce osiągnąć i co nas zatrzyma?” |
| 2 | Odpowiedź na RFP (`docs/02`) | Odpowiedzieć na formalne pytania szpitala | „Czy to w ogóle spełnia nasze wymagania?” |
| 3 | Solution design (`docs/03`) | Narysować, jak to się łączy | „Kto buduje co i którędy płyną dane?” |
| 4 | Zakres, ryzyka, szacunek (`docs/04`) | Ustalić granice i koszt | „Co jest w środku, co może pójść źle, ile to pracy?” |
| 5 | Plan wdrożenia (`docs/05`) | Etapy, terminy, lista go-live | „Kiedy startujemy i po czym poznamy, że można?” |
| 6 | QBR po 3 miesiącach (`docs/06`) | Pokazać wynik liczbami | „Czy to się opłaciło i co dalej?” |
| 7 | Ćwiczenie FHIR (`docs/07`) | Dotknąć prawdziwego API | „Jak wygląda standard, którego szpital użyje w fazie 2?” |

## Jak prowadzić warsztat discovery

**Przed:** wysyłam agendę i listę pytań 3 dni robocze wcześniej. Ludzie przychodzą przygotowani, a ja nie tracę połowy spotkania na pytania, na które ktoś musi sprawdzić odpowiedź.

**Kogo zaprosić:** każdego, kto może później powiedzieć „nie”. W szpitalu to: osoba od bezpieczeństwa klinicznego (Clinical Safety Officer), ochrona danych (IG/DPO), bezpieczeństwo IT, integracje, ktoś od aplikacji i szefowa pielęgniarek z infolinii. Jeśli kogoś zabraknie, jego „nie” przyjdzie w 15. tygodniu.

**W trakcie, 4 zasady:**
1. Ustalamy **zakres**, nie szczegóły techniczne.
2. Pytanie, na które nie ma odpowiedzi w 3 minuty, idzie na listę: kto, do kiedy.
3. Żadnych dat, dopóki lista otwartych pytań nie jest zamknięta.
4. Przy ścieżce pacjenta przechodzimy **jednego konkretnego pacjenta** krok po kroku: dziś i po wdrożeniu. Wtedy wychodzą rzeczy, których nikt nie wymienił w mailach.

**Po:** notatki tego samego dnia, w trzech częściach: co usłyszeliśmy, co **postanowiliśmy** (decyzje z nazwiskiem osoby, która się zgodziła), co jest **do zrobienia** (właściciel + termin).

**Najważniejsze pytanie:** „Co musi być prawdą w dniu startu, żebyście powiedzieli: startujemy?”. Odpowiedź od razu daje listę go-live.

## Jak czytać RFP

RFP (Request for Proposal) to formalna lista pytań, którą klient wysyła kilku dostawcom, żeby ich porównać. Komisja czyta dziesiątki odpowiedzi, więc:

- **Każda odpowiedź zaczyna się od statusu:** Yes / Partly / Depends / No. Komisja skanuje statusy, potem czyta szczegóły.
- **„Depends” to nie wymówka.** Mówi dokładnie, od czego zależy: „zależy od tego, czy wasz silnik integracyjny przyjmuje FHIR R4 — nie widzieliśmy jego specyfikacji”.
- **Nigdy nie obiecuję czegoś, czego nie kontroluję.** Termin wdrożenia zależy głównie od agencji szpitala i od podpisów po ich stronie. Więc piszę „około 20 tygodni, jeśli te 3 rzeczy są potwierdzone do 2. tygodnia”, a nie „20 tygodni”.
- **„No” też jest odpowiedzią.** Lepiej napisać „SCIM jeszcze nie działa, oto jak to obchodzimy”, niż obiecać i się wycofać po podpisaniu umowy. Szpital to sprawdzi.
- Czytając RFP, szukam **pytań, które mówią więcej, niż pytają.** Pytanie o hosting w UK znaczy: dział ochrony danych już siedzi przy stole. Pytanie o dostępność znaczy: aplikacja ma użytkowników starszych lub z niepełnosprawnościami.

## Jak szacować pracę

1. **Rozbijam pracę na małe zadania** (tu 23), każde z właścicielem: dostawca czy szpital.
2. **Dla każdego trzy liczby:** optymistyczna, najbardziej prawdopodobna, pesymistyczna (w osobodniach, czyli dniach pracy jednej osoby).
3. **Liczę wartość oczekiwaną:** (optymistyczna + 4 × prawdopodobna + pesymistyczna) / 6. To metoda PERT: środek waży najwięcej, ale pesymistyczny wariant podciąga wynik w górę, bo projekty częściej się wydłużają niż skracają.
4. **Do każdego zadania jedno założenie**, które najbardziej zmienia wynik. Np. „agencja ma już backend i tylko dokłada endpointy”. Jeśli założenie padnie, przeliczam jedną linijkę, nie cały plan.
5. **Liczę też pracę klienta.** Tu wyszło, że 2/3 pracy jest po stronie szpitala. To najważniejszy wniosek z szacunku: termin zależy od ich agencji, nie od nas. Dlatego to ryzyko R04 i zadanie A5.

Wynik: 143 osobodni oczekiwane (zakres 102–202). Liczy to `scripts/estimate.py`, więc nie ma błędów w dodawaniu.

## Czym jest FHIR

**FHIR** (czyt. „fajer”) to standard wymiany danych medycznych przez zwykłe API REST. Wymyśliła go organizacja HL7.

- Dane są w **zasobach** (resources): `Patient` to pacjent, `Observation` to pomiar (np. tętno), `QuestionnaireResponse` to odpowiedzi z ankiety.
- Każdy zasób ma adres: `GET /Patient/829749` czyta pacjenta, `POST /Patient` tworzy nowego, `PUT` aktualizuje.
- **Wyszukiwanie** to parametry w adresie: `GET /Observation?subject=Patient/829749` zwraca paczkę wyników (`Bundle`). Paczkę zawsze, nawet przy jednym wyniku albo zerowym.
- **Kody** są wspólne dla wszystkich systemów: LOINC `8867-4` to zawsze tętno. Dzięki temu dwa systemy rozumieją liczbę tak samo.
- **Wersje:** każda zmiana podbija numer wersji. Nagłówek `If-Match` mówi: „zmień tylko, jeśli nikt inny nie zmienił w międzyczasie”. Sprawdziłem: drugi taki sam `PUT` dostał **409 Conflict**.
- **Błędy** przychodzą jako zasób `OperationOutcome` z polem `diagnostics`. To pole trzeba logować, bo od niego zaczyna się każde zgłoszenie do wsparcia.

**Gdzie FHIR jest w tym wdrożeniu:** w fazie 2, kiedy wynik oceny ma trafić do dokumentacji pacjenta w szpitalu (EPR). W fazie 1 go nie ma, bo zespół integracji szpitala jest zajęty (decyzja D6).

**Co sam zrobiłem:** prawdziwe zapytania do publicznego serwera HAPI FHIR, na wymyślonym pacjencie „Demo Testpatient”. Widziałem statusy 200, 201, 400, 404, 409 i 412. Odpowiedzi są w `api-exercise/responses/`.

**Dwie rzeczy, których się nie spodziewałem (i to jest najcenniejsze z ćwiczenia):**
- Drugi raz ten sam pacjent → **412**, serwer nie wpuszcza duplikatu. Wniosek do wdrożenia: webhook Medivane może przyjść dwa razy, więc szpital musi sprawdzać `event_id`, zanim zapisze cokolwiek do dokumentacji.
- Wyszukiwanie pokazało 1 pacjenta, choć były już 3, bo serwer trzymał stary wynik w pamięci. Z nagłówkiem `Cache-Control: no-cache` pokazał 3. Wniosek: po zapisie sprawdzam po ID, nie wyszukiwaniem.

## Jak czytać QBR

QBR (Quarterly Business Review) to spotkanie po kwartale, na którym pokazujemy klientowi wynik. Trzy zasady:

1. **Każda liczba ma definicję i źródło.** Klient ma te same dane i sprawdzi. Dlatego KPI liczy skrypt, a w dokumencie jest licznik i mianownik.
2. **Nie ukrywam tego, co nie działa.** Krótko, co działa, a zaraz potem incydenty, z liczbami i z tym, co zmieniamy. Klient i tak o nich wie. Jeśli ja ich nie powiem, przestaje mi ufać.
3. **Szansa na rozszerzenie idzie do handlowca, nie do klienta.** Szefowa SOR zapytała o użycie produktu w punkcie przyjęć. Nie obiecuję jej niczego, bo nie wiem, czy produkt jest do tego dopuszczony. Zapisuję kontakt, cytat i otwarte pytania i przekazuję account executive’owi.

Jedna rzecz, której pilnuję: **wysoki wskaźnik zgody pielęgniarek (92%) nie musi być dobry.** Może znaczyć, że przestały sprawdzać. Dlatego rekomendacja to przejrzeć 347 zmienionych przypadków, a nie tylko pochwalić się procentem.

## Słowniczek

| Pojęcie | Znaczenie |
|---|---|
| Discovery | Faza poznawania klienta przed budową |
| RFP | Formalne zapytanie ofertowe z listą pytań |
| BFF (backend for frontend) | Serwer aplikacji szpitala, przez który aplikacja rozmawia z Medivane; trzyma klucze API, żeby nie były w telefonie |
| Webhook | Medivane sam wysyła wiadomość do szpitala, kiedy coś się stanie (np. pilny wynik) |
| HMAC | Podpis wiadomości wspólnym sekretem; szpital sprawdza, że webhook naprawdę przyszedł od Medivane |
| OAuth 2.0 client credentials | Sposób logowania system–system: serwer dostaje token na 15 minut |
| SSO / SAML | Pielęgniarka loguje się do konsoli Medivane swoim szpitalnym kontem |
| SCIM | Automatyczne zakładanie i usuwanie kont; tu jeszcze go nie ma |
| DPIA | Ocena skutków dla ochrony danych, wymagana przy danych o zdrowiu |
| Administrator / podmiot przetwarzający | Kto decyduje o danych (szpital) i kto je przetwarza na jego zlecenie (Medivane) — założenie do sprawdzenia przez prawników |
| Clinical safety case | Dokument bezpieczeństwa klinicznego: jakie są zagrożenia i jak je ograniczamy |
| Hypercare | Pierwsze tygodnie po starcie, kiedy patrzymy codziennie |
| PERT | Metoda szacowania z trzech liczb |
| QBR | Przegląd wyników co kwartał |

---

## 8 pytań rekrutacyjnych (po angielsku) z krótkimi odpowiedziami

Odpowiedzi mówią o tym projekcie portfolio. Nie udaję, że prowadziłem prawdziwe wdrożenie w szpitalu.

**1. How do you prepare for a discovery workshop?**
I send the agenda and the questions three days before, so people can check their answers. I make sure everyone who can block the project later is in the room: clinical safety, data protection, IT security, integrations. In the session I walk one patient through today's process and the new one. I end with decisions and actions, each with an owner and a date, and the notes go out the same day.

**2. What is the most important question in discovery?**
"What must be true on go-live day for you to say go?" The answer gives me the go-live checklist on day one. In this case it showed that the safety case and the data protection review were the slow items, so I started them in week 2, not after the build.

**3. How do you answer an RFP question when you don't know the answer?**
I write "Depends" and say exactly what it depends on. For example, writing outcomes to the hospital record depends on their integration engine, which I had not seen. I offer the next step, like a one-hour session with their team. I don't promise a date or a feature I don't control, because the client will hold us to it after signing.

**4. How do you estimate implementation effort?**
I split the work into small tasks, each with an owner on our side or the client's side. Each task gets three numbers: best case, likely, worst case, and one assumption. Then I use the three-point formula. The useful result here was not the total, it was that two thirds of the work sat with the hospital's app agency. That told me where the real risk to the date was.

**5. What would you do if the client's team is the bottleneck?**
Show it early, with numbers, not blame. I put it in the risk register with an owner on their side and an early warning sign: "backend endpoints not in sandbox by week 8". I make it easier for them: sample code, two review sessions a week. And if the sign appears, we re-plan together instead of keeping a date nobody believes.

**6. What do you put in a QBR?**
A short page: the headline, five KPIs with how each one is calculated, what works, what doesn't, and recommendations with owners. Every number has a numerator and a denominator, because the client has the same data. I include the incidents. In my case a webhook problem delayed hospital alerts in week 6; I explain what happened, why patients were still safe, and what changes.

**7. A KPI looks very good. Is that always good news?**
No. Nurses accepted the suggested urgency in about 92% of cases. That could mean the product is right, or that nurses stopped checking. So my recommendation was to review the 347 cases they did change, grouped by symptom, with both clinical leads.

**8. The client mentions a new use case during the QBR. What do you do?**
I listen and write down who asked, their exact words and what we don't know yet. In this case: is the product validated for that use, does it fit the contract, who owns the safety case. I don't answer those myself. I pass it to the account executive and tell the client the right people will come back to them. My job is to keep their trust, not to close a deal in the meeting.
