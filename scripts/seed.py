"""
Seed script: NovaTech Solutions demo data.

Run from the project root:
    python scripts/seed.py
"""
from __future__ import annotations

import hashlib
import sys
import uuid
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models import Budget, Department, Employee, Project, ProjectAssignment, Role, User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash_password(password: str) -> str:
    """SHA-256 placeholder — replaced with bcrypt in Phase 4 (Authentication)."""
    return hashlib.sha256(password.encode()).hexdigest()


def _is_seeded(db: Session) -> bool:
    return db.query(Role).first() is not None


def _are_projects_seeded(db: Session) -> bool:
    return db.query(Project).first() is not None


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

def seed_roles(db: Session) -> dict[str, Role]:
    data = [
        ("admin",    "Full system access"),
        ("manager",  "Department management access"),
        ("hr",       "HR system access"),
        ("finance",  "Finance and budget access"),
        ("employee", "Standard employee access"),
    ]
    roles: dict[str, Role] = {}
    for name, description in data:
        role = Role(name=name, description=description)
        db.add(role)
        roles[name] = role
    db.flush()
    return roles


# ---------------------------------------------------------------------------
# Departments
# ---------------------------------------------------------------------------

def seed_departments(db: Session) -> dict[str, Department]:
    data = [
        ("Engineering",      "ENG", "Software engineering and infrastructure"),
        ("Finance",          "FIN", "Financial management and reporting"),
        ("HR",               "HRD", "Human resources and talent acquisition"),
        ("Marketing",        "MKT", "Brand, content, and digital marketing"),
        ("Sales",            "SAL", "Revenue generation and account management"),
        ("Operations",       "OPS", "Business operations and process management"),
        ("Customer Support", "CSP", "Customer success and technical support"),
    ]
    depts: dict[str, Department] = {}
    for name, code, description in data:
        dept = Department(name=name, code=code, description=description)
        db.add(dept)
        depts[name] = dept
    db.flush()
    return depts


# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------

def seed_employees(db: Session, depts: dict[str, Department]) -> dict[str, Employee]:
    """
    Seed 38 employees across 7 departments.

    Director IDs are pre-generated so reports can reference manager_id
    immediately without a second DB round-trip.
    """
    # Pre-generate UUIDs for department directors.
    alice_id  = uuid.uuid4()   # Director of Engineering
    james_id  = uuid.uuid4()   # CFO
    olivia_id = uuid.uuid4()   # HR Director
    sam_id    = uuid.uuid4()   # Marketing Director
    xavier_id = uuid.uuid4()   # VP of Sales
    daniel_id = uuid.uuid4()   # Operations Director
    hugo_id   = uuid.uuid4()   # Customer Support Director

    # Columns:
    # (emp_num, first, last, email, phone, title, salary, hire_date,
    #  emp_type, status, location, dept_key, manager_id, preset_id)
    records: list[tuple] = [
        # ── Engineering ──────────────────────────────────────────────────────
        ("EMP001", "Alice",  "Johnson",  "alice.johnson@novatech.com",  "+1-415-555-0101",
         "Director of Engineering",      Decimal("185000.00"), date(2018,  3, 15),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Engineering",      None,      alice_id),
        ("EMP002", "Bob",    "Smith",    "bob.smith@novatech.com",      "+1-415-555-0102",
         "Senior Software Engineer",     Decimal("145000.00"), date(2019,  6,  1),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Engineering",      alice_id,  None),
        ("EMP003", "Carol",  "White",    "carol.white@novatech.com",    "+1-503-555-0103",
         "Software Engineer",            Decimal("110000.00"), date(2021,  8, 20),
         "FULL_TIME", "ACTIVE",   "Remote",            "Engineering",      alice_id,  None),
        ("EMP004", "David",  "Brown",    "david.brown@novatech.com",    "+1-206-555-0104",
         "DevOps Engineer",              Decimal("125000.00"), date(2020,  2, 10),
         "FULL_TIME", "ACTIVE",   "Seattle, WA",       "Engineering",      alice_id,  None),
        ("EMP005", "Emma",   "Davis",    "emma.davis@novatech.com",     "+1-512-555-0105",
         "QA Engineer",                  Decimal("95000.00"),  date(2022,  1, 15),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Engineering",      alice_id,  None),
        ("EMP006", "Frank",  "Wilson",   "frank.wilson@novatech.com",   "+1-415-555-0106",
         "Backend Developer",            Decimal("118000.00"), date(2021,  5,  1),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Engineering",      alice_id,  None),
        ("EMP007", "Grace",  "Lee",      "grace.lee@novatech.com",      "+1-503-555-0107",
         "Frontend Developer",           Decimal("108000.00"), date(2022,  9, 12),
         "FULL_TIME", "ACTIVE",   "Remote",            "Engineering",      alice_id,  None),
        ("EMP008", "Henry",  "Martinez", "henry.martinez@novatech.com", "+1-212-555-0108",
         "Data Engineer",                Decimal("130000.00"), date(2020,  7, 20),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Engineering",      alice_id,  None),
        ("EMP009", "Iris",   "Taylor",   "iris.taylor@novatech.com",    "+1-415-555-0109",
         "Machine Learning Engineer",    Decimal("155000.00"), date(2019, 11,  5),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Engineering",      alice_id,  None),
        # ── Finance ──────────────────────────────────────────────────────────
        ("EMP010", "James",  "Anderson", "james.anderson@novatech.com", "+1-212-555-0110",
         "CFO",                          Decimal("195000.00"), date(2017,  9,  1),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Finance",          None,      james_id),
        ("EMP011", "Kate",   "Thompson", "kate.thompson@novatech.com",  "+1-212-555-0111",
         "Financial Analyst",            Decimal("85000.00"),  date(2021,  3, 22),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Finance",          james_id,  None),
        ("EMP012", "Liam",   "Jackson",  "liam.jackson@novatech.com",   "+1-312-555-0112",
         "Senior Accountant",            Decimal("78000.00"),  date(2020,  6, 15),
         "FULL_TIME", "ACTIVE",   "Chicago, IL",       "Finance",          james_id,  None),
        ("EMP013", "Mia",    "Harris",   "mia.harris@novatech.com",     "+1-212-555-0113",
         "Budget Analyst",               Decimal("82000.00"),  date(2022,  4, 10),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Finance",          james_id,  None),
        ("EMP014", "Noah",   "Clark",    "noah.clark@novatech.com",     "+1-212-555-0114",
         "Tax Specialist",               Decimal("90000.00"),  date(2019,  8, 30),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Finance",          james_id,  None),
        # ── HR ───────────────────────────────────────────────────────────────
        ("EMP015", "Olivia", "Lewis",    "olivia.lewis@novatech.com",   "+1-415-555-0115",
         "HR Director",                  Decimal("130000.00"), date(2018,  5, 20),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "HR",               None,      olivia_id),
        ("EMP016", "Paul",   "Robinson", "paul.robinson@novatech.com",  "+1-415-555-0116",
         "HR Manager",                   Decimal("95000.00"),  date(2020, 11,  1),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "HR",               olivia_id, None),
        ("EMP017", "Quinn",  "Walker",   "quinn.walker@novatech.com",   "+1-503-555-0117",
         "Senior Recruiter",             Decimal("75000.00"),  date(2021,  7, 14),
         "FULL_TIME", "ACTIVE",   "Remote",            "HR",               olivia_id, None),
        ("EMP018", "Rachel", "Hall",     "rachel.hall@novatech.com",    "+1-415-555-0118",
         "HR Coordinator",               Decimal("58000.00"),  date(2023,  2, 28),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "HR",               olivia_id, None),
        # ── Marketing ────────────────────────────────────────────────────────
        ("EMP019", "Sam",    "Young",    "sam.young@novatech.com",      "+1-212-555-0119",
         "Marketing Director",           Decimal("140000.00"), date(2019,  2, 11),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Marketing",        None,      sam_id),
        ("EMP020", "Tina",   "King",     "tina.king@novatech.com",      "+1-212-555-0120",
         "Marketing Manager",            Decimal("105000.00"), date(2020,  8, 17),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Marketing",        sam_id,    None),
        ("EMP021", "Uma",    "Wright",   "uma.wright@novatech.com",     "+1-503-555-0121",
         "Content Strategist",           Decimal("72000.00"),  date(2022,  3,  5),
         "FULL_TIME", "ACTIVE",   "Remote",            "Marketing",        sam_id,    None),
        ("EMP022", "Victor", "Scott",    "victor.scott@novatech.com",   "+1-512-555-0122",
         "Digital Marketing Specialist", Decimal("68000.00"),  date(2022, 11,  1),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Marketing",        sam_id,    None),
        ("EMP023", "Wendy",  "Chen",     "wendy.chen@novatech.com",     "+1-212-555-0123",
         "Brand Designer",               Decimal("76000.00"),  date(2021,  6, 20),
         "CONTRACT",  "ACTIVE",   "New York, NY",      "Marketing",        sam_id,    None),
        # ── Sales ────────────────────────────────────────────────────────────
        ("EMP024", "Xavier", "Baker",    "xavier.baker@novatech.com",   "+1-212-555-0124",
         "VP of Sales",                  Decimal("165000.00"), date(2018,  7,  1),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Sales",            None,      xavier_id),
        ("EMP025", "Yara",   "Nelson",   "yara.nelson@novatech.com",    "+1-312-555-0125",
         "Senior Sales Executive",       Decimal("95000.00"),  date(2020,  4, 15),
         "FULL_TIME", "ACTIVE",   "Chicago, IL",       "Sales",            xavier_id, None),
        ("EMP026", "Zach",   "Carter",   "zach.carter@novatech.com",    "+1-415-555-0126",
         "Account Manager",              Decimal("72000.00"),  date(2021,  9,  8),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Sales",            xavier_id, None),
        ("EMP027", "Amy",    "Mitchell", "amy.mitchell@novatech.com",   "+1-212-555-0127",
         "Business Dev Manager",         Decimal("110000.00"), date(2019, 12,  2),
         "FULL_TIME", "ACTIVE",   "New York, NY",      "Sales",            xavier_id, None),
        ("EMP028", "Ben",    "Foster",   "ben.foster@novatech.com",     "+1-512-555-0128",
         "Sales Representative",         Decimal("60000.00"),  date(2023,  1, 16),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Sales",            xavier_id, None),
        ("EMP029", "Clara",  "Stevens",  "clara.stevens@novatech.com",  "+1-503-555-0129",
         "Sales Representative",         Decimal("60000.00"),  date(2023,  5, 22),
         "FULL_TIME", "INACTIVE", "Remote",            "Sales",            xavier_id, None),
        # ── Operations ───────────────────────────────────────────────────────
        ("EMP030", "Daniel", "Perez",    "daniel.perez@novatech.com",   "+1-415-555-0130",
         "Operations Director",          Decimal("145000.00"), date(2018, 10,  1),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Operations",       None,      daniel_id),
        ("EMP031", "Elena",  "Roberts",  "elena.roberts@novatech.com",  "+1-415-555-0131",
         "Operations Manager",           Decimal("105000.00"), date(2020,  3, 15),
         "FULL_TIME", "ACTIVE",   "San Francisco, CA", "Operations",       daniel_id, None),
        ("EMP032", "Felix",  "Turner",   "felix.turner@novatech.com",   "+1-312-555-0132",
         "Process Analyst",              Decimal("78000.00"),  date(2021, 12,  6),
         "FULL_TIME", "ACTIVE",   "Chicago, IL",       "Operations",       daniel_id, None),
        ("EMP033", "Gina",   "Phillips", "gina.phillips@novatech.com",  "+1-512-555-0133",
         "Supply Chain Coordinator",     Decimal("65000.00"),  date(2022,  8, 29),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Operations",       daniel_id, None),
        # ── Customer Support ─────────────────────────────────────────────────
        ("EMP034", "Hugo",   "Campbell", "hugo.campbell@novatech.com",  "+1-512-555-0134",
         "Customer Support Director",    Decimal("120000.00"), date(2019,  4, 20),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Customer Support", None,      hugo_id),
        ("EMP035", "Iris",   "Evans",    "iris.evans@novatech.com",     "+1-512-555-0135",
         "Support Team Lead",            Decimal("82000.00"),  date(2020,  9, 14),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Customer Support", hugo_id,   None),
        ("EMP036", "Jake",   "Collins",  "jake.collins@novatech.com",   "+1-503-555-0136",
         "Support Specialist",           Decimal("52000.00"),  date(2022,  6,  1),
         "FULL_TIME", "ACTIVE",   "Remote",            "Customer Support", hugo_id,   None),
        ("EMP037", "Karen",  "Stewart",  "karen.stewart@novatech.com",  "+1-512-555-0137",
         "Customer Success Manager",     Decimal("88000.00"),  date(2021, 10, 25),
         "FULL_TIME", "ACTIVE",   "Austin, TX",        "Customer Support", hugo_id,   None),
        ("EMP038", "Liam",   "Brooks",   "liam.brooks@novatech.com",    None,
         "Support Specialist",           Decimal("50000.00"),  date(2023,  7, 10),
         "PART_TIME", "ACTIVE",   "Remote",            "Customer Support", hugo_id,   None),
    ]

    employees: dict[str, Employee] = {}
    for (
        emp_num, first, last, email, phone, title, salary, hire_dt,
        emp_type, status, location, dept_key, mgr_id, preset_id,
    ) in records:
        kwargs: dict = dict(
            employee_number=emp_num,
            first_name=first,
            last_name=last,
            email=email,
            phone_number=phone,
            job_title=title,
            salary=salary,
            hire_date=hire_dt,
            employment_type=emp_type,
            status=status,
            office_location=location,
            department_id=depts[dept_key].id,
            manager_id=mgr_id,
        )
        if preset_id is not None:
            kwargs["id"] = preset_id
        emp = Employee(**kwargs)
        db.add(emp)
        employees[emp_num] = emp

    db.flush()
    return employees


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def seed_users(
    db: Session,
    roles: dict[str, Role],
    employees: dict[str, Employee],
) -> None:
    """
    Create 9 application users covering all roles.
    Passwords are SHA-256 placeholders (Phase 4 replaces with bcrypt).
    Default seed password: NovaTech@2024
    """
    pwd = _hash_password("NovaTech@2024")

    # (username, email, display_name, role_name, is_active)
    data = [
        ("admin",          "admin@novatech.com",                   "System Administrator", "admin",    True),
        ("alice.johnson",  employees["EMP001"].email,              "Alice Johnson",         "manager",  True),
        ("james.anderson", employees["EMP010"].email,              "James Anderson",        "finance",  True),
        ("olivia.lewis",   employees["EMP015"].email,              "Olivia Lewis",          "hr",       True),
        ("sam.young",      employees["EMP019"].email,              "Sam Young",             "manager",  True),
        ("xavier.baker",   employees["EMP024"].email,              "Xavier Baker",          "manager",  True),
        ("daniel.perez",   employees["EMP030"].email,              "Daniel Perez",          "manager",  True),
        ("hugo.campbell",  employees["EMP034"].email,              "Hugo Campbell",         "manager",  True),
        ("bob.smith",      employees["EMP002"].email,              "Bob Smith",             "employee", True),
    ]

    for username, email, display_name, role_name, is_active in data:
        user = User(
            username=username,
            email=email,
            hashed_password=pwd,
            display_name=display_name,
            is_active=is_active,
            role_id=roles[role_name].id,
        )
        db.add(user)
    db.flush()


# ---------------------------------------------------------------------------
# Projects, Budgets, Project Assignments
# ---------------------------------------------------------------------------

def seed_projects_budgets_assignments(
    db: Session,
    depts: dict[str, Department],
    employees: dict[str, Employee],
) -> None:
    """
    Seed 10 projects, 10 budgets, and 39 project assignments.
    2 projects are intentionally over budget for AI query variety.
    """
    # ── Projects ─────────────────────────────────────────────────────────────
    # (name, description, status, start_date, end_date, dept_key)
    project_records = [
        ("AI Platform Migration",
         "Migrate legacy AI workloads to a unified cloud-native platform.",
         "ACTIVE", date(2024, 1, 15), date(2024, 12, 31), "Engineering"),
        ("Cloud Infrastructure Upgrade",
         "Upgrade on-premise servers to AWS with auto-scaling and DR.",
         "ACTIVE", date(2024, 3, 1), date(2024, 9, 30), "Engineering"),
        ("ERP System Rollout",
         "Deploy company-wide ERP to replace disparate finance tools.",
         "ACTIVE", date(2024, 2, 1), date(2024, 11, 30), "Finance"),
        ("Annual Audit 2025",
         "Internal and external financial audit for fiscal year 2025.",
         "COMPLETED", date(2025, 1, 5), date(2025, 3, 15), "Finance"),
        ("Employee Onboarding Portal",
         "Self-service portal for new hire onboarding and document management.",
         "ACTIVE", date(2024, 4, 1), date(2024, 10, 31), "HR"),
        ("Brand Refresh Campaign",
         "Redesign brand identity and launch updated digital presence.",
         "ACTIVE", date(2024, 5, 1), date(2024, 12, 31), "Marketing"),
        ("Q4 2024 Sales Drive",
         "Targeted outreach and incentive program to hit Q4 revenue targets.",
         "COMPLETED", date(2024, 10, 1), date(2024, 12, 31), "Sales"),
        ("CRM Integration",
         "Integrate Salesforce CRM with internal data warehouse.",
         "ACTIVE", date(2024, 6, 1), date(2025, 3, 31), "Sales"),
        ("Supply Chain Optimization",
         "Reduce procurement lead times and inventory carrying costs.",
         "ON_HOLD", date(2024, 3, 15), None, "Operations"),
        ("Customer Portal v2",
         "Next-generation self-service portal with AI-powered ticket routing.",
         "PLANNING", date(2025, 1, 1), None, "Customer Support"),
    ]

    projects: dict[str, Project] = {}
    for name, desc, status, start, end, dept_key in project_records:
        project = Project(
            name=name,
            description=desc,
            status=status,
            start_date=start,
            end_date=end,
            department_id=depts[dept_key].id,
        )
        db.add(project)
        projects[name] = project
    db.flush()

    # ── Budgets ───────────────────────────────────────────────────────────────
    # (project_name, total_amount, spent_amount, fiscal_year)
    # Projects 2 and 5 are over budget (spent > total).
    budget_records = [
        ("AI Platform Migration",       Decimal("500000.00"), Decimal("480000.00"), 2024),
        ("Cloud Infrastructure Upgrade",Decimal("300000.00"), Decimal("342500.00"), 2024),  # OVER BUDGET
        ("ERP System Rollout",          Decimal("250000.00"), Decimal("190000.00"), 2024),
        ("Annual Audit 2025",           Decimal("80000.00"),  Decimal("75200.00"),  2025),
        ("Employee Onboarding Portal",  Decimal("120000.00"), Decimal("138000.00"), 2024),  # OVER BUDGET
        ("Brand Refresh Campaign",      Decimal("200000.00"), Decimal("155000.00"), 2024),
        ("Q4 2024 Sales Drive",         Decimal("150000.00"), Decimal("143000.00"), 2024),
        ("CRM Integration",             Decimal("180000.00"), Decimal("92000.00"),  2024),
        ("Supply Chain Optimization",   Decimal("220000.00"), Decimal("48000.00"),  2024),
        ("Customer Portal v2",          Decimal("160000.00"), Decimal("8000.00"),   2025),
    ]

    for project_name, total, spent, fiscal_year in budget_records:
        budget = Budget(
            project_id=projects[project_name].id,
            total_amount=total,
            spent_amount=spent,
            fiscal_year=fiscal_year,
        )
        db.add(budget)
    db.flush()

    # ── Project Assignments ───────────────────────────────────────────────────
    # (project_name, emp_num, role, assigned_date, end_date)
    assignment_records = [
        # AI Platform Migration — Engineering (cross: Finance analyst)
        ("AI Platform Migration",        "EMP001", "Lead",              date(2024,  1, 15), None),
        ("AI Platform Migration",        "EMP002", "Developer",         date(2024,  1, 15), None),
        ("AI Platform Migration",        "EMP009", "ML Engineer",       date(2024,  1, 15), None),
        ("AI Platform Migration",        "EMP008", "Data Engineer",     date(2024,  1, 15), None),
        ("AI Platform Migration",        "EMP011", "Analyst",           date(2024,  2,  1), None),
        # Cloud Infrastructure Upgrade — Engineering
        ("Cloud Infrastructure Upgrade", "EMP001", "Lead",              date(2024,  3,  1), None),
        ("Cloud Infrastructure Upgrade", "EMP004", "DevOps Engineer",   date(2024,  3,  1), None),
        ("Cloud Infrastructure Upgrade", "EMP006", "Developer",         date(2024,  3,  1), None),
        ("Cloud Infrastructure Upgrade", "EMP003", "Developer",         date(2024,  3,  1), None),
        # ERP System Rollout — Finance (cross: Operations, Engineering)
        ("ERP System Rollout",           "EMP010", "Lead",              date(2024,  2,  1), None),
        ("ERP System Rollout",           "EMP011", "Analyst",           date(2024,  2,  1), None),
        ("ERP System Rollout",           "EMP012", "Analyst",           date(2024,  2,  1), None),
        ("ERP System Rollout",           "EMP031", "Analyst",           date(2024,  2, 15), None),
        ("ERP System Rollout",           "EMP002", "Developer",         date(2024,  2, 15), None),
        # Annual Audit 2025 — Finance
        ("Annual Audit 2025",            "EMP010", "Lead",              date(2025,  1,  5), date(2025, 3, 15)),
        ("Annual Audit 2025",            "EMP014", "Analyst",           date(2025,  1,  5), date(2025, 3, 15)),
        ("Annual Audit 2025",            "EMP013", "Analyst",           date(2025,  1,  5), date(2025, 3, 15)),
        # Employee Onboarding Portal — HR (cross: Engineering)
        ("Employee Onboarding Portal",   "EMP015", "Lead",              date(2024,  4,  1), None),
        ("Employee Onboarding Portal",   "EMP016", "Analyst",           date(2024,  4,  1), None),
        ("Employee Onboarding Portal",   "EMP007", "Developer",         date(2024,  4,  1), None),
        ("Employee Onboarding Portal",   "EMP005", "QA",                date(2024,  4,  1), None),
        # Brand Refresh Campaign — Marketing
        ("Brand Refresh Campaign",       "EMP019", "Lead",              date(2024,  5,  1), None),
        ("Brand Refresh Campaign",       "EMP020", "Manager",           date(2024,  5,  1), None),
        ("Brand Refresh Campaign",       "EMP023", "Designer",          date(2024,  5,  1), None),
        ("Brand Refresh Campaign",       "EMP021", "Content Strategist",date(2024,  5,  1), None),
        # Q4 2024 Sales Drive — Sales
        ("Q4 2024 Sales Drive",          "EMP024", "Lead",              date(2024, 10,  1), date(2024, 12, 31)),
        ("Q4 2024 Sales Drive",          "EMP027", "Manager",           date(2024, 10,  1), date(2024, 12, 31)),
        ("Q4 2024 Sales Drive",          "EMP025", "Sales Executive",   date(2024, 10,  1), date(2024, 12, 31)),
        ("Q4 2024 Sales Drive",          "EMP026", "Account Manager",   date(2024, 10,  1), date(2024, 12, 31)),
        # CRM Integration — Sales (cross: Engineering)
        ("CRM Integration",              "EMP024", "Lead",              date(2024,  6,  1), None),
        ("CRM Integration",              "EMP027", "Manager",           date(2024,  6,  1), None),
        ("CRM Integration",              "EMP006", "Developer",         date(2024,  6,  1), None),
        ("CRM Integration",              "EMP007", "Developer",         date(2024,  6,  1), None),
        # Supply Chain Optimization — Operations
        ("Supply Chain Optimization",    "EMP030", "Lead",              date(2024,  3, 15), None),
        ("Supply Chain Optimization",    "EMP031", "Manager",           date(2024,  3, 15), None),
        ("Supply Chain Optimization",    "EMP032", "Analyst",           date(2024,  3, 15), None),
        # Customer Portal v2 — Customer Support
        ("Customer Portal v2",           "EMP034", "Lead",              date(2025,  1,  1), None),
        ("Customer Portal v2",           "EMP037", "Manager",           date(2025,  1,  1), None),
        ("Customer Portal v2",           "EMP035", "Analyst",           date(2025,  1,  1), None),
    ]

    for project_name, emp_num, role, assigned_date, end_date in assignment_records:
        assignment = ProjectAssignment(
            project_id=projects[project_name].id,
            employee_id=employees[emp_num].id,
            role=role,
            assigned_date=assigned_date,
            end_date=end_date,
        )
        db.add(assignment)
    db.flush()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    db: Session = SessionLocal()
    try:
        if not _is_seeded(db):
            print("Seeding roles...")
            roles = seed_roles(db)
            print(f"  {len(roles)} roles created.")

            print("Seeding departments...")
            depts = seed_departments(db)
            print(f"  {len(depts)} departments created.")

            print("Seeding employees...")
            employees = seed_employees(db, depts)
            print(f"  {len(employees)} employees created.")

            print("Seeding users...")
            seed_users(db, roles, employees)
            print("  9 users created.")

            db.commit()
            print("Base seed complete.\n")
        else:
            print("Base data already present.")
            depts     = {d.name: d for d in db.query(Department).all()}
            employees = {e.employee_number: e for e in db.query(Employee).all()}

        if not _are_projects_seeded(db):
            print("Seeding projects, budgets, and assignments...")
            seed_projects_budgets_assignments(db, depts, employees)
            db.commit()
            print("  10 projects, 10 budgets, 39 assignments created.")
        else:
            print("Projects already present.")

        print("\nNovaTech Solutions is ready.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
