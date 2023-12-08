import pandas as pd

def read_csv_data(path):
    """
    Read data from a CSV file and return it as a pandas DataFrame.

    Parameters:
    - path (str): The file path of the CSV file to be read.

    Raises:
    - AssertionError: If the input path is not a string, or if its length is less than 5, or if it does not end with '.csv'.
    - FileNotFoundError: If the specified file path does not exist.

    Returns:
    - pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    assert isinstance(path, str) and len(path) > 4 and path[-4:] == ".csv", "Invalid file path format"

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(path))

    return df