"""
===============================================================
 VACCINATION TRACKER
 PROG211 Object-Oriented Programming 1 - Individual Assignment
 Domain: Health
===============================================================

Run the interactive menu:   python vaccination_tracker.py
Run the automatic demo:     python vaccination_tracker.py --demo

The file is organised into clear sections so each part can be
reused on its own:

    SECTION 1 - Fixed vaccine schedule (tuples)
    SECTION 2 - Classes: Patient, Vaccine, VaccinationRecord
    SECTION 3 - Record functions (dictionaries)
    SECTION 4 - Sample data
    SECTION 5 - User input helpers
    SECTION 6 - Menu actions
    SECTION 7 - Menu and demo

PRIVACY (DPG): a Patient only stores a patient ID, a FIRST name,
a birth YEAR and a district. No surname, full date of birth, phone
number, home address, national ID number or medical diagnosis is
ever collected or stored.

NOTE: the vaccine schedule below is a simplified example for this
assignment. It is not medical guidance.
"""

import sys
from datetime import date, datetime


# ===============================================================
# SECTION 1 - FIXED VACCINE SCHEDULE (TUPLES)
# Tuples are used because these values must NEVER change while
# the program runs. A tuple is immutable, so no part of the
# program can accidentally add, remove or edit a vaccine.
# ===============================================================

# Each inner tuple is: (vaccine code, vaccine name, doses required)
VACCINE_SCHEDULE = (
    ("BCG",   "BCG (Tuberculosis)",        1),
    ("OPV",   "Oral Polio Vaccine",        3),
    ("PENTA", "Pentavalent (DTP-HepB-Hib)", 3),
    ("PCV",   "Pneumococcal Vaccine",      3),
    ("MR",    "Measles-Rubella",           2),
    ("YF",    "Yellow Fever",              1),
)

# Status labels: (label when complete, label when not complete)
STATUS_LABELS = ("FULLY VACCINATED", "DOSES MISSING")

DATE_FORMAT = "%Y-%m-%d"   # dates are typed as YYYY-MM-DD, e.g. 2026-03-14


# ===============================================================
# SECTION 2 - CLASSES
# ===============================================================

class Patient:
    """A person (usually a child) whose vaccinations are tracked."""

    # Class attribute - shared by every Patient object
    total_patients = 0

    def __init__(self, patient_id, first_name, birth_year, district):
        # Instance attributes - unique to each Patient object
        self.patient_id = patient_id
        self.first_name = first_name
        self.birth_year = birth_year
        self.district = district
        # Dictionary of this patient's doses: {record_id: VaccinationRecord}
        self.records = {}
        Patient.total_patients += 1

    # ---------- Instance methods ----------
    def add_record(self, record):
        """Attach a VaccinationRecord object to this patient."""
        self.records[record.record_id] = record

    def doses_received(self, vaccine):
        """Return how many doses of one vaccine this patient has had."""
        count = 0
        for record in self.records.values():
            if record.vaccine is vaccine:
                count += 1
        return count

    def completion_percent(self, vaccines):
        """Return the percentage of all required doses this patient has received."""
        required = 0
        received = 0
        for vaccine in vaccines.values():
            required += vaccine.doses_required
            received += min(self.doses_received(vaccine), vaccine.doses_required)
        if required == 0:
            return 0
        return round(received / required * 100)

    def is_fully_vaccinated(self, vaccines):
        """Return True if every vaccine has all of its doses."""
        return self.completion_percent(vaccines) == 100

    def status(self, vaccines):
        """Return a status label from the STATUS_LABELS tuple."""
        complete_label, missing_label = STATUS_LABELS   # tuple unpacking
        return complete_label if self.is_fully_vaccinated(vaccines) else missing_label

    def display_info(self):
        """Print the patient's basic details."""
        print(f"  Patient ID : {self.patient_id}")
        print(f"  First name : {self.first_name}")
        print(f"  Birth year : {self.birth_year}")
        print(f"  District   : {self.district}")
        print(f"  Doses      : {len(self.records)} recorded")

    def display_vaccination_card(self, vaccines):
        """Print a vaccination card showing every vaccine and its doses."""
        print("=" * 62)
        print("                      VACCINATION CARD")
        print("=" * 62)
        self.display_info()
        print("-" * 62)
        print(f"  {'Vaccine':<29}{'Doses':>8}   Dates given")
        print("-" * 62)
        for vaccine in vaccines.values():
            dates = ""
            for record in self.records.values():
                if record.vaccine is vaccine:
                    dates += record.date_given + " "
            given = self.doses_received(vaccine)
            print(f"  {vaccine.name:<29}{given:>4}/{vaccine.doses_required:<3}   "
                  f"{dates.strip() or '-'}")
        print("-" * 62)
        print(f"  Completion : {self.completion_percent(vaccines)}%")
        print(f"  Status     : {self.status(vaccines)}")
        print("=" * 62)

    # ---------- Class methods ----------
    @classmethod
    def from_string(cls, text):
        """Create a Patient from text like 'P003, Fatmata, 2025, Kenema'."""
        patient_id, first_name, birth_year, district = (part.strip() for part in text.split(","))
        return cls(patient_id, first_name, int(birth_year), district)

    @classmethod
    def get_total_patients(cls):
        """Return how many patients are currently registered."""
        return cls.total_patients

    @classmethod
    def record_removal(cls):
        """Reduce the patient count when a patient is deleted."""
        cls.total_patients -= 1

    # ---------- Static methods ----------
    @staticmethod
    def is_valid_birth_year(year):
        """A birth year must be a whole number between 1900 and this year."""
        return isinstance(year, int) and 1900 <= year <= date.today().year

    @staticmethod
    def find_most_protected(patients, vaccines):
        """Return the patient with the highest completion percentage (or None)."""
        top = None
        for patient in patients.values():
            if top is None or patient.completion_percent(vaccines) > top.completion_percent(vaccines):
                top = patient
        return top


class Vaccine:
    """A vaccine on the schedule and how many doses it needs."""

    total_vaccines = 0

    def __init__(self, code, name, doses_required):
        self.code = code.upper()
        self.name = name
        self.doses_required = doses_required
        Vaccine.total_vaccines += 1

    # ---------- Instance methods ----------
    def display_info(self):
        """Print the vaccine details on one line."""
        print(f"  {self.code:<8}{self.name:<32}{self.doses_required} dose(s)")

    def get_coverage(self, patients):
        """
        Work out how many patients have completed this vaccine.
        Returns a TUPLE: (patients completed, patients total, percentage)
        """
        completed = 0
        total = len(patients)
        for patient in patients.values():
            if patient.doses_received(self) >= self.doses_required:
                completed += 1
        percent = round(completed / total * 100) if total else 0
        return completed, total, percent

    # ---------- Class methods ----------
    @classmethod
    def from_schedule(cls, schedule_entry):
        """Create a Vaccine from one tuple in VACCINE_SCHEDULE."""
        code, name, doses = schedule_entry   # tuple unpacking
        return cls(code, name, doses)

    @classmethod
    def get_total_vaccines(cls):
        """Return how many Vaccine objects have been created."""
        return cls.total_vaccines


class VaccinationRecord:
    """One dose of one vaccine given to one patient."""

    total_records = 0   # how many records currently exist
    next_number = 1     # gives every record a unique ID (never reused)

    def __init__(self, patient, vaccine, date_given, health_centre):
        if not VaccinationRecord.is_valid_date(date_given):
            raise ValueError("Date must be a real past date written as YYYY-MM-DD.")
        dose_number = patient.doses_received(vaccine) + 1
        if dose_number > vaccine.doses_required:
            raise ValueError(f"{patient.first_name} has already had all "
                             f"{vaccine.doses_required} dose(s) of {vaccine.code}.")
        self.record_id = f"V{VaccinationRecord.next_number:03d}"
        VaccinationRecord.next_number += 1
        VaccinationRecord.total_records += 1
        self.patient = patient          # a Patient OBJECT, not just an ID
        self.vaccine = vaccine          # a Vaccine OBJECT
        self.dose_number = dose_number  # worked out automatically
        self.date_given = date_given
        self.health_centre = health_centre
        # Objects interacting: the record registers itself with the patient
        patient.add_record(self)

    # ---------- Instance methods ----------
    def update_date(self, new_date):
        """Correct the date of this dose (e.g. after a typing mistake)."""
        if not VaccinationRecord.is_valid_date(new_date):
            raise ValueError("Date must be a real past date written as YYYY-MM-DD.")
        old_date = self.date_given
        self.date_given = new_date
        print(f"  Updated {self.record_id}: {old_date} -> {new_date}")

    def display_info(self):
        """Print this record on one line."""
        dose = f"{self.dose_number}/{self.vaccine.doses_required}"
        print(f"  {self.record_id:<6}{self.patient.patient_id:<6}{self.patient.first_name:<11}"
              f"{self.vaccine.code:<7}{dose:<6}{self.date_given:<12}{self.health_centre}")

    # ---------- Class methods ----------
    @classmethod
    def from_record(cls, record_text, patients, vaccines):
        """
        Create a record from text like 'P001, OPV, 2025-03-10, Bo CHC'.
        Looks the patient and vaccine up in their dictionaries.
        """
        patient_id, code, date_given, centre = (part.strip() for part in record_text.split(","))
        patient = patients.get(patient_id.upper())
        vaccine = vaccines.get(code.upper())
        if patient is None:
            raise ValueError(f"No patient with ID '{patient_id}'.")
        if vaccine is None:
            raise ValueError(f"No vaccine with code '{code}'.")
        return cls(patient, vaccine, date_given, centre)

    @classmethod
    def get_total_records(cls):
        """Return how many vaccination records currently exist."""
        return cls.total_records

    @classmethod
    def record_removal(cls):
        """Reduce the record count when a record is deleted."""
        cls.total_records -= 1

    # ---------- Static method ----------
    @staticmethod
    def is_valid_date(text):
        """Check a date is written as YYYY-MM-DD and is not in the future."""
        try:
            given = datetime.strptime(text, DATE_FORMAT).date()
        except ValueError:
            return False
        return given <= date.today()


# ===============================================================
# SECTION 3 - RECORD FUNCTIONS (DICTIONARIES)
# A DICTIONARY is the one data structure used to store multiple
# objects. Each object is stored with its unique ID as the key:
#     patients = {"P001": <Patient>, ...}
#     vaccines = {"OPV":  <Vaccine>, ...}
#     records  = {"V001": <VaccinationRecord>, ...}
# ===============================================================

def add_record(records, key, item):
    """Add an object to a dictionary. Refuses duplicate IDs."""
    if key in records:
        print(f"  [!] A record with ID '{key}' already exists - not added.")
        return False
    records[key] = item
    return True


def find_record(records, key):
    """Return the object stored under key, or None if it does not exist."""
    return records.get(key)


def delete_patient_record(patients, records, patient_id):
    """
    Remove a patient AND all of their vaccination records.
    Returns the deleted Patient object, or None if the ID was not found.
    """
    patient = patients.pop(patient_id, None)
    if patient is None:
        return None
    for record_id in patient.records:
        del records[record_id]
        VaccinationRecord.record_removal()
    Patient.record_removal()
    return patient


def search_patients(patients, text):
    """Display every patient whose ID or first name contains the search text."""
    text = text.lower()
    found = 0
    for patient in patients.values():
        if text in patient.first_name.lower() or text in patient.patient_id.lower():
            print(f"  {patient.patient_id:<7}{patient.first_name:<12}"
                  f"{patient.birth_year:<8}{patient.district}")
            found += 1
    return found


def display_patients(patients, vaccines):
    """Display every Patient object in the dictionary."""
    print(f"\n  ALL PATIENTS ({len(patients)})")
    print("  " + "-" * 58)
    print(f"  {'ID':<7}{'Name':<12}{'Born':<8}{'District':<20}Complete")
    print("  " + "-" * 58)
    for patient in patients.values():
        print(f"  {patient.patient_id:<7}{patient.first_name:<12}{patient.birth_year:<8}"
              f"{patient.district:<20}{patient.completion_percent(vaccines):>5}%")


def display_vaccines(vaccines):
    """Display every Vaccine object in the dictionary."""
    print(f"\n  VACCINE SCHEDULE ({len(vaccines)} vaccines)")
    print("  " + "-" * 58)
    for vaccine in vaccines.values():
        vaccine.display_info()


def display_records(records):
    """Display every VaccinationRecord object in the dictionary."""
    print(f"\n  ALL VACCINATION RECORDS ({len(records)})")
    print("  " + "-" * 60)
    print(f"  {'ID':<6}{'Pat.':<6}{'Name':<11}{'Code':<7}{'Dose':<6}{'Date':<12}Health centre")
    print("  " + "-" * 60)
    for record in records.values():
        record.display_info()


# ===============================================================
# SECTION 4 - SAMPLE DATA (made-up patients - no real personal data)
# ===============================================================

def load_sample_data():
    """Create sample objects and store them in dictionaries."""
    patients = {}
    vaccines = {}
    records = {}

    # Creating Vaccine objects from the tuple schedule (class method)
    for entry in VACCINE_SCHEDULE:
        vaccine = Vaccine.from_schedule(entry)
        add_record(vaccines, vaccine.code, vaccine)

    # Creating Patient objects - normal constructor and class method
    sample_patients = (
        Patient("P001", "Aminata", 2024, "Western Area Urban"),
        Patient("P002", "Mohamed", 2025, "Bo"),
        Patient.from_string("P003, Fatmata, 2025, Kenema"),
        Patient("P004", "Ibrahim", 2024, "Bombali"),
    )
    for patient in sample_patients:
        add_record(patients, patient.patient_id, patient)

    # Creating VaccinationRecord objects from text (class method)
    sample_records = (
        "P001, BCG, 2024-02-03, Freetown CHC",
        "P001, OPV, 2024-03-16, Freetown CHC",
        "P001, OPV, 2024-04-13, Freetown CHC",
        "P001, OPV, 2024-05-11, Freetown CHC",
        "P001, PENTA, 2024-03-16, Freetown CHC",
        "P001, PENTA, 2024-04-13, Freetown CHC",
        "P001, PENTA, 2024-05-11, Freetown CHC",
        "P001, PCV, 2024-03-16, Freetown CHC",
        "P001, PCV, 2024-04-13, Freetown CHC",
        "P001, PCV, 2024-05-11, Freetown CHC",
        "P001, MR, 2024-11-02, Freetown CHC",
        "P001, MR, 2025-05-03, Freetown CHC",
        "P001, YF, 2024-11-02, Freetown CHC",
        "P002, BCG, 2025-01-20, Bo CHC",
        "P002, OPV, 2025-03-04, Bo CHC",
        "P002, PENTA, 2025-03-04, Bo CHC",
        "P003, BCG, 2025-04-08, Kenema CHC",
        "P003, OPV, 2025-05-20, Kenema CHC",
        "P003, OPV, 2025-06-17, Kenema CHC",
        "P003, PENTA, 2025-05-20, Kenema CHC",
        "P003, PENTA, 2025-06-17, Kenema CHC",
        "P003, PCV, 2025-05-20, Kenema CHC",
        "P004, BCG, 2024-07-15, Makeni CHC",
    )
    for line in sample_records:
        record = VaccinationRecord.from_record(line, patients, vaccines)
        add_record(records, record.record_id, record)

    return patients, vaccines, records


# ===============================================================
# SECTION 5 - USER INPUT HELPERS (clear prompts, never crash)
# ===============================================================

def ask_text(prompt):
    """Ask for text and remove extra spaces."""
    return input(prompt).strip()


def ask_date(prompt):
    """Keep asking until a valid past date (YYYY-MM-DD) is entered."""
    while True:
        text = input(prompt).strip()
        if VaccinationRecord.is_valid_date(text):
            return text
        print("  [!] Please type a real date that is not in the future, like 2026-03-14.")


def ask_birth_year(prompt):
    """Keep asking until a valid birth year is entered."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and Patient.is_valid_birth_year(int(text)):
            return int(text)
        print(f"  [!] Please type a year from 1900 to {date.today().year}, like 2025.")


# ===============================================================
# SECTION 6 - MENU ACTIONS
# ===============================================================

def record_new_dose(patients, vaccines, records):
    patient_id = ask_text("  Enter patient ID (e.g. P002): ").upper()
    patient = find_record(patients, patient_id)
    if patient is None:
        print(f"  [!] No patient found with ID '{patient_id}'.")
        return
    code = ask_text("  Enter vaccine code (BCG, OPV, PENTA, PCV, MR, YF): ").upper()
    vaccine = find_record(vaccines, code)
    if vaccine is None:
        print(f"  [!] No vaccine found with code '{code}'.")
        return
    if patient.doses_received(vaccine) >= vaccine.doses_required:
        print(f"  [!] {patient.first_name} has already had all "
              f"{vaccine.doses_required} dose(s) of {code}.")
        return
    date_given = ask_date("  Enter date given (YYYY-MM-DD): ")
    centre = ask_text("  Enter health centre: ") or "Not stated"
    record = VaccinationRecord(patient, vaccine, date_given, centre)
    add_record(records, record.record_id, record)
    print(f"  [OK] Saved as {record.record_id}: {patient.first_name}, {code} dose "
          f"{record.dose_number} of {vaccine.doses_required} on {date_given}")


def correct_dose_date(records):
    record_id = ask_text("  Enter record ID to correct (e.g. V015): ").upper()
    record = find_record(records, record_id)
    if record is None:
        print(f"  [!] No record found with ID '{record_id}'.")
        return
    record.display_info()
    new_date = ask_date("  Enter the correct date (YYYY-MM-DD): ")
    record.update_date(new_date)


def show_vaccination_card(patients, vaccines):
    patient_id = ask_text("  Enter patient ID (e.g. P001): ").upper()
    patient = find_record(patients, patient_id)
    if patient is None:
        print(f"  [!] No patient found with ID '{patient_id}'.")
        return
    print()
    patient.display_vaccination_card(vaccines)


def register_patient(patients):
    patient_id = ask_text("  Enter new patient ID (e.g. P005): ").upper()
    if not patient_id:
        print("  [!] Patient ID cannot be empty.")
        return
    if patient_id in patients:
        print(f"  [!] A patient with ID '{patient_id}' already exists - not added.")
        return
    first_name = ask_text("  Enter first name only: ")
    if not first_name:
        print("  [!] First name cannot be empty.")
        return
    birth_year = ask_birth_year("  Enter birth year (e.g. 2025): ")
    district = ask_text("  Enter district: ") or "Not stated"
    patient = Patient(patient_id, first_name, birth_year, district)
    add_record(patients, patient_id, patient)
    print(f"  [OK] Patient {patient_id} registered.")


def delete_patient(patients, records):
    patient_id = ask_text("  Enter the ID of the patient to delete: ").upper()
    patient = find_record(patients, patient_id)
    if patient is None:
        print(f"  [!] No patient found with ID '{patient_id}'.")
        return
    patient.display_info()
    confirm = ask_text("  Type YES to delete this patient and all their records: ")
    if confirm.upper() != "YES":
        print("  Cancelled - nothing was deleted.")
        return
    count = len(patient.records)
    delete_patient_record(patients, records, patient_id)
    print(f"  [OK] Deleted {patient.first_name} ({patient_id}) and {count} record(s).")


def search_patient(patients):
    text = ask_text("  Enter part of a first name or ID to search for: ")
    if not text:
        print("  [!] Please type at least one letter or number.")
        return
    print(f"\n  SEARCH RESULTS FOR '{text}'")
    print("  " + "-" * 58)
    if search_patients(patients, text) == 0:
        print("  No patients matched your search.")


def show_most_protected(patients, vaccines):
    """Uses the STATIC method Patient.find_most_protected()."""
    top = Patient.find_most_protected(patients, vaccines)
    print("\n  MOST PROTECTED PATIENT (highest completion)")
    print("  " + "-" * 44)
    if top is None:
        print("  No patients are registered.")
        return
    print(f"  {top.first_name} ({top.patient_id}), born {top.birth_year}, {top.district}")
    print(f"  Doses received : {len(top.records)}")
    print(f"  Completion     : {top.completion_percent(vaccines)}%")
    print(f"  Status         : {top.status(vaccines)}")


def show_missing_doses(patients, vaccines):
    """Follow-up list: every patient who still needs doses, and which ones."""
    print("\n  FOLLOW-UP LIST - PATIENTS WITH MISSING DOSES")
    print("  " + "-" * 58)
    found = 0
    for patient in patients.values():
        if patient.is_fully_vaccinated(vaccines):
            continue
        found += 1
        missing = ""
        for vaccine in vaccines.values():
            still_needed = vaccine.doses_required - patient.doses_received(vaccine)
            if still_needed > 0:
                missing += f"{vaccine.code} x{still_needed}  "
        print(f"  {patient.patient_id} {patient.first_name:<10}({patient.district})")
        print(f"       Still needs: {missing.strip()}")
    if found == 0:
        print("  Everyone is fully vaccinated.")


def show_coverage(patients, vaccines):
    """Uses the INSTANCE method vaccine.get_coverage(), which returns a tuple."""
    print("\n  VACCINE COVERAGE (patients who completed each vaccine)")
    print("  " + "-" * 58)
    for vaccine in vaccines.values():
        completed, total, percent = vaccine.get_coverage(patients)   # tuple unpacking
        bar = "#" * (percent // 10) + "." * (10 - percent // 10)
        print(f"  {vaccine.code:<7}{completed:>2} of {total:<3} [{bar}] {percent:>3}%")
    print("  " + "-" * 58)


def show_summary(patients, vaccines, records):
    """Uses CLASS METHODS to report totals for the whole system."""
    fully = 0
    for patient in patients.values():
        if patient.is_fully_vaccinated(vaccines):
            fully += 1
    total = Patient.get_total_patients()
    print("\n  SYSTEM SUMMARY")
    print("  " + "-" * 40)
    print(f"  Patients registered  : {total}")
    print(f"  Vaccines on schedule : {Vaccine.get_total_vaccines()}")
    print(f"  Doses recorded       : {VaccinationRecord.get_total_records()}")
    print(f"  Fully vaccinated     : {fully}")
    print(f"  Patients with gaps   : {total - fully}")
    print("\n  VACCINE SCHEDULE (fixed tuple)")
    for code, name, doses in VACCINE_SCHEDULE:
        print(f"    {code:<7}{name:<30}{doses} dose(s)")


# ===============================================================
# SECTION 7 - MENU AND DEMO
# ===============================================================

MENU = (
    " 1. View all patients",
    " 2. View vaccine schedule",
    " 3. View all vaccination records",
    " 4. Record a new dose",
    " 5. Correct the date of a dose",
    " 6. Print a vaccination card",
    " 7. Register a new patient",
    " 8. Delete a patient",
    " 9. Search for a patient",
    "10. Show the most protected patient",
    "11. Show patients with missing doses",
    "12. Show vaccine coverage",
    "13. System summary",
    " 0. Exit",
)


def run_menu():
    patients, vaccines, records = load_sample_data()
    print("\n" + "=" * 62)
    print("                  VACCINATION TRACKER")
    print("=" * 62)
    print("  Type the number of an option and press Enter.")
    while True:
        print()
        for option in MENU:
            print(f"  {option}")
        choice = ask_text("\n  Your choice: ")
        if choice == "1":
            display_patients(patients, vaccines)
        elif choice == "2":
            display_vaccines(vaccines)
        elif choice == "3":
            display_records(records)
        elif choice == "4":
            record_new_dose(patients, vaccines, records)
        elif choice == "5":
            correct_dose_date(records)
        elif choice == "6":
            show_vaccination_card(patients, vaccines)
        elif choice == "7":
            register_patient(patients)
        elif choice == "8":
            delete_patient(patients, records)
        elif choice == "9":
            search_patient(patients)
        elif choice == "10":
            show_most_protected(patients, vaccines)
        elif choice == "11":
            show_missing_doses(patients, vaccines)
        elif choice == "12":
            show_coverage(patients, vaccines)
        elif choice == "13":
            show_summary(patients, vaccines, records)
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  [!] That is not an option. Please type a number from the menu.")


def run_demo():
    """Automatic demonstration of every requirement (no typing needed)."""
    print("=" * 62)
    print("  DEMO: Vaccination Tracker")
    print("=" * 62)

    print("\n[Task 1] Creating objects and showing their attributes")
    patients, vaccines, records = load_sample_data()
    patients["P002"].display_info()

    print("\n[Task 2] Records stored in dictionaries (ID -> object)")
    display_patients(patients, vaccines)
    display_vaccines(vaccines)

    print("\n[Task 3] Instance method: update_date() corrects a typing mistake")
    records["V015"].update_date("2025-03-05")

    print("\n[Task 3] Class method: VaccinationRecord.from_record()")
    new_record = VaccinationRecord.from_record("P002, OPV, 2025-04-01, Bo CHC", patients, vaccines)
    add_record(records, new_record.record_id, new_record)
    new_record.display_info()

    print("\n[Task 3] Static method: VaccinationRecord.is_valid_date()")
    for text in ("2025-04-01", "2025-13-40", "01/04/2025"):
        print(f"  is_valid_date('{text}') -> {VaccinationRecord.is_valid_date(text)}")

    print("\n[Validation] Trying to give a 2nd BCG dose (only 1 is needed)")
    try:
        VaccinationRecord(patients["P001"], vaccines["BCG"], "2025-01-01", "Freetown CHC")
    except ValueError as error:
        print(f"  [!] Rejected: {error}")

    print("\n[Interaction] Card built from Patient + Vaccine + VaccinationRecord objects\n")
    patients["P003"].display_vaccination_card(vaccines)

    print("\n[Feature] Most protected patient (static method)")
    show_most_protected(patients, vaccines)

    print("\n[Feature] Follow-up list of missing doses")
    show_missing_doses(patients, vaccines)

    print("\n[Feature] Vaccine coverage (instance method returning a tuple)")
    show_coverage(patients, vaccines)

    print("\n[Feature] Deleting patient P004 and their records")
    deleted = delete_patient_record(patients, records, "P004")
    print(f"  [OK] Deleted {deleted.first_name} ({deleted.patient_id}).")

    show_summary(patients, vaccines, records)


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()
