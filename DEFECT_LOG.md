# 🐞 Defect Log — SQL ETL Data Quality Framework

> Defects detected automatically by this framework in the HR employee dataset.
> Each entry includes detection method, business impact, and recommended fix.
> All defects were caught by automated tests — zero manual inspection required.

---

## ETL-001 — Duplicate Employee Record

| Field | Detail |
|-------|--------|
| **ID** | ETL-001 |
| **Severity** | 🔴 P1 — Critical |
| **Detected By** | `test_no_duplicates` (pandas) + `test_sql_no_duplicate_ids` (SQL) |
| **Detection Layer** | Dual — caught by both pandas and SQL independently |
| **Status** | Documented — requires source system fix |

### What Was Found
id=2, name=Bob Smith, age=28, department=Marketing
appears twice in source dataset — exact duplicate row.

### Business Impact
- Payroll systems processing this record will pay Bob Smith twice
- Headcount reports will show inflated employee count
- Any aggregation (total salary, department averages) will be skewed
- Audit trail will show two records for one employee — compliance risk

### Root Cause
Duplicate record introduced at data entry level in source system.
No deduplication logic exists in current ETL pipeline.

### Recommended Fix
Add deduplication step at ETL ingestion layer:
```python
df = df.drop_duplicates(subset=["id"], keep="first")
```
Add unique constraint at database level on employee ID column.

---

## ETL-002 — Missing Employee Name

| Field | Detail |
|-------|--------|
| **ID** | ETL-002 |
| **Severity** | 🔴 P1 — Critical |
| **Detected By** | `test_no_null_names` (pandas) + `test_sql_no_null_names` (SQL) |
| **Detection Layer** | Dual — caught by both pandas and SQL independently |
| **Status** | Documented — requires manual data review |

### What Was Found
id=7, name=NULL, age=38, department=Sales
Employee record exists with no identifying name.

### Business Impact
- Payroll cannot be processed for an unidentified employee
- Legal and compliance teams cannot audit this record
- HR reporting will contain an anonymous entry
- Cannot be matched to any external system (benefits, tax records)

### Root Cause
Missing mandatory field validation at data entry point.
Source system accepted a record without a name value.

### Recommended Fix
Add NOT NULL constraint on name column at source system level.
Add validation check at ETL ingestion:
```python
df = df[df["name"].notna()]
# Flag rejected records to a separate error log
```

---

## ETL-003 — Missing Salary Value

| Field | Detail |
|-------|--------|
| **ID** | ETL-003 |
| **Severity** | 🔴 P1 — Critical |
| **Detected By** | `test_no_null_salaries` (pandas) + `test_sql_salary_integrity` (SQL) |
| **Detection Layer** | Dual — caught by both pandas and SQL independently |
| **Status** | Documented — requires payroll team review |

### What Was Found
id=9, name=Ian Taylor, age=26, department=Sales, salary=NULL
Active employee record with no salary value.

### Business Impact
- Payroll processing will fail or skip Ian Taylor entirely
- No salary means no tax withholding calculation possible
- Benefits calculations dependent on salary will break
- Financial reporting will understate total payroll costs

### Root Cause
Salary field left empty during employee onboarding data entry.
No mandatory field enforcement at source system level.

### Recommended Fix
Add salary validation at ETL ingestion:
```python
invalid_salary = df[df["salary"].isna() | (df["salary"] <= 0)]
# Route to error queue for manual review
```

---

## ETL-004 — Row Count Mismatch (Data Loss)

| Field | Detail |
|-------|--------|
| **ID** | ETL-004 |
| **Severity** | 🟡 P2 — High |
| **Detected By** | `test_row_count_match` (pandas) |
| **Detection Layer** | pandas |
| **Status** | Documented — ETL pipeline investigation required |

### What Was Found
Source record count:  10 rows
Target record count:  9 rows
Records lost:         1 row

### Business Impact
- One employee record was silently dropped during ETL transformation
- Any downstream reporting will be missing one employee
- If the lost record belongs to a recently hired employee
  their payroll will not be processed
- Silent data loss is the most dangerous failure type
  because it produces no error — just wrong results

### Root Cause
ETL transformation step dropped one record without logging the rejection.
Likely caused by a filter condition or join failure during processing.

### Recommended Fix
Add row count reconciliation step at end of every ETL run:
```python
assert len(source) == len(target), (
    f"Row count mismatch: {len(source)} source vs {len(target)} target"
)
```
Add rejection logging — every dropped record must be written
to an error log with reason for rejection.

---

## Defect Summary

| ID | Severity | Detection Method | Business Risk | Status |
|----|----------|-----------------|---------------|--------|
| ETL-001 | 🔴 P1 Critical | pandas + SQL | Payroll double-payment | Documented |
| ETL-002 | 🔴 P1 Critical | pandas + SQL | Compliance failure | Documented |
| ETL-003 | 🔴 P1 Critical | pandas + SQL | Payroll failure | Documented |
| ETL-004 | 🟡 P2 High | pandas | Silent data loss | Documented |

> All defects detected automatically with zero manual intervention.
> Framework caught 3 P1 Critical issues that would have reached
> production without automated validation in place.
