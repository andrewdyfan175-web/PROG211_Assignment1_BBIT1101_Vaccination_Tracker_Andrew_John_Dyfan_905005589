# Vaccination Tracker

**PROG211 – Object-Oriented Programming 1 | Individual Assignment**
**Domain:** Health
**Language:** Python 3 (no external libraries needed)

A small, open-source Python program that helps a health centre track which vaccine doses each child has received. It can record doses, print vaccination cards, list children who still need follow-up doses, show vaccine coverage, find the most protected patient and delete patient records. It is built with Object-Oriented Programming and follows Digital Public Goods (DPG) principles.

> The vaccine schedule in this program is a simplified example for a programming assignment. It is not medical guidance.

---

## 1. The problem

In many communities, a child's vaccination history is kept only on a paper card that can be lost or damaged, or in a handwritten clinic register. Health workers find it hard to see which children have missed doses, and it is difficult to measure how well a community is covered for each vaccine. Missed doses leave children unprotected against diseases such as polio and measles.

This program keeps every patient, vaccine and dose in one place. It works out each child's next dose number automatically, refuses impossible entries, and produces follow-up lists and coverage figures in seconds.

## 2. Features

| # | Menu option | What it does |
|---|---|---|
| 1 | View all patients | Lists every patient with their completion percentage |
| 2 | View vaccine schedule | Lists every vaccine and how many doses it needs |
| 3 | View all vaccination records | Lists every dose given, with date and health centre |
| 4 | Record a new dose | Saves a dose; the dose number is worked out automatically, and extra doses are refused |
| 5 | Correct the date of a dose | Fixes a typing mistake in a dose date |
| 6 | Print a vaccination card | Shows one patient's doses for every vaccine, completion and status |
| 7 | Register a new patient | Adds a patient (duplicate IDs and invalid birth years are refused) |
| 8 | **Delete a patient** | Removes a patient **and all their records**, after typing YES to confirm |
| 9 | **Search for a patient** | Finds patients by part of their first name or ID (any case) |
| 10 | **Most protected patient** | Shows the patient with the highest completion percentage |
| 11 | **Patients with missing doses** | A follow-up list of every patient who still needs doses, and which ones |
| 12 | **Vaccine coverage** | For each vaccine, how many patients have completed it, with a text bar chart |
| 13 | System summary | Totals for patients, vaccines, doses and fully vaccinated patients, plus the schedule |
| 0 | Exit | Closes the program |

## 3. Project files

```
vaccination-tracker/
├── vaccination_tracker.py   # The complete program (all code in one file)
├── README.md                # This file
└── LICENSE                  # MIT open-source licence
```

The program is one file, divided into clearly labelled sections:

| Section | Contents |
|---|---|
| 1 – Vaccine schedule | `VACCINE_SCHEDULE`, `STATUS_LABELS` (tuples) and `DATE_FORMAT` |
| 2 – Classes | `Patient`, `Vaccine`, `VaccinationRecord` |
| 3 – Record functions | `add_record()`, `find_record()`, `delete_patient_record()`, `search_patients()`, `display_patients()`, `display_vaccines()`, `display_records()` |
| 4 – Sample data | `load_sample_data()` – made-up patients and doses |
| 5 – Input helpers | `ask_text()`, `ask_date()`, `ask_birth_year()` – safe input that never crashes |
| 6 – Menu actions | One function per menu option |
| 7 – Menu and demo | `run_menu()` and `run_demo()` |

## 4. How to run

You only need Python 3.8 or newer.

```bash
git clone https://github.com/<your-username>/vaccination-tracker.git
cd vaccination-tracker

python vaccination_tracker.py           # interactive menu
python vaccination_tracker.py --demo    # automatic demo of every feature
```

## 5. How the assignment tasks are met

### Task 1 – Classes, attributes and objects

| Class | Attributes | Methods |
|---|---|---|
| `Patient` | `patient_id`, `first_name`, `birth_year`, `district`, `records`, `total_patients` (class attribute) | `add_record()`, `doses_received()`, `completion_percent()`, `is_fully_vaccinated()`, `status()`, `display_info()`, `display_vaccination_card()`, `from_string()`, `get_total_patients()`, `record_removal()`, `is_valid_birth_year()`, `find_most_protected()` |
| `Vaccine` | `code`, `name`, `doses_required`, `total_vaccines` (class attribute) | `display_info()`, `get_coverage()`, `from_schedule()`, `get_total_vaccines()` |
| `VaccinationRecord` | `record_id`, `patient`, `vaccine`, `dose_number`, `date_given`, `health_centre`, `total_records` and `next_number` (class attributes) | `update_date()`, `display_info()`, `from_record()`, `get_total_records()`, `record_removal()`, `is_valid_date()` |

**How the objects interact:**
- A `VaccinationRecord` object holds a real `Patient` object and a real `Vaccine` object, not just their IDs.
- When a record is created, it asks the patient how many doses of that vaccine they already have. It uses the answer to set its own dose number, and it refuses a dose the patient doesn't need.
- The new record then calls `patient.add_record(self)`, so the patient "knows" its own doses.
- A vaccination card is built by the `Patient` going through every `Vaccine` and counting its own records for each one.
- Vaccine coverage is worked out by each `Vaccine` object asking every `Patient` how many doses they have received.
- Deleting a patient also removes all of that patient's `VaccinationRecord` objects.

### Task 2 – Data structure (dictionary)

The program uses **one data structure, the dictionary**, to store multiple objects. Each object's unique ID is its key:

```python
patients = {"P001": <Patient>, "P002": <Patient>, ...}
vaccines = {"BCG": <Vaccine>,  "OPV": <Vaccine>, ...}
records  = {"V001": <VaccinationRecord>, "V002": <VaccinationRecord>, ...}
```

Simple functions work with these dictionaries:
- **Add:** `add_record()` adds an object and refuses duplicate IDs.
- **Find:** `find_record()` looks an object up by its ID.
- **Delete:** `delete_patient_record()` removes a patient and all their records.
- **Search:** `search_patients()` finds patients by part of their first name or ID.
- **Display:** `display_patients()`, `display_vaccines()` and `display_records()` print the records.

Using the ID as the key means any record can be found or deleted instantly, without looping through every item.

**Optional tuples (bonus):** fixed values that must never change are stored as tuples:

```python
# (vaccine code, vaccine name, doses required)
VACCINE_SCHEDULE = (
    ("BCG",   "BCG (Tuberculosis)",         1),
    ("OPV",   "Oral Polio Vaccine",         3),
    ("PENTA", "Pentavalent (DTP-HepB-Hib)", 3),
    ("PCV",   "Pneumococcal Vaccine",       3),
    ("MR",    "Measles-Rubella",            2),
    ("YF",    "Yellow Fever",               1),
)
STATUS_LABELS = ("FULLY VACCINATED", "DOSES MISSING")
```

Tuples are also used for:
- **The menu and the sample data** (`MENU`, `sample_patients`, `sample_records`).
- **A returned value:** `vaccine.get_coverage()` returns `(completed, total, percent)`.

Tuple unpacking reads them, for example:

```python
code, name, doses = schedule_entry
complete_label, missing_label = STATUS_LABELS
completed, total, percent = vaccine.get_coverage(patients)
```

### Task 3 – Methods

| Type | Example | What it does |
|---|---|---|
| Instance method | `record.update_date("2025-03-05")` | Corrects the date of one dose |
| Instance method | `patient.completion_percent(vaccines)` | Works out what percentage of required doses one patient has received |
| Instance method | `patient.doses_received(vaccine)` | Counts one patient's doses of one vaccine |
| Instance method | `vaccine.get_coverage(patients)` | Works out how many patients have completed one vaccine |
| Class method | `VaccinationRecord.from_record("P002, OPV, 2025-04-01, Bo CHC", patients, vaccines)` | Creates a record object from a line of text |
| Class method | `Patient.from_string("P003, Fatmata, 2025, Kenema")` | Creates a patient object from a line of text |
| Class method | `Vaccine.from_schedule(("OPV", "Oral Polio Vaccine", 3))` | Creates a vaccine object from a schedule tuple |
| Class method | `Patient.get_total_patients()` / `VaccinationRecord.get_total_records()` | Read the class attributes that count objects |
| Class method | `Patient.record_removal()` / `VaccinationRecord.record_removal()` | Update the counts when a patient is deleted |
| Static method | `VaccinationRecord.is_valid_date("2025-13-40")` | Checks a date is real, written YYYY-MM-DD and not in the future |
| Static method | `Patient.is_valid_birth_year(2099)` | Checks a birth year is realistic |
| Static method | `Patient.find_most_protected(patients, vaccines)` | Finds the patient with the highest completion percentage |

## 6. How the solution meets DPG standards

| DPG principle | How this project meets it |
|---|---|
| **Open-source** | All source code is public on GitHub under the **MIT licence**. Anyone (clinics, NGOs, the Ministry of Health) can use, study, change and share it for free. It uses only standard Python, so there is nothing to buy. |
| **Inclusive and accessible design** | It runs in any text terminal on low-cost computers with no internet connection, which suits rural health centres. The numbered menu uses plain English, and every prompt gives an example (e.g. "Enter date given (YYYY-MM-DD)"). IDs, vaccine codes and searches work in upper or lower case. Wrong input never crashes the program: it shows a clear message and asks again. Messages use text labels such as `[OK]` and `[!]`, and coverage uses a `#` text bar, so nothing depends on colour. Deleting asks for confirmation. |
| **Privacy-respecting** | Health information is sensitive, so only the minimum needed to track doses is stored: a patient ID, a **first name only**, a **birth year only** and a district. **No** surname, full date of birth, phone number, home address, national ID number, photo or medical diagnosis is collected. Data stays in memory on the local machine and is never sent anywhere. Deleting a patient removes all of their dose records too, so no personal data is left behind. All sample data is made up. |
| **Modular and reusable** | The code is organised into labelled sections, each with one job: the schedule, the classes, the record functions, sample data, input helpers, menu actions and the menu itself. Each feature is its own small function. The vaccine schedule can be changed in one place (one tuple). The three classes can be copied or imported into another program, such as a web or mobile health app, without being changed. |

## 7. Example usage

### Recording a dose (option 4), including invalid dates

```
  Your choice: 4
  Enter patient ID (e.g. P002): p002
  Enter vaccine code (BCG, OPV, PENTA, PCV, MR, YF): opv
  Enter date given (YYYY-MM-DD): 2025-13-01
  [!] Please type a real date that is not in the future, like 2026-03-14.
  Enter date given (YYYY-MM-DD): 2099-01-01
  [!] Please type a real date that is not in the future, like 2026-03-14.
  Enter date given (YYYY-MM-DD): 2025-06-02
  Enter health centre: Bo CHC
  [OK] Saved as V024: Mohamed, OPV dose 2 of 3 on 2025-06-02
```

### Trying to give a dose that is not needed

```
  Your choice: 4
  Enter patient ID (e.g. P002): P001
  Enter vaccine code (BCG, OPV, PENTA, PCV, MR, YF): BCG
  [!] Aminata has already had all 1 dose(s) of BCG.
```

### Correcting a date (option 5)

```
  Your choice: 5
  Enter record ID to correct (e.g. V015): V015
  V015  P002  Mohamed    OPV    1/3   2025-03-04  Bo CHC
  Enter the correct date (YYYY-MM-DD): 2025-03-05
  Updated V015: 2025-03-04 -> 2025-03-05
```

### Deleting a patient (option 8)

```
  Your choice: 8
  Enter the ID of the patient to delete: P003
  Patient ID : P003
  First name : Fatmata
  Birth year : 2025
  District   : Kenema
  Doses      : 6 recorded
  Type YES to delete this patient and all their records: YES
  [OK] Deleted Fatmata (P003) and 6 record(s).
```

If anything other than YES is typed, the program shows `Cancelled - nothing was deleted.`

### Searching (option 9)

```
  Your choice: 9
  Enter part of a first name or ID to search for: mo

  SEARCH RESULTS FOR 'mo'
  ----------------------------------------------------------
  P002   Mohamed     2025    Bo
```

### Most protected patient (option 10)

```
  Your choice: 10

  MOST PROTECTED PATIENT (highest completion)
  --------------------------------------------
  Aminata (P001), born 2024, Western Area Urban
  Doses received : 13
  Completion     : 100%
  Status         : FULLY VACCINATED
```

### Follow-up list (option 11)

```
  Your choice: 11

  FOLLOW-UP LIST - PATIENTS WITH MISSING DOSES
  ----------------------------------------------------------
  P002 Mohamed   (Bo)
       Still needs: OPV x2  PENTA x2  PCV x3  MR x2  YF x1
  P003 Fatmata   (Kenema)
       Still needs: OPV x1  PENTA x1  PCV x2  MR x2  YF x1
  P004 Ibrahim   (Bombali)
       Still needs: OPV x3  PENTA x3  PCV x3  MR x2  YF x1
```

### Vaccine coverage (option 12)

```
  Your choice: 12

  VACCINE COVERAGE (patients who completed each vaccine)
  ----------------------------------------------------------
  BCG     4 of 4   [##########] 100%
  OPV     1 of 4   [##........]  25%
  PENTA   1 of 4   [##........]  25%
  PCV     1 of 4   [##........]  25%
  MR      1 of 4   [##........]  25%
  YF      1 of 4   [##........]  25%
  ----------------------------------------------------------
```

### Vaccination card (option 6)

```
==============================================================
                      VACCINATION CARD
==============================================================
  Patient ID : P003
  First name : Fatmata
  Birth year : 2025
  District   : Kenema
  Doses      : 6 recorded
--------------------------------------------------------------
  Vaccine                         Doses   Dates given
--------------------------------------------------------------
  BCG (Tuberculosis)              1/1     2025-04-08
  Oral Polio Vaccine              2/3     2025-05-20 2025-06-17
  Pentavalent (DTP-HepB-Hib)      2/3     2025-05-20 2025-06-17
  Pneumococcal Vaccine            1/3     2025-05-20
  Measles-Rubella                 0/2     -
  Yellow Fever                    0/1     -
--------------------------------------------------------------
  Completion : 46%
  Status     : DOSES MISSING
==============================================================
```

## 8. Possible future improvements

- Save records to a file or database so they remain after the program closes.
- Work out when each child's next dose is due and flag overdue doses.
- Add health-worker log-in so only authorised staff can change or delete records.

## 9. Licence

Released under the MIT Licence – see [LICENSE](LICENSE).
