from utils.data_loader import load_data

source = load_data("data/source.csv")
target = load_data("data/target.csv")

def test_no_duplicates():
    assert source.duplicated().sum() == 0, "Duplicate records found"

def test_no_nulls():
    assert source.isnull().sum().sum() == 0, "Null values found"

def test_row_count():
    assert len(source) == len(target), "Row count mismatch"

def test_transformation():
    for _, row in source.iterrows():
        if row["age"] < 25:
            expected = "Young"
        else:
            expected = "Adult"

        match = target[target["name"] == row["name"]]
        if not match.empty:
            assert match.iloc[0]["age_group"] == expected
