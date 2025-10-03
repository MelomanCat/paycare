import os
import pandas as pd
from etl import extract_data, transform_data, load_data

def test_extract_data():
    # create test CSV 
    test_file = "test_input.csv"
    pd.DataFrame({
        "employee": ["Alice", "Bob"],
        "salary": [1000, 2000]
    }).to_csv(test_file, index=False)

    df = extract_data(test_file)

    assert df is not None
    assert not df.empty
    assert list(df.columns) == ["employee", "salary"]

    os.remove(test_file)  # clear after test

def test_transform_data():
    # create test DataFrame with missing data
    df = pd.DataFrame({
        "employee": ["Alice", "Bob", None],
        "salary": [1000, 2000, 3000]
    })

    transformed = transform_data(df)

    # ensure NaN is removed
    assert transformed["employee"].isnull().sum() == 0
    # Check the tax calculation
    assert all(transformed["tax"] == transformed["salary"] * 0.1)
    # Ensure net_salary is correct
    assert all(transformed["net_salary"] == transformed["salary"] - transformed["tax"])

def test_load_data():
    # Prepare DataFrame
    df = pd.DataFrame({
        "employee": ["Alice", "Bob"],
        "salary": [1000, 2000],
        "tax": [100, 200],
        "net_salary": [900, 1800]
    })

    output_file = "test_output.csv"
    load_data(df, output_file)

    # Check if teh file is created
    assert os.path.exists(output_file)

    # Check the loaded data
    loaded = pd.read_csv(output_file)
    assert "tax" in loaded.columns
    assert "net_salary" in loaded.columns
    assert len(loaded) == 2

    os.remove(output_file)