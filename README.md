# 🗄️ SQL + ETL Testing Project

## 🚀 Overview

This project is designed to validate ETL (Extract, Transform, Load) processes by comparing source and target datasets using Python and pandas.

## 🎯 Objective

To ensure data integrity, consistency, and correctness during ETL transformations.

---

## 🧪 Test Coverage

### ✅ Duplicate Detection

* Ensures no duplicate records in source data

### ✅ Null Validation

* Detects missing values in dataset

### ✅ Row Count Validation

* Ensures no data loss between source and target

### ✅ Transformation Validation

* Verifies correct transformation logic (age → age_group)

---

## 🛠️ Tech Stack

* Python
* pandas
* pytest

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m pytest -v --html=report.html --self-contained-html
```

---

## 📊 Results

* Duplicate test: FAILED (intentional)
* Row count test: FAILED (intentional)
* Null check: PASSED
* Transformation test: PASSED

---

## 🧠 Key Learnings

* ETL testing fundamentals
* Data validation using pandas
* Detecting real-world data issues
* Writing automated test cases

---


