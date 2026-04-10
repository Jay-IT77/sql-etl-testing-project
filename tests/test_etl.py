import pandas as pd
import sqlite3
import pytest

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def source():
    """Load source dataset — raw HR records before ETL transformation."""
    return pd.read_csv("data/source.csv")

@pytest.fixture
def target():
    """Load target dataset — records after ETL transformation."""
    return pd.read_csv("data/target.csv")

@pytest.fixture
def db_conn(source):
    """
    Load source data into SQLite in-memory database.
    yield-based teardown guarantees connection closes
    even if a test fails mid-execution.
    """
    conn = sqlite3.connect(":memory:")
    source.to_sql("employees", conn, if_exists="replace", index=False)
    yield conn
    conn.close()

# ============================================================
# PANDAS TESTS
# ============================================================

def test_no_duplicates(source):
    """
    INTENTIONAL FAILURE — framework detects duplicate records.
    Source has 1 duplicate row (Bob Smith, id=2).
    Risk: payroll double-payment.
    """
    duplicates = source.duplicated().sum()
    assert duplicates == 0, (
        f"DEFECT DETECTED: {duplicates} duplicate record(s) found. "
        f"Risk: payroll double-payment, reporting inflation."
    )

def test_no_null_names(source):
    """
    INTENTIONAL FAILURE — framework detects missing employee names.
    Row 7 has no name. Risk: compliance failure.
    """
    null_names = source["name"].isnull().sum()
    assert null_names == 0, (
        f"DEFECT DETECTED: {null_names} record(s) with missing name. "
        f"Risk: compliance failure, unidentifiable payroll records."
    )

def test_no_null_salaries(source):
    """
    INTENTIONAL FAILURE — framework detects missing salary data.
    Ian Taylor has no salary. Risk: payroll processing failure.
    """
    null_salaries = source["salary"].isnull().sum()
    assert null_salaries == 0, (
        f"DEFECT DETECTED: {null_salaries} record(s) with missing salary. "
        f"Risk: payroll processing failure."
    )

def test_row_count_match(source, target):
    """
    INTENTIONAL FAILURE — source has 10 rows, target has 9 rows.
    Data was lost during ETL transformation.
    """
    assert len(source) == len(target), (
        f"DEFECT DETECTED: Source has {len(source)} rows, "
        f"target has {len(target)} rows. "
        f"Data loss occurred during ETL transformation."
    )

def test_transformation_logic(target):
    """
    PASSES — verifies age_group transformation is correctly applied.
    None age = Unknown, age under 25 = Young, age 25+ = Adult.
    """
    for _, row in target.iterrows():
        if pd.isnull(row["age"]):
            assert row["age_group"] == "Unknown", (
                f"Expected Unknown for null age, got {row['age_group']}"
            )
        elif row["age"] < 25:
            assert row["age_group"] == "Young", (
                f"Expected Young for age {row['age']}, got {row['age_group']}"
            )
        else:
            assert row["age_group"] == "Adult", (
                f"Expected Adult for age {row['age']}, got {row['age_group']}"
            )

# ============================================================
# SQL TESTS
# ============================================================

def test_sql_no_duplicate_ids(db_conn):
    """
    SQL layer — detects duplicate IDs using GROUP BY.
    Mirrors what a bank audit team runs against transaction tables daily.
    """
    query = """
        SELECT id, COUNT(*) as cnt
        FROM employees
        GROUP BY id
        HAVING cnt > 1
    """
    result = pd.read_sql_query(query, db_conn)
    assert len(result) == 0, (
        f"DEFECT DETECTED via SQL: {len(result)} duplicate ID(s) found.\n{result}"
    )

def test_sql_no_null_names(db_conn):
    """
    SQL layer — detects missing employee names using WHERE IS NULL.
    """
    query = """
        SELECT * FROM employees
        WHERE name IS NULL
    """
    result = pd.read_sql_query(query, db_conn)
    assert len(result) == 0, (
        f"DEFECT DETECTED via SQL: {len(result)} record(s) with null name.\n{result}"
    )

def test_sql_salary_integrity(db_conn):
    """
    SQL layer — detects missing or invalid salary values.
    Business rule: every active employee must have a valid salary.
    """
    query = """
        SELECT * FROM employees
        WHERE salary IS NULL OR salary <= 0
    """
    result = pd.read_sql_query(query, db_conn)
    assert len(result) == 0, (
        f"DEFECT DETECTED via SQL: {len(result)} record(s) with invalid salary.\n{result}"
    )

def test_sql_row_count(db_conn):
    """
    SQL layer — confirms records exist in source table.
    Catches silent ETL load failures.
    """
    query = "SELECT COUNT(*) as total FROM employees"
    result = pd.read_sql_query(query, db_conn)
    total = result["total"][0]
    assert total > 0, "Source table is empty — ETL load failed."
