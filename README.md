# 🗄️ SQL + ETL Data Quality Framework

![CI](https://github.com/Jay-IT77/sql-etl-testing-project/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![pytest](https://img.shields.io/badge/tested%20with-pytest-orange)
![SQL](https://img.shields.io/badge/SQL-SQLite-lightblue)
![Data](https://img.shields.io/badge/validation-pandas%20%2B%20SQL-brightgreen)

> **Built to catch what ETL pipelines silently break.**

Most data quality issues don't throw errors.
They pass through pipelines quietly — duplicate records inflating reports,
missing salaries breaking payroll, lost rows nobody notices until audit day.

This framework catches them automatically, before they reach production.

**4 real data defects detected in this dataset:**
- Duplicate employee record — payroll double-payment risk
- Missing employee name — compliance failure risk
- Missing salary value — payroll processing failure
- ETL row count mismatch — silent data loss during transformation

---

## 🎯 What This Framework Does

Validates ETL pipelines using a **dual validation layer** —
pandas for Python-based checks, SQLite for SQL-based checks.
Mirrors the exact validation pattern used by bank data teams daily.

| Layer | Tool | What It Checks |
|-------|------|---------------|
| Python | pandas | Duplicates, nulls, row counts, transformation logic |
| SQL | SQLite | Duplicate IDs, null names, salary integrity, record counts |

---

## 🐞 Defects Detected

| ID | Severity | Description | Business Impact |
|----|----------|-------------|----------------|
| ETL-001 | 🔴 High | Duplicate employee record (Bob Smith, id=2) | Payroll double-payment risk |
| ETL-002 | 🔴 High | Missing employee name (Row 7) | Compliance and audit failure |
| ETL-003 | 🔴 High | Missing salary value (Ian Taylor) | Payroll processing failure |
| ETL-004 | 🟡 Medium | Row count mismatch — 10 source, 9 target | Silent data loss during ETL |

→ Full details in [DEFECT_LOG.md](./DEFECT_LOG.md)

---

## 🧪 Test Results

| Test | Type | Result | Notes |
|------|------|--------|-------|
| test_no_duplicates | pandas | ❌ FAILED | Intentional — duplicate detected |
| test_no_null_names | pandas | ❌ FAILED | Intentional — missing name detected |
| test_no_null_salaries | pandas | ❌ FAILED | Intentional — missing salary detected |
| test_row_count_match | pandas | ❌ FAILED | Intentional — data loss detected |
| test_transformation_logic | pandas | ✅ PASSED | ETL logic verified correct |
| test_sql_no_duplicate_ids | SQL | ❌ FAILED | Intentional — SQL caught duplicate |
| test_sql_no_null_names | SQL | ❌ FAILED | Intentional — SQL caught null name |
| test_sql_salary_integrity | SQL | ❌ FAILED | Intentional — SQL caught null salary |
| test_sql_row_count | SQL | ✅ PASSED | Table loaded successfully |

> ⚠️ Failures are **intentional and expected.**
> The dataset was seeded with known data quality issues.
> A passing framework is one that detects every problem — which this does.

---

## 🗂️ Dataset

**source.csv** — Raw HR employee records before ETL transformation

| Column | Type | Notes |
|--------|------|-------|
| id | integer | Employee ID — should be unique |
| name | string | Employee full name — required |
| age | integer | Employee age — nullable |
| department | string | Department name |
| salary | float | Annual salary — required |
| hire_date | date | Employment start date |

**target.csv** — Processed records after ETL transformation

Same columns as source plus:

| Column | Type | Notes |
|--------|------|-------|
| age_group | string | Derived field: Young / Adult / Unknown |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas | Data loading and validation |
| SQLite | In-memory SQL database for SQL-layer tests |
| pytest | Test framework |
| GitHub Actions | CI/CD — runs on every push |

---

## ▶️ How to Run

```bash
git clone https://github.com/Jay-IT77/sql-etl-testing-project
cd sql-etl-testing-project
pip install -r requirements.txt
python -m pytest -v
```
## 📁 Project Structure
sql-etl-testing-project/
├── data/
│   ├── source.csv          # Raw HR dataset with seeded defects
│   └── target.csv          # ETL output with age_group transformation
├── tests/
│   └── test_etl.py         # Pandas + SQL dual validation layer
├── utils/
├── .github/workflows/      # CI/CD pipeline
├── requirements.txt
├── DEFECT_LOG.md           # Detailed defect documentation
└── README.md

---

## 🧠 Key Learnings

- ETL pipelines fail silently — automated validation is not optional
- SQL and pandas catch different failure patterns — both layers are needed
- Business impact framing turns test failures into actionable findings
- yield-based fixtures guarantee database cleanup even when tests fail
